# W0 — Виртуальный мир / Virtual World

[Roadmap](../ROADMAP.md) · **Status:** in_progress — первый WSL2 backend подготовлен, не установлен и не принят / first WSL2 backend prepared, not installed or accepted. [RU](../docs/ru/14-wsl2-backend.md) · [EN](../docs/en/14-wsl2-backend.md).

**RU:** Инфраструктурная фаза перед исполнением развивающегося организма. Мир спроектирован людьми и ограничивает организм снаружи; не эволюционирует вместе с ним. Контракты генома и клетки можно разрабатывать параллельно. P2-02 перенесена сюда с сохранением ID; новые P2-06…09 продолжают исходную группу инфраструктурных задач.

**EN:** Infrastructure phase before a developing organism executes. Humans engineer the world, which externally bounds the organism and does not co-evolve with it. Genome/cell contracts may be designed concurrently. P2-02 moved here with its ID preserved; P2-06…09 continue the original infrastructure task group.

| ID | To-do RU / EN | Status | Зависимость и результат / Dependency and evidence |
| --- | --- | --- | --- |
| P2-02 | Внешняя изоляция, общие квоты и жёсткие тайм-ауты / External isolation, aggregate quotas and hard deadlines | in_progress | [Профиль](../world/wsl2/policy.json), slices и service-план подготовлены; фактическое применение не проверено / profile, slices and service plan prepared; live enforcement unverified |
| P2-06 | Выбрать и собрать исполнитель мира с фиксированной политикой / Select and build the world executor with fixed policy | in_progress | [ADR-007](../adr/007-wsl2-laboratory-backend.md), [код](../world/wsl2/controller.py); установка/полный запуск впереди / installation/full execution pending |
| P2-07 | Ограниченные каналы входа/выхода и закрытые по умолчанию доступы / Bounded I/O channels and default-deny permissions | in_progress | JSONL/лимиты/закрытый rootfs-план; только фиксированная проба, реальная граница ещё не проверена / JSONL/limits/closed-rootfs plan; fixed probe only, live boundary unverified |
| P2-08 | Внешний надзор, остановка всего исполнения и восстановление / External supervision, whole-execution stopping and recovery | in_progress | Контроллер, тайм-ауты, BindsTo и остановка подготовлены; отказы systemd/bwrap не испытаны / controller, deadlines, BindsTo and stop prepared; live failure tests pending |
| P2-09 | Приёмка границ мира до запуска развивающихся вариантов / Accept world boundaries before developing candidates run | todo | P2-02/07/08; превышения ресурсов, запрещённый доступ, зависание, дочерние процессы, параллельные миры / resource exhaustion, denied access, hangs, descendants and concurrent worlds |
| P2-10 | Определить семантический протокол наблюдений, действий и переходов мира / Define semantic observation/action/transition protocol | todo | Интерфейс среды отдельно от транспорта и фенотипа; минимальная схема до первого организма / environment interface distinct from transport and phenotype; minimal schema before first organism |
| P2-11 | Генератор ниш/задач и правила истощаемых ресурсов/опасностей / Niche/task generator and depletable-resource/hazard rules | deferred | После W0 и базового онтогенеза; экземпляры внутри фиксированных границ, критерии версионированы / after W0 and basic ontogenesis; instances within fixed boundaries, versioned criteria |

**Критерий / Exit:** внешние ограничения фактически действуют; у компьютера остаётся измеренный резерв; нарушение/отказ приводит к ограниченному завершению; разрешённые операции работают / external limits actually hold, the host retains measured reserve, violations/failure lead to bounded shutdown, authorized work succeeds. [RU](../docs/ru/13-virtual-world.md) · [EN](../docs/en/13-virtual-world.md).

**Проверено 2026-11-01 / Checked:** 33 модульных теста Windows/WSL, синтаксис установочных скриптов, сборка BPF и ожидаемый отказ preflight / 33 Windows/WSL unit tests, installer syntax, BPF construction and expected preflight refusal. Это не приёмка W0 / This is not W0 acceptance. Изменения общей WSL-конфигурации и перезапуск согласуются отдельно / Shared WSL configuration changes and restart require separate agreement.
