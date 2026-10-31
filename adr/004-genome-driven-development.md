# ADR-004 — Развитие из генома / Genome-Driven Development

**Дата / Date:** 2026-10-31.

**Статус / Status:** принятое уточнение модели по замечанию пользователя; реализация впереди / accepted model clarification following user feedback; implementation pending.

## Контекст / Context

**RU:** Цепочка «поступление → пищеварение → проверка → усвоение → хранение → использование» описывает функции уже сформированных органов. В ADR-003 не был достаточно явно задан предшествующий процесс развития. Нельзя встроить готовые органы в среду, назвать их биодвижком и объявить, что организм развился.

**EN:** The sequence “intake → digestion → validation → assimilation → storage → use” describes functions of already formed organs. ADR-003 did not explicitly establish the preceding developmental process. Prebuilt organs embedded in the runtime cannot be presented as an organism having developed.

## Решение / Decision

**RU:** Различить среду исполнения/развития и состояние конкретного организма. Среда предоставляет реализации примитивов, ресурсы, исполнение правил сборки и проверку контрактов. Геном описывает начальное состояние, доступные механизмы и правила/ограничения развития. Онтогенетический цикл по геному и текущим условиям создаёт и изменяет механизмы, клеточные экземпляры и их связи; функционально согласованные группы могут образовать органы. Точный язык правил развития ещё нужно определить.

**EN:** Distinguish the execution/development environment from a particular organism's state. The environment supplies primitive implementations, resources, assembly-rule execution and contract checking. The genome describes initial state, available mechanisms and developmental rules/constraints. An ontogenetic cycle uses the genome and current conditions to create and change mechanisms, cell instances and connections; functionally coordinated groups may form organs. The developmental-rule language remains to be defined.

**RU:** Функциональные способности подтверждаются работой полученной структуры. Регистрировать происхождение «ген/правило → изменение структуры → выполненная функция». Изменение возраста, имени стадии или флага «орган готов» не заменяет этого следа. Развёртывание предписанной структуры само по себе не доказывает обучение; приобретение новой композиции требует отдельного сравнения до/после и проверки на новых входах.

**EN:** Functional capabilities are established through the resulting structure's work. Record “gene/rule → structural change → performed function” provenance. Age increments, stage names or an “organ ready” flag cannot replace this trace. Unfolding a prescribed structure alone does not demonstrate learning; acquiring a new composition needs separate before/after comparison and checks on new inputs.

## Альтернативы / Alternatives

**RU:** Жёстко заданный конвейер органов; переключение готовых функций по счётчику зрелости; один готовый решатель под именем примитива. Они могут служить контрольными реализациями, но не доказательством развития из генома.

**EN:** A hard-coded organ pipeline, unlocking prebuilt functions through maturity counters, or one complete solver named a primitive. These may serve as controls, but not as evidence of genome-driven development.

## Последствия и проверка / Consequences and Verification

**RU:** Перед приёмкой пищеварительного цикла P1-16 реализовать развёртывание генома P1-17 и онтогенетический цикл P1-18. Показать ограниченное начальное состояние, реальные изменения структуры и появление проверяемой функции; при том же исполнителе изменения генома должны отражаться в структуре и поведении согласно контрактам. Наследуемый геном не переписывается локально; его эволюционные изменения остаются под Genesis. Внешние агенты не требуются. ADR-001/002 сохраняются; ADR-003 уточняется порядком развития.

**EN:** Before digestive-cycle acceptance P1-16, implement genome unfolding P1-17 and an ontogenetic cycle P1-18. Show limited initial state, actual structural changes and a verifiable function becoming available; with the same executor, genome changes must affect structure and behavior according to contracts. Local development does not rewrite the heritable genome; its evolutionary changes remain under Genesis. External agents are not required. Preserve ADR-001/002 and clarify ADR-003's developmental order.

**Модель / Model:** [RU](../docs/ru/11-bioengine-and-applications.md), [EN](../docs/en/11-bioengine-and-applications.md). **Задачи / Tasks:** [P1](../planning/phase-1.md).
