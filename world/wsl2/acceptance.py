"""Fixed W0 acceptance suite. Run only the root-owned installed copy in WSL.

No candidate programs, paths, shell commands or policy overrides are accepted.
The pids stress helper is trusted infrastructure, outside the workload seccomp
profile, and remains inside exactly the same worker cgroup resource limits.
"""
import ctypes
import fcntl
import hashlib
import json
import os
from pathlib import Path
import pwd
import resource
import signal
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
import direct


def check(value, message):
    if not value:
        raise RuntimeError(message)


def snapshot():
    return {
        "wsl_conf_sha256": hashlib.sha256(Path("/etc/wsl.conf").read_bytes()).hexdigest(),
        "pid1": Path("/proc/1/comm").read_text().strip(),
        "root_controllers": sorted((direct.CGROOT / "cgroup.subtree_control").read_text().split()),
        "docker_pids": subprocess.check_output(["/usr/bin/pgrep", "-x", "dockerd"], text=True).split(),
        "private_cgroup_absent": not direct.BASE.exists(),
    }


def table(raw):
    return {k: int(v) for k, v in (line.split() for line in raw.splitlines())}


def execute(mode):
    started = time.monotonic()
    result = subprocess.run(["/usr/bin/timeout", "--signal=KILL", "80s", sys.executable,
                             "-I", str(direct.ASSETS / "direct.py"), mode],
                            capture_output=True, text=True, timeout=85)
    report = json.loads(result.stdout)
    check("outcome" in report, f"{mode}: no completed report: {report}")
    check(report["worker_populated_after"] is False, f"{mode}: worker survived")
    check(report["cleanup"]["private_cgroup_removed"], f"{mode}: cleanup failed")
    check(report["cleanup"]["root_controllers_restored"], f"{mode}: controller restoration failed")
    check(report["enforced_limits"]["worker"] == direct.LIMITS["worker"], "worker limits changed")
    check(time.monotonic() - started < 80, f"{mode}: outer watchdog fired")
    return report


def pids_helper():
    check(os.geteuid() != 0, "helper must be unprivileged")
    check(Path("/proc/self/cgroup").read_text().strip() == "0::/pe-world-current-v0/worker", "helper outside worker")
    children, denied = [], False
    try:
        for _ in range(80):  # at most 80 attempts; kernel TasksMax is 64
            try:
                pid = os.fork()
            except BlockingIOError:
                denied = True
                break
            if pid == 0:
                time.sleep(3)
                os._exit(0)
            children.append(pid)
        print(json.dumps({"denied": denied, "children": len(children)}), flush=True)
    finally:
        for pid in children:
            os.waitpid(pid, 0)


