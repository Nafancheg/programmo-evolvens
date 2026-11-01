# W0 boundary acceptance

**Result, 2026-11-01:** 13 scenarios passed; 46 Linux tests, 39 Windows tests and seven Linux-only skips. Acceptance covers only the described profile.

[Русский](../ru/16-w0-acceptance.md) · [Measurements](../../world/wsl2/evidence/w0-acceptance-2026-11-01.json) · [Plan](../../planning/world.md) · [ADR-009](../../adr/009-w0-acceptance-scope.md)

## Verification scope

Acceptance covers the serial, single-threaded Python profile in the existing WSL: aggregate 512 MiB/1.25 cores/128 tasks, worker 256 MiB/one core/64 tasks, no swap. The syscall set, rootfs, read-only input, bounded tmpfs and channels are fixed. A second concurrent launch is rejected. WSL and Docker settings remain unchanged.

This permits using the verified boundary for the next development stage; it does not claim safety for arbitrary code or absence of kernel vulnerabilities. A new candidate entry point must reuse the same boundary. Networking, processes/threads, extra packages, mounts or permission expansion require a policy change and renewed acceptance. The organism cannot authorize those changes.

## Trials

| Scenario | Required observed result |
| --- | --- |
| Memory | Attempt 320 MiB allocation inside a 256 MiB worker; cgroup OOM kill event |
| Output | Stderr stream above 1 MiB is stopped; at most 1 MiB combined output retained |
| Long line | More than 16 KiB without newline → `line_limit` |
| Protocol | Duplicate JSON key → `protocol_error` |
| Hang | Missing heartbeat → stop after five seconds |
| Closed channels | Closing stdout/stderr does not bypass supervision; stop after five seconds |
| Permissions | Deny fork/clone3, namespaces, mount, ptrace, BPF and socket; no capabilities, no_new_privs enabled |
| Storage and descriptors | Enforce 16 MiB tmpfs and 256 descriptor limits |
| Visibility | Check UID/GID, filesystem, networking and cleared environment |
| CPU | Saturate one core: observe throttling and CPU-time or wall-time termination |
| Wall deadline | Heartbeats continue with mostly idle CPU; stop after 70 seconds |
| Tasks | Trusted infrastructure helper reaches 64 tasks in the same worker; kernel denies another |
| Controller death | Worker empties after controller SIGKILL; concurrent launch is rejected |
| Recovery | Cleanup and a normal smoke probe succeed after the failure |

Every normally observed case checks an empty worker, private cgroup removal and controller restoration. The external tester performs those checks after controller death. WSL state and Docker PIDs are compared before and after the full series.

The pids helper is fixed trusted infrastructure code temporarily creating sleeping processes inside worker quotas. The workload profile still forbids process creation: seccomp was not relaxed to test the task limit.

## Reproduction and logs

Suite: [acceptance.py](../../world/wsl2/acceptance.py), fixed faults: [fault.py](../../world/wsl2/probes/fault.py). The installed copy is root-owned; user paths or code are not accepted. Run from PowerShell:

```text
.\world\wsl2\config\run-acceptance.ps1
```

The outer suite deadline is 200 seconds, each run has an 80-second outer deadline; the Windows free-memory check requires at least 2 GiB. Expected suite duration is about 160 seconds because two independent trials last 70 seconds each.

Logs remain in `/var/lib/pe-world/runs`, summaries in `/var/lib/pe-world/acceptance-*.json`. Input, policy and executable components have SHA-256 hashes in the report. A full active journal rejects launches; an operator may preserve older files in `runs/history`, without deletion and within the total 32 MiB budget. Active runs are limited to 16.

The first series stopped on an overly narrow CPU-test expectation: the kernel stopped the process around 70 seconds before the controller, exit code 137. This negative tester result is preserved. The final series admits both intended CPU-trial deadlines and separately tests the wall deadline on another process.

## Next-stage boundary

Environment acceptance does not establish an organism, learning or evolution. Next come the cell/genome contracts, traceable structural unfolding P1-17 and development P1-18. Function must follow from the resulting elements and connections; a mature organ hard-coded into the environment cannot substitute for it.

Individual `w0_accepted: false` records describe a probe executed before the aggregate decision. Positive acceptance is recorded in `acceptance.accepted`; the dashboard additionally checks hashes and the kernel version.
