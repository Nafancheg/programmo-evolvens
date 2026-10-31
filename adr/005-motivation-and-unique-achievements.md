# ADR-005 — Мотивация и однократные достижения / Motivation and One-Time Achievements

**Дата / Date:** 2026-10-31.

**Статус / Status:** принципы зафиксированы по предложению пользователя; механизм и параметры требуют разработки / principles recorded following user proposal; mechanism and parameters require development.

## Контекст / Context

**RU:** Пользователь предлагает положительное подкрепление за достижения, запрещает повторную награду за достигнутое и предлагает отрицательную реакцию на такие попытки. Отсутствие новых подкреплений должно мотивировать поиск. Не использовать название «боль».

**EN:** The user proposes positive reinforcement for achievements, prohibits rewarding the same achievement again, and proposes a negative response to repeat attempts. Absence of new reinforcement should motivate search. Avoid the term “pain.”

## Решение / Decision

**RU:** Спроектировать сигналы удовлетворения, неудовлетворённости и напряжения поиска. Вознаграждать новую подтверждённую способность/уровень один раз по смысловому ключу в долговременном журнале. Повторную заявку не награждать и сопровождать отрицательным сигналом. Обычное использование освоенной способности не является такой заявкой и не штрафуется. Предлагаемое напряжение ограничено активным допустимым поиском; простой и исчерпанный бюджет не должны создавать бесконечное воздействие.

**EN:** Design satisfaction, dissatisfaction and search-tension signals. Reward a newly verified capability/level once using a semantic key in a durable ledger. Deny repeat claims and produce a negative signal. Ordinary use of an established capability is not such a claim and is not penalized. Proposed tension is bounded to active permitted search; idle periods and exhausted budgets must not produce endless pressure.

**RU:** Проверку результата и историю наград защитить от изменения кандидатом. Перезапуск, откат, переименование или восстановление уже достигнутого не создают новизну. Подкрепление не заменяет полезную работу и не является вычислительной энергией. Реакции должны влиять на выбор действий; точные коэффициенты и правила восстановления остаются открытыми. По ADR-004 сложный контур формируется из генома. Субъективные эмоции не утверждаются.

**EN:** Protect outcome verification and reward history from candidate changes. Restart, rollback, renaming or restoring prior achievement do not create novelty. Reinforcement neither replaces useful work nor constitutes compute energy. Reactions must affect action selection; exact weights and recovery rules remain open. Under ADR-004, the complex controller develops from the genome. Subjective emotions are not claimed.

## Альтернативы / Alternatives

**RU:** Награда за каждый повтор; штраф за любое применение знакомого навыка; произвольная новизна как достаточный успех; неограниченное недовольство при отсутствии задач. Эти правила не принимаются: они расходятся с однократностью достижения или сохранением полезной работы.

**EN:** Reward every repetition; penalize any familiar-skill use; treat arbitrary novelty as sufficient success; grow dissatisfaction without bounds when no tasks exist. These rules are not adopted because they conflict with one-time achievement or useful-work preservation.

## Последствия и проверка / Consequences and Verification

**RU:** Нужны контракты достижений, долговременный журнал, формируемый по геному регулятор и проверки обходов/повторной выдачи. Ближайшая работа по развитию из генома сохраняется; контур ещё не реализован. Подробности: [RU](../docs/ru/12-motivation-and-reinforcement.md), [задачи P3](../planning/phase-3.md).

**EN:** Requires achievement contracts, a durable ledger, a genome-developed regulator and tests for bypasses/duplicate issuance. Current genome-development work remains the priority; the controller is unimplemented. Details: [EN](../docs/en/12-motivation-and-reinforcement.md), [P3 tasks](../planning/phase-3.md).
