# Genome and Heredity

[Русская версия](../ru/03-genome-and-heredity.md) · [Project home](../../README.md) · [ADR-001](../../adr/001-genetic-model.md)

**Status — 2026-10-31:** agreed architectural direction; the genome format, runtime and experiment have not been implemented. Composition from a small primitive set remains an untested hypothesis.

## Biological analogy and levels of organization

DNA consists of **nucleotides**, whereas proteins consist of **amino acids**. Genes encode functional products, including RNA and, through translation, proteins. The software model uses this relationship between description and function as an analogy, rather than literally reproducing molecular biology.

Working hierarchy: **nucleotide → gene → functional mechanism → cell → organ → organism**.

| Level | Meaning in Programmo Evolvens |
| --- | --- |
| Nucleotide | Minimal genome encoding element, such as a typed symbol or structural token. The alphabet and format remain undecided. |
| Gene | Versioned, heritable description of a function or property: primitive composition, connections, parameters and constraints. |
| Functional mechanism | Behavior assembled from available implementations of functional primitives according to a gene description. |
| Cell | Isolated executable component with a contract, state and health indicators, implementing mechanisms. |
| Organ | Coordinated group of cells serving a common function. |
| Organism | Complete adaptive software system with a genome, organs, memory and regulation. |

These are responsibility levels, not a requirement for a one-gene-to-one-cell mapping: a mechanism may depend on several genes, and a cell may implement several mechanisms.

## Two distinct kinds of primitives

An **atomic encoding element (a “nucleotide”)** belongs to the syntax used to represent the genome. A **functional primitive (Programmatic Primitive, PP)** is a minimal semantic capability with a formal contract, available for composition. One PP may require many encoding elements; a token alone is not an executable capability. PP atomicity is relative to the chosen behavioral model, rather than processor instructions.

Python, C#, Rust and other programming languages **are not genome primitives** or amino-acid equivalents. They implement the runtime and adapters. The genome describes structure and capabilities; the runtime binds that description to validated implementations. Language independence is a project requirement that still needs testing by comparing the behavior of different implementations.

## Declarative genome

The genome is a **versioned, programming-language-independent declarative manifest**, not source code. It should describe identity, genes, component types, data/control graphs, exposed capabilities, parameters, immutable policy constraints, resource envelopes, contract versions, compatibility and rollback hooks. The concrete schema and serialization remain undecided.

The description references a versioned registry of available primitives. Naming an unknown operation or embedding executable text cannot create a new capability. Types, connections, permissions and budgets must be checked before execution. A new primitive implementation requires a separate controlled engineering change and validation.

## Candidate functional primitive set

| PP | Purpose | Responsibility boundary |
| --- | --- | --- |
| `SENSE` | Obtain an observation from the environment | Read through an authorized source; return a value and provenance. |
| `COMPARE` | Compare values or states | Return a relation, deviation or match; do not select an action. |
| `TRANSFORM` | Transform data | Apply a declared typed transformation; do not hide a complete task or arbitrary code. |
| `DECIDE` | Select a branch or action | Apply a declared policy; return a choice without performing an external action. |
| `ACT` | Perform an action | Produce an authorized external effect and return its outcome. |
| `STORE` | Save and retrieve state or experience | Explicitly declare read/write mode, scope, retention and provenance. |
| `SIGNAL` | Send an event or message | Respect the declared delivery protocol and addressing. |
| `REGULATE` | Change control parameters | Change only permitted parameters within allowed ranges; do not rewrite the genome or invariants. |

These are candidates, not a final alphabet. In particular, combining reads and writes in `STORE`, overlap between `ACT`/`SIGNAL`, and the generality of `TRANSFORM` need testing. The set may be revised based on evidence, with an explicitly versioned decision.

Illustrative composition: `SENSE → COMPARE → DECIDE → SIGNAL` for threshold-based anomaly detection. An actual mechanism needs typed ports, forwarding of the original observation, branching conditions and failure handling; a list of names is not an executable genome.

