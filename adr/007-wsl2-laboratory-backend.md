# ADR-007 — Первый backend W0 на WSL2 / First WSL2 W0 Backend

**Дата / Date:** 2026-11-01.

**Статус / Status:** выбран для подготовки и проверки; W0 не принят / selected for preparation and evaluation; W0 not accepted.

## Контекст / Context

**RU:** Пользователь предложил WSL2 + systemd/cgroups + bubblewrap/seccomp, heartbeat и внешний JSONL-журнал. Дополнительно нужны семантика наблюдений/действий, правила ресурсов и контракт Genesis. Текущий дистрибутив запускает Docker при загрузке, systemd отключён; менять общие настройки без согласования нельзя.

**EN:** The user proposed WSL2 + systemd/cgroups + bubblewrap/seccomp, heartbeat and an external JSONL journal. Observation/action semantics, resource rules and a Genesis contract are also needed. The existing distro starts Docker at boot and has systemd disabled; shared settings require separate agreement before changing them.

## Решение / Decision

**RU:** Подготовить первый лабораторный backend для отдельного дистрибутива. Использовать общий worker slice и transient service на запуск: 256 MiB, одно ядро CPU, 64 задачи, 256 дескрипторов, RuntimeMaxSec=70s; внешняя проверка heartbeat 5 секунд. Контроллер имеет отдельный ограниченный slice; worker связан с его жизненным циклом. Окружение и capabilities очищаются, rootfs read-only, записываемые tmpfs ограничены, сеть/Windows interop и host mounts недоступны организму.

**EN:** Prepare a first laboratory backend for a separate distro. Use an aggregate worker slice and a transient service per run: 256 MiB, one CPU core, 64 tasks, 256 descriptors, RuntimeMaxSec=70s; externally check heartbeat over five seconds. Bound the controller separately and bind worker lifetime to it. Clear environment/capabilities, mount a read-only rootfs and bounded tmpfs, and keep network/Windows interop/host mounts unavailable to the organism.

**RU:** BPF-файл открывается внутри worker; FD не предполагается наследуемым от контроллера через systemd. Для первой подготовки разрешена только фиксированная доверенная smoke-проба. Журнал, output budget и лимит числа архивов внешние. Preflight и smoke не снимают запрет исполнения развивающихся кандидатов до полного P2-09. Общие `.wslconfig` и текущий дистрибутив не изменять автоматически.

**EN:** Open BPF inside the worker; do not assume the controller FD survives systemd. Initially admit only a fixed trusted smoke probe. Keep journals, output budgets and archive-count limits external. Preflight/smoke do not admit developing candidates before full P2-09 acceptance. Do not automatically alter shared `.wslconfig` or the existing distro.

**RU:** Семантические правила мира отделены от защитного периметра. Генератор создаёт экземпляры внутри фиксированных правил, не меняет защиту и критерии задним числом. Наблюдения/действия — интерфейс мира; фенотип — организация/поведение организма. Научная уникальность генератора и Genesis-контракта не установлена.

**EN:** Separate world semantics from containment. A generator produces instances within fixed rules rather than changing protection or criteria retroactively. Observations/actions are the world interface; phenotype is organism organization/behavior. Generator/Genesis-contract scientific uniqueness is not established.

## Альтернативы / Alternatives

**RU:** Отдельная полноценная VM остаётся вариантом более сильной границы. WSL2 не считается изоляцией от произвольной атаки на общее Linux-ядро. Scope вместо service возможен при другом контроллере, который самостоятельно задаёт ограничения исполнения; здесь выбран service. Произвольные готовые парсеры/агенты не заменяют развитие организма.

**EN:** A dedicated full VM remains an option for a stronger boundary. WSL2 is not presented as isolation against arbitrary attacks on its shared Linux kernel. Scopes could work with a different launcher enforcing execution limits; this implementation chooses services. Prebuilt parsers/agents do not replace organism development.

## Последствия и проверка / Consequences and Verification

**RU:** Подготовлены код, конфигурация, сборщики rootfs/BPF и установочные действия. 33 модульные проверки прошли на Windows и WSL; BPF собран без загрузки в организм; preflight отказал в текущем окружении. Установка, реальный systemd/bwrap-запуск и граничные испытания впереди. Полное описание: [RU](../docs/ru/14-wsl2-backend.md), [W0](../planning/world.md).

**EN:** Code, configuration, rootfs/BPF builders and installation actions are prepared. 33 unit checks passed on Windows/WSL; BPF was built without loading it into an organism; preflight refused the current environment. Installation, actual systemd/bwrap execution and boundary tests remain pending. Details: [EN](../docs/en/14-wsl2-backend.md), [W0](../planning/world.md).
