# Идеи: text conditioning / structured prompts / VLM embedder

Стиль как в вашем примере: **Проблема → контекст → барьер → мотивация из наблюдений → Цель → направления**.

---

## Проблема 1: Победы structured prompts смешаны с лишней информацией

Context Scaling (Seed, `2607.29679`) — сейчас главный текст про scaling text conditioning. Авторы показывают, что длина NL не масштабирует diffusion loss, а image-grounded информация (GPG/ED) — масштабирует. На этом основании они вводят structured prompts (JSON со слотами intent / scene / elements / bbox / depth / …), учат diffuser на SP и LLM-prompter user→SP, и получают сильный end-to-end результат. Matched NL control на том же Qwen-Image, данных и бюджетах заметно слабее SP — и из этого делают вывод, что дело в structured interface, а не просто в «дольше учили».

Однако контроль у них честный по **compute и архитектуре**, но нечестный по **содержимому caption’а**. Dense NL даже на длинной ступени сидит на ED ≈ 0.75 и GPG ≈ 112, а Structured L10 — на ED ≈ 0.83 и GPG ≈ 210. То есть SP не только «организует», он ещё и **несёт больше деталей**. FIBO делает похожий ход: long JSON против short captions. Примеры с project page (living room schema.json, pineapple PE) это же подтверждают глазами: в SP либо denser dump с фото, либо явное дозаполнение сцены.

Получается практический барьер для нас: если мы сейчас заложим следующий **VLM-эмбеддер** под JSON только потому что «Seed сказал SP ≫ NL», мы можем оптимизировать не ту ось. Нужно понять, что важнее — **структура** или **coverage фактов**.

Одна из мотиваций — прямо их Figure 3 / Appendix F.3: NL-лестница сохраняет те же entities и наращивает длину elaboration’ом, при этом reconstruction плоская; SP-лестница восстанавливает поля и растёт. Но это сравнивает «воду» с «новыми полями», а не две упаковки одного и того же набора фактов.

**Цель.** Построить честный эксперимент NL ↔ SP при **выровненной realized information** (matched attribute set / ED/GPG в допуске) и получить вердикт: даёт ли организация в schema выигрыш сама по себе — и какой IR тогда класть в дальнейший VLM conditioner.

1. **Info-matched verbalizer.** Из одного evidence bundle (VLM + boxes/depth) собрать SP-full и NL, который обязан покрыть тот же inventory атрибутов; hard filter / retry, пока ED(NL) не войдёт в коридор ED(SP).
2. **Controls на две стороны confound’а.** NL-water (те же факты, больше слов) и SP-sparse (те же факты, меньше organization) — чтобы отделить verbosity от structure.
3. **Один backbone, matched train budget.** LoRA/continued FT одного DiT на каждом arm; readout: train loss + GenEval2/DPG + reconstruction probe. Вывод — рекомендация для embedder: schema-aware vs dense prose.

---

## Проблема 2: Непонятно, какой post-training prompter’а реально нужен

В том же Context Scaling качество на inference упирается не только в формат, но и в **promptability**: LLM должен из короткого user prompt собрать полный IR, на котором учили diffuser. Авторы поднимают это через SFT → cold-start → verifier-gated OPSD и опциональный agentic loop. Table 4 показывает, что SFT даёт главный скачок structure; OPSD сильнее GRPO; Table 5 — что Base даже за 8 rounds loop не догоняет Trained за 1 shot, а loop быстро saturates.

Однако это всё ещё **одна лаборатория, один schema, одна cost-неявная ось**. Рядом PromptEnhancer, APE и продуктовые PE рассказывают другие истории про RFT и multi-agent, но без общего ответа: *надо ли task-specific учить prompter вообще*, если уже есть огромный frozen LLM, и *какой этап покупает сколько качества за сколько GPU-h / latency*.

