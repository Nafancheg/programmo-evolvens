# Реестр идей / Idea Register

[Roadmap](../ROADMAP.md)

**RU:** Сохраняем концепции до выбора реализации. `captured` — записана, `research` — исследуется, `deferred` — отложена с условием возврата. Результаты и возражения дописываем, исходный замысел сохраняем. Связь с to-do не означает подтверждение идеи. Начальные записи перенесены из согласованной концепции; I-007 — из пожелания пользователя 2026-10-31.

**EN:** Preserve concepts before implementation choices. `captured` means recorded, `research` means under investigation, `deferred` means postponed with a revisit condition. Append evidence and objections while preserving intent. A to-do link does not validate an idea. Initial entries come from the agreed concept; I-007 comes from the user's request on 2026-10-31.

| ID | Идея / Idea | Фаза / Phase | Status | Вопрос и условие возврата / Question and revisit condition |
| --- | --- | --- | --- | --- |
| I-001 | Алфавит нуклеотидов / Nucleotide alphabet | 0, P0-04 | captured | Нужен ли слой ниже структурного JSON? После первых графов / Need a layer below structured JSON? After initial graphs |
| I-002 | Эволюция набора PP / Evolution of the PP set | 5, P5-03 | captured | Выразительность и совместимость; после испытания текущего набора / Expressiveness and compatibility; after testing the current set |
| I-003 | Один геном, разные языки / One genome, multiple languages | 5, P5-05 | deferred | Сравнить результаты и ошибки после стабилизации контрактов / Compare outcomes and errors after contracts stabilize |
| I-004 | Композиционность 8–12 PP / Compositionality of 8–12 PPs | 1, P1-06 | research | [ADR-001](../adr/001-genetic-model.md); исключить скрытые решатели, отложенные задачи / Exclude hidden solvers, use held-out tasks |
| I-005 | Функциональная сингулярность / Functional singularity | 5, P5-04 | captured | Как отличить достаточность от слабого оценщика? / Distinguish sufficient capability from a weak evaluator? |
| I-006 | Коэволюция Genesis / Genesis co-evolution | 5, P5-02 | captured | Внешняя проверка компетентности до допуска / External competence testing before admission |
| I-007 | Не терять идеи будущих фаз / Retain ideas for future phases | 0, P0-02 | captured | Новые идеи сохранять, несколько задач могут быть в работе / Preserve new ideas; multiple tasks may be active |
| I-008 | Компенсация и идемпотентность внешних действий / External-action compensation and idempotency | 2, P2-03 | captured | Из прототипа 2026-10-31: ACT может выполниться до позднего отказа; перед автоматическими повторами / From prototype 2026-10-31: ACT may precede a later failure; revisit before automatic retries |
| I-009 | Компиляция нескольких генов в рабочий граф / Compile multiple genes into a working graph | 0/2, P0-04, P2-05 | deferred | После уточнения семантики генов; сохранить связь описания с исполнением / After gene semantics are refined; preserve description-to-execution mapping |
| I-010 | Процессы, параллельный граф и бинарное представление / Processes, parallel graphs and binary representation | 1/2, P1-07, P2-02, P0-04 | deferred | После последовательных измерений; сравнить сложность и реальные преимущества / After sequential measurements; compare complexity and actual benefits |
| I-011 | Прикладная эволюция Excel → итоговая матрица по эталонным парам / Applied Excel → target-matrix evolution from reference pairs | 0/1, P0-06, P1-09/10/11 | captured | Постановка пользователя 2026-10-31: способ преобразования свободен, результат проверяется эталонами; нужны реальные файлы и последовательности актуализации / User requirement 2026-10-31: transformation method is open, references verify outcomes; actual files and update sequences needed; [RU](../docs/ru/10-excel-to-matrix.md), [EN](../docs/en/10-excel-to-matrix.md) |
| I-012 | Genesis создаёт варианты кода отдельно от работающего экземпляра / Genesis creates code variants separately from the running instance | 0/4, P1-11, P4-03 | captured | Из обсуждения применимости 2026-10-31: возможное расширение за пределы PP; сначала оценить необходимость и оформить изменение ADR / From feasibility discussion 2026-10-31: possible extension beyond PPs; assess need and record an ADR change first |

**Новая запись / New entry:** ID; дата/источник / date/source; замысел / intent; предполагаемая фаза / candidate phase; status; вопросы / questions; условие проверки/возврата / test/revisit condition; ссылки на задачи и результаты / task and evidence links.
