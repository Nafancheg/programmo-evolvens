# ADR-009 — Область приёмки W0 / W0 Acceptance Scope

**Дата / Date:** 2026-11-01.

**Статус / Status:** принято для фиксированного профиля; [измерения / evidence](../world/wsl2/evidence/w0-acceptance-2026-11-01.json) / accepted for the fixed profile.

## Контекст / Context

**RU:** Первые smoke/inspect-пробы проверили запуск, но не исчерпание ресурсов и аварии. Нужны измеримые условия завершения W0 в текущем WSL без расширения разрешений организма.

**EN:** Initial smoke/inspect probes checked startup, not exhaustion or failures. W0 needs measurable completion criteria in the existing WSL without expanding workload permissions.

## Решение / Decision

**RU:** W0 принимается для фиксированного последовательного однопоточного Python-профиля ADR-008 после фактических испытаний памяти, CPU и настенного времени, вывода, протокола, зависаний, закрытых каналов, полномочий, tmpfs, дескрипторов, количества задач, смерти контроллера и восстановления. Параллельный запуск отклоняется, поэтому общая квота не умножается числом запросов. Свободный резерв компьютера измеряется перед испытанием. Самопроверки организма не являются доказательством; внешний испытатель проверяет квоты, события ядра, состояние процессов и очистку.

**EN:** Accept W0 for the fixed serial, single-threaded Python profile of ADR-008 after live memory, CPU/wall-time, output, protocol, hang, closed-channel, permission, tmpfs, descriptor, task-count, controller-death and recovery trials. Reject concurrent launches so aggregate quotas do not multiply with requests. Measure host reserve before the trial. Organism self-checks are insufficient evidence; an external tester checks quotas, kernel events, process state and cleanup.

**RU:** Для проверки pids.max допускается отдельный фиксированный доверенный helper в той же cgroup worker с теми же квотами. Он проверяет ограничение ядра, а не возможности организма. Его возможность fork не добавляется в seccomp организма. Расширение профиля, в том числе потоки/процессы, сеть или новые монтирования, требует отдельного решения и повторной приёмки.

**EN:** A separate fixed trusted helper in the same worker cgroup and quotas may exercise pids.max. It tests the kernel boundary, not organism capabilities. Its fork permission is not added to workload seccomp. Profile expansion, including threads/processes, networking or new mounts, requires a separate decision and renewed acceptance.

## Альтернативы / Alternatives

**RU:** Считать успешный smoke достаточной приёмкой или разрешить fork организму ради теста pids.max. Оба варианта отклонены: первый не проверяет отказы, второй меняет проверяемый профиль.

**EN:** Treat a successful smoke run as sufficient acceptance, or allow workload fork to exercise pids.max. Reject both: the former misses failures; the latter changes the profile under test.

## Последствия / Consequences

**RU:** Положительный итог снимает зависимость P2-09 для разработки следующего этапа в проверенной границе. Новый исполнитель генома обязан использовать её и проверять применимость отчёта к своим компонентам; нынешний CLI по-прежнему принимает только фиксированные пробы. Приёмка не означает обучение, эволюцию, готовый организм или доказанную безопасность любого кода. Отрицательные попытки и журналы сохраняются; статус `done` требует ссылки на положительный итог.

**EN:** A positive result satisfies P2-09 for subsequent work inside the verified boundary. A new genome executor must reuse it and verify that the evidence applies to its components; the current CLI still accepts only fixed probes. Acceptance does not establish learning, evolution, a ready organism or proven safety for arbitrary code. Preserve negative attempts and logs; `done` requires a link to positive evidence.

[Проверки RU](../docs/ru/16-w0-acceptance.md) · [Checks EN](../docs/en/16-w0-acceptance.md) · [План / Plan](../planning/world.md).
