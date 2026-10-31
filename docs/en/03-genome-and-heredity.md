# Genome and Heredity

[Русская версия](../ru/03-genome-and-heredity.md) · [Project home](../../README.md)

The genome is a **versioned declarative manifest**, not source code. Candidate fields: identity, component types, dependency graph, exposed capabilities, policy constraints, resource envelopes, compatibility schema and rollback hooks.

Three separately versioned inheritances:
1. Genome: validated functional composition and immutable constraints.
2. Regulatory state: optional effective settings, with expiry and scope.
3. Validated knowledge: generalizable lessons with source, confidence, applicability and expiry.

Do not inherit raw transient failures, unverified interpretations or secrets. Each inheritance decision carries evidence and can be reversed.

A new generation must provide a migration plan, compatibility checks and tests on a held-out workload.
