# Roadmap / Дорожная карта

**Текущий приоритет / Current priority:** W0 принят для фиксированного профиля; наблюдаем лабораторию и переходим к прослеживаемому развитию структуры из генома / W0 accepted for the fixed profile; observe the laboratory and proceed to traceable genome-driven structural development. Пищеварение остаётся первой целевой функцией / digestion remains the first target function. [Приёмка RU](docs/ru/16-w0-acceptance.md) · [Acceptance EN](docs/en/16-w0-acceptance.md) · [Лаборатория / Lab](docs/ru/17-laboratory-dashboard.md).

**Два слоя / Two layers:** ядро и прикладные продукты / core and application products. Для первой рабочей модели не нужны пользовательский Excel и дашборд; проверки проводим на небольших определённых наборах входов / user Excel files and a dashboard are not prerequisites for the first working model; use small defined input sets for checks. Внешние ИИ-агенты и языковые модели не требуются для работы ядра / external AI agents and language models are not required at core runtime.

**2026-11-01:** границы W0 приняты для фиксированного последовательного профиля: [13 live-проверок / trials](docs/ru/16-w0-acceptance.md), [EN](docs/en/16-w0-acceptance.md). По прямому запросу пользователя наблюдение перенесено вперёд: [локальная лаборатория и установка / local lab and setup](docs/ru/17-laboratory-dashboard.md), [EN](docs/en/17-laboratory-dashboard.md). Развитие из генома — следующий этап; семантика мира P2-10/11 ещё впереди / genome-driven development is next; world semantics remain pending.

## Биодвижок: фазы / Bioengine Phases

| Phase | RU | EN | Status | To-do |
| --- | --- | --- | --- | --- |
| W0 | Виртуальный мир: внешняя изоляция, ресурсы и доступы | Virtual world: external isolation, resources and permissions | Boundaries accepted; semantics pending | [W0](planning/world.md) |
| 0 | Контракты и границы первой рабочей модели | Contracts and first-model boundaries | In progress | [P0](planning/phase-0.md) |
| 1 | Биодвижок: питание, усвоение, композиция | Bioengine: feeding, assimilation, composition | In progress | [P1](planning/phase-1.md) |
| 2 | Клетки, телеметрия, отказоустойчивость | Cells, telemetry and resilience | In progress | [P2](planning/phase-2.md) |
| 3 | Память, обучение и контроль качества | Memory, learning and evaluation | Planned | [P3](planning/phase-3.md) |
| 4 | Genesis: оценка, эволюционный запрос, допуск | Genesis: assessment and approval | Planned | [P4](planning/phase-4.md) |
| 5 | Коэволюция Genesis и проверка новых поколений | Genesis co-evolution and generation testing | Planned | [P5](planning/phase-5.md) |
| 6 | Веб-дашборд на реальных событиях | Dashboard backed by observed events | In progress: user priority | [P6](planning/phase-6.md) |

**RU:** Первая граница исполнения — приёмка мира P2-09 в W0. Контракты генома/клеток P0-09, P1-13/P2-01 проектируются параллельно, но развёртывание P1-17, развитие P1-18 и подбор кандидатов запускаются внутри принятого мира. Затем P1-16 проверяет пищеварительную функцию. Мир создаётся разработчиками и не эволюционирует автоматически; организм и Genesis не расширяют его доступы/квоты. Скалярный Python-прототип не является такой защитой.

**EN:** The first execution boundary is world acceptance P2-09 in W0. Design genome/cell contracts P0-09, P1-13/P2-01 concurrently, but run unfolding P1-17, development P1-18 and candidate search inside the accepted world. P1-16 then checks digestive function. Developers build the world; it does not evolve automatically, and the organism/Genesis cannot expand its permissions or quotas. The scalar Python prototype does not provide this protection.

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
