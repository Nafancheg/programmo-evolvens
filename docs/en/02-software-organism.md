# Software Organism

[Русская версия](../ru/02-software-organism.md) · [Project home](../../README.md)

## Operational definition
A runtime system that (1) accepts tasks from an external environment, (2) executes with bounded resources, (3) monitors itself, (4) updates non-code policy from outcomes, and (5) emits an auditable evolutionary request when a structural limitation is demonstrated.

## State
Identity; generation G; maturity M; genome version; cells and capabilities; resource budgets; regulatory signals; episode and knowledge stores; health; provenance.

## Invariants
- No arbitrary executable code modification by the organism.
- No self-authorized reproduction.
- Every action and adaptation is logged with timestamps, inputs and outcomes.
- Failed adaptation must be reversible.
- An unhandled task is evidence of a gap, not automatic reproduction.

## Lifecycle
Birth -> operation -> adaptation/learning -> assessment -> continued operation OR Genesis-controlled reproduction. Prior generations remain available as baselines or for rollback.
