# Bioengine and Application Layer

[Русский](../ru/11-bioengine-and-applications.md) · [Project home](../../README.md) · [Plan](../../ROADMAP.md) · [ADR-003](../../adr/003-bioengine-first.md)

**Date:** 2026-10-31. **Status:** recorded implementation direction. Mechanisms below are development requirements; the current executor supplies only a small foundation. Biological terms identify engineering roles rather than equivalence to living systems.

## 1. Goal and Two Layers

**Programmo Evolvens aims to build an autonomous software organism that accepts information, transforms it into usable internal structures, stores and uses them, and develops available processing methods through mechanism composition and selection.**

| Layer | Responsibility | First outcome |
| --- | --- | --- |
| 1. Bioengine | Primitives, genome, mechanisms, cells, data movement, assimilation, memory, regulation and internal composition search. Genesis separately governs heritable structural generations. | A complete intake, processing, verification, assimilation and reuse cycle. |
| 2. Application | Specific tasks and output presentations: Excel → report, target matrix, dashboard and other products. | An application on a working core, with its own inputs and criteria. |

Applications supply desired outcomes and constraints through contracts. The bioengine executes and develops processing mechanisms without branching on application names. Application adapters may provide operations, but their pre-existing availability is not an acquired capability.

The immediate priority is layer 1. Core construction does not depend on receiving user Excel files. Application ideas remain in a [separate backlog](../../planning/applications.md). Research and comparisons inform engineering decisions; the next deliverable is working, checked behavior rather than proof of scientific uniqueness.

## 2. Feeding, Digestion and Assimilation

| Analogy | Engineering meaning | Verifiable outcome |
| --- | --- | --- |
| Food | An input packet: bytes or stream, source, time, identifier and available provenance. | Original material is retained or available for replay. |
| Mouth / input bus | A single intake point, queue and initial size/access checks. | Packet accepted or rejected with a reason; outcome does not rely solely on a filename extension. |
| Digestion | Available operations extract structure through decoding, splitting, field recognition and transformation. | Typed units with the mechanism used and remaining unprocessed content. |
| Enzymes | Implementations of bounded operations with inputs, outputs, conditions, effects and cost. | Operations satisfy their contracts and perform the declared work. |
| Assimilation | Validate extracted units, bind them to an internal schema and persist them with provenance. | Stored data can be found and used by another operation after restart. |
| Waste / undigested remainder | Unsupported, damaged, ambiguous or inapplicable material. | Remainder and reasons are known; data loss is not presented as success. |
| Metabolism | Usable data moves between mechanisms and cells, consuming resources to do work. | Inputs used, outputs produced and resource costs are observable. |

**Parsing, assimilation and use are distinct achievements.** Reading a string does not establish understanding its meaning. An assimilated unit needs a defined type/schema, provenance and a verifiable use. Ambiguous interpretations remain hypotheses until checked.

Information is processing material and a possible source of useful experience. Compute energy does not arise from the number of bytes read: the environment supplies time, memory and computation. The first core tracks actual budgets and useful outcomes. A possible internal energy balance remains a separate idea; an arbitrarily increasing counter will not demonstrate development.

## 3. Building the Organism

Preserve the ADR-001 hierarchy **nucleotide → gene → functional mechanism → cell → organ → organism**.

- A nucleotide is an encoding element. Its alphabet remains undecided; it is not a functional operation.
- A functional primitive PP is a capability with a formal contract. `SENSE`, `COMPARE`, `TRANSFORM`, `DECIDE`, `ACT`, `STORE`, `SIGNAL`, `REGULATE` remain provisional families. Their final count is not fixed.
- A gene is a heritable declarative description of a property or composition: operations, parameters, connections and constraints. It is not automatically generated source code.
- A mechanism is an executable chain or graph assembled from a description. Even simple processing may need multiple genes and mechanisms.
- A cell executes mechanisms with its own state, contract, inputs/outputs and lifecycle. Naming a graph node a cell does not make it one.
- An organ is a coordinated subsystem of cells. Information digestion and assimilation are the first assembly domain.

