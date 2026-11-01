# First prescribed genome-driven development

[Русский](../ru/18-prescribed-development.md) · [ADR-011](../../adr/011-prescribed-development-v0.md) · [Genome](../../examples/development/text-retention.json) · [Evidence](../../world/wsl2/evidence/development-2026-11-01.json)

## What is tested

The first limited example must follow **genome → actual mechanisms and cells → connection → performed function**. Initially there is one cell without mechanisms or connections. Transforming text and delivering it to memory must become possible after structural changes.

This is prescribed development: developers write the rules stored in the genome. It does not establish learning, autonomous composition discovery or evolution. In-cell storage here is not durable assimilation; organs and the digestive cycle remain unimplemented.

## V0 contract

`development-v0` is language-independent JSON data describing `initial`, `genes` and `endpoint`. Python implements the executor and is not a genome primitive. JSON remains a working encoding; the final nucleotide alphabet is undecided.

| Element | Contract |
| --- | --- |
| Initial state | One cell with no mechanisms; genome specifies ID and budget |
| Mechanism gene | `kind: mechanism`, existing-PP program with one text output `out` |
| Structural gene | `kind: development`, ordered `when.feedback` → `action` rules |
| `express` | Express the specified mechanism gene inside an existing cell |
| `bud` | Create a child cell with parent, separate memory and bounded budget |
| `connect` | Connect one cell's `out` to another's `in`; reject cycles and duplicates |
| Rule condition | Actual observed structural/delivery deficiency; each rule fires once |
| Output | Value actually delivered to `endpoint.cell.out`; external evaluator owns the reference |

Model limits: 16 KiB genome, 4 KiB text input, at most four cells, eight mechanisms, 16 rules and 16 structural steps; each mechanism has at most eight PPs. A cell has at most 64 executed operations over its lifetime. These bounds do not replace external W0 quotas.

A cell owns mechanisms, a runtime instance with memory, a queue holding at most four messages, `in/out: text` ports, `idle/running/stopped` states and health. Operations consume its budget; exhaustion stops it with a reason. The existing runtime provides memory transactions per mechanism. Cell regeneration and recovery are unimplemented.

## Structure and feedback

The [example](../../examples/development/text-retention.json) has three genes: `clean`, `retain`, `body`. The structural gene supplies four rules:

1. Source has no mechanism → express `clean` inside `seed`.
2. Destination cell is missing → create `memory` as a child of `seed`.
3. Destination has no mechanism → express `retain` there.
4. Delivery is missing → connect `seed.out → memory.in`.

`clean` contains `SENSE → TRANSFORM(strip) → TRANSFORM(lower)`. `retain` contains `SENSE → STORE → SIGNAL`. The environment has no built-in mature normalization organ: it executes the declared primitives and rules. Execute the actual existing structure again after each change.

Every event has `seq`, `tick`, a genome hash and an associated source journal. Cell, mechanism and link creation additionally reference their gene and rule. The laboratory shows cell instances, mechanisms, memory, step costs, links and source events. Displayed state comes from the latest experiment; age changes are not used.

## Run and controls

From the repository root:

```powershell
.\scripts\setup-lab.ps1 -UpdateWorld
.\world\wsl2\config\run-acceptance.ps1
.\scripts\run-development.ps1
.\scripts\start-lab.ps1
```

The executor admits a fixed trusted zipapp containing the example and controls. Arbitrary code paths and new genomes through the CLI are not yet admitted. A mismatch between installed environment and W0 evidence blocks development pending acceptance. The fixed experiment and all modified variants execute inside bwrap/cgroup; ordinary unittest checks only schema, packaging and admission.

The evaluator checks initial non-functionality, final `hello` for input `  HeLLo  `, separate `last` memory, provenance of four changes, reproducibility, another public input `  NeW DATA\t`, changed output after removing `lower`, absent delivery after link removal, budget stopping, unknown-operation rejection and genome immutability. The extra public input is not a held-out compositionality trial.

Preserve the summary and event sequence. Capability here means execution of genome-prescribed structure, without claiming autonomous acquisition. Next come input-packet contracts, durable storage and autonomous mechanism search.

## Where to inspect the result and its code

The experiment produces a saved `text-retention` instance: two cells, two mechanisms, one connection and `memory.last = "hello"`. Its execution process has finished; it is not a continuously running organism. The genome specifies the instance program, interpreted by the shared engine. The experiment does not generate a new Python application.

The **“Resulting instance”** panel at the top of the laboratory shows input and output. “Inspect organism” opens actual state; “Genome JSON” shows the program and rules; “Executor source” and “Primitive source” show exact sources from the executed zipapp. Sources are available when the installed bundle hash matches the journal. “Download specimen JSON” saves state, genome, source, provenance and checks. API: `/api/organism`.

Below is **recorded execution**: “Show development”, previous/next steps and a slider. Each frame derives from 20 actual events; playback speed is not organism execution time. Captions explain the missing function and the rule changing structure. Viewing does not start another experiment. Interface file changes automatically refresh the page to the new version.

The passport uses `organism-snapshot-v0`. Importing it and resuming execution are not implemented yet; they belong to future P1-14. Repeat the fixed experiment with `run-development.ps1` inside accepted W0.

**Checked, 2026-11-01:** 10 developing-variant checks inside W0; 20 recorded events; 53 data/admission/interface tests on Linux, 44 on Windows and nine Linux-only skips; recorded frames additionally checked in Node. Repeat the W0 probes for the new entry point before executing development.
