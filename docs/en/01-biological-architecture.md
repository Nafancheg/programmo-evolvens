# Biological Architecture

[Русская версия](../ru/01-biological-architecture.md) · [Project home](../../README.md)

Biology is a design analogy, not proof of equivalence.

Implementation priority and the full feeding/assimilation cycle: [Bioengine and Application Layer](11-bioengine-and-applications.md). Build the bioengine first; application examples do not replace its architecture.

| Analogy | Proposed software responsibility |
| --- | --- |
| Cell | Isolated executable worker with a contract and health state |
| Organ | Coordinated functional subsystem |
| Genome | Versioned declarative composition and invariants |
| Nervous system | Event and command transport |
| Immune system | Anomaly detection, quarantine, recovery |
| Endocrine system | Slow global regulatory signals, not direct commands |
| Metabolism | Resource budgets and scheduling |
| Homeostasis | Controlled operating ranges with hysteresis |
| Memory | Event history plus distilled validated knowledge |
| Regeneration | Restore or replace a failed worker |
| Apoptosis | Controlled worker termination |

Every subsystem requires explicit interfaces, observable inputs/outputs and tests. The first prototype must avoid biological terminology without operational meaning.
