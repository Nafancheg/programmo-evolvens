# Programmo Evolvens

**Biologically Inspired Evolutionary Software Organisms**  
**Биологически ориентированные эволюционирующие программные организмы**

**Status / Статус:** Engineering prototype; bioengine under construction / Инженерный прототип; биодвижок в разработке — 2026-10-31.

## Текущее направление / Current Direction

**RU:** Создаём автономный биодвижок: информация поступает на единую входящую шину, проходит разбор, проверку и усвоение, сохраняется и используется дальше. Движок должен самостоятельно подбирать совместимые композиции доступных операций без внешних ИИ-агентов и языковых моделей. Гены описывают сборку механизмов из примитивов; механизмы исполняются клетками, клетки объединяются в органы и организм. Нуклеотиды относятся к кодированию генома. Ближайший результат — первый рабочий цикл питания и усвоения. Excel-продукт и дашборд относятся к последующим задачам. Самостоятельный подбор и усвоение пока не реализованы.

**EN:** Build an autonomous bioengine: information enters through one input bus, is parsed, validated, assimilated, persisted and reused. The engine must search compatible compositions of available operations without external AI agents or language models. Genes describe mechanisms assembled from primitives; cells execute mechanisms and form organs and the organism. Nucleotides belong to genome encoding. Next deliverable: a first working feeding/assimilation cycle. Excel products and dashboards are later tasks. Autonomous search and assimilation are not implemented yet.

[Целостная модель RU](docs/ru/11-bioengine-and-applications.md) · [Complete model EN](docs/en/11-bioengine-and-applications.md) · [План ядра / Core plan](ROADMAP.md) · [Прикладная очередь / Application backlog](planning/applications.md)

## Первый прототип / First Prototype

**RU:** Добавлен исследовательский последовательный исполнитель восьми PP, три декларативных JSON-генома и тесты. Примеры: пороговое обнаружение аномалий, нормализация поля записи и регулирование реальной очереди в памяти. Это первый срез фазы 1; обучение, Genesis, изоляция клеток и закрытый эксперимент ещё впереди.

**EN:** A research sequential executor of eight PPs, three declarative JSON genomes and tests are available. Examples cover threshold anomaly detection, record-field normalization and control of an actual in-memory queue. This is the first phase-1 slice; learning, Genesis, cell isolation and held-out evaluation remain future work.

Python 3.11+; tested on 3.14. No external dependencies / Без внешних зависимостей. Run from the repository root / Запуск из корня репозитория:

```text
python -m programmo_evolvens --output artifacts/smoke.json
python -m unittest discover -s tests -v
```

[Прототип RU](docs/ru/09-first-prototype.md) · [Prototype EN](docs/en/09-first-prototype.md) · [Фазы и to-do / Phases and to-dos](ROADMAP.md) · [Идеи / Ideas](planning/ideas.md)

## Русский

**Programmo Evolvens** — концепция программного организма, который выполняет задания внешней среды, поддерживает работоспособность, накапливает опыт и совершенствует своё поведение.

**Genesis** — независимая система оценки и воспроизводства структурных поколений. Организм не инициирует репродукцию и не переписывает исполняемый код. При достаточности текущих возможностей он продолжает внутреннее развитие без смены поколения — **функциональная сингулярность** (термин данного проекта, не технологическая сингулярность).

Genesis также может эволюционировать, но его обновление допускается только после внешней проверки компетентности. Главный критерий успеха — **измеримые результаты реальных заданий**, а не симулированные баллы.

## English

**Programmo Evolvens** investigates software organisms that execute externally assigned tasks, maintain operational health, accumulate experience and improve behavior.

**Genesis** independently assesses readiness and governs structural reproduction. Organisms cannot self-authorize reproduction or arbitrarily rewrite executable code. When current capabilities suffice, learning continues without generation changes, a reversible state called **functional singularity** (project-specific, not technological singularity).

Genesis may also evolve, subject to external competence validation. The primary success criterion is **measurable performance on real tasks**, not simulated scores.

## Documentation / Документация

| Topic / Тема | English | Русский |
| --- | --- | --- |
| Vision and Scope / Видение и границы | [EN](docs/en/00-vision.md) | [RU](docs/ru/00-vision.md) |
| Biological Architecture / Биологическая архитектура | [EN](docs/en/01-biological-architecture.md) | [RU](docs/ru/01-biological-architecture.md) |
| Software Organism / Программный организм | [EN](docs/en/02-software-organism.md) | [RU](docs/ru/02-software-organism.md) |
| Genome and Heredity / Геном и наследование | [EN](docs/en/03-genome-and-heredity.md) | [RU](docs/ru/03-genome-and-heredity.md) |
| Learning and Development / Обучение и развитие | [EN](docs/en/04-learning-and-development.md) | [RU](docs/ru/04-learning-and-development.md) |
| Genesis / Genesis — механизм воспроизводства | [EN](docs/en/05-genesis.md) | [RU](docs/ru/05-genesis.md) |
| Genesis Co-evolution / Коэволюция Genesis | [EN](docs/en/06-coevolution.md) | [RU](docs/ru/06-coevolution.md) |
| Functional Singularity / Функциональная сингулярность | [EN](docs/en/07-functional-singularity.md) | [RU](docs/ru/07-functional-singularity.md) |
| Research Methodology / Методика исследований | [EN](docs/en/08-research-methodology.md) | [RU](docs/ru/08-research-methodology.md) |
| First Prototype / Первый прототип | [EN](docs/en/09-first-prototype.md) | [RU](docs/ru/09-first-prototype.md) |
| Deferred Excel Scenario / Отложенный Excel-сценарий | [EN](docs/en/10-excel-to-matrix.md) | [RU](docs/ru/10-excel-to-matrix.md) |
| Bioengine and Applications / Биодвижок и приложения | [EN](docs/en/11-bioengine-and-applications.md) | [RU](docs/ru/11-bioengine-and-applications.md) |

## Research / Исследования

- [Hypotheses / Гипотезы](research/hypotheses.md)
- [Metrics / Метрики](research/metrics.md)
- [Experiments / Эксперименты](research/experiments.md)
- [Roadmap / План](ROADMAP.md)
- [ADR / Решения](adr/README.md)

**RU:** Реализован только описанный выше исследовательский прототип. Браузерная демонстрация из предшествующего обсуждения не является доказательством обучения или эволюции. Лицензия пока не выбрана.

**EN:** Only the research prototype described above is implemented. The prior browser demonstration does not demonstrate actual learning or evolution. No license selected yet.
