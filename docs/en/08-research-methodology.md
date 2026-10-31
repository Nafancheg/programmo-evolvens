# Research Methodology

[Русская версия](../ru/08-research-methodology.md) · [Project home](../../README.md)

## Initial testbed
Real data-processing tasks: parse, validate, transform, route and serialize structured records. Inputs and outputs must be verifiable. Introduce workload changes, injected failures and resource budgets.

## Comparison arms
A. Conventional fixed-policy executor.
B. Same executor with adaptive policy only.
C. Organism with regulation, memory and adaptive components.
D. Candidate evolved generation, evaluated only after Genesis approval.

## Design
Use identical task corpora, seeded workload ordering, resource budgets and hardware; randomize run order; isolate training and held-out evaluation. Repeat across seeds; report distributions and confidence intervals. Keep immutable experiment manifests (git revision, config hash, seed, environment).

## Falsification
Reject the claimed benefit if gains disappear on held-out tasks, are explained by extra resources, break functional correctness, or are not attributable to the mechanisms tested. Track time/complexity cost of adaptation.

## Observable artifacts
Event log, task outcomes, cell state transitions, resource usage, policy snapshots, ERI/competence evidence, Genesis decisions, lineage and comparable scorecards.

No dashboard metric without a traceable data source.
