# Virtual World: Organism Habitat Boundaries

**Update:** [fixed-profile W0 acceptance passed](16-w0-acceptance.md); [dashboard and portability](17-laboratory-dashboard.md). Initial preparation context is preserved below.

[Русский](../ru/13-virtual-world.md) · [World plan W0](../../planning/world.md) · [ADR-006](../../adr/006-world-before-organism.md)

**Source:** user requirement, 2026-10-31. **Status 2026-11-01:** an [existing-WSL backend](15-current-wsl-launch.md) is installed and passed fixed probes; full W0 acceptance remains pending. The in-process scalar Python prototype itself is not an isolation boundary.

## Purpose and Architectural Placement

Before running a developing organism, build an engineered **virtual world** with bounded resources and authority. It supplies living conditions and contains execution effects within a defined scope. Do not embed completed digestion or other organs in it: the organism still develops from its genome under ADR-004.

This is first-layer infrastructure rather than another application product: **computer → external controller and isolation → virtual world → developing organism → organ functions → application outcomes**.

Developers design and change the world. Its implementation, limits and permissions do not evolve with the organism. Internal resource allocation may change but cannot exceed the external ceiling. The organism, genome, motivation and Genesis cannot expand that ceiling themselves.

## Externally Enforced Limits

| Area | Requirement |
| --- | --- |
| Memory | A hard world-wide cap, accounting for swap and service overhead, with host reserve. Exceeding it terminates or rejects work inside the world. |
| CPU | Cap aggregate CPU share over a specified scheduling interval and attempt duration. Virtual-core count alone does not sufficiently establish host-load limits. |
| Disk | Separate bounded world storage; quotas for data, temporary files, logs, snapshots, file count and I/O. Virtual-disk growth must not fill the host disk. |
| Processes | Limit process/thread counts and nested execution. Descendants share the overall budget and terminate with the attempt; leaving the controlled scope is prohibited. |
| Time | External clocks and attempt/run deadlines; an infinite loop must not prevent forced stopping. |
| Host files | System drives and user folders are not writable world resources. No physical-disk or partition-management access. Host secrets and credentials are not supplied. |
| Network and devices | External networking, physical host devices and host-management interfaces are unavailable by default. World policy and bounded interfaces specify required virtual devices and interactions. |
| Administration | No administrative authority, world-controller access, isolation configuration access or means of launching uncontrolled external executors. |

Choose actual numbers after assessing the computer and service overhead. No number here is claimed already configured. Multiple worlds also need a global ceiling: creating many organisms or evaluation runs must not evade limits. Account for search, candidate evaluation and helper execution; the external controller has its own bounded budget and reserve.

An OS/hypervisor or another selected isolation mechanism enforces limits independently of organism correctness. JSON-size checks, a separate folder, Python exceptions, step counts and voluntary process sleeping do not replace that boundary.

## Mediated Input and Output

External files enter through a broker: check size and policy → copy into the world's input area → organism reads the copy. The source file and path do not grant arbitrary host-filesystem access. Input names and paths must not escape permitted scope, including through links or special paths.

Export results as bounded artifacts through a checked channel. The organism gains no authority to write arbitrary host directories or execute exported code outside. Original inputs are read-only; internal state and working files use the allocated writable area. Developers specify channel extensions through a versioned world policy.

Protect the evaluator, criteria and reward ledger from candidate writes. World restarts or organism rollback do not clear protected achievement history. Control data and logs also have quotas so supervision cannot exhaust the host.

## Supervision and Lifecycle

A trusted controller lives outside the organism's mutable scope. It sets policy, checks actual enforcement before startup, observes costs, bounds transfers and stops the world on budget exhaustion or failure. If supervision itself fails, execution must end or be denied rather than continue unprotected.

Lifecycle: create from a known image → apply policy → verify enforcement → load initial state/genome → run → observe → stop → collect bounded output and trace → restore or remove the world through controlled operations. Incomplete output does not automatically become validated knowledge.

The organism monitoring its own boundary cannot be the only protection. Internal regulation helps, but external enforcement remains when regulation fails. Seeking extra privileges is not a motivational achievement. Organism autonomy remains inside the world; changing world rules is an engineering action.

## Implementation Choice

Following the user proposal on 2026-11-01, select [WSL2/systemd/bwrap/seccomp](14-wsl2-backend.md) as the first laboratory backend under [ADR-007](../../adr/007-wsl2-laboratory-backend.md). Code/profile are prepared but have not passed W0 acceptance. A dedicated full VM with its own disk remains an alternative for a stronger boundary. Process controls are not presented as complete file/device protection.

The subsequent direction to retain current settings is implemented under [ADR-008](../../adr/008-current-wsl-direct-cgroups.md): direct cgroup v2 instead of enabling systemd. Initial results are [here](15-current-wsl-launch.md); preserve systemd and a separate VM as alternatives.

On Windows, [Job Objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects) manage process groups, and [CPU rate control](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_cpu_rate_control_information) supports a hard CPU-share cap. These are individual controls, not the complete world. Docker containers [lack resource limits by default](https://docs.docker.com/engine/containers/resource_constraints/); calling something a container does not establish compliance.

## Acceptance Before Developing Candidates Run

1. Verify policy before startup: if mandatory protection is missing, deny execution. Contract/model design may progress in parallel; this boundary is required before developing candidates execute.
2. Use disposable data inside a test world to check forbidden out-of-scope writes and system-resource access. Do not run destructive commands against the actual system disk to demonstrate protection.
3. Test CPU loops, memory allocation, descendant creation, work-disk filling and log floods. Measure aggregate costs and host reserve, including service components.
4. Test external stopping on hangs, controller closure, exhausted budgets, escape attempts and unavailable quota mechanisms.
5. Test blocked networking, I/O-channel bypasses and policy/criterion modification. Authorized operations must continue working within bounds.
6. Test concurrent runs, temporary-resource cleanup, original-file preservation and world recovery. Record actually tested boundaries and residual platform limitations.

Platform infallibility is not assumed. Require an explicit threat model and evidence for chosen boundaries rather than treating all execution as safe by definition. Until W0 acceptance, do not use the current prototype as a protected world for arbitrary or developing variants.
