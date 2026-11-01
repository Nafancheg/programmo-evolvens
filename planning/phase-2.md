# Фаза 2 — Клетки и устойчивость / Phase 2 — Cells and Resilience

[Roadmap](../ROADMAP.md) · **Status:** in_progress

**RU:** Контракт клетки проектируется для P1-17/18 параллельно миру [W0](world.md). Внешняя изоляция компьютера больше не откладывается: она обязательна до исполнения развивающихся вариантов. Позднее можно усиливать изоляцию отдельных клеток уже внутри принятого мира. Клетку не подменяем названием узла графа.

**EN:** Design the cell contract for P1-17/18 alongside [W0](world.md). External host isolation is no longer deferred: require it before developing candidates execute. Later strengthen cell-level isolation inside the accepted world. A cell is not a renamed graph node.

| ID | To-do RU / EN | Status | Зависимость и результат / Dependency and evidence |
| --- | --- | --- | --- |
| P2-01 | Контракт клетки, жизненный цикл и здоровье / Cell contract, lifecycle and health | done | v0: private memory/inbox, text ports, lifetime step budget, idle/running/stopped and health; [Развитие RU](../docs/ru/18-prescribed-development.md), [EN](../docs/en/18-prescribed-development.md), [evidence](../world/wsl2/evidence/development-2026-11-01.json) |
| P2-03 | Телеметрия, происхождение событий, восстановление / Telemetry, provenance and recovery | in_progress | v0 provenance + budget-stop events verified; cell recovery pending P2-04 / происхождение и остановка проверены, восстановление впереди; [Развитие RU](../docs/ru/18-prescribed-development.md), [EN](../docs/en/18-prescribed-development.md), [evidence](../world/wsl2/evidence/development-2026-11-01.json) |
| P2-04 | Гомеостаз, карантин, регенерация и апоптоз / Homeostasis, quarantine, regeneration and apoptosis | todo | P2-02/03; E2 vs restart |
| P2-05 | Контракты органов и каналов сигналов / Organ and signaling-channel contracts | todo | P2-01/03; несколько клеток / multiple cells |

**Критерий / Exit:** RU — измеренное восстановление и соблюдение квот при отказах; EN — measured recovery and quota enforcement under faults. Лимит шагов не равен изоляции / A step limit is not isolation.

**Перенесено / Moved:** P2-02 → [W0](world.md), ID сохранён; P2-06…09 также ведутся там / ID preserved; P2-06…09 are also tracked there.
