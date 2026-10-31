# ADR-002 — Первый исполнитель / First Executor

**Дата / Date:** 2026-10-31.

**Статус / Status:** Принято для прототипа, формат экспериментальный / Accepted for the prototype, experimental format.

## Контекст / Context

**RU:** ADR-001 требует проверить декларативную композицию. Нужен небольшой исполнимый срез до полного E0, клетки и Genesis. Работа разбивается по фазам с отдельными to-do, несколько задач могут быть активны; будущие идеи сохраняются.

**EN:** ADR-001 requires investigating declarative composition. A small executable slice is needed before full E0, cells and Genesis. Work follows phases with separate to-dos and multiple active tasks; future ideas are retained.

## Решение / Decision

**RU:** Использовать Python без внешних зависимостей для первого последовательного исполнителя. JSON v0 задаёт упорядоченный ациклический граф с типизированными скалярными портами и версиями PP. Проверять весь граф до эффектов; доверенные адаптеры подключает ведущая программа. Рабочее состояние отдельно от генома. Восемь PP имеют ограниченные конкретные контракты, а не универсальные решатели. Код геномом не генерируется.

**EN:** Use dependency-free Python for the first sequential executor. JSON v0 defines an ordered acyclic graph with typed scalar ports and PP versions. Validate the whole graph before effects; the host supplies trusted adapters. Keep working state separate from the genome. The eight PPs have limited concrete contracts rather than universal solvers. Genomes do not generate code.

## Альтернативы / Alternatives

**RU:** Двоичный алфавит, граф нескольких генов, другая реализация языка, процессы и параллельный граф сохранены как будущие направления [реестра](../planning/ideas.md) и фаз. Их отсутствие в первом срезе не означает отказ от концепций. Сценарии в геноме с произвольным исполняемым кодом противоречили бы ADR-001.

**EN:** A binary alphabet, multi-gene graphs, another runtime language, processes and parallel graphs remain future directions in the [register](../planning/ideas.md) and phase lists. Omitting them from the first slice does not discard the concepts. Arbitrary executable scripts in genomes would conflict with ADR-001.

## Последствия / Consequences

**RU:** Можно запускать и проверять три поведения при одном исполнителе. JSON v0 не является окончательной спецификацией ДНК; PP не равны клеткам. Логические лимиты не обеспечивают изоляцию или жёсткие тайм-ауты. Внутреннее состояние не фиксируется при отказе, но внешний эффект ACT автоматически не откатывается. Тесты открытых примеров не закрывают E0 и не доказывают обучение, композиционность или эволюцию.

**EN:** Three behaviors can run and be checked with one executor. JSON v0 is not the final DNA specification; PPs are not cells. Logical limits provide neither isolation nor hard timeouts. Internal state does not commit on failure, but external ACT effects are not automatically undone. Public-fixture tests do not complete E0 or prove learning, compositionality or evolution.

**Проверка / Verification:** [тесты / tests](../tests/test_runtime.py), [запуск RU](../docs/ru/09-first-prototype.md), [run EN](../docs/en/09-first-prototype.md), [P1 to-do](../planning/phase-1.md).
