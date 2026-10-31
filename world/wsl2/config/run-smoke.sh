#!/bin/sh
# Reviewed installation under /opt/pe-world is required. No WSL settings changed here.
set -eu
test "$(id -u)" -eq 0 || { echo 'Run as the dedicated distro administrator' >&2; exit 2; }
run_id="$(cat /proc/sys/kernel/random/uuid | tr -d '-')"
exec systemd-run --system --wait --pipe --quiet --service-type=exec \
  --unit="pe-control-${run_id}.service" --slice=pe-control.slice \
  --property=MemoryMax=128M --property=MemorySwapMax=0 --property=TasksMax=32 \
  --property=CPUQuota=25% --property=RuntimeMaxSec=85s \
  --property=TimeoutStopSec=1s --property=KillMode=control-group \
  --property=LimitNOFILE=256 --property=LimitCORE=0 \
  /usr/bin/python3 -I /opt/pe-world/controller.py smoke --seed=1
