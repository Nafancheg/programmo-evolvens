# Фаза 1 — Исполнитель / Phase 1 — Executor

[Roadmap](../ROADMAP.md) · **Status:** in_progress

| ID | To-do RU / EN | Status | Зависимость и результат / Dependency and evidence |
| --- | --- | --- | --- |
| P1-01 | Формат JSON v0 и проверка связей/типов / JSON v0 and connection/type checks | done | [runtime](../programmo_evolvens/runtime.py), [ADR-002](../adr/002-first-executor.md); экспериментальный формат / experimental format |
| P1-02 | Восемь PP, лимит шагов, журнал / Eight PPs, step limit and trace | done | [runtime](../programmo_evolvens/runtime.py); один исполнитель / one executor |
| P1-03 | Три генома и воспроизводимые примеры / Three genomes and reproducible examples | done | [demo](../programmo_evolvens/demo.py), [genomes](../examples/genomes); 14 открытых входов / 14 public inputs |
| P1-04 | Тесты результатов, отказов и ограничений / Outcome, failure and limit tests | done | [tests](../tests/test_runtime.py); python -m unittest discover -s tests -v; 18 тестов прошли 2026-10-31 на Python 3.14 / 18 tests passed 2026-10-31 on Python 3.14 |
| P1-05 | Контроль E0, измерения времени/памяти и отчёт / E0 control, timing/memory measurements and report | todo | P1-03/04; зафиксировать данные и условия / fix workloads and conditions |
| P1-06 | Закрытое испытание композиционности и разрыв связей / Held-out compositionality trial and ablation control | todo | P0-05, P1-05; [protocol](../docs/en/03-genome-and-heredity.md) |
| P1-07 | Параллельное исполнение с эквивалентными результатами / Parallel execution with equivalent outcomes | todo | P1-04/05; детерминизм и бюджеты / determinism and budgets |
| P1-08 | Автоматические проверки на нескольких версиях Python / Automated checks on multiple Python versions | todo | P1-04; пока проверено локально на 3.14 / currently tested locally on 3.14 |
| P1-09 | Собрать входные Excel, эталоны и последовательности обновлений / Collect input Excel, reference matrices and update sequences | todo | P0-06; отделить данные поиска от итоговой проверки / separate search data from final assessment |
| P1-10 | Базовое преобразование, сохранение/актуализация и сравнение матриц / Baseline transformation, storage/updates and matrix comparison | todo | P1-09; договориться о ключах, типах, повторах и критериях / agree keys, types, repeated imports and criteria |
| P1-11 | Автономно изменять и отбирать решения для Excel-сценария / Autonomously vary and select Excel-scenario solutions | todo | P1-10; оценить готовые инструменты и пространство изменений, фиксированный оценщик, бюджет, архив / assess existing tools and change space, fixed evaluator, budget, archive |

**Критерий / Exit:** RU — E0 воспроизводим, ошибки и ресурсы измерены, композиционность оценена по заранее заданному протоколу; EN — reproducible E0, measured failures/resources and compositionality assessed under a predeclared protocol. Три примера не закрывают фазу / Three examples do not close the phase.