A primitive may contain specified logical or computational processing; its capabilities and limits must be explicit. Complexity comes from implementations and their combinations. Do not hide a complete task solution in one operation and call it compositional evolution.

The runtime language is not a genome primitive. The existing Python executor is building material: eight limited PPs, scalar ports, manually authored graphs and checks. Complete cells, structured food units, assimilation, durable storage and autonomous graph search are not implemented yet.

## 4. Acquiring a Capability

The first change mechanism is an **internal search algorithm** executed by the engine itself. It needs available operations, permitted connections/parameters, outcome criteria and a budget. Runtime operation requires no external AI agent, language-model network call or human choosing each next candidate.

Working cycle: accept a packet → try a stored mechanism → check the result → on failure construct candidates within the permitted scope → execute and assess → retain a usable mechanism and experience → apply to subsequent data. Exhausted budgets or unsupported processing produce an explainable failure.

Candidates may change parameters, compatible operation ordering, branches, permitted component membership and connections. Recombination joins compatible fragments; type, constraint and outcome checks remain mandatory. Retain ancestry, changes, costs and outcomes. Candidates cannot change criteria or references. Search remains to be implemented; this is not a description of existing functionality.

**Distinguish four levels:**

| Change | Meaning |
| --- | --- |
| Select an already registered parser | Use an existing capability. This alone is not learning. |
| Autonomously find a new combination of available operations and confirm use on new inputs | Acquire a checked working mechanism within permitted bounds; ontogeny/adaptation in the current generation. |
| Change heritable structure or combine genetic fragments beyond the permitted working scope | Candidate for a new generation under separate Genesis assessment. Local search attempts do not increment generation G. |
| Create an unknown operation type or new executable code | Beyond the first core; requires a separate decision and validated implementation. Agent-based code generation is not a mandatory project mechanism. |

Genesis is a separate assessment/admission controller, not necessarily an AI agent. Automatic working-mechanism search needs no human decision per attempt. The existing human approval requirement for research releases of new structural generations remains; autonomous local attempts and generation release are distinct actions.

Do not promise understanding of every arbitrary file. New combinations are limited to behavior expressible through available operations. Engineers build the starting repertoire. Show acquisition of a previously unprocessed representation within that capability space, including new examples, errors and unsupported-material rejection.

## 5. Next Working Model

Build the vertical slice around **autonomous feeding and assimilation**, without an Excel product or dashboard. Start with a small predefined family of representations of the same structured data. Fix concrete formats and initial operations in contracts before implementing search; do not claim support for all formats.

Completion criteria:

1. A single intake accepts a bounded byte packet and records provenance; unsupported or damaged content gets an explicit outcome.
2. The engine executes bounded-operation compositions through a minimal cell model and yields a common typed representation. Intermediate results and undigested content are observable.
3. Validated units enter durable storage; after restart they can be retrieved and used for another checked transformation or text result.
4. For a selected previously unsolved case, internal search finds, checks and retains an allowed composition; the mechanism then works on a new example. A human does not write the required chain during the run, and an external agent does not supply it.
5. Compare before/after retaining the mechanism, with lineage and checks on new data. Failure remains explicit; regressions allow returning to prior state.
6. Track attempts, time, memory/data sizes and mandatory constraints. Do not infer success from attempt counts, memory size or visualization.

These are first-core development criteria, not achieved results or universality evidence. The full ADR-001 8–12-PP study remains, but does not block constructing a bounded working cycle. Later extensions include richer cells/organs, learning, checked inheritance, structural evolution and application products.

## 6. Current Work and Preserved Directions

Current tasks: **P0-03/P0-08** define PP/data boundaries; **P1-12…P1-16** cover intake, composition, assimilation, internal search and end-to-end acceptance; **P2-01** defines the minimal cell contract. They may progress concurrently according to dependencies. Retain the scalar executor as a prototype rather than presenting it as a complete organism.

Excel/matrix tasks move to the application layer with their original IDs preserved. The dashboard remains a later view of actual events. Nucleotide alphabets, gene combination, PP evolution and internal “energy” remain in the [idea register](../../planning/ideas.md). Revisit them under recorded conditions without changing the current goal whenever a new example arises.
