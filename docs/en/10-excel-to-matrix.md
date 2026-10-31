# Applied Scenario: Excel → Target Matrix

[Русский](../ru/10-excel-to-matrix.md) · [Project home](../../README.md) · [To-dos](../../planning/phase-1.md)

**Source:** user requirements, 2026-10-31. **Status:** deferred application-layer scenario under [ADR-003](../../adr/003-bioengine-first.md); the [bioengine](11-bioengine-and-applications.md) is the current priority. The scenario is preserved; actual files and references have not been supplied. Receiving them does not block core construction. Existing prototype examples do not implement this scenario.

## Task

The user supplies input Excel files and corresponding target matrices prepared manually or by another program. The internal transformation method is not prescribed. The system should find a way to read, interpret, store, update, organize and further transform data to obtain the required result.

Working flow: **Excel → extraction and interpretation → storage/update → organization and transformation (“fermentation”) → target matrix → reference comparison**. This describes responsibilities, not an approved algorithm or a requirement for a separate component per stage.

Possible transformation steps include entity matching, normalization, calculation, source merging, aggregation and grouping. Examples and user requirements determine which are needed; these are possibilities, not agreed rules.

## Test Examples

A one-shot transformation example contains an input file or file set and an expected matrix. An update example contains **initial stored state + a sequence of incoming files → expected states and matrices after updates**. This tests subsequent arrivals as well as first import.

The meaning of repeated imports, corrected rows, duplicates, missing values and record deletion needs agreement. Record keys, source precedence and deletion semantics are not assumed. Different sequences with identical final outputs need not be equivalent: references define the intended semantics.

## Reference Comparison

Before search, specify:

1. Output columns and their meaning, row-matching keys and whether order matters.
2. Types, dates, units, rounding, blanks and allowed tolerances. Compare content; include file formatting only when required.
3. Mandatory conditions, such as no lost or duplicated records and correct updates. The task determines the actual list.
4. Success criteria and time, attempt and compute budgets. An average score must not conceal failure of a mandatory condition.

Use some pairs for candidate search and reserve others for checking new files. Repeated queries to a validation set compromise independence; separate final assessment from search feedback. Matching known examples does not prove recovery of a uniquely correct rule for every future file.

## Autonomous Loop

The search controller creates changed solution candidates, runs them on examples, receives errors and scores from a fixed evaluator, records lineage and selects parents for subsequent candidates. Candidates cannot change the evaluator or reference outputs. An archive preserves promising branches even when a current candidate is not the best.

Stop when agreed criteria or the budget is reached. On budget exhaustion, report the best result and remaining differences without claiming completion. Assess the selected candidate separately on held-out data after search.

Current JSON v0 supports only scalar ports and limited operations; it does not yet define a solution space for this scenario. Using an existing evolution framework, extending the declarative model and producing code variants require separate assessment. Generated-code admission is not automatically an agreed change to ADR-001/002.

## First Practical Outcome

Obtain a verifiable transformation of actual files into the target matrix, including updates, and compare autonomous search against the initial solution under equal conditions. Record correctness, errors, search time/cost and checks on new files. This evaluates practical usefulness; scientific uniqueness is not a condition for accepting useful results.

Tasks **P0-06, P1-09, P1-10, P1-11** are deferred; the P1 tasks moved to [application phase A1](../../planning/applications.md) with IDs preserved. Actual input/output pairs and update sequences will be needed when this scenario resumes. Current core construction uses our own bounded test inputs.
