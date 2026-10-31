# ADR-006 — Сначала ограниченный мир / Bounded World First

**Дата / Date:** 2026-10-31.

**Статус / Status:** принятое требование пользователя; реализация и проверка впереди / accepted user requirement; implementation and verification pending.

## Контекст / Context

**RU:** Организм не должен повреждать компьютер, исчерпывать память, занимать весь CPU или получать произвольные доступы. Пользователь требует заранее спроектированный виртуальный мир. Ранее процессную изоляцию допускалось отложить; для запуска развивающихся вариантов это решение пересматривается.

**EN:** The organism must not damage the host, exhaust memory, monopolize CPU or gain arbitrary access. The user requires an engineered virtual world before execution. Earlier plans allowed deferring process isolation; revise that order for developing candidates.

## Решение / Decision

**RU:** Ввести инфраструктурную фазу W0 перед исполнением развивающихся организмов. Мир задаётся разработчиками, отдельно от генома и развития. Внешний контроллер и ОС/гипервизор обеспечивают общие квоты, доступы, пределы времени и принудительную остановку. Организм и Genesis не могут менять эти границы. Файлы/сеть/устройства закрыты по умолчанию; ввод и вывод идут по ограниченным каналам. Ресурсы нескольких миров и служебных компонентов учитываются суммарно.

**EN:** Add infrastructure phase W0 before developing organisms execute. Developers define the world separately from the genome and development. An external controller and OS/hypervisor enforce aggregate quotas, permissions, deadlines and forced stopping. The organism and Genesis cannot change those boundaries. Files/network/devices are denied by default; input/output uses bounded channels. Account for multiple worlds and service components in aggregate.

**RU:** Конкретная технология и числа ещё не выбраны; первым кандидатом является отдельная VM с собственным диском и внешними ограничениями. Нет обязательного контроля — нет запуска. Проектирование контрактов может продолжаться параллельно W0. Нынешний скалярный прототип не считается защитной средой.

**EN:** Technology and numeric limits are undecided; the first candidate is a dedicated VM with its own disk and external limits. Missing mandatory enforcement means no execution. Contract design may progress alongside W0. The current scalar prototype is not a protective execution environment.

## Альтернативы / Alternatives

**RU:** Добровольное соблюдение лимитов организмом; отдельная папка; только таймер/исключение Python; контейнер без проверенных ограничений. Не принимаются как достаточная граница. Изоляция отдельных клеток внутри принятого мира может развиваться позднее, но внешняя защита компьютера требуется первой.

**EN:** Voluntary organism compliance, a separate folder, only a Python timer/exception, or a container without verified limits are insufficient boundaries. Cell-level isolation inside an accepted world may develop later; external host protection comes first.

## Последствия и проверка / Consequences and Verification

**RU:** P2-02 переносится в W0 с сохранением ID; новые задачи P2-06…09 описывают исполнитель, каналы, надзор и приёмку. P1-17/18 и автономный подбор запускаются после P2-09. Проверки выполняются на одноразовых данных внутри тестовой границы, не разрушительными командами на компьютере. Политика версионируется разработчиком и не эволюционирует автоматически. [Спецификация RU](../docs/ru/13-virtual-world.md), [план W0](../planning/world.md).

**EN:** Move P2-02 into W0 with its ID preserved; P2-06…09 cover the executor, channels, supervision and acceptance. Run P1-17/18 and autonomous search after P2-09. Use disposable data within a test boundary, not destructive host commands. Developers version the policy; it does not evolve automatically. [Specification EN](../docs/en/13-virtual-world.md), [W0 plan](../planning/world.md).

**Уточнение 2026-11-01 / Clarification:** [ADR-007](007-wsl2-laboratory-backend.md) выбирает WSL2/systemd/bwrap/seccomp первым лабораторным backend; границы ADR-006 и обязательная приёмка сохраняются / selects WSL2/systemd/bwrap/seccomp as the first laboratory backend; ADR-006 boundaries and mandatory acceptance remain.
