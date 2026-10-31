# План экспериментов / Experiment Plan

**RU:** Сохранённый план исследований. По [ADR-003](../adr/003-bioengine-first.md) текущий приоритет — создание и инженерная приёмка [первого биодвижка](../docs/ru/11-bioengine-and-applications.md), P1-12…16. Завершение общего исследования композиционности и параллельного исполнителя не блокирует этот срез. Научные гипотезы не удаляются и не считаются подтверждёнными.

**EN:** Preserved research plan. Under [ADR-003](../adr/003-bioengine-first.md), the priority is construction and engineering acceptance of the [first bioengine](../docs/en/11-bioengine-and-applications.md), P1-12…16. Completing the general compositionality study and parallel executor does not block this slice. Scientific hypotheses remain recorded and unproven.

## E0 — Baseline
**RU:** Реальный последовательный/параллельный исполнитель набора задач. Тесты корректности, замеры задержки и ресурсов.  
**EN:** Real sequential/parallel task executor with correctness tests, latency and resource measurements.

**RU — состояние 2026-10-31:** появился [последовательный прототип](../docs/ru/09-first-prototype.md): три генома, 14 открытых входов, эталонные функции и журнал времени. Это предварительные проверки, не завершённый E0: сравнение производительности/ресурсов, параллельный исполнитель и полный протокол остаются в [to-do фазы 1](../planning/phase-1.md). Проверка композиционности проводится отдельно после E0 по [протоколу генома](../docs/ru/03-genome-and-heredity.md).

**EN — status 2026-10-31:** a [sequential prototype](../docs/en/09-first-prototype.md) provides three genomes, 14 public inputs, reference functions and timing traces. These are preliminary checks, not completed E0: performance/resource comparison, a parallel executor and the full protocol remain in [phase 1 to-dos](../planning/phase-1.md). Compositionality is evaluated separately after E0 under the [genome protocol](../docs/en/03-genome-and-heredity.md).

## E1 — Learning
**RU:** Выбор стратегии по истории выполненных заданий; сравнение до/после и с фиксированной политикой.  
**EN:** Strategy selection informed by outcome history; compare pre/post learning and frozen policy.

## E2 — Immunity and homeostasis
**RU:** Инъекции отказов, регуляция нагрузки, изоляция клеток, измерение восстановления.  
**EN:** Fault injection, load regulation, cell isolation and recovery measurement.

## E3 — Genesis assessment
**RU:** Закрытые испытания, подтверждение функционального разрыва, протокол решения и возможный отказ.  
**EN:** Held-out assessments, capability-gap evidence, decision record and possible rejection.

## E4 — Generation comparison
**RU:** Новая композиция компонентов, наследование подтверждённых политик, тестирование против родителя.  
**EN:** New component composition, inheritance of validated policies, evaluation versus parent.

## E5 — Genesis competence upgrade
**RU:** Новые оценочные сценарии и сравнение двух версий Genesis под внешним протоколом.  
**EN:** New assessment cases and comparison of two Genesis versions under external protocol.

**RU:** Последовательность исследовательских сравнений начинается с E0; последующие эксперименты не считаются реализованными. Создание и приёмка первого ядра идут по ADR-003 и текущему плану разработки.

**EN:** The research-comparison sequence starts at E0; subsequent experiments are not implemented yet. Build and accept the first core under ADR-003 and the current implementation plan.
