# Learning and Development

[Русская версия](../ru/04-learning-and-development.md) · [Project home](../../README.md)

## Distinctions
- Learning: change in non-code policy informed by task outcomes.
- Ontogenesis: persistent changes in regulation, memory and allowed runtime composition within one generation.
- Evolution: independently admitted structural redesign in a new generation.

## Demonstrating learning
Measure performance on a held-out dataset **before and after** experience under the same resource and task conditions. Compare against a frozen-policy control and a randomized-history control. Record confidence intervals and any regressions.

## Guardrails

The proposed motivational controller is described separately: [Motivation and Reinforcement](12-motivation-and-reinforcement.md), [ADR-005](../../adr/005-motivation-and-unique-achievements.md). Reward newly verified achievements once, reject repeated claims with dissatisfaction and redirect unproductive search through bounded tension. Ordinary use of a known capability is not penalized. The controller is unimplemented; under ADR-004, its complex structure must develop from the genome.

A policy update is provisional until validated; preserve checkpoints and reversibility. Avoid labeling an incrementing number as intelligence or maturity. M must be derived from a declared test suite rather than manually increased.
