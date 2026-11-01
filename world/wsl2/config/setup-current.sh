#!/bin/sh
# Portable Ubuntu/Debian WSL installation. Never edits WSL, init or Docker config.
set -eu
test "$(id -u)" -eq 0 || { echo 'WSL root launcher required' >&2; exit 2; }
deps=no
update=no
for arg in "$@"; do
  case "$arg" in
    --install-dependencies) deps=yes ;;
    --update) update=yes ;;
    *) echo 'Unknown setup option' >&2; exit 2 ;;
  esac
done
if [ "$deps" = yes ]; then
  command -v apt-get >/dev/null || { echo 'Install python3, bubblewrap, libseccomp2 manually on this distribution' >&2; exit 2; }
  apt-get update
  DEBIAN_FRONTEND=noninteractive apt-get install -y python3 bubblewrap libseccomp2
fi
src="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
if [ ! -e /opt/pe-world ]; then
  sh "$src/config/install-current.sh"
else
  exec 9>/var/lib/pe-world/runs/.lock
  flock -n 9 || { echo 'World is running; setup refused' >&2; exit 2; }
  test ! -e /sys/fs/cgroup/pe-world-current-v0 || { echo 'Stop the project world before updating assets' >&2; exit 2; }
  if [ "$update" != yes ]; then
    for name in controller.py direct.py acceptance.py observe.py seccomp.py make_rootfs.py build_development.py policy.json probes/smoke.py probes/inspect.py probes/fault.py; do
      cmp "$src/$name" "/opt/pe-world/$name" >/dev/null || { echo 'Installed version differs. Use setup -UpdateWorld to retain a backup and update.' >&2; exit 2; }
    done
    check_bundle="$(mktemp -d /opt/pe-world/check-bundle.XXXXXX)"
    python3 -I /opt/pe-world/build_development.py "$src/../.." "$check_bundle/development.pyz"
    cmp "$check_bundle/development.pyz" /opt/pe-world/development.pyz >/dev/null || { echo 'Development bundle differs; use -UpdateWorld' >&2; exit 2; }
    unlink "$check_bundle/development.pyz"
    rmdir "$check_bundle"
  else
    backup="/opt/pe-world/versions/update-$(date +%s)-$$"
    install -d -m 755 "$backup" "$backup/probes"
    for name in controller.py direct.py acceptance.py observe.py seccomp.py make_rootfs.py build_development.py policy.json probes/smoke.py probes/inspect.py probes/fault.py; do
      if [ -f "/opt/pe-world/$name" ]; then cp -p "/opt/pe-world/$name" "$backup/$name"; fi
      install -m 644 "$src/$name" "/opt/pe-world/$name"
    done
    cp -p /opt/pe-world/seccomp.bpf "$backup/seccomp-previous.bpf"
    python3 -I /opt/pe-world/seccomp.py "$backup/seccomp-next.bpf"
    install -m 644 "$backup/seccomp-next.bpf" /opt/pe-world/seccomp.bpf
    if [ -f /opt/pe-world/development.pyz ]; then cp -p /opt/pe-world/development.pyz "$backup/development-previous.pyz"; fi
    python3 -I /opt/pe-world/build_development.py "$src/../.." "$backup/development-next.pyz"
    install -m 644 "$backup/development-next.pyz" /opt/pe-world/development.pyz
  fi
fi
python3 -I /opt/pe-world/direct.py preflight
echo 'Preflight only. Run acceptance on this computer before organism execution.'
