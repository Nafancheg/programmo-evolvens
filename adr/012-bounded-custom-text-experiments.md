# ADR-012 — Свой текст и повторяемость / Custom Text and Repeatability

**Дата / Date:** 2026-11-01. **Статус / Status:** принято по запросу пользователя / accepted at user request.

## Контекст / Context

**RU:** Пользователь требует проверить результат на тексте, отличном от HeLLo, и уточняет, что создано самостоятельно. Все исходники, примитивы и правила v0 написаны разработчиком; программа пока самостоятельно исполняет предписанную сборку. Новый вход и повторяемость не доказывают самостоятельный поиск или эволюцию.

**EN:** The user requests a different input from HeLLo and asks what was created autonomously. Developers authored all v0 sources, primitives and rules; the program autonomously executes prescribed assembly. Different input and repeatability do not establish autonomous search or evolution.

## Решение / Decision

**RU:** Разрешить текст до 256 байт UTF-8 как данные существующего фиксированного генома. Контроллер получает текст через stdin, проверяет размер и передаёт JSON-пакет. Worker создаёт два свежих экземпляра одного генома внутри W0 и сравнивает результат и логический след; внешний эталон — `text.strip().lower()`. Память экземпляров отдельная, исходный геном неизменен. Малый предел ввода удерживает даже экранированные значения в лимите строки телеметрии 16 KiB.

**EN:** Admit at most 256 UTF-8 bytes of text as data for the existing fixed genome. The controller receives stdin, checks size and passes a JSON packet. Inside W0 the worker creates two fresh instances of one genome, comparing outputs and logical traces against external reference `text.strip().lower()`. Instance memories are separate and the genome remains unchanged. The small input bound keeps escaped values within the 16 KiB telemetry-line limit.

**RU:** По прямому запросу добавить одну операцию управления в локальный дашборд: `POST /api/development` с единственным полем `text`. Требовать loopback Host, точный Origin, временный токен страницы, JSON и ограниченный размер тела. Один активный запрос, без очереди; команда запуска фиксирована, текст идёт в stdin, нет shell или выбираемых путей/кода/политики. Проверяются резерв памяти, действующая приёмка и все прежние квоты/тайм-ауты. Наблюдение и прочие API остаются чтением.

**EN:** At explicit user request add one local dashboard action: `POST /api/development`, accepting only `text`. Require loopback Host, exact Origin, an ephemeral page token, JSON and a bounded body. Admit one active request with no queue; the command is fixed, text goes through stdin, with no shell or selectable paths/code/policy. Check host reserve, applicable acceptance and all existing quotas/deadlines. Observation and other APIs remain read-only.

## Альтернативы / Alternatives

**RU:** Подменить HeLLo другим литералом в исходниках; объявить повторение обучением; разрешить произвольные команды/геномы из браузера. Отклонены: пользователь должен задавать данные без правки программы, а область допуска остаётся фиксированной.

**EN:** Replace the HeLLo source literal, call repetition learning, or admit arbitrary commands/genomes from the browser. Reject these: users must supply data without editing code, and admission scope remains fixed.

## Последствия / Consequences

**RU:** Режим без текста сохраняет исходные 10 контролей. Новый текст даёт отдельный журнал, паспорт, запись и пять проверок: доставка, эталон, совпадение двух свежих экземпляров, память и тот же геном. Квоты доступа не расширяются; изменённый контроллер требует повторной приёмки W0. Истощение архива завершает дальнейшие попытки объяснимым отказом. Автономный поиск P1-15 остаётся следующим отдельным шагом.

**EN:** Omitting text preserves the original ten controls. Custom text produces its own journal, specimen, recording and five checks: delivery, reference, two-instance agreement, memory and unchanged genome. Privileges do not expand; the changed controller requires renewed W0 acceptance. Archive exhaustion rejects subsequent attempts with an explanation. Autonomous search P1-15 remains the next separate step.
