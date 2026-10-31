# ADR-008 — Текущий WSL без изменения настроек / Existing WSL Without Configuration Changes

**Дата / Date:** 2026-11-01.

**Статус / Status:** принято по указанию пользователя; первые доверенные пробы выполнены, W0 не принят / accepted at user direction; initial trusted probes completed, W0 not accepted.

## Контекст / Context

**RU:** Пользователь предпочёл текущие настройки и существующий дистрибутив вместо нового ProgrammoWorld и изменения общего профиля. Systemd выключен, Docker работает. Требования внешних квот и изоляции ADR-006 сохраняются.

**EN:** The user chose existing settings/distro rather than a new ProgrammoWorld distribution or shared-profile change. Systemd is disabled and Docker is running. ADR-006 external quotas and isolation remain mandatory.

## Решение / Decision

**RU:** Использовать прямое управление cgroup v2 в собственной временной ветви. Ограничить родителя/контроллер/worker: 512/128/256 MiB без swap; CPU 1,25/0,25/1 ядра; задачи 128/32/64. Worker непривилегированный, bwrap/seccomp/rootfs сохраняются. Не создавать дистрибутив, не менять init/WSL/Docker, не перемещать чужие процессы. Внешние timeout и очистка охватывают доверенную пробу.

**EN:** Manage cgroup v2 directly in a private temporary subtree. Bound parent/controller/worker to 512/128/256 MiB without swap, 1.25/0.25/1 CPU cores and 128/32/64 tasks. Keep the worker unprivileged and retain bwrap/seccomp/rootfs. Create no distro, change no init/WSL/Docker settings and migrate no foreign processes. External timeout and cleanup cover the trusted probe.

## Альтернативы / Alternatives

**RU:** Подготовленный systemd-вариант ADR-007 и отдельная VM сохраняются. Не отключать проверки старого варианта ради запуска в другом окружении; новый backend имеет собственные проверки. Не считать общий лимит WSL резервом исключительно организма.

**EN:** Retain ADR-007's prepared systemd backend and a separate VM as alternatives. Do not disable the old backend's checks to run elsewhere; the new backend has its own checks. The shared WSL limit is not an organism-exclusive reservation.

## Последствия и проверка / Consequences and Verification

**RU:** Установлены собственные служебные файлы и учётная запись. Smoke и 12 проверок видимости/прав прошли; квоты считаны из ядра, worker пуст после завершения, ветвь удалена. Конфигурации и Docker сохранены. 38 тестов прошли в Linux, 33 в Windows (5 пропущены). Полные стрессовые проверки P2-09 остаются открытыми; развивающиеся организмы не допущены. [RU](../docs/ru/15-current-wsl-launch.md), [отчёт](../world/wsl2/evidence/current-wsl-2026-11-01.json).

**EN:** Installed project-owned infrastructure/account. Smoke and 12 visibility/permission checks passed; quotas read from the kernel, worker empty afterward and subtree removed. Configurations and Docker were preserved. Linux passed 38 tests, Windows 33 (five skipped). Full stress tests P2-09 remain open; developing organisms are not admitted. [EN](../docs/en/15-current-wsl-launch.md), [evidence](../world/wsl2/evidence/current-wsl-2026-11-01.json).
