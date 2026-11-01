# Programmo Evolvens

**Biologically Inspired Evolutionary Software Organisms**  
**Биологически ориентированные эволюционирующие программные организмы**

**Status / Статус:** Engineering prototype; W0 accepted; prescribed development demonstrated / Инженерный прототип; W0 принят, показано предписанное развитие — 2026-11-01.

## Текущее направление / Current Direction

**RU:** Сначала создаём и проверяем ограниченный виртуальный мир W0: внешние квоты ресурсов, закрытые по умолчанию доступы и независимая остановка. Мир проектируется разработчиками и не эволюционирует вместе с организмом. Затем внутри него запускаем развитие из генома: механизмы → клетки → органы → проверяемая функция. Пищеварение и усвоение — первая целевая способность; Excel и дашборд остаются последующими задачами. Организм и Genesis не могут расширить границы мира. Внешние ИИ-агенты не требуются. Границы W0 прошли 13 сценариев приёмки; локальный дашборд показывает реальные журналы и ресурсы. Первая предписанная структура развёрнута из генома; самостоятельный поиск и усвоение ещё впереди.

**EN:** First build and verify bounded virtual world W0: external resource quotas, default-deny permissions and independent stopping. Developers engineer the world; it does not co-evolve with the organism. Then run genome-driven development inside it: mechanisms → cells → organs → verifiable function. Digestion and assimilation are the first target capability; Excel and dashboards remain later tasks. Neither the organism nor Genesis can expand world boundaries. External AI agents are not required. W0 boundaries passed 13 acceptance scenarios; a local dashboard displays actual logs and resources. The first prescribed structure unfolds from a genome; autonomous search and assimilation remain pending.

[Целостная модель RU](docs/ru/11-bioengine-and-applications.md) · [Complete model EN](docs/en/11-bioengine-and-applications.md) · [План ядра / Core plan](ROADMAP.md) · [Прикладная очередь / Application backlog](planning/applications.md)

[Виртуальный мир RU](docs/ru/13-virtual-world.md) · [Virtual world EN](docs/en/13-virtual-world.md) · [W0](planning/world.md)

**2026-11-01 — W0 + Lab:** [приёмка RU](docs/ru/16-w0-acceptance.md) / [acceptance EN](docs/en/16-w0-acceptance.md); 62 Linux tests, 52 Windows passed + 10 Linux-only skipped. [Установка и дашборд RU](docs/ru/17-laboratory-dashboard.md) / [setup and dashboard EN](docs/en/17-laboratory-dashboard.md). WSL/Docker settings unchanged; first bounded development experiment executed / Настройки сохранены; первый ограниченный эксперимент развития выполнен в принятом мире.

```powershell
.\scripts\setup-lab.ps1 -InstallDependencies
.\world\wsl2\config\run-acceptance.ps1
.\scripts\run-development.ps1
.\scripts\start-lab.ps1
```

Requires Windows Python 3.11+ and WSL2 Ubuntu/Debian / Нужны Python 3.11+ для Windows и WSL2 Ubuntu/Debian.

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
| Motivation and Reinforcement / Мотивация и подкрепление | [EN](docs/en/12-motivation-and-reinforcement.md) | [RU](docs/ru/12-motivation-and-reinforcement.md) |
| Virtual World and Limits / Виртуальный мир и ограничения | [EN](docs/en/13-virtual-world.md) | [RU](docs/ru/13-virtual-world.md) |
| WSL2 Laboratory Backend / Лабораторный backend WSL2 | [EN](docs/en/14-wsl2-backend.md) | [RU](docs/ru/14-wsl2-backend.md) |
| Existing WSL Launch and Evidence / Запуск в текущем WSL и результаты | [EN](docs/en/15-current-wsl-launch.md) | [RU](docs/ru/15-current-wsl-launch.md) |
| W0 Acceptance / Приёмка W0 | [EN](docs/en/16-w0-acceptance.md) | [RU](docs/ru/16-w0-acceptance.md) |
| Laboratory and Installation / Лаборатория и установка | [EN](docs/en/17-laboratory-dashboard.md) | [RU](docs/ru/17-laboratory-dashboard.md) |
| Prescribed Development and Specimen / Предписанное развитие и экземпляр | [EN](docs/en/18-prescribed-development.md) | [RU](docs/ru/18-prescribed-development.md) |
| Custom Text and Repeatability / Свой текст и повторяемость | [EN](docs/en/19-custom-text-repeatability.md) | [RU](docs/ru/19-custom-text-repeatability.md) |

## Research / Исследования

- [Hypotheses / Гипотезы](research/hypotheses.md)
- [Metrics / Метрики](research/metrics.md)
- [Experiments / Эксперименты](research/experiments.md)
- [Roadmap / План](ROADMAP.md)
- [ADR / Решения](adr/README.md)

**RU:** Реализован только описанный выше исследовательский прототип. Браузерная демонстрация из предшествующего обсуждения не является доказательством обучения или эволюции. Лицензия пока не выбрана.

**EN:** Only the research prototype described above is implemented. The prior browser demonstration does not demonstrate actual learning or evolution. No license selected yet.

**Первый экземпляр / First instance:** `text-retention`: one empty cell → two cells + one link; `  HeLLo  ` → `hello` + private cell memory. [RU](docs/ru/18-prescribed-development.md) / [EN](docs/en/18-prescribed-development.md). 10 in-world checks passed; no learning/evolution claim / 10 проверок в мире прошли; обучение/эволюция не заявляются.

**Другой вход / Different input:** use the laboratory’s “Check twice” button or `.\scripts\run-development.ps1 -Text "  DIFFERENT WoRDS  "`. Same authored genome, two fresh instances; no learning/evolution claim / тот же заданный геном, два свежих экземпляра; обучение/эволюция не заявляются.
