# Custom text and repeatability

[Русский](../ru/19-custom-text-repeatability.md) · [ADR-012](../../adr/012-bounded-custom-text-experiments.md) · [Genome](../../examples/development/text-retention.json)

In the laboratory's “Resulting instance” panel enter text and click **“Check twice”**. For example, `  DIFFERENT WoRDS  ` should produce `different words`. The fixed genome trims surrounding whitespace, lowercases letters and retains the result in cell `memory`.

One request creates **two fresh instances** inside accepted W0. Checks cover delivery, an external reference, equal outputs and logical events, memory and genome immutability. This repeats one program on different data. It does not mean the program invented the transformation or learned: developers authored the sources, genes and four v0 rules.

The top panel displays input, output, reference and instance agreement. Updated telemetry replaces the current specimen and recording. Inspect the genome and verify its hash is unchanged. Resource charts show actual execution; recorded replay is a separate viewing mode.

From the project root in PowerShell:

```powershell
.\scripts\run-development.ps1 -Text "  DIFFERENT WoRDS  "
```

Or directly:

```text
python -m programmo_evolvens.experiment --text "  DIFFERENT WoRDS  "
```

Admit at most **256 UTF-8 bytes**, including whitespace. Empty text is valid and produces empty output. Disable the button when the world is busy, the source unavailable, acceptance mismatched or input oversized. There is no request queue. Full active journals or total storage reject runs; logs are retained.

Control is limited to this experiment type: the browser cannot select code, genome, path, command or quotas. Text is stdin data for a fixed command. Require Origin and the local page's ephemeral token; bind the server only to loopback. Check free host reserve and W0 admission before each trial.

V0's autonomous part executes four prescribed rules and constructs the intended structure. It does not create new rules or logic. The next substantive stage is P1-15: construct composition candidates autonomously, evaluate against an immutable criterion and select working variants.

**Checked, 2026-11-01:** [three actual inputs](../../world/wsl2/evidence/custom-text-2026-11-01.json): different ASCII text, Cyrillic through the button and empty text; two fresh instances and the same genome each time; five checks per request passed. 62 Linux tests, 52 Windows tests and ten Linux-only skips. The original ten controls without custom text also passed after updating.
