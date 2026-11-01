# Architecture Decision Records / Журнал архитектурных решений

**RU:** Для архитектурных изменений заводим ADR с разделами: контекст, решение, альтернативы, последствия, дата, статус. Не меняем утверждённые принципы без отдельного решения.

**EN:** Record architectural changes with context, decision, alternatives, consequences, date and status. No silent changes to accepted principles.

## Решения / Decisions

- [ADR-001 — Генетическая модель / Genetic Model](001-genetic-model.md) — принято как архитектурное направление; гипотеза не проверена / accepted as architectural direction; hypothesis untested.
- [ADR-002 — Первый исполнитель / First Executor](002-first-executor.md) — принято для прототипа; JSON v0 экспериментальный / accepted for prototype; experimental JSON v0.
- [ADR-003 — Сначала биодвижок / Bioengine First](003-bioengine-first.md) — принято; два слоя, автономный цикл питания/усвоения и внутренний поиск без внешних агентов / accepted; two layers, autonomous feeding/assimilation and internal search without external agents.
- [ADR-004 — Развитие из генома / Genome-Driven Development](004-genome-driven-development.md) — принято; развёртывание и развитие структуры предшествуют работе органов / accepted; structural unfolding and development precede organ function.
- [ADR-005 — Мотивация и однократные достижения / Motivation and One-Time Achievements](005-motivation-and-unique-achievements.md) — принципы зафиксированы; механизм и параметры впереди / principles recorded; mechanism and parameters pending.
- [ADR-006 — Сначала ограниченный мир / Bounded World First](006-world-before-organism.md) — принято; внешняя защита и приёмка W0 предшествуют запуску развивающегося организма / accepted; external protection and W0 acceptance precede developing-organism execution.
- [ADR-007 — Первый backend W0 на WSL2 / First WSL2 W0 Backend](007-wsl2-laboratory-backend.md) — выбран для подготовки; установка и приёмка впереди / selected for preparation; installation/acceptance pending.
- [ADR-008 — Текущий WSL без изменения настроек / Existing WSL Without Configuration Changes](008-current-wsl-direct-cgroups.md) — реализован первый доверенный запуск через прямой cgroup v2; полная приёмка впереди / initial trusted launch implemented using direct cgroup v2; full acceptance pending.

- [ADR-009 — Область приёмки W0 / W0 Acceptance Scope](009-w0-acceptance-scope.md) — 13 сценариев прошли для фиксированного профиля / 13 scenarios passed for the fixed profile.
- [ADR-010 — Локальная лаборатория и перенос / Local Laboratory and Portability](010-local-lab-and-portable-setup.md) — ранний дашборд по запросу пользователя; установка проверена здесь, второй ПК впереди / early dashboard at user request; local setup verified, second PC pending.
