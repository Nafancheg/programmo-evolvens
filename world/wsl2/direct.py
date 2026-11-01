"""Trusted smoke probes in the existing WSL distro, without an init/config change.

Only this project's private cgroup subtree is populated or killed. Arbitrary
organism code is not admitted. W0 acceptance remains a separate requirement.
"""

import argparse
import ctypes
import fcntl
import importlib.util
import json
import os
from pathlib import Path
import platform
import pwd
import resource
import selectors
import signal
import subprocess
import sys
import time
import uuid

ASSETS = Path(__file__).resolve().parent
CGROOT = Path("/sys/fs/cgroup")
BASE = CGROOT / "pe-world-current-v0"
ARCHIVE = Path("/var/lib/pe-world/runs")
CONTROLLERS = {"cpu", "memory", "pids"}
FAULTS = {"memory", "cpu", "deadline", "hang", "output", "line", "protocol", "permissions", "closed-pipes"}
LIMITS = {
    "parent": {"memory.max": "536870912", "memory.swap.max": "0", "pids.max": "128", "cpu.max": "125000 100000"},
    "control": {"memory.max": "134217728", "memory.swap.max": "0", "pids.max": "32", "cpu.max": "25000 100000"},
    "worker": {"memory.max": "268435456", "memory.swap.max": "0", "pids.max": "64", "cpu.max": "100000 100000"}
}


