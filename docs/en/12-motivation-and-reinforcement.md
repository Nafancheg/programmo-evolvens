# Motivation and Reinforcement

[Русский](../ru/12-motivation-and-reinforcement.md) · [Organism model](11-bioengine-and-applications.md) · [ADR-005](../../adr/005-motivation-and-unique-achievements.md)

**Source:** user idea, 2026-10-31. **Status:** principles recorded, mechanisms proposed for development; not implemented in current code. “Satisfaction,” “dissatisfaction” and “search tension” name regulatory signals. Subjective experience is not claimed. The term “pain” is avoided at the user's request.

## Purpose

Positive reinforcement should guide the organism toward new verified achievements. An already rewarded achievement receives no further positive response. A repeat claim for that reward produces a negative signal. Absence of new reinforcement during active search should encourage leaving an unproductive strategy.

This motivates development within the existing model. Under ADR-004, a complex motivational organ must develop from the genome rather than appear prebuilt under a new name. The environment supplies verified events and protects the ledger; the genome defines permitted reactions and regulatory bounds. A minimal initial response may be an explicit genome property. Complex organization requires a “gene/rule → structure → function” trace.

## Proposed Signals

| Event | Reinforcement | Response |
| --- | --- | --- |
| First verification of a meaningful achievement | One positive satisfaction pulse | Retain the acquired capability and favor the productive search method. |
| An established mechanism performs useful work again | Zero additional novelty reinforcement | Continue working. A known action does not become bad simply because it repeats. |
| An already rewarded achievement is resubmitted as grounds for another reward | Negative dissatisfaction signal | Reduce preference for that repeated claim; grant no reward. |
| No newly verified progress for a long time during active permitted search | Bounded growth of search tension | Reconsider the branch, parameters or attempt allocation. |
| No tasks, goal completed or budget/repertoire exhausted | Pause or explainable failure | Do not grow tension indefinitely or simulate mandatory activity. |

The response must change subsequent action selection. Merely incrementing a variable motivates nothing. Reliable execution of established tasks retains priority; intrinsic novelty reinforcement does not replace external useful-work criteria.

## Defining a New Achievement

The first version needs a finite registry of achievement types with verifiable conditions, such as confirmed mastery of a transformation class or first reaching a quality level under given constraints. Fix type, scope, level and equivalence rules before search. A new filename, different ID, row permutation, random bytes or unpredictability alone do not constitute a new achievement.

The initial implementation compares events through predefined semantic keys rather than solving general semantic equivalence. A verifier supplies outcome evidence and an achievement key. The organism may submit results but cannot change criteria, certify itself or directly increase reinforcement.

One-time reinforcement requires a durable ledger: achievement key, assessment conditions, attained level, evidence and delivered-pulse status. Novelty checks, achievement recording and event issuance must be coordinated so retries or restarts cannot double the reward. Redelivery of one event must not create another pulse either.

A technical retry of the same request returns the prior decision without a new positive or negative event. A new claim for an already rewarded semantic result produces dissatisfaction. An unsuccessful attempt at a genuinely new solution is not itself such a repeated claim.

Memory deletion, rollback, restart, degradation and restoration of prior ability do not reset reward history. Compare progress against the best already rewarded state. Inheriting validated knowledge carries associated achievement history; exact rules for nontransferred experience and new organisms remain open. Changing G alone does not create novelty.

## Motivational Control Limits

1. Grant positive reinforcement for verified useful novelty. Verified intermediate achievements are allowed, but arbitrary subdivision of one job creates no extra rewards.
2. Dissatisfaction applies to an observable repeated reward claim, not presumed program intentions. Normal repeated execution and rechecking an old result are not penalized.
3. Tension grows only within budgeted, permitted active search. Idle time, missing inputs and unsupported goals do not create an endless negative loop. Reducing tension does not by itself create another positive reward.
4. Signals change permitted search policy, not success criteria, the ledger, invariants or Genesis authority. Novelty seeking must not displace useful ongoing work or retained capabilities.
5. Weights, intervals, bounds and tension-recovery rules remain to be defined and tested. Escalating reward needs or unbounded pressure are not intended.

## Checks Before Use

One achievement yields exactly one pulse; a duplicate claim yields a negative signal; ordinary reuse remains permitted. Check restart, event redelivery, rollback, renaming, noise and “degrade → restore” loops. Long unproductive search should change strategy within budget while preserving mastered functions. Also check completed tasks and absence of available new achievements.

Compare otherwise identical search with regulation enabled and disabled: verified new capabilities, useful-task correctness, costs and repeated claims. The number of “positive emotions” is not an independent quality metric.

Tasks: **P0-10, P3-06…P3-08**. Genome unfolding P1-17/18 remains the immediate priority. This idea is not presented as an already formed organ.

## Prior Approaches

Intrinsic motivation signals have been studied in [Curiosity-driven Exploration](https://arxiv.org/abs/1705.05363) and [Never Give Up](https://arxiv.org/abs/2002.06038). These inform comparison rather than implement our rules: lifetime one-time reinforcement of verified achievements and a negative signal for repeated claims are separate project choices. These rules do not inherently require a neural network or external AI.