def pids_test():
    errors = direct.preflight()
    check(not errors, str(errors))
    with (direct.ARCHIVE / ".lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        origin = direct.origin_group()
        direct.prepare_groups()
        process = None
        try:
            account = pwd.getpwnam("pe-organism")
            def enter():
                direct.set_file(direct.BASE / "worker", "cgroup.procs", str(os.getpid()))
                resource.setrlimit(resource.RLIMIT_NOFILE, (256, 256))
                resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
                resource.setrlimit(resource.RLIMIT_CPU, (5, 5))
                os.setgroups([])
                os.setgid(account.pw_gid)
                os.setuid(account.pw_uid)
                libc = ctypes.CDLL(None)
                if libc.prctl(38, 1, 0, 0, 0) or libc.prctl(1, signal.SIGKILL, 0, 0, 0):
                    os._exit(120)
            process = subprocess.Popen([sys.executable, "-I", str(Path(__file__).resolve()), "--pids-helper"],
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, preexec_fn=enter)
            out, err = process.communicate(timeout=10)
            report = {"helper": json.loads(out), "returncode": process.returncode,
                      "worker_stats": direct.sample_stats(direct.BASE / "worker"),
                      "scope": "trusted kernel quota stress; workload seccomp unchanged"}
            check(process.returncode == 0 and report["helper"]["denied"], f"pids not denied: {err}")
            check(int(report["worker_stats"]["pids.peak"]) == 64, "pids peak differs from policy")
            check(table(report["worker_stats"]["pids.events"])["max"] > 0, "no kernel pids limit event")
        finally:
            direct.kill_worker()
            if process is not None:
                process.wait(timeout=3)
            direct.leave_control(origin)
            cleaned = direct.cleanup()
        report["cleanup"] = cleaned
        return report


def controller_death_test():
    before = set(direct.ARCHIVE.glob("*.jsonl"))
    process = subprocess.Popen([sys.executable, "-I", str(direct.ASSETS / "direct.py"), "hang"],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        end = time.monotonic() + 4
        while True:
            worker = direct.BASE / "worker"
            if worker.exists() and direct.populated(worker):
                # Wait for a flushed heartbeat to prove the sandbox actually started.
                new = set(direct.ARCHIVE.glob("*.jsonl")) - before
                if any(p.with_suffix(".stdout").exists() and b'"heartbeat"' in p.with_suffix(".stdout").read_bytes() for p in new):
                    break
            check(time.monotonic() < end and process.poll() is None, "death probe did not start")
            time.sleep(.05)
        busy = subprocess.run([sys.executable, "-I", str(direct.ASSETS / "direct.py"), "smoke"],
                              capture_output=True, text=True, timeout=3)
        check(busy.returncode == 2 and "error" in json.loads(busy.stdout), "concurrent world was admitted")
        check(direct.members(direct.BASE / "control") == [process.pid], "concurrent probe changed controller")
        started = time.monotonic()
        process.kill()
        process.communicate(timeout=3)
        while direct.populated(worker):
            check(time.monotonic() - started < 3, "workers survived controller death")
            time.sleep(.02)
        report = {"controller_returncode": process.returncode,
                  "worker_empty_after_seconds": time.monotonic() - started,
                  "concurrent_launch_rejected": True, "worker_stats": direct.sample_stats(worker),
                  "interrupted_journals": [p.name for p in set(direct.ARCHIVE.glob("*.jsonl")) - before]}
    finally:
        if process.poll() is None:
            process.kill()
            process.communicate(timeout=3)
        report_cleanup = direct.cleanup()
    report["cleanup"] = report_cleanup
    return report


def suite():
    check(direct.shared().trusted_tree(Path(__file__)), "run installed root-owned suite only")
    errors = direct.preflight()
    check(not errors, str(errors))
    report = {"profile": "existing-wsl-serial-single-thread-v0", "started_unix": time.time(),
              "before": snapshot(), "cases": {}, "accepted": False,
              "suite_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    target = direct.ARCHIVE.parent / f"acceptance-{int(time.time())}.json"
    try:
        for mode, expected in (("memory", "probe_failed"), ("output", "output_limit"),
                               ("line", "line_limit"), ("protocol", "protocol_error"),
                               ("hang", "heartbeat_timeout"), ("closed-pipes", "heartbeat_timeout"),
                               ("permissions", "passed"), ("inspect", "passed"),
                               ("cpu", "cpu_or_wall_limit"), ("deadline", "runtime_limit")):
            result = execute(mode)
            report["cases"][mode] = result
            if mode == "cpu":
                check(result["outcome"] == "runtime_limit" or
                      (result["outcome"] == "probe_failed" and result["returncode"] == 137),
                      "CPU stress was not stopped by its CPU or wall deadline")
            else:
                check(result["outcome"] == expected, f"{mode}: expected {expected}, got {result['outcome']}")
            if mode == "memory":
                check(table(result["worker_stats"]["memory.events"])["oom_kill"] > 0, "no cgroup OOM kill")
            if mode == "output":
                check(result["captured_bytes"] <= 1048576 and result["observed_bytes"] > 1048576, "output cap not exercised")
            if mode in {"hang", "closed-pipes"}:
                check(5 <= result["elapsed_seconds"] < 7, "heartbeat deadline outside tolerance")
            if mode == "cpu":
                stats = table(result["worker_stats"]["cpu.stat"])
                check(69 <= result["elapsed_seconds"] < 73, "CPU deadline outside tolerance")
                check(stats["nr_throttled"] > 0 and stats["usage_usec"] / 1e6 / result["elapsed_seconds"] < 1.1,
                      "CPU cap not exercised")
                check(stats["usage_usec"] > 68_000_000, "CPU termination was premature")
            if mode == "deadline":
                check(70 <= result["elapsed_seconds"] < 73, "wall deadline outside tolerance")
            print(json.dumps({"case": mode, "passed": True}), flush=True)
        report["cases"]["pids"] = pids_test()
        print(json.dumps({"case": "pids", "passed": True}), flush=True)
        report["cases"]["controller-death-and-concurrency"] = controller_death_test()
        print(json.dumps({"case": "controller-death-and-concurrency", "passed": True}), flush=True)
        report["cases"]["recovery"] = execute("smoke")
        check(report["cases"]["recovery"]["outcome"] == "passed", "recovery failed")
        report["after"] = snapshot()
        check(report["before"] == report["after"], "shared distro state changed")
        report["accepted"] = True
    except Exception as exc:
        report["error"] = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        report["finished_unix"] = time.time()
        target.write_text(json.dumps(report, indent=2) + "\n")
        print(json.dumps({"evidence": str(target), "accepted": report["accepted"]}), flush=True)


if __name__ == "__main__":
    if sys.argv[1:] == ["--pids-helper"]:
        pids_helper()
    elif not sys.argv[1:]:
        suite()
    else:
        raise SystemExit("no custom arguments admitted")
