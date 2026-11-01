# Фаза 6 — Наблюдение / Phase 6 — Observation

[Roadmap](../ROADMAP.md) · **Status:** in_progress — explicit user priority 2026-11-01 / прямой запрос пользователя

| ID | To-do RU / EN | Status | Зависимость и результат / Dependency and evidence |
| --- | --- | --- | --- |
| P6-01 | Формат событий и чтение реальных журналов / Event format and actual trace ingestion | done | [WSL exporter](../world/wsl2/observe.py), [dashboard](../programmo_evolvens/lab.py); actual W0 JSONL + source metadata / реальные события W0; cell events await P2-03 |
| P6-02 | Граф генома, клетки, временная шкала / Genome graph, cells and timeline | in_progress | Actual v0 cells/mechanisms/links + 20 recorded events; broader genome graph pending / клетки и связи показаны, полный граф генома впереди; [Развитие RU](../docs/ru/18-prescribed-development.md), [EN](../docs/en/18-prescribed-development.md), [evidence](../world/wsl2/evidence/development-2026-11-01.json) |
| P6-03 | Метрики задач, ресурсов, поколений / Task, resource and generation metrics | in_progress | CPU/memory/pids, trial outcomes and live UI verified / ресурсы и исходы W0 проверены; generations await P4-05, no invented values / поколения впереди |
| P6-04 | Воспроизведение запуска и RU/EN интерфейс / Run replay and RU/EN interface | done | v0: RU/EN, recorded playback, exact source/specimen export and custom-text re-execution verified / запись, код/паспорт и повторный запуск с новым текстом; [evidence](../world/wsl2/evidence/custom-text-2026-11-01.json) |
| P6-05 | Переносимая настройка и запуск лаборатории / Portable laboratory setup and launch | in_progress | [Setup](../scripts/setup-lab.ps1), [RU](../docs/ru/17-laboratory-dashboard.md), [EN](../docs/en/17-laboratory-dashboard.md); update + check-only verified locally; clean second PC pending / чистый второй ПК впереди |

**Критерий / Exit:** RU — каждый показатель связан с исходным событием; EN — every indicator traces to an actual event. Чтение журналов можно делать параллельно ранним фазам / Trace ingestion can progress alongside earlier phases.