def shared():
    spec = importlib.util.spec_from_file_location("pe_world_shared", ASSETS / "controller.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def assert_private_path(path):
    if BASE.parent != CGROOT or BASE.name != "pe-world-current-v0":
        raise RuntimeError("invalid private cgroup root")
    if path not in (BASE, BASE / "control", BASE / "worker") or path.is_symlink():
        raise RuntimeError("refusing an unowned cgroup target")


def set_file(group, name, value):
    assert_private_path(group)
    (group / name).write_text(value)


def members(group):
    return [int(v) for v in (group / "cgroup.procs").read_text().split()]


def populated(group):
    values = dict(line.split() for line in (group / "cgroup.events").read_text().splitlines())
    return values["populated"] == "1"


def check_limits(group, values):
    for name, expected in values.items():
        if " ".join((group / name).read_text().split()) != expected:
            raise RuntimeError(f"kernel did not enforce {group.name}/{name}={expected}")


def origin_group():
    value = Path("/proc/self/cgroup").read_text().strip()
    if not value.startswith("0::/") or "\n" in value:
        raise RuntimeError("requires the unified cgroup v2 hierarchy")
    path = CGROOT / value[4:]
    resolved = path.resolve(strict=True)
    if not resolved.is_relative_to(CGROOT) or resolved.is_relative_to(BASE):
        raise RuntimeError("invalid trusted controller origin")
    return resolved


def leave_control(origin):
    # Move only our trusted PID back, never foreign processes or their quotas.
    target = origin if origin.exists() else CGROOT
    (target / "cgroup.procs").write_text(str(os.getpid()))


def preflight():
    errors = []
    if sys.platform != "linux" or platform.machine() != "x86_64" or os.geteuid() != 0:
        return ["requires the trusted WSL x86-64 administrator launcher"]
    if "microsoft" not in Path("/proc/sys/kernel/osrelease").read_text().lower():
        errors.append("not a WSL2 kernel")
    if not (CGROOT / "cgroup.controllers").exists() or not CONTROLLERS <= set((CGROOT / "cgroup.controllers").read_text().split()):
        errors.append("cpu/memory/pids cgroup v2 controllers unavailable")
    try:
        origin_group()
    except (OSError, RuntimeError) as exc:
        errors.append(str(exc))
    module = shared()
    for item in ("controller.py", "direct.py", "policy.json", "seccomp.bpf", "rootfs",
                 "rootfs.manifest.json", "probes/smoke.py", "probes/inspect.py", "probes/fault.py"):
        if not module.trusted_tree(ASSETS / item):
            errors.append(f"missing or writable trusted asset: {item}")
    if not module.trusted_tree(ARCHIVE):
        errors.append("archive must be root-owned and non-writable by the workload")
    try:
        account = pwd.getpwnam("pe-organism")
        if account.pw_uid == 0 or account.pw_gid == 0:
            errors.append("pe-organism must be unprivileged")
    except KeyError:
        errors.append("pe-organism account missing")
    return errors


def prepare_groups():
    assert_private_path(BASE)
    if BASE.exists():
        raise RuntimeError("private cgroup already exists; run trusted cleanup before retry")
    before = set((CGROOT / "cgroup.subtree_control").read_text().split())
    state = {"root_controllers_before": sorted(before), "added": sorted(CONTROLLERS - before)}
    (ARCHIVE / ".current-state.json").write_text(json.dumps(state))
    if state["added"]:
        (CGROOT / "cgroup.subtree_control").write_text(" ".join("+" + v for v in state["added"]))
    BASE.mkdir()
    for name, value in LIMITS["parent"].items():
        set_file(BASE, name, value)
    set_file(BASE, "cgroup.subtree_control", "+cpu +memory +pids")
    for child in ("control", "worker"):
        group = BASE / child
        group.mkdir()
        for name, value in LIMITS[child].items():
            set_file(group, name, value)
        set_file(group, "memory.oom.group", "1")
        check_limits(group, LIMITS[child])
    check_limits(BASE, LIMITS["parent"])
    if not (BASE / "worker/cgroup.kill").is_file():
        raise RuntimeError("kernel cgroup.kill is required before a probe starts")
    set_file(BASE / "control", "cgroup.procs", str(os.getpid()))
    if Path("/proc/self/cgroup").read_text().strip() != "0::/pe-world-current-v0/control":
        raise RuntimeError("controller did not enter its bounded cgroup")


def kill_worker():
    group = BASE / "worker"
    assert_private_path(group)
    if not group.exists():
        return
    set_file(group, "cgroup.kill", "1")
    deadline = time.monotonic() + 3
    while populated(group):
        if time.monotonic() >= deadline:
            raise RuntimeError("worker cgroup remains populated after cgroup.kill")
        time.sleep(.02)


def cleanup():
    if os.geteuid() != 0:
        raise RuntimeError("trusted administrator required for cleanup")
    assert_private_path(BASE)
    if BASE.exists():
        control = BASE / "control"
        if control.exists() and members(control):
            raise RuntimeError("controller still running; refusing to interfere")
        kill_worker()
        for name in ("worker", "control"):
            group = BASE / name
            if group.exists():
                assert_private_path(group)
                group.rmdir()
        BASE.rmdir()
    restored = False
    state_file = ARCHIVE / ".current-state.json"
    if state_file.exists():
        state = json.loads(state_file.read_text())
        added = set(state["added"])
        if not added <= CONTROLLERS:
            raise RuntimeError("invalid controller restoration state")
        foreign = [p for p in CGROOT.iterdir() if p.is_dir()]
        if not foreign:
            if added:
                (CGROOT / "cgroup.subtree_control").write_text(" ".join("-" + v for v in sorted(added)))
        restored = set((CGROOT / "cgroup.subtree_control").read_text().split()) == set(state["root_controllers_before"])
        # If Docker created a cgroup meanwhile, never disable its controllers.
        state_file.unlink()
    return {"private_cgroup_removed": not BASE.exists(), "root_controllers_restored": restored}


def sample_stats(group):
    result = {}
    for name in ("memory.peak", "memory.events", "pids.peak", "pids.events", "cpu.stat"):
        path = group / name
        if path.exists():
            result[name] = path.read_text().strip()
    return result


def runtime_identity():
    module = shared()
    result = {key: module.digest((ASSETS / name).read_bytes()) for key, name in (
        ('controller_sha256', 'direct.py'), ('shared_controller_sha256', 'controller.py'),
        ('policy_sha256', 'policy.json'), ('seccomp_sha256', 'seccomp.bpf'),
        ('rootfs_manifest_sha256', 'rootfs.manifest.json'))}
    result['kernel_release'] = platform.release()
    return result


def require_acceptance():
    module = shared()
    current = runtime_identity()
    suite = module.digest((ASSETS / 'acceptance.py').read_bytes())
    required = {'memory', 'output', 'line', 'protocol', 'hang', 'closed-pipes', 'permissions',
                'inspect', 'cpu', 'deadline', 'pids', 'controller-death-and-concurrency', 'recovery'}
    for path in sorted(ARCHIVE.parent.glob('acceptance-*.json'), reverse=True)[:16]:
        if not module.trusted_tree(path) or path.stat().st_size > 262144:
            raise RuntimeError('untrusted W0 acceptance record')
        raw = path.read_bytes()
        record = json.loads(raw)
        cases = record.get('cases', {})
        if (record.get('accepted') is True and record.get('profile') == 'existing-wsl-serial-single-thread-v0'
                and record.get('suite_sha256') == suite and required <= cases.keys()
                and all(all(cases[key].get(field) == value for field, value in current.items())
                        for key in required - {'pids', 'controller-death-and-concurrency'})):
            return {'source': str(path), 'sha256': module.digest(raw), 'profile': record['profile']}
    raise RuntimeError('current W0 acceptance required before development; run run-acceptance.ps1')


def request_bytes(seed, probe, text=None):
    payload = {}
    if text is not None:
        if probe != 'development' or not isinstance(text, str) or len(text.encode('utf-8')) > 256:
            raise ValueError('custom development text must be at most 256 UTF-8 bytes')
        payload['text'] = text
    return json.dumps({'version': 1, 'seed': seed, 'payload': payload}, ensure_ascii=False).encode('utf-8') + b'\n'


def run(seed, probe, text=None):
    request = request_bytes(seed, probe, text)
    errors = preflight()
    if errors:
        raise RuntimeError("; ".join(errors))
    if probe not in {"smoke", "inspect", "development"} | FAULTS:
        raise RuntimeError("only fixed trusted probes are admitted before W0 acceptance")
    module = shared()
    policy, policy_hash = module.load_policy()
    account = pwd.getpwnam("pe-organism")
    libc = ctypes.CDLL(None, use_errno=True)
    parent = os.getpid()
    with (ARCHIVE / ".lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        admission = None
        if probe == 'development':
            if not module.trusted_tree(ASSETS / 'development.pyz'):
                raise RuntimeError('trusted development bundle missing')
            admission = require_acceptance()
        archive_files = list(ARCHIVE.rglob("*"))
        if any(p.is_symlink() for p in archive_files):
            raise RuntimeError("archive contains a symlink")
        if (len(list(ARCHIVE.glob("*.jsonl"))) >= policy["max_runs"] or
                sum(p.stat().st_size for p in archive_files if p.is_file()) + 2 * policy["max_output_bytes"] > policy["max_archive_bytes"]):
            raise RuntimeError("bounded archive is full")
        origin = origin_group()
        prepare_groups()
        run_id = uuid.uuid4().hex
        monitor = module.Monitor(policy, time.monotonic())
        process = None
        outcome = "controller_error"
        count = 0
        hashes = {"stdout": __import__("hashlib").sha256(), "stderr": __import__("hashlib").sha256()}
        report = {"run_id": run_id, "backend": "direct-cgroup-v2", "probe": probe,
                  "seed": seed, "policy_version": policy["version"], "policy_sha256": policy_hash,
                  "input_sha256": module.digest(request), "started_unix": time.time(),
                  **runtime_identity(),
                  "wsl_global_settings_changed": False, "w0_accepted": admission is not None,
                  "admission": admission}
        report["enforced_limits"] = {kind: {name: (group / name).read_text().strip() for name in LIMITS[kind]}
                                     for kind, group in (("parent", BASE), ("control", BASE / "control"), ("worker", BASE / "worker"))}
        fd = os.open(ASSETS / "seccomp.bpf", os.O_RDONLY | os.O_NOFOLLOW)
        args = module.bwrap_args(fd)
        if probe == "inspect":
            args[args.index(str(ASSETS / "probes/smoke.py"))] = str(ASSETS / "probes/inspect.py")
        elif probe in FAULTS:
            args[args.index(str(ASSETS / "probes/smoke.py"))] = str(ASSETS / "probes/fault.py")
            args.append(probe)
        elif probe == 'development':
            args[args.index(str(ASSETS / 'probes/smoke.py'))] = str(ASSETS / 'development.pyz')
        source = ASSETS / 'development.pyz' if probe == 'development' else ASSETS / 'probes' / (
            'fault.py' if probe in FAULTS else probe + '.py')
        report['probe_sha256'] = module.digest(source.read_bytes())

        def enter_worker():
            set_file(BASE / "worker", "cgroup.procs", str(os.getpid()))
            resource.setrlimit(resource.RLIMIT_NOFILE, (256, 256))
            resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
            resource.setrlimit(resource.RLIMIT_FSIZE, (1048576, 1048576))
            resource.setrlimit(resource.RLIMIT_CPU, (70, 70))
            os.setgroups([])
            os.setgid(account.pw_gid)
            os.setuid(account.pw_uid)
            if libc.prctl(38, 1, 0, 0, 0) != 0 or libc.prctl(1, signal.SIGKILL, 0, 0, 0) != 0:
                os._exit(120)
            if os.getppid() != parent:
                os._exit(121)

        with (ARCHIVE / f"{run_id}.jsonl").open("x", encoding="utf-8") as journal:
            journal.write(json.dumps(dict(report, event="start")) + "\n")
            journal.flush()
            try:
                process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE, pass_fds=(fd,), preexec_fn=enter_worker)
                os.close(fd)
                fd = -1
                process.stdin.write(request)
                process.stdin.close()
                with selectors.DefaultSelector() as selector, (ARCHIVE / f"{run_id}.stdout").open("xb") as out, (ARCHIVE / f"{run_id}.stderr").open("xb") as err:
                    for stream, name, dest in ((process.stdout, "stdout", out), (process.stderr, "stderr", err)):
                        os.set_blocking(stream.fileno(), False)
                        selector.register(stream, selectors.EVENT_READ, (name, dest))
                    # Closing pipes must not bypass heartbeat/runtime supervision.
                    while selector.get_map() or process.poll() is None:
                        reason = monitor.tick(time.monotonic())
                        if reason:
                            outcome = reason
                            break
                        for key, _ in selector.select(.1):
                            chunk = os.read(key.fileobj.fileno(), 4096)
                            if not chunk:
                                selector.unregister(key.fileobj)
                                continue
                            name, dest = key.data
                            hashes[name].update(chunk)
                            piece = chunk[:max(0, policy["max_output_bytes"] - count)]
                            dest.write(piece)
                            dest.flush()
                            count += len(piece)
                            monitor.feed(chunk, time.monotonic(), stdout=name == "stdout")
                    else:
                        code = process.wait(timeout=2)
                        if probe == "smoke":
                            expected = {"type": "result", "seed": seed, "uid": 65534, "message": "trusted smoke probe"}
                            valid = monitor.result == expected
                        else:
                            valid = bool(monitor.result and monitor.result.get("passed") is True and monitor.result.get("seed") == seed)
                        outcome = "passed" if code == 0 and valid and not monitor.pending and not monitor.reason else "probe_failed"
            finally:
                if fd >= 0:
                    os.close(fd)
                kill_worker()
                if process is not None:
                    process.wait(timeout=3)
                report.update(outcome=outcome, returncode=process.returncode if process else None,
                              elapsed_seconds=time.monotonic() - monitor.started,
                              observed_bytes=monitor.output_bytes, captured_bytes=count,
                              observed_sha256={name: h.hexdigest() for name, h in hashes.items()},
                              result=monitor.result, worker_stats=sample_stats(BASE / "worker"),
                              worker_populated_after=populated(BASE / "worker"),
                              hash_scope="observed bytes before stopping")
                # Move only this trusted controller back for removal of its own subtree.
                leave_control(origin)
                report["cleanup"] = cleanup()
                journal.write(json.dumps(dict(report, event="finish")) + "\n")
        return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("preflight", "smoke", "inspect", "development", "cleanup", *sorted(FAULTS)))
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument('--text-stdin', action='store_true', help='bounded text data for the fixed development genome')
    args = parser.parse_args()
    try:
        if args.mode == "cleanup":
            with (ARCHIVE / ".lock").open("a") as lock:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                print(json.dumps(cleanup()))
            return 0
        if args.mode == "preflight":
            errors = preflight()
            print(json.dumps({"ready": not errors, "errors": errors, "w0_accepted": False}))
            return 2 if errors else 0
        text = None
        if args.text_stdin:
            raw = sys.stdin.buffer.read(257)
            if len(raw) > 256 or args.mode != 'development':
                raise ValueError('text input requires development and at most 256 UTF-8 bytes')
            text = raw.decode('utf-8')
        result = run(args.seed, args.mode, text)
        print(json.dumps(result))
        return 0 if result["outcome"] == "passed" else 1
    except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as exc:
        print(json.dumps({"error": str(exc), "w0_accepted": False}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
