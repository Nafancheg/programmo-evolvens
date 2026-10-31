# Фаза 3 — Память и обучение / Phase 3 — Memory and Learning

[Roadmap](../ROADMAP.md) · **Status:** planned

**Мотивация / Motivation:** [RU](../docs/ru/12-motivation-and-reinforcement.md), [EN](../docs/en/12-motivation-and-reinforcement.md). Однократное подкрепление подтверждённых достижений и регуляция поиска пока только предложены / One-time reinforcement of verified achievements and search regulation remain a proposed design. Приоритет P1-17/18 сохраняется / P1-17/18 remain the priority.

| ID | To-do RU / EN | Status | Зависимость и результат / Dependency and evidence |
| --- | --- | --- | --- |
| P3-01 | Память опыта, происхождение и актуальность / Experience memory, provenance and expiry | todo | P1-14 даёт базовое долговременное усвоение; здесь обобщение, актуальность и применимость / P1-14 supplies basic durable assimilation; add generalization, expiry and applicability here |
| P3-02 | Обновление политики в разрешённых пределах / Bounded policy updates | todo | P3-01, P0-03; без изменения генома / no genome rewrite |
| P3-03 | Проверка качества, контрольные состояния и откат / Quality checks, checkpoints and rollback | todo | P3-02; неудачные адаптации / unsuccessful adaptations |
| P3-04 | E1: отложенные задачи, замороженная/перемешанная история / E1: held-out tasks, frozen/shuffled-history controls | todo | P1-05, P3-03; интервалы и регрессии / intervals and regressions |
| P3-05 | Разрешённая структурная адаптация / Permitted structural adaptation | todo | P2-05, P3-03; граница поколения / generation boundary |
| P3-06 | Долговременная история достижений и однократная выдача подкрепления / Durable achievement history and one-time reinforcement issuance | todo | P0-10, P1-14; перезапуск/откат не дают повторную награду / restart/rollback must not create repeat rewards |
| P3-07 | Развиваемый по геному мотивационный контур / Genome-developed motivational controller | todo | P1-18, P3-02/06; удовлетворение, неудовлетворённость и ограниченное напряжение меняют выбор действий / satisfaction, dissatisfaction and bounded tension affect action selection |
| P3-08 | Проверить повторы, ложную новизну, отсутствие прогресса и сохранение полезной работы / Test repeats, false novelty, absent progress and useful-work preservation | todo | P3-03/07; шум, переименование, откат, ухудшение/восстановление, пауза, исчерпание бюджета / noise, renaming, rollback, degrade/restore, idle and exhausted budgets |

**Критерий / Exit:** RU — воспроизводимый выигрыш на отложенных задачах и надёжный откат; EN — reproducible held-out improvement and reliable rollback. Рост памяти не доказывает обучение / Memory growth does not prove learning.
