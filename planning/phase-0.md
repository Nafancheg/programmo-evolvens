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
| P0-09 | Определить начальное состояние и правила развития из генома / Define initial state and genome-driven developmental rules | in_progress | [ADR-004](../adr/004-genome-driven-development.md); нужны точные правила создания/изменения механизмов, клеток и связей / exact mechanism, cell and connection creation/change rules needed |

**Критерий / Exit:** RU — контракты и критерии первого ядра достаточно точны для реализации и воспроизводимой проверки; EN — first-core contracts and criteria support implementation and reproducible checking. Новые идеи сохраняем отдельно, академическая новизна не блокирует создание / Preserve new ideas separately; academic novelty does not gate construction.
