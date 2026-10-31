# First Launch in the Existing WSL

[Русский](../ru/15-current-wsl-launch.md) · [Evidence](../../world/wsl2/evidence/current-wsl-2026-11-01.json) · [W0 plan](../../planning/world.md) · [ADR-008](../../adr/008-current-wsl-direct-cgroups.md)

**Date:** 2026-11-01. At the user's direction, use existing Ubuntu-26.04 without changing its settings. No distro was created; `.wslconfig`, `/etc/wsl.conf`, PID 1 and Docker settings were unchanged. `smoke` and `inspect` succeeded; this is a first probe launch, not admission of arbitrary or developing organisms.

## Enforcement

Because systemd is disabled, add a separate [direct.py](../../world/wsl2/direct.py) backend using Linux cgroup v2 directly. Preserve the prepared systemd backend. Its strict dedicated-distro checks were not disabled: the new backend separately checks current prerequisites and actual quotas.

Only private subtree `/sys/fs/cgroup/pe-world-current-v0` exists during a probe, with an empty parent and `control`/`worker` leaves. Docker processes are never moved into it or assigned new quotas. Activate necessary controllers during execution and restore them after cleanup unless another dependent group appeared meanwhile; never disable another workload's controllers.

| Group | Memory | Swap | CPU per 100-ms interval | Tasks |
| --- | --- | --- | --- | --- |
| Aggregate | 512 MiB | 0 | 125 ms: at most 1.25 cores for controller and worker together | 128 |
| Controller | 128 MiB | 0 | 25 ms: one quarter core | 32 |
| Worker | 256 MiB | 0 | 100 ms: one core | 64 |

Read quotas back from the kernel before execution. Place the worker in its group before dropping privileges and executing bwrap. Bound file descriptors, file size, core dumps and CPU time; retain read-only rootfs, namespaces, seccomp and bounded tmpfs. Inner UID/GID are 65534; actual outer permissions belong to dedicated unprivileged `pe-organism`.

The external controller stops a probe on protocol violation, five-second heartbeat absence or 70-second runtime. `cgroup.kill` stops only its worker, then verifies no live processes remain. Parent-death signaling and bwrap `--die-with-parent` supplement this; the Windows launcher adds an 80-second outer timeout and cleanup after return. Controller-death behavior still needs a separate P2-09 test.

The shared outer WSL profile remains 28 GB/28 processors/8-GB swap at the user's choice. Internal caps bound our work, not other WSL applications. The Windows launcher requires 2 GiB free host memory before probing. This samples current reserve rather than reserving memory against all other applications.

Mechanism references: [cgroup v2](https://docs.kernel.org/admin-guide/cgroup-v2.html), [parent-death signal](https://man7.org/linux/man-pages/man2/PR_SET_PDEATHSIG.2const.html). Kernel limits and visibility were checked for these probes; stress acceptance remains incomplete.

## Installed Components

Only project infrastructure was created in existing Ubuntu: root-owned `/opt/pe-world`, `/var/lib/pe-world/runs` and unprivileged `pe-organism`. Build the rootfs from trusted system Python/libraries and BPF through libseccomp. Do not grant arbitrary Windows-file access to the world.

Neither WSL nor Docker restarted. Post-probe checks found Docker running, unchanged WSL config, no worker cgroup and restored original controller configuration. Installed source hashes match the repository.

Repeat from PowerShell:

```text
.\world\wsl2\config\run-current.ps1 -Probe smoke
.\world\wsl2\config\run-current.ps1 -Probe inspect
```

[install-current.sh](../../world/wsl2/config/install-current.sh) was already executed and refuses to overwrite the installation. The backend admits only two fixed trusted probes, not arbitrary code or candidate paths.

## Results

- `smoke`: returned expected seed/UID. Worker memory peak was 18,317,312 bytes; controller-measured runtime approximately 0.097 s.
- `inspect`: 12 checks passed: UID/GID, hidden Windows drive/home/cgroup/Docker socket, denied socket creation, denied root write, read-only root mount, private network, writable private tmpfs and cleared environment. Memory peak was 9,830,400 bytes; runtime approximately 0.067 s.
- Both probes left no live worker processes; the private cgroup was removed. Original shared configuration was verified.
- The first failed start exposed missing `wait4`/`waitid` calls required by bubblewrap's reaper. Adding them produced `wsl2-probe-v0.2`. Networking and process-creation denials remain; the failed-attempt journal was retained.
- Unit checks: Linux passed 38; Windows passed 33 and skipped five Linux-only tests.

Full counters, hashes and unchanged-configuration checks are in the [JSON evidence](../../world/wsl2/evidence/current-wsl-2026-11-01.json). It records fixed-probe results and separate installed-asset verification, not a claim that every future program is safe.

## Remaining Work

P2-09 remains `todo`: bounded memory/CPU/process/output exhaustion, hangs, controller death, cleanup and bypass testing. The initial launch establishes none of these untested properties. No developing organisms ran; admission remains closed until W0 acceptance. Revisit systemd or a separate VM by a separate decision while preserving prepared work.