Практический барьер: post-training 397B-класса и verifier loops дорогие. Без ROI-карты легко потратить месяцы на RL, хотя хватило бы SFT — или наоборот, остановиться на zero-shot и недобрать composition.

Мотивация из их же цифр: DPG почти не двигается по стадиям (~+1.3), а structure/GSB — сильно. Значит разные метрики по-разному чувствуют обучение; без cost-normalized сравнения легко «улучшить не то».

**Цель.** На фиксированном diffuser и фиксированном IR снять карту достаточности обучения promptability: zero-shot → SFT → distillation/RL → test-time loop — и понять минимальный рецепт, который стоит своих денег.

1. **Factorial по стадиям при matched evaluation.** Один harness, eval vs original user prompt, одни судьи; кумулятивно добавлять SFT / cold-start / RL.
2. **Cost-normalized Pareto.** Ось качества (structure, GenEval2, GSB) против GPU-h обучения и против latency на inference (включая loop rounds).
3. **Sufficiency test.** При каком масштабе frozen LLM (если доступен) zero-shot/CoT уже достаточен, а task-FT даёт убывающую отдачу — чтобы не абсолютизировать рецепт Seed.

---

## Проблема 3: SOTA смешивает потолок формата и потолок prompter’а

Seed вводит полезную формулу: качество ≈ **Diffusability × Promptability**. Diffusability — насколько формат/annotation отдаёт информацию diffuser’у; Promptability — насколько LLM умеет этот формат заполнить с user prompt. Дальше они улучшают оба рычага и репортят сумму.

Однако из end-to-end таблицы нельзя понять, **куда упирается система**. Если D-oracle (идеальный IR с картинки) уже почти не лучше реального prompter’а — надо долбить формат/annotate. Если D-oracle далеко впереди — надо долбить user→IR. Сейчас labs двигают оба и спорят «наш SP» vs «наш RFT», сравнивая несопоставимые суммы.

Барьер для знания: без разделённых потолков нельзя решать, куда вкладывать следующий доллар research/compute, и нельзя честно читать чужие SOTA.

Мотивация: у Seed diffuser fixed в prompter ablations (это правильно для promptability), но полного oracle-decomposition на generation metrics с image-conditioned IR vs user-only IR как стандарта нет. В нашем аудите это N01 — OPEN.

**Цель.** Построить измерительный протокол с двумя оракулами на одном backbone и публиковать gaps, а не только absolute scores.

1. **D-oracle.** Кормить DiT IR, собранным с reference image (верх diffusability+annotation).
2. **P-oracle / P-ceiling.** Лучший IR, достижимый без image leak (сильный prompter, human fill schema, ensemble) — потолок promptability.
3. **Gap tables.** `D-oracle − real`, `P-ceiling − zero-shot`, плюс стык с Проблемой 1: `D-oracle(SP) − D-oracle(NL-matched)` как чистый format gap.

---

## Проблема 4: Неизвестно, в каком звене цепочки умирает conditioning-сигнал

Даже если structured captions «работают», сообщество спорит, *почему*. Seed говорит про organization полей. Split-Text Conditioning и длинные encoder’ы — про comprehension defect / softmax competition / positional bias в text encoder. SoftREPA — про soft tokens без текстового rewrite. Каждый чинит своё звено и показывает локальный выигрыш.

Цепочка на самом деле такая:

```
annotate факты → serialize (NL/JSON) → tokenize / VLM encode → DiT cross-attn
```

Барьер: без **локализации bottleneck** на одной и той же пачке фактов мы не знаем, что проектировать в следующем VLM-эмбеддере — schema compiler, другой tokenizer, другой encoder, или непрерывный bridge мимо текста.

Мотивация для нас прямая: Ideя 1 скажет, важен ли serialize; Ideя 4 должна сказать, не убивает ли всё уже **encoder**, даже при честных фактах. Иначе можно год полировать JSON зря.

**Цель.** Сделать causal audit одной цепочки: вмешательства по звеньям при фиксированном fact package и карта чувствительности «где падает качество».

