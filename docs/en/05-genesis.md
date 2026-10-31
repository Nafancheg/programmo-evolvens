# Genesis

[Русская версия](../ru/05-genesis.md) · [Project home](../../README.md)

Genesis independently assesses organism capability and decides whether a new generation is justified. It does **not** accept the organism's self-reported readiness as authoritative.

## Evidence pipeline
1. Collect external requirements and observed task outcomes.
2. Test on unseen challenges, including fault recovery and transfer of learning.
3. Identify a persistent capability gap after reasonable in-generation adaptation.
4. Check whether Genesis is competent to evaluate the current system.
5. If not competent: first propose, validate and admit an improved Genesis.
6. Produce a measurable evolutionary request (problem, evidence, target, constraints, acceptance tests).
7. Build a new configuration/implementation using controlled engineering.
8. Independently compare candidate versus parent and baseline; approve or reject.

## ERI
Evolutionary Readiness Index is a **candidate** multi-dimensional assessment, not a magic score. Initially use explicit per-dimension thresholds and safety gates; no universal threshold across generations. Generation change requires a demonstrable capability gap AND credible improvement under held-out tests.

## Governance
Validation criteria are frozen before candidate evaluation. Rollback and a human approval gate are mandatory at research stage.
