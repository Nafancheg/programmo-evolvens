# Roadmap / Дорожная карта

**Текущий приоритет / Current priority:** создать автономный биодвижок: приём информации → разбор → проверка → усвоение → память → использование, с самостоятельным подбором допустимых композиций / build an autonomous bioengine: intake → parsing → validation → assimilation → memory → use, with internal search over permitted compositions. [Модель RU](docs/ru/11-bioengine-and-applications.md) · [Model EN](docs/en/11-bioengine-and-applications.md) · [ADR-003](adr/003-bioengine-first.md).

**Два слоя / Two layers:** ядро и прикладные продукты / core and application products. Для первой рабочей модели не нужны пользовательский Excel и дашборд; проверки проводим на небольших определённых наборах входов / user Excel files and a dashboard are not prerequisites for the first working model; use small defined input sets for checks. Внешние ИИ-агенты и языковые модели не требуются для работы ядра / external AI agents and language models are not required at core runtime.

## Биодвижок: фазы / Bioengine Phases

| Phase | RU | EN | Status | To-do |
| --- | --- | --- | --- | --- |
| 0 | Контракты и границы первой рабочей модели | Contracts and first-model boundaries | In progress | [P0](planning/phase-0.md) |
| 1 | Биодвижок: питание, усвоение, композиция | Bioengine: feeding, assimilation, composition | In progress | [P1](planning/phase-1.md) |
| 2 | Клетки, телеметрия, отказоустойчивость | Cells, telemetry and resilience | In progress | [P2](planning/phase-2.md) |
| 3 | Память, обучение и контроль качества | Memory, learning and evaluation | Planned | [P3](planning/phase-3.md) |
| 4 | Genesis: оценка, эволюционный запрос, допуск | Genesis: assessment and approval | Planned | [P4](planning/phase-4.md) |
| 5 | Коэволюция Genesis и проверка новых поколений | Genesis co-evolution and generation testing | Planned | [P5](planning/phase-5.md) |
| 6 | Веб-дашборд на реальных событиях | Dashboard backed by observed events | Planned | [P6](planning/phase-6.md) |

**RU:** Ближайший результат — сквозная рабочая модель по P1-12…P1-16 и минимальный контракт клетки P2-01. Фазы 0/1/2 могут двигаться параллельно. Приёмка требует работающего цикла и проверок на новых входах; завершение академического исследования универсальности не является условием начала разработки. Python используется для первого исполнителя; язык генома им не ограничивается. Скалярный прототип ещё не выполняет полный цикл и не подтверждает общую композиционность.

**EN:** Next deliverable: an end-to-end working model through P1-12…P1-16 and the minimal cell contract P2-01. Phases 0/1/2 may progress concurrently. Acceptance requires a working cycle and checks on new inputs; finishing an academic universality study is not a prerequisite for development. Python is used for the first executor and does not constrain the genome language. The scalar prototype does not yet complete this cycle or validate general compositionality.

## Прикладной слой / Application Layer

| Phase | RU / EN | Status | To-do |
| --- | --- | --- | --- |
| A1 | Excel → матрица и другие продукты на ядре / Excel → matrix and other products on the core | Deferred until first core acceptance | [Application backlog](planning/applications.md) |

**RU:** P1-09/10/11 перенесены в A1 с сохранением ID; P0-06 отложена. Возврат — после первого работающего ядра либо явного изменения приоритета пользователем. Пример применения не меняет автоматически текущий план.

**EN:** P1-09/10/11 moved to A1 with IDs preserved; P0-06 is deferred. Resume after the first working core or an explicit user priority change. An illustrative application does not automatically change current work.

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
