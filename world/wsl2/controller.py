"""Prepared W0 controller. Only a fixed trusted smoke probe is admitted in v0.

No installation, WSL restart or candidate evolution is performed by this module.
The full hostile-boundary acceptance suite is still required.
"""

import argparse
import configparser
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import re
import selectors
import signal
import subprocess
import sys
import time
import uuid

ASSETS = Path(__file__).resolve().parent
PROPERTIES = {
    "MemoryMax": "268435456", "MemoryHigh": "234881024", "MemorySwapMax": "0",
    "CPUQuota": "100%", "TasksMax": "64", "LimitNOFILE": "256",
    "LimitCORE": "0", "LimitFSIZE": "1048576", "RuntimeMaxSec": "70s",
    "TimeoutStopSec": "1s", "KillMode": "control-group", "OOMPolicy": "kill",
    "User": "pe-organism", "Group": "pe-organism", "NoNewPrivileges": "yes",
    "CapabilityBoundingSet": "", "UMask": "0077", "SendSIGKILL": "yes"
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def strict_json(data):
    def invalid_constant(value):
        raise ValueError(f"non-finite JSON constant {value}")
    def object_pairs(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate JSON key")
            result[key] = value
        return result
    return json.loads(data, parse_constant=invalid_constant, object_pairs_hook=object_pairs)


def load_policy():
    data = (ASSETS / "policy.json").read_bytes()
    policy = json.loads(data)
    expected = {"memory_bytes": 268435456, "cpu_percent_of_one_core": 100,
                "tasks_max": 64, "nofile": 256, "runtime_seconds": 70,
                "heartbeat_seconds": 5, "max_input_bytes": 65536,
                "max_line_bytes": 16384, "max_output_bytes": 1048576,
                "max_archive_bytes": 33554432, "max_runs": 16,
                "work_bytes": 16777216, "tmp_bytes": 8388608}
    if set(policy) != set(expected) | {"version"} or not isinstance(policy["version"], str):
        raise ValueError("unexpected policy schema")
    if any(type(policy[k]) is not int or policy[k] != v for k, v in expected.items()):
        raise ValueError("v0 controller admits only its reviewed fixed resource profile")
    return policy, digest(data)


class Monitor:
    """Bounded JSONL parser. Time comes from the controller, never the workload."""

    def __init__(self, policy, started):
        self.policy, self.started, self.last_heartbeat = policy, started, started
        self.pending = bytearray()
        self.output_bytes = 0
        self.sequence = -1
        self.result = None
        self.reason = None

    def feed(self, chunk, now, *, stdout=True):
        self.output_bytes += len(chunk)
        if self.output_bytes > self.policy["max_output_bytes"]:
            self.reason = "output_limit"
            return
        if not stdout:
            return
        self.pending.extend(chunk)
        while b"\n" in self.pending and not self.reason:
            line, _, rest = self.pending.partition(b"\n")
            self.pending = bytearray(rest)
            if len(line) > self.policy["max_line_bytes"]:
                self.reason = "line_limit"
                break
            try:
                event = strict_json(line)
                if not isinstance(event, dict):
                    raise ValueError("event is not an object")
                kind = event.get("type")
                if kind == "heartbeat":
                    seq, stamp = event.get("seq"), event.get("timestamp")
                    if (type(seq) is not int or seq != self.sequence + 1
                            or type(stamp) not in (int, float) or not math.isfinite(stamp)):
                        raise ValueError("invalid heartbeat")
                    self.sequence, self.last_heartbeat = seq, now
                elif kind == "result":
                    if self.result is not None:
                        raise ValueError("duplicate result")
                    self.result = event
                else:
                    raise ValueError("unknown event type")
            except (ValueError, UnicodeError, OverflowError, RecursionError):
                self.reason = "protocol_error"
        if len(self.pending) > self.policy["max_line_bytes"]:
            self.reason = "line_limit"

    def tick(self, now):
        if self.reason:
            return self.reason
        if now - self.started >= self.policy["runtime_seconds"]:
            return "runtime_limit"
        if now - self.last_heartbeat >= self.policy["heartbeat_seconds"]:
            return "heartbeat_timeout"
        return None


def trusted_tree(path):
    path = Path(path)
    if path.is_symlink() or not path.exists():
        return False
    for item in (path, *path.parents):
        st = item.stat()
        if st.st_uid != 0 or st.st_mode & 0o022:
            return False
    return True


def preflight():
    errors = []
    if platform.system() != "Linux" or platform.machine() != "x86_64":
        return ["requires Linux x86_64 in a dedicated WSL2 distribution"]
    if "microsoft" not in Path("/proc/sys/kernel/osrelease").read_text().lower():
        errors.append("not a WSL kernel")
    memory = {}
    for line in Path("/proc/meminfo").read_text().splitlines():
        key, _, value = line.partition(":")
        if key in {"MemTotal", "SwapTotal"}:
            memory[key] = int(value.split()[0]) * 1024
    if memory.get("MemTotal", 2**63) > 4 * 1024**3:
        errors.append("outer WSL memory envelope exceeds proposed 4 GiB profile")
    if memory.get("SwapTotal", 1) != 0:
        errors.append("outer WSL swap must be disabled for this profile")
    if not 1 <= (os.cpu_count() or 0) <= 2:
        errors.append("outer WSL processor count exceeds proposed 2-CPU profile")
    if Path("/proc/1/comm").read_text().strip() != "systemd":
        errors.append("systemd is not PID 1; no workload will start")
    if not {"cpu", "memory", "pids"} <= set(Path("/sys/fs/cgroup/cgroup.controllers").read_text().split()):
        errors.append("required cgroup v2 controllers unavailable")
    conf = configparser.ConfigParser()
    conf.read("/etc/wsl.conf")
    for section, key, value in (("boot", "systemd", True), ("automount", "enabled", False),
                                ("automount", "mountFsTab", False), ("interop", "enabled", False),
                                ("interop", "appendWindowsPath", False)):
        if conf.getboolean(section, key, fallback=not value) != value:
            errors.append(f"dedicated distro requires [{section}] {key}={str(value).lower()}")
    for name in ("/usr/bin/bwrap", "/usr/bin/systemd-run", "/usr/bin/systemctl"):
        if not Path(name).is_file():
            errors.append(f"missing {name}")
    for name in ("rootfs", "rootfs.manifest.json", "seccomp.bpf", "controller.py",
                 "policy.json", "probes/smoke.py"):
        if not trusted_tree(ASSETS / name):
            errors.append(f"missing or non-root-owned writable asset: {name}")
    try:
        executable = (ASSETS / "rootfs/usr/bin/python3").resolve(strict=True)
        if not executable.is_relative_to((ASSETS / "rootfs").resolve()) or not trusted_tree(executable):
            errors.append("rootfs Python must resolve to a trusted file inside the image")
    except OSError:
        errors.append("rootfs Python is missing")
    for name in ("pe-world.slice", "pe-control.slice"):
        if not trusted_tree(Path("/etc/systemd/system") / name):
            errors.append(f"missing trusted installed {name}")
    return errors


def bwrap_args(seccomp_fd):
    return ["/usr/bin/bwrap", "--unshare-user", "--unshare-pid", "--unshare-net",
            "--unshare-ipc", "--unshare-uts", "--unshare-cgroup", "--disable-userns",
            "--assert-userns-disabled", "--uid", "65534", "--gid", "65534",
            "--cap-drop", "ALL", "--new-session", "--die-with-parent", "--clearenv",
            "--ro-bind", str(ASSETS / "rootfs"), "/",
            "--proc", "/proc", "--dev", "/dev", "--size", "16777216", "--tmpfs", "/work",
            "--size", "8388608", "--tmpfs", "/tmp", "--ro-bind",
            str(ASSETS / "probes/smoke.py"), "/app/main.py",
            "--setenv", "PATH", "/usr/bin", "--setenv", "LANG", "C.UTF-8",
            "--setenv", "PYTHONHASHSEED", "0", "--chdir", "/work",
            "--seccomp", str(seccomp_fd), "--", "/usr/bin/python3", "-I", "-S", "-B", "/app/main.py"]


def worker():
    # Open inside the service: systemd does not inherit an arbitrary controller FD 10.
    check_worker_limits()
    fd = os.open(ASSETS / "seccomp.bpf", os.O_RDONLY | os.O_NOFOLLOW)
    os.set_inheritable(fd, True)
    os.execv("/usr/bin/bwrap", bwrap_args(fd))


def worker_unit(run_id, controller_unit):
    if not re.fullmatch(r"[a-f0-9]{32}", run_id):
        raise ValueError("invalid run id")
    if not re.fullmatch(r"pe-control-[a-f0-9]{32}\.service", controller_unit):
        raise ValueError("controller must run in its dedicated bounded service")
    unit = f"pe-run-{run_id}.service"
    props = dict(PROPERTIES, BindsTo=controller_unit, After=controller_unit)
    command = ["/usr/bin/systemd-run", "--system", "--wait", "--pipe", "--quiet",
               "--service-type=exec", "--expand-environment=no", f"--unit={unit}",
               "--slice=pe-world.slice"]
    for key, value in props.items():
        command.append(f"--property={key}={value}")
    command += ["--", "/usr/bin/python3", "-I", str(ASSETS / "controller.py"), "worker"]
    return unit, command


def checked_control_group():
    group = Path("/proc/self/cgroup").read_text().strip()
    match = re.fullmatch(r"0::(/pe\.slice/pe-control\.slice/(pe-control-[a-f0-9]{32}\.service))", group)
    if not match:
        raise RuntimeError("launch through config/run-smoke.sh in bounded pe-control.slice")
    base = Path("/sys/fs/cgroup") / match[1].lstrip("/")
    for key, expected in (("memory.max", "134217728"), ("memory.swap.max", "0"), ("pids.max", "32")):
        if (base / key).read_text().strip() != expected:
            raise RuntimeError(f"controller {key} is not the required hard limit")
    quota, period = (base / "cpu.max").read_text().split()
    if quota == "max" or int(quota) / int(period) > .25:
        raise RuntimeError("controller CPU quota exceeds 25% of one core")
    return match[2]


def check_worker_limits():
    group = Path("/proc/self/cgroup").read_text().strip()
    match = re.fullmatch(r"0::(/pe\.slice/pe-world\.slice/pe-run-[a-f0-9]{32}\.service)", group)
    if not match or os.geteuid() == 0:
        raise RuntimeError("worker must be an unprivileged systemd worker service")
    base = Path("/sys/fs/cgroup") / match[1].lstrip("/")
    for directory, memory, tasks in ((base, "268435456", "64"), (base.parent, "536870912", "128")):
        for key, expected in (("memory.max", memory), ("memory.swap.max", "0"), ("pids.max", tasks)):
            if (directory / key).read_text().strip() != expected:
                raise RuntimeError(f"worker {key} enforcement differs from policy")
        quota, period = (directory / "cpu.max").read_text().split()
        if quota == "max" or int(quota) > int(period):
            raise RuntimeError("worker CPU cap exceeds one core")
    import resource
    if resource.getrlimit(resource.RLIMIT_NOFILE) != (256, 256):
        raise RuntimeError("worker file-descriptor limit is not 256")


def stop_unit(unit):
    results = []
    for args in (("kill", "--kill-whom=all", "--signal=KILL", unit), ("stop", "--no-block", unit)):
        try:
            results.append(subprocess.run(["/usr/bin/systemctl", *args], stdout=subprocess.DEVNULL,
                                          stderr=subprocess.DEVNULL, timeout=3).returncode)
        except subprocess.TimeoutExpired:
            results.append(-1)
    return results


def run_probe(seed):
    errors = preflight()
    if errors:
        raise RuntimeError("; ".join(errors))
    controller_unit = checked_control_group()
    policy, policy_hash = load_policy()
    archive = Path("/var/lib/pe-world/runs")
    if not trusted_tree(archive):
        raise RuntimeError("archive must be root-owned and unavailable to pe-organism")
    import fcntl
    with (archive / ".lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)  # v0 is deliberately serial
        files = list(archive.rglob("*"))
        if any(p.is_symlink() for p in files):
            raise RuntimeError("unexpected archive symlink")
        if (sum(p.stat().st_size for p in files if p.is_file()) + 2 * policy["max_output_bytes"]
                > policy["max_archive_bytes"] or len(list(archive.glob("*.jsonl"))) >= policy["max_runs"]):
            raise RuntimeError("archive budget exhausted; operator must archive results")
        run_id = uuid.uuid4().hex
        unit, command = worker_unit(run_id, controller_unit)
        request = json.dumps({"version": 1, "seed": seed, "payload": {}}, sort_keys=True).encode() + b"\n"
        if len(request) > policy["max_input_bytes"]:
            raise ValueError("input exceeds policy limit")
        monitor = Monitor(policy, time.monotonic())
        process = None
        outcome = "controller_error"
        hashes = {"stdout": hashlib.sha256(), "stderr": hashlib.sha256()}
        retained = 0
        with (archive / f"{run_id}.jsonl").open("x", encoding="utf-8") as journal:
            journal.write(json.dumps({"event": "start", "run_id": run_id, "seed": seed,
                          "started_unix": time.time(),
                          "policy_version": policy["version"], "policy_sha256": policy_hash,
                          "seccomp_sha256": digest((ASSETS / "seccomp.bpf").read_bytes()),
                          "controller_sha256": digest(Path(__file__).read_bytes()),
                          "rootfs_manifest_sha256": digest((ASSETS / "rootfs.manifest.json").read_bytes()),
                          "input_sha256": digest(request), "scope": "trusted smoke probe only"}) + "\n")
            journal.flush()
            try:
                process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE, start_new_session=True)
                process.stdin.write(request)
                process.stdin.close()
                with selectors.DefaultSelector() as selector, (archive / f"{run_id}.stdout").open("xb") as out, (archive / f"{run_id}.stderr").open("xb") as err:
                    for stream, label in ((process.stdout, "stdout"), (process.stderr, "stderr")):
                        os.set_blocking(stream.fileno(), False)
                        selector.register(stream, selectors.EVENT_READ, (label, out if label == "stdout" else err))
                    while selector.get_map():
                        reason = monitor.tick(time.monotonic())
                        if reason:
                            outcome = reason
                            break
                        for key, _ in selector.select(.1):
                            chunk = os.read(key.fileobj.fileno(), 4096)
                            if not chunk:
                                selector.unregister(key.fileobj)
                                continue
                            label, stream = key.data
                            hashes[label].update(chunk)
                            keep = chunk[:max(0, policy["max_output_bytes"] - retained)]
                            stream.write(keep)
                            retained += len(keep)
                            monitor.feed(chunk, time.monotonic(), stdout=label == "stdout")
                    else:
                        code = process.wait(timeout=2)
                        expected = {"type": "result", "seed": seed, "uid": 65534, "message": "trusted smoke probe"}
                        outcome = ("passed" if code == 0 and not monitor.reason and monitor.result == expected and not monitor.pending
                                   else "probe_failed")
            finally:
                termination = stop_unit(unit)
                if process is not None:
                    try:
                        process.wait(timeout=3)
                    except subprocess.TimeoutExpired:
                        os.killpg(process.pid, signal.SIGKILL)
                        process.wait(timeout=3)
                journal.write(json.dumps({"event": "finish", "outcome": outcome,
                              "finished_unix": time.time(),
                              "elapsed_seconds": time.monotonic() - monitor.started,
                              "captured_bytes": retained, "observed_bytes": monitor.output_bytes,
                              "observed_sha256": {k: h.hexdigest() for k, h in hashes.items()},
                              "hash_scope": "bytes observed before stopping; not an unseen full stream",
                              "stop_status": termination, "heartbeat_is_not_progress": True}) + "\n")
        return {"run_id": run_id, "outcome": outcome, "w0_accepted": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("preflight", "smoke", "worker"))
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args()
    if args.mode == "worker":
        worker()
        return 1
    try:
        if args.mode == "preflight":
            errors = preflight()
            print(json.dumps({"ready": not errors, "errors": errors, "w0_accepted": False}, indent=2))
            return 2 if errors else 0
        result = run_probe(args.seed)
        print(json.dumps(result))
        return 0 if result["outcome"] == "passed" else 1
    except (RuntimeError, OSError, ValueError) as exc:
        print(json.dumps({"ready": False, "error": str(exc), "w0_accepted": False}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
