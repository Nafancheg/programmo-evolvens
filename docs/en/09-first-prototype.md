# First Prototype

**Current priority:** the [first bioengine cycle](11-bioengine-and-applications.md). This document describes the existing scalar foundation; autonomous search, assimilation and cells remain to be built.

**Isolation:** [ADR-006](../../adr/006-world-before-organism.md) requires an accepted [W0 world](13-virtual-world.md) before developing/mutating variants execute. This in-process prototype does not provide that protection; its fixed examples and trusted development checks do not demonstrate isolation.

[Русский](../ru/09-first-prototype.md) · [Project home](../../README.md) · [Phase 1 to-dos](../../planning/phase-1.md)

**Date:** 2026-10-31. A research sequential Python executor with no external dependencies. Targets Python 3.11+, locally tested on Python 3.14. Copy the repository and run from its root:

```text
python -m programmo_evolvens --output artifacts/smoke.json
python -m unittest discover -s tests -v
```

The first command runs three genomes on the same executor class, compares outputs with simple reference functions and exits nonzero on mismatch. The second checks contracts and failures. The report includes all outputs, signals, node traces, actual per-run timing, environment information and file SHA-256 hashes. Reports are created locally; `artifacts/` is excluded from Git.

## What runs

| Genome | Input | Outcome |
| --- | --- | --- |
| [anomaly](../../examples/genomes/anomaly.json) | Five numeric observations, including threshold 75 | `normal` for ≤75, `anomaly` and a signal for >75. |
| [normalize](../../examples/genomes/normalize.json) | Four JSONL records with a text `name` field | Strip surrounding whitespace, lowercase, store the last value and signal. Single-field normalization, not a full file validator. |
| [queue](../../examples/genomes/queue.json) | Five arrival ticks | Batch size 4 for depth >3, otherwise 1; bounds 1–4; `ACT` removes actual items from an in-memory FIFO queue. Counts, processed-item order and remaining items are compared. |

The eight PPs live in [runtime.py](../../programmo_evolvens/runtime.py), scenarios and the authorized queue adapter in [demo.py](../../programmo_evolvens/demo.py). The `queue_take` adapter only takes the declared number of items; the genome defines batch selection policy. `TRANSFORM` currently supports only `strip` and `lower`. The executor does not branch on genome names; reference functions live in the demonstration evaluator.

## Working JSON v0 format

A genome contains `schema_version: 0`, `id`, ordered `steps` and `outputs`. Each step has `id`, `pp`, `version: 1`, `inputs`, `params`. An input binding is exactly one object `{"literal": ...}` or `{"ref": "earlier_id"}`. Port types are currently only `number` (finite numeric value), `text` and `bool`. Arrays and objects are not port values in v0.

See the genome files for complete structures. Forward references, cycles, duplicate IDs, unknown fields/operations/versions, incompatible types and missing outputs are rejected before execution. All `SENSE` observations are checked for presence and type before the first effect. This is a linear representation of an acyclic graph, not yet a complete model of multiple genes, cells and organs. The schema is experimental: [ADR-002](../../adr/002-first-executor.md).

| PP | v1 contract |
| --- | --- |
| `SENSE` | `params.source/type`; returns a typed observation supplied by the host. |
| `COMPARE` | Numeric `left/right`; `operator`: `gt`, `ge`, `lt`, `le`, `eq`; returns `bool`. |
| `TRANSFORM` | Text `value`; operation `strip` or `lower`; returns `text`. |
| `DECIDE` | `condition: bool`, same-type `if_true/if_false`; returns the selected value. Branches do not lazily execute nodes. |
| `ACT` | `value` of the adapter's declared type; `params.target` must be host-authorized. Output is checked against the adapter contract. |
| `STORE` | `params.mode/key/type`; `write` accepts `value`, `read` has no inputs. Missing keys or wrong types fail. Storage exists only in the Runtime object's memory. |
| `SIGNAL` | Any scalar port `value`, `when: bool`; true appends an event to the local `channel` list; always returns `value`. No network delivery. |
| `REGULATE` | Numeric `value`, `params.key/min/max`; clamps the value and stores the setting. Genome bounds must fit host-authorized bounds. |

## Limits and remaining work

The host defaults to 64 steps and 65,536 bytes of JSON payload. It checks genome size, observations and the aggregate of computed values/state/signals. These are logical limits on already loaded data, not process memory quotas or protection against a hanging trusted adapter. Hard timeouts, isolation, aggregate cell quotas and parallelism remain in P2/P1-07.

`STORE` and regulation commit only after a successful run. On a node failure, `RunError.trace` contains the trace up to failure. An external `ACT` already performed is not automatically undone, so the host must decide about retries; there are no automatic retries. Trusted adapters run as ordinary host code. This prototype is not a facility for safely executing arbitrary code.

Traces and durations are observable, but fixtures are public and small. Checks do not validate performance, sufficiency of 8–12 PPs or the full genome-section experiment. There is no learning, Genesis, inter-generation inheritance or complete cell model. P1-05/06 remain open: full E0, resource measurements, predeclared thresholds, held-out data and an independent evaluator are needed. Further directions are preserved in the [idea register](../../planning/ideas.md).
