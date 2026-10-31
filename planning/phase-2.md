# Фаза 2 — Клетки и устойчивость / Phase 2 — Cells and Resilience

[Roadmap](../ROADMAP.md) · **Status:** planned

| ID | To-do RU / EN | Status | Зависимость и результат / Dependency and evidence |
| --- | --- | --- | --- |
| P2-01 | Контракт клетки, жизненный цикл и здоровье / Cell contract, lifecycle and health | todo | P1-04; клетка не равна узлу / cell is distinct from a node |
| P2-02 | Изоляция, квоты памяти и жёсткие тайм-ауты / Isolation, memory quotas and hard timeouts | todo | P2-01; границы процесса / process boundaries |
| P2-03 | Телеметрия, происхождение событий, восстановление / Telemetry, provenance and recovery | todo | P2-01; реальные отказы / real failures |
| P2-04 | Гомеостаз, карантин, регенерация и апоптоз / Homeostasis, quarantine, regeneration and apoptosis | todo | P2-02/03; E2 vs restart |
| P2-05 | Контракты органов и каналов сигналов / Organ and signaling-channel contracts | todo | P2-01/03; несколько клеток / multiple cells |

**Критерий / Exit:** RU — измеренное восстановление и соблюдение квот при отказах; EN — measured recovery and quota enforcement under faults. Лимит шагов не равен изоляции / A step limit is not isolation.