1. **Coverage knock-out.** Дропать атрибуты/объекты в annotate — baseline чувствительности к info.
2. **Serialize swap.** Те же факты: JSON ↔ matched prose; key-order shuffle; synonym keys — brittleness представления.
3. **Encoder / DiT swap и soft bridge.** Менять text encoder при fixed DiT (и наоборот); опционально continuous conditioning вместо discrete IR — чтобы увидеть, нужен ли текст как API вообще.

---

## Проблема 5: При конечном бюджете токенов непонятно, какие факты класть

Современный стек почти всегда учится на re-prompt / dense caption. Значит на inference и train conditioning — это не «включить PE или нет», а **борьба за бюджет**: контекст VLM/encoder, attention, FLOPs. Seed в field ablation на BAGEL показал, что scene context важнее depth/relationships по вкладу в loss. Но это снятие целых групп с полного L10, а не ответ на вопрос: *при лимите 256 / 512 / 1024 токенов что класть первым — объекты, атрибуты, геометрию, свет, relations?*

Барьер: captioner’ы и schema design сейчас эвристические («больше полей = лучше»). Для VLM embedder нужен packing recipe: marginal gain типа факта под лимитом.

Мотивация: GPG/ED растут от полезной структуры, но encoder’ы страдают от плотного мусора и конкуренции токенов. Field ablation ≠ budgeted allocation. Long-prompt papers не говорят, что выкидывать первым.

**Цель.** Получить Pareto quality vs token budget для разных политик заполнения conditioning и закон marginal value типов visual facts.

1. **Budgeted packs из одного L10.** При фиксированном N токенов политики: objects-first / attributes-first / geometry-first / style-first / balanced.
2. **Matched train или frozen probe.** Смотреть loss и gen metrics как функцию политики × бюджета.
3. **Связка с Проблемой 1.** Повторить allocation и в NL-matched, и в SP — чтобы packing recipe не был артефактом JSON.

---

## Что брать первым

**Проблема 1** — первая: пока не снят confound structure/coverage, нельзя честно проектировать VLM embedder и нельзя правильно читать seed-like SOTA.

Дальше логичная очередь: **4** (где чинить стек) → **3** (куда headroom) → **5** (как паковать) → **2** (как учить prompter уже под выбранный IR).

---

## План проверки Проблем 1 (минимум)

**Нарратив статьи.** Все бегут в structured captions после Context Scaling / FIBO. Но победа SP смешана с тем, что в JSON просто больше деталей. Мы выравниваем факты, сравниваем упаковки и отвечаем: учить следующий conditioner на schema или на dense prose. Оба исхода — знание.

**Сетап.** Один open DiT (Qwen-Image LoRA/FT или SD3.5) + его text encoder. 50k–200k images → evidence → arms: SP-full, NL-matched (hard ED/attribute gate), NL-water, SP-sparse. Метрики: train MSE, open ED/GPG, GenEval2/DPG subset, reconstruction probe.

**Бейзлайны.** Unmatched SP vs short NL (реплика confound’а); matched-train NL без info-gate (как Seed); official short prompt.

**Код.** DiffSynth / FlyMyAI LoRA; свой verbalizer+filter; куски evalkit Seed; публичные GenEval/DPG.

**Ожидание.** NL-water ≈ NL-matched. Unmatched SP ≫ short NL. Главный fork: SP-full vs NL-matched либо сохраняет gap (**structure real**), либо схлопывается (**info был confound**).

**Sanity.** ED(NL-matched)≈ED(SP); shuffle attributes → падение; JSON-ключи без values → слабо.

**Успех.** Стабильный info-match + чёткий исход A/B + рекомендация для embedder.  
**Провал / пивот.** Не удаётся свести ED в fluent NL → уходим в Проблему 4 (возможно bottleneck в serialize/encoder) или 3 (oracles на SP-only мире).
