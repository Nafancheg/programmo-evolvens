# ADR-001 — Генетическая модель / Genetic Model

**Дата / Date:** 2026-10-31  
**Статус / Status:** Принято как архитектурное направление; исследовательская гипотеза не проверена. / Accepted as architectural direction; the research hypothesis is untested.

## Контекст / Context

**RU:** Необходимо определить строительные элементы программного организма, не смешивая кодирование наследуемого описания с исполняемыми способностями. ДНК состоит из нуклеотидов, белки — из аминокислот; биологическая аналогия не является доказательством программной модели. Репозиторий находится на стадии концепции, реализации ещё нет.

**EN:** The software organism needs building blocks that distinguish encoding a heritable description from executable capabilities. DNA consists of nucleotides and proteins of amino acids; the biological analogy does not validate the software model. The repository is at the concept stage, with no implementation yet.

## Решение / Decision

**RU:** Принять иерархию «нуклеотид → ген → функциональный механизм → клетка → орган → организм». Разделить атомарные элементы кодирования генома и семантические функциональные примитивы с контрактами. Геном — версионированное декларативное описание, независимое от языка программирования; язык служит средством реализации среды и не является примитивом генома.

**EN:** Adopt the hierarchy “nucleotide → gene → functional mechanism → cell → organ → organism.” Separate atomic genome encoding elements from semantic functional primitives with contracts. The genome is a versioned declarative description independent of the programming language; the language implements the runtime and is not a genome primitive.

**RU:** Начать исследование с кандидатов `SENSE`, `COMPARE`, `TRANSFORM`, `DECIDE`, `ACT`, `STORE`, `SIGNAL`, `REGULATE`. До реализации определить типы, условия, эффекты, полномочия, ресурсы, отказы и воспроизводимость. Формат генома и окончательный набор PP пока не утверждать.

**EN:** Start investigation with candidates `SENSE`, `COMPARE`, `TRANSFORM`, `DECIDE`, `ACT`, `STORE`, `SIGNAL`, `REGULATE`. Define types, conditions, effects, permissions, resources, failures and reproducibility before implementation. Leave the genome format and final PP set undecided.

**RU:** Обучение и разрешённая рабочая перекомпоновка происходят внутри поколения. Изменение наследуемого функционального состава или структуры за пределами этой области требует независимой оценки и допуска нового поколения Genesis. Организм не пишет новый исполняемый код и не разрешает собственную репродукцию; новые типы PP требуют проверенных реализаций.

**EN:** Learning and permitted working recomposition occur within a generation. Changes to heritable functional composition or structure beyond that scope require independent Genesis assessment and admission of a new generation. The organism does not write new executable code or authorize its own reproduction; new PP types require validated implementations.

## Альтернативы / Alternatives

**RU:** Не приняты: язык программирования как строительный примитив (связывает модель с технологией); исходный код как геном (смешивает описание и реализацию); немедленная фиксация большого каталога операций (может скрыть отсутствие композиционности). Прямое программирование остаётся контрольным способом решения задач в эксперименте.

**EN:** Not adopted: a programming language as the building primitive (ties the model to a technology); source code as the genome (conflates description and implementation); immediately fixing a large operation catalog (may conceal a lack of compositionality). Direct programming remains the experimental baseline.

## Последствия и проверка / Consequences and Validation

**RU:** Реестр, контракты, валидатор и исполнение предстоит спроектировать. Гипотеза: фиксированный набор из 8–12 PP порождает разные способности изменением только генома. Проверка после E0: три заранее определённых класса задач, замороженные реализации и адаптеры, отложенные данные, независимая оценка, ресурсные ограничения и воспроизводимые журналы. Нельзя скрывать специализированные решатели внутри общих PP. Необходимость менять код или провал заранее заданных порогов не подтверждает выбранный набор и требует пересмотра с новым испытанием. Успех не докажет универсальность, обучение или эволюцию.

**EN:** The registry, contracts, validator and execution remain to be designed. Hypothesis: a fixed set of 8–12 PPs produces different capabilities through genome changes alone. Test after E0 using three predefined task classes, frozen implementations and adapters, held-out data, independent assessment, resource limits and reproducible logs. General PPs must not hide specialized solvers. Requiring code changes or missing predeclared thresholds does not support the chosen set and requires revision followed by a new trial. Success will not establish universality, learning or evolution.

**RU:** Подробные определения, контракты, правила наследования и критерии эксперимента: [Геном и наследование](../docs/ru/03-genome-and-heredity.md).

**EN:** Detailed definitions, contracts, inheritance rules and experimental criteria: [Genome and Heredity](../docs/en/03-genome-and-heredity.md).
