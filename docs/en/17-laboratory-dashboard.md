# Laboratory dashboard and installation on another PC

[Русский](../ru/17-laboratory-dashboard.md) · [W0 acceptance](16-w0-acceptance.md) · [Observation phase](../../planning/phase-6.md)

## Open the laboratory

From the repository root in PowerShell:

```powershell
.\scripts\start-lab.ps1
```

This opens `http://127.0.0.1:8765`. The terminal keeps the server running; Ctrl+C ends observation. Use `-Port 8766` for another port, `-NoBrowser` to skip opening the browser. Alternatively run `python -m programmo_evolvens.lab --open`.

The page displays the current probe, CPU, memory, process/thread count, W0 acceptance applicability, the latest 80 runs and source events with hashes. Data refreshes every two seconds. Search filters IDs and probes; selecting a row reveals its source event. Pause stops page refresh, not the world. The interface switches between RU and EN.

A short probe may finish between samples: its measured peak memory appears in the journal but may not appear on the live chart. CPU uses external counter deltas; the first sample of a new run has no estimate. Missing sources show an error rather than fabricated zeros. Interrupted runs differ from completed ones; expected stops from accepted trial series have separate labels.

First prescribed cell development is demonstrated in a [limited experiment](18-prescribed-development.md); generations and organ functions remain pending. The dashboard can run the fixed experiment with custom text; code and genome remain unchanged. Acceptance applies only when controller, policy, seccomp, rootfs-manifest and tester hashes match installed components.

## New Windows PC

The initial installer targets Windows x64 with WSL2 Ubuntu/Debian, Windows Python 3.11+ and package-repository access. Node, Docker, npm and external AI are unnecessary. Actual checks used the current Ubuntu-26.04/Python 3.14; a clean second PC and a systemd distribution have not been tested yet.

If WSL is missing, follow [Microsoft's installation instructions](https://learn.microsoft.com/en-us/windows/wsl/install): `wsl --install -d Ubuntu`, perform any requested restart and complete first launch. Windows Python is available on the [official download page](https://www.python.org/downloads/windows/). Setup checks these prerequisites and explains missing items; it does not restart Windows or create a distribution without a separate user command.

Clone the repository or extract its ZIP. From its root:

```powershell
.\scripts\setup-lab.ps1 -InstallDependencies
.\world\wsl2\config\run-acceptance.ps1
.\scripts\start-lab.ps1
```

To select a specific installed distribution:

```powershell
.\scripts\setup-lab.ps1 -Distro Ubuntu -InstallDependencies
```

The choice is saved in ignored `.local/lab.json`. Subsequent commands use it; override with `-Distro` or `PE_WSL_DISTRO`. Neither Ubuntu-26.04 nor a user's home path is hard-coded in setup. There is no need to transfer `.local` from the previous PC.

Setup adds `python3`, `bubblewrap`, `libseccomp2`, root-owned `/opt/pe-world`, bounded log storage and a service account. It preserves `.wslconfig`, `/etc/wsl.conf`, Docker and init mode. Foreign cgroup quotas remain unchanged; the trusted controller returns only its own PID to its original group. Missing mandatory enforcement blocks execution.

Logs and a positive report from this computer do not verify the new PC. Run acceptance again; if it fails the dashboard remains available for diagnosis, but organism admission is unconfirmed.

## Update and check

```powershell
.\scripts\setup-lab.ps1 -CheckOnly
.\scripts\setup-lab.ps1 -UpdateWorld
```

Check-only leaves installation unchanged. Updating requires a stopped world, uses the shared lock, preserves previous components in `/opt/pe-world/versions` and retains logs. A different installation is not overwritten without `-UpdateWorld`. Repeat acceptance when profile components change. At 16 active journals further runs are rejected: preserve old files in `runs/history` within the total budget, without deleting evidence.

The server binds only to `127.0.0.1`; its HTTP interface supports reading and one bounded text-check action under [ADR-012](../../adr/012-bounded-custom-text-experiments.md). The WSL exporter executes fixed journal/cgroup-reading code. The page cannot supply commands or arbitrary paths.

**Update, 2026-11-01:** the laboratory includes a resulting instance, genome/source from its executed bundle, specimen JSON export and stepwise recorded replay. After acceptance run `.\scripts\run-development.ps1` to create an instance on this PC. [Result description](18-prescribed-development.md).

**Custom text:** enter at most 256 UTF-8 bytes and click “Check twice”. This uses a fixed genome and does not establish learning. [Repeatability checks](19-custom-text-repeatability.md).