## Contract for each PP

Before implementation, each primitive must define:

1. Identifier, semantics, version and compatibility rules.
2. Input/output types and units, valid ranges, preconditions and postconditions.
3. Permitted effects, state access, permissions and isolation scope.
4. Time, memory, I/O and data-volume limits; behavior on budget exhaustion.
5. Errors, timeouts, cancellation, retry rules, idempotency and recovery.
6. Determinism or sources of randomness/time, observable events and information needed for replay.

Composition is valid only with compatible contracts and preserved system constraints. These are requirements for a future system, not a description of an existing validator.

## Learning, adaptation and Genesis

| Change | Generation boundary |
| --- | --- |
| Updating parameters, policy and memory from experience | Learning within a generation, preserving contracts and constraints. |
| Switching or recomposing existing mechanisms within a pre-authorized working graph | Structural adaptation within a generation; the baseline heritable genome is not rewritten. |
| Changing heritable functional composition or structure beyond the permitted working graph | Candidate for a new generation, assessed and admitted by Genesis. |

Not every connection change constitutes evolution: the permitted adaptation scope and changes to heritable structure determine the boundary. New PP types require validated implementations; the organism does not write new executable code or authorize its own reproduction.

For a persistent capability gap, the organism supplies observations and evidence, while Genesis independently checks the need for and outcome of a new generation. Criteria are fixed before assessment, mandatory invariants are preserved, and human approval and rollback are required during research. See [learning](04-learning-and-development.md) and [Genesis](05-genesis.md).

## Heredity

Three separately versioned inheritances:

1. Genome: validated functional composition and immutable constraints.
2. Regulatory state: effective settings with scope and expiry.
3. Validated knowledge: generalizable lessons with source, confidence, applicability and expiry.

Do not inherit raw transient failures, unverified interpretations or secrets. Each inheritance decision carries evidence and can be reversed. Transferring a setting or knowledge does not itself demonstrate structural evolution. A new generation must provide a migration plan, compatibility checks and tests on a held-out workload.

## Compositionality hypothesis and testable experiment

**Untested hypothesis:** a fixed set of 8–12 functional primitives can produce different classes of capabilities solely through genome changes, without changing executable code. The initial eight PPs are candidates for testing, not evidence of sufficiency or universality.

Proposed protocol, not yet executed:

1. After the [E0](../../research/experiments.md) baseline executor, freeze a registry of 8–12 PPs, their contracts, implementations, adapters, permitted operations and checksums. Disable learning in the first study to isolate the contribution of composition. Do not hide a task-class-specific solver inside `TRANSFORM`, `ACT` or another PP.
2. Before evaluation, define three task classes: threshold-based stream anomaly detection, validation/normalization/storage of file records, and queue regulation under changing load. Fix reference answers or target ranges, quality thresholds, resource budgets, run counts, random seeds and development/held-out splits, including failures.
3. Build separate declarative genomes for the three classes using one unchanged executor. Change only the composition's membership, connections and permitted parameters. An independent evaluator must check held-out results; compare with the conventional E0 executor and a control with essential connections disabled.
4. Record task success rate, p95 latency, memory, contract violations and regressions for each class; report variability and confidence intervals. Retain genomes, versions, checksums, data and logs for reproduction.
5. Success in this experiment means all three classes meet predeclared thresholds with unchanged implementations and mandatory constraints satisfied. Requiring new code, a hidden special-purpose operation, or missing thresholds means the chosen set has not supported the hypothesis in this trial. Revising the set requires a separate record and a new trial; a negative result does not disprove every possible set of 8–12 PPs.

Even a successful result supports only bounded compositionality on the selected tasks. It does not establish universality, learning, Genesis evolution or language portability. The latter needs a separate test of the same genome on a second implementation against identical contracts and observable outcomes.
