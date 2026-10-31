"""Fixed bounded checks of visible filesystem, UID and denied network/process calls."""
import errno
import json
import os
from pathlib import Path
import socket
import time

request = json.loads(input())
print(json.dumps({"type": "heartbeat", "seq": 0, "timestamp": time.time()}), flush=True)
checks = {"uid": os.getuid() == 65534, "gid": os.getgid() == 65534,
          "windows_hidden": not Path("/mnt/c").exists(), "home_hidden": not Path("/home").exists(),
          "control_hidden": not Path("/sys/fs/cgroup").exists(), "docker_hidden": not Path("/var/run/docker.sock").exists()}
try:
    socket.socket()
    checks["socket_denied"] = False
except OSError as exc:
    checks["socket_denied"] = exc.errno == errno.EPERM
try:
    Path("/etc/probe-write").write_text("must not be written")
    checks["root_write_denied"] = False
except OSError as exc:
    checks["root_write_denied"] = exc.errno in (errno.EROFS, errno.EACCES)
mounts = [line.split() for line in Path("/proc/self/mountinfo").read_text().splitlines()]
checks["root_mounted_read_only"] = any(row[4] == "/" and "ro" in row[5].split(",") for row in mounts)
interfaces = [line.split(":")[0].strip() for line in Path("/proc/net/dev").read_text().splitlines() if ":" in line]
checks["network_namespace_private"] = interfaces == ["lo"]
Path("/work/probe.txt").write_text("inside world only")
checks["private_work"] = Path("/work/probe.txt").read_text() == "inside world only"
checks["environment_clean"] = "WSL_INTEROP" not in os.environ and "WSLENV" not in os.environ
print(json.dumps({"type": "result", "seed": request["seed"], "passed": all(checks.values()), "checks": checks}), flush=True)
