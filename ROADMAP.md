# Roadmap / Дорожная карта

**Первый прикладной сценарий / First applied scenario:** [Excel → итоговая матрица (RU)](docs/ru/10-excel-to-matrix.md) · [Excel → target matrix (EN)](docs/en/10-excel-to-matrix.md). Проверка по входным/эталонным парам, включая актуализацию данных / Reference input/output pairs, including data updates. P0-06 и P1-09/10/11; реализация ожидает реальные примеры / implementation awaits actual examples.

| Phase | RU | EN | Status | To-do |
| --- | --- | --- | --- | --- |
| 0 | Концепция, гипотезы и критерии доказательности | Charter, hypotheses and evidence criteria | In progress | [P0](planning/phase-0.md) |
| 1 | Реальный исполнитель задач и контрольная группа | Real task executor and baseline | In progress | [P1](planning/phase-1.md) |
| 2 | Клетки, телеметрия, отказоустойчивость | Cells, telemetry and resilience | Planned | [P2](planning/phase-2.md) |
| 3 | Память, обучение и контроль качества | Memory, learning and evaluation | Planned | [P3](planning/phase-3.md) |
| 4 | Genesis: оценка, эволюционный запрос, допуск | Genesis: assessment and approval | Planned | [P4](planning/phase-4.md) |
| 5 | Коэволюция Genesis и проверка новых поколений | Genesis co-evolution and generation testing | Planned | [P5](planning/phase-5.md) |
| 6 | Веб-дашборд на реальных событиях | Dashboard backed by observed events | Planned | [P6](planning/phase-6.md) |

**RU:** Переходы только после воспроизводимых испытаний. Python используется для первого исследовательского исполнителя; язык генома им не ограничивается. Первый прототип не завершает E0 и не подтверждает композиционность.

**EN:** Progress only after reproducible tests. Python is used for the first research executor; it does not constrain the genome language. The first prototype does not complete E0 or validate compositionality.

## Правила работы / Workflow

**RU:** У каждой фазы свой список to-do с постоянными ID, статусами, зависимостями и проверяемым результатом. Несколько задач и фаз могут одновременно быть в работе. Зависимости ограничивают конкретные задачи, а не всю фазу.

**EN:** Each phase has to-dos with stable IDs, statuses, dependencies and verifiable outcomes. Several tasks and phases may be active simultaneously. Dependencies constrain individual tasks, not an entire phase.

- `todo` — запланировано / planned.
- `in_progress` — в работе; число активных задач не ограничено / active; no concurrency limit.
- `blocked` — указать причину и зависимость / state the reason and dependency.
- `done` — указать результат и проверку / link the result and verification.
- `deferred` — сохранить замысел и условие возврата / preserve intent and revisit condition.

**RU:** Новая мысль сначала сохраняется в [реестре идей](planning/ideas.md): смысл, предполагаемая фаза, вопросы и условие проверки. Не удаляем концепцию из-за отсутствия реализации сейчас. Можно отложить, уточнить или опровергнуть с доказательствами. Запись не означает утверждение или обещание реализации. При переносе задачи сохраняем ID и ссылку на новую фазу. Архитектурные изменения фиксируем в ADR; гипотезы, прототипы и подтверждённые результаты различаем явно.

**EN:** Capture new thoughts in the [idea register](planning/ideas.md): intent, candidate phase, questions and test condition. Do not delete a concept merely because it cannot be implemented now. Defer, refine or contradict it with evidence. Recording does not mean acceptance or a commitment to implementation. Preserve IDs and link the new phase when moving tasks. Record architectural changes in ADRs; explicitly distinguish hypotheses, prototypes and validated outcomes.
