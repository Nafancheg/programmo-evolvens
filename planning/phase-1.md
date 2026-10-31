# Фаза 1 — Биодвижок / Phase 1 — Bioengine

[Roadmap](../ROADMAP.md) · **Status:** in_progress

**RU:** Текущая цель — автономный цикл питания и усвоения из [модели](../docs/ru/11-bioengine-and-applications.md). P1-01…04 фиксируют сделанный скалярный фундамент; они не означают готовность организма. Ближайший путь: P0-08 → P1-12/13/14 и P2-01 → P1-15 → P1-16. Внешние агенты и LLM не являются зависимостью исполнения.

**EN:** Current goal: the [model's](../docs/en/11-bioengine-and-applications.md) autonomous feeding/assimilation cycle. P1-01…04 record the completed scalar foundation, not organism readiness. Next path: P0-08 → P1-12/13/14 and P2-01 → P1-15 → P1-16. External agents and LLMs are not runtime dependencies.

| ID | To-do RU / EN | Status | Зависимость и результат / Dependency and evidence |
| --- | --- | --- | --- |
| P1-01 | Формат JSON v0 и проверка связей/типов / JSON v0 and connection/type checks | done | [runtime](../programmo_evolvens/runtime.py), [ADR-002](../adr/002-first-executor.md); экспериментальный формат / experimental format |
| P1-02 | Восемь PP, лимит шагов, журнал / Eight PPs, step limit and trace | done | [runtime](../programmo_evolvens/runtime.py); один исполнитель / one executor |
| P1-03 | Три генома и воспроизводимые примеры / Three genomes and reproducible examples | done | [demo](../programmo_evolvens/demo.py), [genomes](../examples/genomes); 14 открытых входов / 14 public inputs |
| P1-04 | Тесты результатов, отказов и ограничений / Outcome, failure and limit tests | done | [tests](../tests/test_runtime.py); python -m unittest discover -s tests -v; 18 тестов прошли 2026-10-31 на Python 3.14 / 18 tests passed 2026-10-31 on Python 3.14 |
| P1-05 | Контроль E0, измерения времени/памяти и отчёт / E0 control, timing/memory measurements and report | todo | P1-03/04; зафиксировать данные и условия / fix workloads and conditions |
| P1-06 | Закрытое испытание композиционности и разрыв связей / Held-out compositionality trial and ablation control | deferred | После первого ядра P1-16; [protocol](../docs/en/03-genome-and-heredity.md); не блокирует ограниченную реализацию / after first core P1-16; does not block bounded implementation |
| P1-07 | Параллельное исполнение с эквивалентными результатами / Parallel execution with equivalent outcomes | deferred | После последовательного ядра P1-16 и измерений P1-05 / after sequential core P1-16 and measurements P1-05 |
| P1-08 | Автоматические проверки на нескольких версиях Python / Automated checks on multiple Python versions | todo | P1-04; пока проверено локально на 3.14 / currently tested locally on 3.14 |
| P1-12 | Единый приём пакетов, структурированные типы и непереваренный остаток / Unified packet intake, structured types and undigested remainder | todo | P0-08; байты/текст/записи, происхождение, размеры и явный исход / bytes/text/records, provenance, sizes and explicit outcomes |
| P1-13 | Описания генов/механизмов и совместимая сборка графов / Gene/mechanism descriptions and compatible graph assembly | todo | P0-03/08; параметры, соединения, типы и допустимая область изменений / parameters, connections, types and permitted change scope |
| P1-14 | Усвоение и долговременное хранение единиц и рабочих механизмов / Assimilate and persist units and working mechanisms | todo | P0-08, P1-12/13; проверки, происхождение, чтение после перезапуска / validation, provenance, retrieval after restart |
| P1-15 | Встроенный подбор, мутации и рекомбинация рабочих композиций без агентов / Internal search, mutation and recombination of working compositions without agents | todo | P1-12/13, P2-01, P0-05; фиксированный критерий, бюджет, предки; без изменения базового генома и G / fixed criterion, budget, lineage; no baseline-genome rewrite or G change |
| P1-16 | Сквозная приёмка: принять → подобрать → усвоить → сохранить → повторно использовать / End-to-end acceptance: intake → search → assimilate → persist → reuse | todo | P1-14/15, P2-01; новый пример, перезапуск, отказ, откат и реальные затраты / new example, restart, failure, rollback and actual costs |

**Перенесено / Moved:** P1-09, P1-10, P1-11 → [прикладная фаза A1](applications.md), ID сохранены / IDs preserved.

**Критерий первого ядра / First-core acceptance:** RU — выполнен P1-16 в пределах зафиксированного репертуара: без ручного выбора следующей попытки и внешних агентов, с усвоением, повторным использованием, отказами и проверками на новых данных; EN — P1-16 works within the fixed repertoire, without manual next-attempt selection or external agents, including assimilation, reuse, failure handling and checks on new data. Не означает завершение отложенного общего исследования композиционности или всех задач фазы / Does not complete the deferred general compositionality study or every phase task.
