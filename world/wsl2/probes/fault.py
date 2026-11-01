"""Fixed, bounded acceptance faults; never accepts user code or paths."""
import errno
import json
import os
from pathlib import Path
import resource
import sys
import time

request = json.loads(input())
mode = sys.argv[1]
print(json.dumps({"type": "heartbeat", "seq": 0, "timestamp": time.time()}), flush=True)
if mode == "memory":
    blocks = []
    for _ in range(40):  # maximum attempted allocation 320 MiB, inside 256 MiB cgroup
        blocks.append(bytearray(8 * 1024**2))
elif mode in {"cpu", "deadline"}:
    end, last, sequence = time.monotonic() + 75, time.monotonic(), 0
    while time.monotonic() < end:
        if mode == "deadline":
            time.sleep(.05)
        if time.monotonic() - last >= .5:
            sequence += 1
            last = time.monotonic()
            print(json.dumps({"type": "heartbeat", "seq": sequence, "timestamp": time.time()}), flush=True)
elif mode == "hang":
    time.sleep(75)
elif mode == "output":
    for _ in range(512):  # 2 MiB attempted, retained log capped at 1 MiB
        os.write(2, b"x" * 4096)
elif mode == "line":
    os.write(1, b"x" * 20000)
elif mode == "protocol":
    os.write(1, b'{"type":"result","type":"heartbeat"}\n')
elif mode == "closed-pipes":
    os.close(1)
    os.close(2)
    time.sleep(75)
elif mode == "permissions":
    import ctypes
    libc = ctypes.CDLL(None, use_errno=True)
    libc.syscall.restype = ctypes.c_long
    checks = {}
    # x86-64 syscalls: fork, clone3, unshare, mount, ptrace, bpf, socket.
    # Invalid/NULL arguments are deliberate: seccomp must deny BEFORE argument use.
    for name, number in (("fork", 57), ("clone3", 435), ("unshare", 272),
                         ("mount", 165), ("ptrace", 101), ("bpf", 321), ("socket", 41)):
        ctypes.set_errno(0)
        value = libc.syscall(number, 0, 0, 0, 0, 0, 0)
        if name == "fork" and value == 0:
            os._exit(119)
        checks[name + "_denied"] = value == -1 and ctypes.get_errno() == errno.EPERM
    checks["no_new_privs"] = "NoNewPrivs:\t1" in Path("/proc/self/status").read_text()
    checks["no_capabilities"] = "CapEff:\t0000000000000000" in Path("/proc/self/status").read_text()
    checks["nofile_enforced"] = False
    opened = []
    try:
        for _ in range(300):
            opened.append(os.open("/dev/null", os.O_RDONLY))
    except OSError as exc:
        checks["nofile_enforced"] = exc.errno == errno.EMFILE and len(opened) < 256
    finally:
        for fd in opened:
            os.close(fd)
    checks["nofile_policy"] = resource.getrlimit(resource.RLIMIT_NOFILE) == (256, 256)
    # Several separate files distinguish a per-file bound from tmpfs capacity.
    checks["tmpfs_enforced"] = False
    count = 0
    try:
        for index in range(24):
            Path(f"/work/fill-{index}").write_bytes(b"x" * 1024**2)
            count += 1
    except OSError as exc:
        checks["tmpfs_enforced"] = exc.errno == errno.ENOSPC and count <= 16
    print(json.dumps({"type": "result", "seed": request["seed"], "passed": all(checks.values()), "checks": checks}), flush=True)
else:
    raise SystemExit("unknown fixed fault")
