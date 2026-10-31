# ADR-003 — Сначала биодвижок / Bioengine First

**Дата / Date:** 2026-10-31.

**Статус / Status:** Принято как направление разработки по уточнению пользователя; реализация впереди / Accepted implementation direction following user clarification; implementation pending.

## Контекст / Context

**RU:** Обсуждение сместилось от примитивов и структуры организма к прикладной обработке Excel и агентной генерации кода. Пользователь уточнил: создать автономный биодвижок, способный принимать, перерабатывать, усваивать и использовать информацию, строить и менять цепочки механизмов без внешних агентов. Прикладные продукты относятся к следующему слою. Сохранять идеи, стабилизировать текущие задачи и двигаться через рабочие реализации.

**EN:** Discussion shifted from primitives and organism structure toward Excel applications and agentic code generation. The user clarified: build an autonomous bioengine that accepts, processes, assimilates and uses information, composing and changing mechanisms without external agents. Application products belong to a later layer. Preserve ideas, stabilize current work and advance through working implementations.

## Решение / Decision

**RU:** Разделить биодвижок и прикладной слой. Ближайший вертикальный срез — приём → разбор → проверка → усвоение → долговременная память → повторное использование, с минимальной клеточной моделью и встроенным подбором композиций ограниченных операций. Excel/матрица отложены в прикладную очередь без удаления исходных задач. Дашборд не является условием готовности ядра.

**EN:** Separate the bioengine and application layer. The next vertical slice is intake → parsing → validation → assimilation → durable memory → reuse, with a minimal cell model and internal search over bounded-operation compositions. Defer Excel/matrix work to an application backlog while preserving task IDs. A dashboard is not a core-readiness prerequisite.

**RU:** Сохранить иерархию и независимый от языка декларативный геном ADR-001. Восемь PP — предварительные семейства. Необходимые реализации и начальные возможности задаются инженерно; встроенный алгоритм самостоятельно варьирует и проверяет разрешённые композиции. Не требовать внешнего ИИ, языковой модели или человека для каждой попытки. Готовый парсер сам по себе не является результатом обучения.

**EN:** Preserve ADR-001's hierarchy and language-independent declarative genome. The eight PPs remain provisional families. Engineers supply starting capabilities and implementations; an internal algorithm autonomously varies and checks permitted compositions. Do not require external AI, a language model or a human per attempt. A prebuilt parser alone is not evidence of learning.

**RU:** Локальная адаптация не меняет наследуемый базовый геном и не увеличивает G. Структурная эволюция и объединение наследуемых фрагментов за пределами разрешённой области остаются под Genesis; человеческое утверждение исследовательского выпуска нового поколения сохраняется. Генерация кода агентом и изменение реализации PP не включаются в первое ядро и не отменяют ранее принятых инвариантов.

**EN:** Local adaptation neither rewrites the baseline heritable genome nor increments G. Structural evolution and heritable-fragment combination beyond permitted scope remain under Genesis; human approval of research releases of new generations remains. Agentic code generation and PP implementation changes are outside the first core and do not repeal prior invariants.

## Альтернативы / Alternatives

**RU:** Прикладной Excel-конвейер первым; внешний LLM/агент как обязательный создатель каждого варианта; большой перечень готовых парсеров, названный обучением; ожидание завершения обзора литературы до сборки ядра. Первые два направления сохранены как идеи для отдельной оценки, но не задают текущую работу. Проверки корректности остаются обязательной частью разработки.

**EN:** Start with an Excel application; require an external LLM/agent to create every candidate; call a large catalog of prebuilt parsers learning; wait for literature review completion before building the core. Preserve the first two directions for separate assessment without letting them drive current work. Correctness checks remain part of development.

## Последствия и проверка / Consequences and Verification

**RU:** Нужно расширить скалярный прототип структурированными типами, описаниями механизмов, минимальной клеткой, усвоением, долговременным хранением и внутренним поиском. Исходный материал, происхождение, непереваренный остаток, расходы и отказы наблюдаемы. Поддержка произвольного формата не обещается. Информация не заменяет реальные вычислительные бюджеты. Конкретные критерии — [модель RU](../docs/ru/11-bioengine-and-applications.md), задачи — [план](../ROADMAP.md).

**EN:** Extend the scalar prototype with structured types, mechanism descriptions, a minimal cell, assimilation, durable storage and internal search. Observe source material, provenance, undigested content, costs and failures. Do not promise arbitrary-format support. Information does not replace real compute budgets. Concrete criteria: [model EN](../docs/en/11-bioengine-and-applications.md); tasks: [plan](../ROADMAP.md).

**RU:** Уточняет текущий приоритет ADR-001/002 и переносит Excel-сценарий из активного ядра в прикладную очередь. Не означает, что автономное пищеварение или эволюция уже реализованы.

**EN:** Clarifies ADR-001/002 implementation priority and moves the Excel scenario out of active core work into the application backlog. It does not claim autonomous digestion or evolution is already implemented.
