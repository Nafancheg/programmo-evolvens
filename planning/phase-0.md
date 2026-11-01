# Фаза 0 — Контракты и границы / Phase 0 — Contracts and Boundaries

[Roadmap](../ROADMAP.md) · **Status:** in_progress

| ID | To-do RU / EN | Status | Зависимость и результат / Dependency and evidence |
| --- | --- | --- | --- |
| P0-01 | Закрепить генетическую модель / Record the genetic model | done | [ADR-001](../adr/001-genetic-model.md), RU/EN genome docs |
| P0-02 | Фазы, to-do и сохранение идей / Phases, to-dos and idea preservation | done | Roadmap, семь списков / seven lists, [ideas](ideas.md) |
| P0-03 | Уточнить атомарность и границы восьми PP / Refine atomicity and boundaries of eight PPs | in_progress | [Два слоя RU](../docs/ru/11-bioengine-and-applications.md), [EN](../docs/en/11-bioengine-and-applications.md); нужны конкретные операции первого репертуара / concrete first-repertoire operations needed |
| P0-04 | Определить алфавит и версионирование генома / Define genome alphabet and versioning | todo | I-001; JSON v0 — рабочее представление / JSON v0 is a working representation |
| P0-05 | Пороги и отложенные данные до испытания / Predeclare thresholds and held-out data | todo | Для проверки первого ядра P1-16 и позднее P1-06; критерий задаётся до подбора / For first-core P1-16 and later P1-06; fix criteria before search |
| P0-06 | Уточнить прикладной сценарий Excel → матрица по эталонам / Specify applied Excel → matrix scenario from reference pairs | deferred | [A1](applications.md); вернуться после первого ядра, не блокирует его / revisit after first core, not a core dependency |
| P0-07 | Зафиксировать два слоя и самостоятельную работу биодвижка / Record two layers and autonomous bioengine operation | done | [ADR-003](../adr/003-bioengine-first.md), [RU](../docs/ru/11-bioengine-and-applications.md), [EN](../docs/en/11-bioengine-and-applications.md) |
| P0-08 | Задать контракты пищи, усвоенных единиц, результата и первого репертуара / Define food, assimilated-unit, outcome and starting-repertoire contracts | in_progress | Модель описана; точные схемы, операции и наборы входов ещё нужны / Model described; exact schemas, operations and input sets still needed; P1-12…16 |
| P0-09 | Определить начальное состояние и правила развития из генома / Define initial state and genome-driven developmental rules | done | v0: initial cell + express/bud/connect by execution feedback; prescribed scope / предписанная область; [Развитие RU](../docs/ru/18-prescribed-development.md), [EN](../docs/en/18-prescribed-development.md), [evidence](../world/wsl2/evidence/development-2026-11-01.json) |
| P0-10 | Определить смысловую новизну достижений и правила подкрепления / Define semantic achievement novelty and reinforcement rules | todo | [ADR-005](../adr/005-motivation-and-unique-achievements.md); типы достижений, эквивалентность, область истории, пределы напряжения / achievement types, equivalence, history scope and tension bounds |
| P0-11 | Определить модель угроз и политику виртуального мира / Define virtual-world threat model and policy | done | [ADR-009](../adr/009-w0-acceptance-scope.md), [W0](world.md), [измерения / evidence](../world/wsl2/evidence/w0-acceptance-2026-11-01.json); фиксированный последовательный профиль / fixed serial profile |

**Критерий / Exit:** RU — контракты и критерии первого ядра достаточно точны для реализации и воспроизводимой проверки; EN — first-core contracts and criteria support implementation and reproducible checking. Новые идеи сохраняем отдельно, академическая новизна не блокирует создание / Preserve new ideas separately; academic novelty does not gate construction.
