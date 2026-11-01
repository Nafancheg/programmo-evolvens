# ADR-011 — Предписанное развитие v0 / Prescribed Development v0

**Дата / Date:** 2026-11-01. **Статус / Status:** принято для ограниченного первого эксперимента / accepted for the limited first experiment.

## Контекст / Context

**RU:** После W0 нужен проверяемый переход от генома к структуре. Ручные графы скалярного исполнителя не показывают формирования клеток. ADR-004 требует происхождения структуры и выполненной функции, а ADR-006 — исполнения в принятом мире.

**EN:** After W0, demonstrate the transition from genome to structure. Hand-authored scalar graphs do not establish cell formation. ADR-004 requires structural/function provenance, and ADR-006 requires execution inside the accepted world.

## Решение / Decision

**RU:** Добавить декларативную схему `development-v0`: исходная клетка без механизмов, гены механизмов на существующих PP и структурный ген с правилами `express`, `bud`, `connect`. Правило выбирается по фактической обратной связи исполнения: отсутствие механизма источника, целевой клетки, её механизма либо доставки. После каждого изменения структура действительно исполняется. Доставка в объявленный выход — наблюдаемый исход; правильность значения проверяет внешний испытатель. Нет возраста или флага готового органа, включающего готовую функцию.

**EN:** Add declarative `development-v0`: an initial cell without mechanisms, mechanism genes using existing PPs, and a structural gene with `express`, `bud`, `connect` rules. Actual execution feedback selects a rule: missing source mechanism, destination cell, destination mechanism or delivery. Execute the structure after every change. Delivery to the declared output is an observed outcome; the external evaluator checks its value. Age or mature-organ flags cannot unlock a prebuilt function.

**RU:** Клетка содержит механизмы, собственные память/очередь, типизированные текстовые порты, бюджет и жизненный цикл idle/running/stopped. Один механизм содержит несколько операций; клетка не равна узлу графа PP. Наследуемое описание копируется и остаётся неизменным. Каждое структурное изменение ссылается на ген, правило и хеш генома. Сравнение с другим геномом и удаление связи — заранее заданные контроли, не эволюция.

**EN:** A cell owns mechanisms, memory/queue, typed text ports, budget and idle/running/stopped lifecycle. A mechanism contains several operations; a cell is not a PP graph node. Copy and preserve the heritable description. Each structural change references its gene, rule and genome hash. Comparing another genome and removing a connection are predefined controls, not evolution.

**RU:** Доверенный детерминированный zipapp подменяет только read-only содержимое существующего `/app/main.py` в bwrap; новые внешние права и квоты не добавляются. Режим `development` сверяет положительный отчёт W0 с текущими компонентами под lock до создания cgroup и запуска. При несовпадении нет исполнения. Контрактные тесты вне мира проверяют только данные и сборку; сами развивающиеся варианты и контроли исполняются внутри W0.

**EN:** A trusted deterministic zipapp replaces only the read-only contents at the existing bwrap `/app/main.py`; add no external privileges or quotas. Under the lock, `development` compares positive W0 evidence with current components before cgroup creation or execution. A mismatch refuses execution. Tests outside the world validate only data and packaging; developing variants and controls execute inside W0.

## Альтернативы / Alternatives

**RU:** Готовая функция нормализации в среде; переименование узлов PP в клетки; выполнение экспериментальных кандидатов в обычном unittest. Отклонены: они подменяют развитие или обходят принятую границу.

**EN:** Hard-code a normalizer into the environment, rename PP nodes as cells, or execute candidates in ordinary unittest. Reject these: they substitute for development or bypass the accepted boundary.

## Последствия / Consequences

**RU:** Результат показывает только развитие предписанной организации и ограниченную функцию текста/памяти. Нет утверждений об обучении, автономном подборе композиции, пищеварении произвольных файлов, долговременном усвоении, органах или Genesis. Следующие задачи P1-12/14/15/16 сохраняются. [Контракт и эксперимент RU](../docs/ru/18-prescribed-development.md), [EN](../docs/en/18-prescribed-development.md).

**EN:** The result establishes prescribed organization development and a limited text/memory function. It does not establish learning, autonomous composition search, arbitrary-file digestion, durable assimilation, organs or Genesis. Preserve P1-12/14/15/16 as subsequent work. [Contract and experiment RU](../docs/ru/18-prescribed-development.md), [EN](../docs/en/18-prescribed-development.md).

**Наблюдение / Observation:** показывать итоговый экземпляр, его геном/исходники и паспорт отдельно от пошаговой записи; запись не является новым исполнением / show the resulting instance, genome/source and passport separately from recorded replay; replay does not execute a new organism.
