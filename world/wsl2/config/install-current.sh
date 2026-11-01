#!/bin/sh
# Install only project-owned assets/account. Never changes WSL init or Docker.
set -eu
umask 022
test "$(id -u)" -eq 0 || { echo 'Trusted WSL administrator required' >&2; exit 2; }
test ! -e /opt/pe-world || { echo 'Existing installation: inspect rather than overwrite' >&2; exit 2; }
for tool in bwrap python3 ldd useradd; do command -v "$tool" >/dev/null; done
src="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
install -d -m 755 /opt/pe-world /opt/pe-world/probes /opt/pe-world/config
for name in controller.py direct.py acceptance.py observe.py seccomp.py make_rootfs.py build_development.py policy.json; do
  install -m 644 "$src/$name" "/opt/pe-world/$name"
done
for name in smoke inspect fault; do install -m 644 "$src/probes/$name.py" "/opt/pe-world/probes/$name.py"; done
if ! id pe-organism >/dev/null 2>&1; then useradd --system --no-create-home --shell /usr/sbin/nologin pe-organism; fi
install -d -m 700 /var/lib/pe-world /var/lib/pe-world/runs
python3 -I /opt/pe-world/make_rootfs.py /opt/pe-world/rootfs
python3 -I /opt/pe-world/seccomp.py /opt/pe-world/seccomp.bpf
python3 -I /opt/pe-world/build_development.py "$src/../.." /opt/pe-world/development.pyz
echo 'Current-distro trusted probe assets installed. WSL/Docker settings unchanged; W0 not accepted.'
