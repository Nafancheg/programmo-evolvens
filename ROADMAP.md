# Roadmap / Дорожная карта

**Текущий приоритет / Current priority:** создать развёртывание и развитие организма из генома: начальное состояние → механизмы/клетки/связи → функциональная структура → проверяемая работа органов. Пищеварение и усвоение — первая целевая функция, не встроенный готовый орган / build genome-driven unfolding and development: initial state → mechanisms/cells/connections → functional structure → verifiable organ work. Digestion and assimilation are the first target function, not a prebuilt organ. [Модель RU](docs/ru/11-bioengine-and-applications.md) · [Model EN](docs/en/11-bioengine-and-applications.md) · [ADR-004](adr/004-genome-driven-development.md).

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

**RU:** Ближайший шаг — P0-09, P1-13/P2-01 → P1-17 → P1-18: контракты, развёртывание генома, онтогенетический цикл. Затем P1-16 проверяет развитие до пищеварительной функции с P1-12/14/15. Фазы 0/1/2 идут по зависимостям параллельно. Развитие требует следа от генома через структурные изменения к выполненной функции. Научная уникальность не блокирует создание. Скалярный Python-прототип пока не реализует развитие или полный цикл; язык генома им не ограничен.

**EN:** Next step: P0-09, P1-13/P2-01 → P1-17 → P1-18: contracts, genome unfolding, ontogenetic cycle. P1-16 then checks development toward digestive function alongside P1-12/14/15. Phases 0/1/2 progress concurrently by dependency. Require genome-to-structure-to-function provenance. Scientific uniqueness does not gate construction. The scalar Python prototype does not implement development or the complete cycle; Python does not constrain the genome language.

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
