#!/bin/sh
# Explicit operator action in a dedicated distro. Does not modify .wslconfig/wsl.conf.
set -eu
umask 022
test "$(id -u)" -eq 0 || { echo 'Dedicated distro administrator required' >&2; exit 2; }
test -f /etc/programmo-world-dedicated || { echo 'Dedicated distro marker missing; refusing shared distro' >&2; exit 2; }
test "$(cat /proc/1/comm)" = systemd || { echo 'systemd must already be PID 1' >&2; exit 2; }
test ! -e /opt/pe-world || { echo '/opt/pe-world exists; refusing overwrite' >&2; exit 2; }
test ! -e /etc/systemd/system/pe-world.slice || exit 2
test ! -e /etc/systemd/system/pe-control.slice || exit 2
command -v bwrap >/dev/null
command -v python3 >/dev/null
command -v ldd >/dev/null
src="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
install -d -m 755 /opt/pe-world /opt/pe-world/probes /opt/pe-world/config
for name in controller.py seccomp.py make_rootfs.py policy.json; do
  install -m 644 "$src/$name" "/opt/pe-world/$name"
done
install -m 644 "$src/probes/smoke.py" /opt/pe-world/probes/smoke.py
install -m 755 "$src/config/run-smoke.sh" /opt/pe-world/config/run-smoke.sh
install -m 644 "$src/config/pe-world.slice" /etc/systemd/system/pe-world.slice
install -m 644 "$src/config/pe-control.slice" /etc/systemd/system/pe-control.slice
if ! id pe-organism >/dev/null 2>&1; then
  useradd --system --no-create-home --shell /usr/sbin/nologin pe-organism
fi
install -d -m 700 /var/lib/pe-world /var/lib/pe-world/runs
python3 -I /opt/pe-world/make_rootfs.py /opt/pe-world/rootfs
python3 -I /opt/pe-world/seccomp.py /opt/pe-world/seccomp.bpf
systemctl daemon-reload
systemctl start pe-world.slice pe-control.slice
echo 'Prepared trusted smoke-probe installation. W0 is NOT accepted.'
