# First W0 Backend: WSL2, systemd and Bubblewrap

[Русский](../ru/14-wsl2-backend.md) · [World boundaries](13-virtual-world.md) · [Code](../../world/wsl2/controller.py) · [Plan](../../planning/world.md) · [ADR-007](../../adr/007-wsl2-laboratory-backend.md)

**Date:** 2026-11-01. **Status:** reviewable code/configuration prepared; installation and W0 acceptance are pending. No developing organism was executed.

## What We Adopt

WSL2 supplies the outer compute envelope; cgroup v2/systemd limits execution groups; bubblewrap constructs filesystem/namespaces; seccomp restricts syscalls. Control, world rules and the journal stay outside organism-writable scope. This is a first laboratory backend, not a claim of protection against arbitrary kernel attacks.

WSL2 has shared resources and a shared kernel; a dedicated distribution is not a separate hardware VM per organism. A stronger dedicated VM remains an alternative if the threat model requires it. Admit a profile only after ADR-006 checks.

## Observed Local Environment

A read-only check on 2026-11-01 found Ubuntu-26.04/WSL2, bubblewrap 0.11.1 and cgroup v2 with `cpu`, `memory`, `pids`. PID 1 is not systemd; `/etc/wsl.conf` specifies `systemd=false` and a Docker startup command. Shared `.wslconfig` permits 28 GB RAM, 28 processors and 8 GB swap. These settings were not changed; `wsl --shutdown` was not executed.

Propose a dedicated `ProgrammoWorld` distribution. The [`.wslconfig` template](../../world/wsl2/config/wslconfig.example) proposes 4 GB, 2 processors and no swap; this is a reviewable profile, not an applied setting. It affects all WSL2 distributions. The [`wsl.conf` template](../../world/wsl2/config/wsl.conf.example) enables systemd and disables drive automount, fstab processing and Windows interop in the dedicated distribution.

[WSL documentation](https://learn.microsoft.com/en-us/windows/wsl/wsl-config) explains scope and restart requirements. Changing shared resources and stopping other distributions needs separate agreement; no installation was performed here.

## Launch-Scheme Corrections

1. Use `pe-world.slice` as the aggregate group and a transient `.service` per run. Do not use a template `.scope`: scopes are created programmatically, while a service supports execution settings such as descriptor limits.
2. `CPUQuota=100%` means one CPU core, not the entire host. The aggregate slice has one core, 512 MiB with no swap and 128 tasks; each run has 256 MiB, 64 tasks and 256 descriptors. The separate controller group has 128 MiB, 25% of a core and 32 tasks. These are nested budgets rather than multiplied allowances per organism.
3. Use `RuntimeMaxSec=70s` for execution and `TimeoutStopSec=1s` for stopping. `TimeoutSec=70` alone does not establish an active-runtime limit. The controller has a separate 85-second cap.
4. `--seccomp 10` names an open BPF file descriptor, not profile number 10. A trusted worker opens the file inside the service and passes its actual FD to bwrap; an arbitrary controller descriptor is not assumed inherited through systemd.
5. In addition to network/PID, isolate user, IPC, UTS and cgroup namespaces, drop capabilities/environment, create a new session and stop with the parent. Inside UID/GID are 65534; outside, the service uses dedicated unprivileged `pe-organism`.
6. Use a prepared read-only Python rootfs. `/work` and `/tmp` are bounded 16/8-MiB tmpfs mounts. Do not expose writable Windows directories, home, Docker socket, D-Bus or management interfaces.

References: [scope](https://www.freedesktop.org/software/systemd/man/latest/systemd.scope.html), [resource control](https://www.freedesktop.org/software/systemd/man/latest/systemd.resource-control.html), [service](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html), [bubblewrap](https://github.com/containers/bubblewrap/blob/main/README.md). Prepared files do not establish actual limit enforcement.

## Controller and Probe

[controller.py](../../world/wsl2/controller.py) includes preflight, shell-free argv construction, actual cgroup-limit checks, a bounded JSONL parser, heartbeat timing using controller monotonic time and whole-service stopping. The worker has `BindsTo` to the controller service. Five seconds without heartbeat ends the attempt; workload timestamps cannot extend deadlines. Heartbeat indicates liveness only, not useful progress or maturity.

Combined stdout/stderr is capped at 1 MiB and each line at 16 KiB. Exceeding a cap stops the run; truncated streams are not complete results. The archive is capped at 32 MiB and 16 runs; refuse new probes when full. V0 is serial and never automatically deletes old outcomes.

JSONL records seed, policy version/hash, input/filter/controller/rootfs-manifest hashes, outcome and hashes of observed output. Hash scope is explicit: unseen output after forced stopping is unknown. Store records in `/var/lib/pe-world/runs`, outside the organism filesystem.

V0 admits only a fixed [smoke probe](../../world/wsl2/probes/smoke.py), not arbitrary code/paths or developing candidates. Check its result against seed and UID. The [seccomp builder](../../world/wsl2/seccomp.py) creates an x86-64 allowlist for a single-threaded Python probe, denying networking and process creation. It is not a universal organism profile or a fork-load process-quota test.

## Prepared Installation Actions

First select/create a separate distribution and agree on shared `.wslconfig`. In the dedicated distro, apply `wsl.conf`, restart at an agreed time and install required packages (`python3`, `bubblewrap`, `libseccomp2`, systemd and `ldd`). `/etc/programmo-world-dedicated` records the operator's distro choice; it is not a security boundary.

After reviewing [install-dedicated.sh](../../world/wsl2/config/install-dedicated.sh), the operator runs it in the dedicated distro. It refuses to overwrite an existing installation, creates `pe-organism`, installs trusted components under `/opt/pe-world`, builds a rootfs from system Python/libraries, creates BPF and installs slice files. It changes neither `.wslconfig` nor `/etc/wsl.conf` and does not launch an organism. Partial installation failures need investigation; no automatic deletion occurs.

Prepared post-installation sequence:

```text
python3 -I /opt/pe-world/controller.py preflight
sudo /opt/pe-world/config/run-smoke.sh
```

Linux preflight currently refuses correctly: systemd is not PID 1, closed configuration and installed trusted images are absent. `ready` describes probe prerequisites; even a successful probe returns `w0_accepted: false`.

## Verified and Pending Work

33 unit checks passed on Windows Python 3.14.0 and WSL Python 3.14.4. WSL checks covered both shell scripts' syntax and BPF construction using installed libseccomp; no filter was loaded into a running organism. Preflight refusal in the unprepared environment was verified. These are ordinary trusted development checks, not developing-organism execution.

Installation, rootfs/bwrap startup, end-to-end systemd probing, memory/CPU/process/controller-failure tests, bypass tests, disk/service accounting and Windows reserve verification remain undone. P2-09 remains `todo`; W0 is not accepted. Developing candidates must not run before acceptance.

## World Semantics

Record a separate design concern: structured observations/actions, available resources/hazards, transition rules, task generation and the Genesis↔world contract. JSONL/stdin/stdout transport does not itself define these semantics. The observation/action interface belongs to the environment; phenotype is the organism's realized organization and behavior under ADR-004.

W0 safety rules remain fixed. A generator may create varied task/world instances only inside these rules, with recorded versions and seeds. Do not change assessment criteria after seeing a candidate answer. Niches, depletable resources and health maintenance remain later tasks rather than expanding the first isolator to include everything.

[POET](https://arxiv.org/abs/1901.01753) already generates environments and transfers solutions. Do not claim established uniqueness for our generator or Genesis contract. Our organism needs its own working contracts; reuse existing tools where suitable.
