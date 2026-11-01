# ADR-010 — Локальная лаборатория и перенос / Local Laboratory and Portability

**Дата / Date:** 2026-11-01. **Статус / Status:** принято по прямому запросу пользователя / accepted at explicit user request.

## Контекст / Context

**RU:** Пользователь переносит дашборд наблюдения вперёд и требует установку на другом ПК. Раннее наблюдение должно показывать реальные данные, сохраняя приоритет развития автономного ядра.

**EN:** The user brings observation forward and requests installation on another PC. Early observation must show real data while preserving autonomous-core development as the underlying goal.

## Решение / Decision

**RU:** Реализовать локальный RU/EN HTTP-дашборд на стандартной библиотеке Python, фиксированный read-only экспортёр WSL и PowerShell-скрипты настройки/запуска. Привязка только к loopback, без удалённого сервиса и команд управления миром. Хеши компонентов определяют применимость приёмки. Выбор дистрибутива локален и переопределяем, rootfs строится из системного Python нового ПК, приёмка выполняется заново.

**EN:** Build a local RU/EN HTTP dashboard using Python's standard library, a fixed read-only WSL exporter and PowerShell setup/launch scripts. Bind only to loopback, without a remote service or world-control commands. Component hashes determine acceptance applicability. Distribution selection is local and overridable; build rootfs from the new PC's system Python and repeat acceptance there.

**RU:** Для совместимости с systemd-сессиями доверенный root-контроллер может начинать в существующей cgroup v2. Перед пробой он перемещает только себя в собственный ограниченный control, после завершения возвращается в исходную группу; чужие процессы и квоты не меняются. Исходный путь проверяется на принадлежность дереву cgroup и запрет собственного рабочего поддерева. Числа, полномочия worker и seccomp не расширяются. В текущем WSL выполнена повторная полная серия; systemd-сценарий покрыт проверкой пути, но ещё не live-испытан.

**EN:** For systemd-session compatibility the trusted root controller may originate in an existing cgroup v2 scope. Before a probe it moves only itself into its bounded control group and returns afterward; foreign processes and quotas remain unchanged. Validate the origin inside the cgroup tree and outside the private working subtree. Worker numbers, permissions and seccomp do not expand. The full suite was repeated in the current WSL; systemd origin parsing is tested, but not live-verified there.

## Альтернативы / Alternatives

**RU:** Отложить весь интерфейс до поколений; публиковать облачный сайт; использовать копии демонстрационных данных. Отклонены по запросу раннего локального наблюдения. Облачная публикация не даёт прямого доступа к метрикам этого WSL.

**EN:** Defer the entire UI until generations, publish a cloud site, or use demonstration data. Reject these for the requested early local observation. Cloud publication cannot directly read this WSL's measurements.

## Последствия / Consequences

**RU:** P6-01 и P6-03 реализуются для лаборатории W0; граф клеток/генома, поколения и воспроизведение остаются отдельными задачами. Новый ПК требует предпосылок WSL2/Python и своей приёмки; чистая установка на втором устройстве пока не проверена. [RU](../docs/ru/17-laboratory-dashboard.md), [EN](../docs/en/17-laboratory-dashboard.md).

**EN:** Implement P6-01 and P6-03 for the W0 laboratory; cell/genome graphs, generations and replay remain separate work. A new PC needs WSL2/Python prerequisites and local acceptance; a clean installation on a second device is not verified yet. [RU](../docs/ru/17-laboratory-dashboard.md), [EN](../docs/en/17-laboratory-dashboard.md).

**Уточнение / Update:** [ADR-012](012-bounded-custom-text-experiments.md) по запросу пользователя добавляет одну ограниченную команду опыта с текстом; наблюдение остаётся чтением / adds one bounded text-experiment action at user request; observation remains read-only.
