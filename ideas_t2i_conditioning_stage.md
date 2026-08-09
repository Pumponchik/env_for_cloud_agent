# Идеи для статьи: точки свободы text conditioning в T2I

Переписано ясно. Сначала — **какие ручки вообще существуют**. Потом 5 идей: **две ваши** + **три заново**, за которые стоит хвататься, чтобы принести знание в мир (не ещё один rewriter).

---

## Карта точек свободы (что можно крутить)

Пайплайн современного стека (train on re-prompt / SP):

```
картинка ──annotate──► факты
                              │
user user prompt ──prompter──► conditioning IR ──text encoder / VLM──► DiT ──► image
```

| # | Ручка | Вопрос знания |
|---|--------|----------------|
| A | **Сколько фактов** в conditioning | coverage / info |
| B | **Как упакованы** факты (prose / JSON / layout) | structure ⊥ info |
| C | **Кто пишет** IR с user prompt и как его учат | promptability recipe |
| D | **Где теряется сигнал** (annotate → serialize → encode → attend) | bottleneck |
| E | **Потолки по отдельности**: формат vs prompter | Diffusability × Promptability |
| F | **Бюджет токенов/FLOPs** conditioning: на что тратить | allocation |

Старое «всегда ли PE включать» при train-on-reprompt — слабая ручка; ниже её нет.

---

## Идея 1 (ваша). Честный NL ↔ SP при равной информации

### (1) В чём идея?
В Seed SP побеждает NL, но в SP **заведомо больше деталей** (ED/GPG выше; JSON плотнее).  
Мы делаем сравнение, где **набор фактов одинаковый**, меняется только упаковка: prose vs schema.  
Так отвечаем: для дальнейшего **VLM-эмбеддера** важнее структура или просто coverage.

### (2) Цель
Получить **несмещённый вердикт по формату conditioning**, который можно перенести в дизайн text encoder / VLM conditioner.  
Не «SP круче в их paper», а «при равной информации что есть».

### (3) Мотивация
- Seed Matched NL = matched **train**, не matched **info** (ED NL≈0.75 vs SP L10≈0.83; GPG 112 vs 210).  
- FIBO: long JSON vs **short** captions — тот же confound.  
- Примеры SP (schema_room, pineapple PE) показывают denser dump / дозаполнение.  
Если не выровнять info, весь следующий embedder могут зря заточить под JSON.

### (4) Новизна
Близко: Seed, FIBO, Cosmos.  
**Нет** опубликованного hard info-match (attribute/ED gate) NL↔SP + вывода для conditioner.  
Это не реплика Seed — это снятие их главного confound.

**Знание в мир:** structure effect ⊥ information effect.

---

## Идея 2 (ваша). Как учить prompter: SFT / RL / loop — и надо ли учить

### (1) В чём идея?
Зафиксировать diffuser + IR. Крутить только **способ получить IR из user prompt**:

- frozen LLM zero-shot  
- SFT  
- cold-start / distillation  
- RL (GRPO / OPSD)  
- test-time loop (render→judge→edit)  

Сравнить **качество и цену** (GPU-h, latency, $). Вопрос: что покупает каждый этап.

### (2) Цель
Карта **ROI обучения promptability**: когда хватает большого frozen LLM, когда SFT обязателен, когда RL/loop окупаются.  
Практический выход: минимальный достаточный рецепт под выбранный IR.

### (3) Мотивация
Seed Table 4/5: SFT даёт главный jump; OPSD > GRPO; Base@8 rounds < Trained@1; loop быстро saturates.  
Но это одна lab, один schema, без единой cost-оси. PromptEnhancer/APE — другие reward’ы, другие выводы.  
В мире train-on-reprompt prompter — часть контракта; вопрос «надо ли task-FT» остаётся открытым и дорогим.

### (4) Новизна
Есть внутриpaper ablations. Нет **cost-normalized cross-recipe** карты с eval vs **original** user prompt.  
Знание: не новый rewriter, а закон «какой post-training нужен».

**Знание в мир:** promptability training scaling / sufficiency.

---

## Идея 3 (новая). Разделить потолки: Diffusability vs Promptability oracles

### (1) В чём идея?
Seed назвал `Quality ≈ Diffusability × Promptability`, но почти всегда двигает оба сразу.  
Мы строим **два оракула** на одном backbone:

| Оракул | Что подаём в DiT | Что меряем |
|--------|------------------|------------|
| **D-oracle** | SP/NL с **картинки** (идеальная аннотация) | потолок формата + annotation |
| **P-oracle** | лучший IR, который можно вывести **только из user prompt** (или human-filled schema без image leak) | потолок prompter’а |
| **Real system** | обычный prompter | где мы сейчас |

Gaps:  
`D-oracle − real` = сколько теряем на promptability  
`P-ceiling − zero-shot` = headroom обучения prompter’а  
`D-oracle(SP) − D-oracle(NL-matched)` = чистый format gap (стык с идеей 1)

### (2) Цель
Ответить науке: **куда вкладывать следующий доллар** — в лучший annotate/format (diffusability) или в лучший user→IR (promptability).  
Сейчас labs делают и то и то и репортят сумму.

### (3) Мотивация
Без разделения потолков нельзя интерпретировать SOTA: выиграли форматом или prompter’ом?  
Seed держит diffuser fixed в prompter ablations, но не публикует полный oracle decomposition на gen metrics.  
N01 в нашем аудите — OPEN.

### (4) Новизна
Словарь Seed есть; **измерительный протокол с двумя оракулами и gap-таблицами** — нет как стандарт.  
Отличие от идеи 1: 1 крутит формат при matched info; 3 крутит **источник** IR (image vs user) и показывает headroom.

**Знание в мир:** куда упирается качество — в формат или в перевод user→формат.

---

## Идея 4 (новая). Где умирает сигнал: localize bottleneck в цепочке

### (1) В чём идея?
Даже если SP «лучше», непонятно **какое звено** это объясняет:

```
(1) annotate  →  (2) serialize IR  →  (3) tokenize / VLM encode  →  (4) DiT attend
```

Делаем **causal interventions** на одном датасете/модели:

| Вмешательство | Если качество падает сильно → bottleneck здесь |
|---------------|-----------------------------------------------|
| Те же факты, хуже annotate (дроп атрибутов) | coverage |
| Те же факты, JSON→prose / prose→JSON | serialize / structure |
| Те же токены, shuffle JSON key order / synonym keys | encoder brittleness |
| Заменить text encoder, DiT fixed (или наоборот) | encoder vs DiT |
| Soft/continuous conditioning вместо discrete IR | нужен ли текст вообще |

Цель — не SOTA, а **карта чувствительности** для дизайна следующего VLM embedder.

### (2) Цель
Сказать миру: «не надо оптимизировать JSON schema, если убийца — tokenizer/encoder» (или наоборот).  
Это прямо про вашу следующую задачу (VLM embedder).

### (3) Мотивация
Split-Text Conditioning и длинные encoder’ы намекают на comprehension defect; Seed — на organization; SoftREPA — на soft tokens.  
Все правят **разные** звенья и спорят результатами. Без localization спор вечный.  
Идея 1 отвечает «format vs info»; идея 4 отвечает «format vs encoder vs DiT».

### (4) Новизна
Куски ablations есть везде по отдельности.  
**Сквозной causal audit одной цепочки** с единым fact package — не видели как paper.  
Это systems-science, не новый loss.

**Знание в мир:** в каком модуле лежит text-conditioning gap.

---

## Идея 5 (новая). Бюджет conditioning: на что тратить токены

### (1) В чём идея?
VLM/text encoder имеет **конечный бюджет** (контекст, FLOPs, attention).  
При фиксированном бюджете токенов/полей: что класть?

- больше объектов  
- плотнее атрибуты  
- геометрия (bbox/depth)  
- style/lighting  
- relations  

Seed снимал поля целиком (scene важнее depth) на BAGEL, но это не **allocation under budget** и не про VLM embedder.  
Мы строим Pareto: quality vs token budget при разных политиках заполнения.

### (2) Цель
**Рецепт packing** для conditioner: при 256 / 512 / 1024 токенах какой content mix оптимален.  
Это знание, которое сразу идёт в training recipe captioner’а и в schema design.

### (3) Мотивация
Train-on-reprompt мир = борьба за каждый токен conditioning, не «выключить PE».  
GPG растёт с полезной структурой; softmax competition / length issues у encoder’ов — с мусорной плотностью.  
Нужен закон: *marginal gain от следующего типа факта*.

### (4) Новизна
Field ablation Seed ≠ budgeted allocation.  
Long-caption papers не решают «что выкинуть первым при лимите».  
Отличие от идеи 1: 1 сравнивает две упаковки; 5 оптимизирует **состав** при лимите.

**Знание в мир:** marginal value типов visual facts в conditioning.

---

## Ранжирование: за что хвататься

| Rank | Идея | Ручка | Какое знание | Почему сейчас |
|------|------|-------|--------------|---------------|
| **1** | **#1 Info-matched NL↔SP** | B ⊥ A | structure vs coverage | блокер для VLM embedder; дыра Seed |
| **2** | **#4 Bottleneck localization** | D | где чинить стек | после/вместе с #1; напрямую про embedder |
| **3** | **#3 Diff × Prompt oracles** | E | куда headroom | объясняет SOTA; дёшево на fixed G |
| **4** | **#5 Budget allocation** | F | packing recipe | естественно из #1+#4 |
| **5** | **#2 Prompter training** | C | ROI post-training | после выбора IR |

### Почему №1 всё ещё лучший старт
Пока не ясно, нужен ли JSON при равных фактах, идеи 2/5 строят prompter и packing «в неизвестный IR», а идея 4 не знает, какой serialize baseline честный.  
#1 — prior. #4 — следующий удар под embedder. #3 — дешёвый companion measurement.

---

## Часть II. План проверки лучшей (#1) — коротко и жёстко

### Нарратив
Проблема: все бегут в structured captions.  
Недостаток: победы SP смешаны с лишней информацией.  
Идея: выровнять факты, сравнить упаковки.  
Польза: решить, учить ли следующий VLM на schema или на dense prose.  
Вывод: structure real / или coverage был confound — оба исхода knowledge.

### Минимальный сетап
- **Модель:** один open DiT + его text encoder (Qwen-Image LoRA/FT или SD3.5).  
- **Данные:** 50k–200k images → evidence bundle →  
  - SP-full  
  - NL-matched (hard attribute/ED gate к SP)  
  - NL-water (те же факты, больше слов)  
  - SP-sparse (меньше organization)  
- **Метрики:** train MSE; gen GenEval2/DPG subset; reconstruction probe; open ED/GPG.

### Бейзлайны
Seed-style unmatched SP vs short NL; matched-train NL без info-gate; official model short prompt.

### Код
DiffSynth/FlyMyAI LoRA для DiT; свой verbalizer+filter; куски evalkit Seed для метрик; публичные GenEval/DPG.

### Ожидание
NL-water ≈ NL-matched; unmatched SP ≫ short NL; **fork:** SP-full vs NL-matched либо остаётся gap (structure) либо схлопывается (info confound).

### Sanity
ED(NL-matched)≈ED(SP); shuffle attributes → падение; JSON без values → слабо.

### Success / fail
- **Success:** стабильный info-match + чёткий A или B + рекомендация для embedder.  
- **Fail/pivot:** не сводим ED в fluent NL → идём в #4 (может encoder/serialize) или #3 (oracles на SP-only).

---

## Что сознательно выкинули
- Always-on PE gating как main — слабо при train-on-reprompt.  
- Размытые «bakeoff всех каналов» без causal вопроса — низкий knowledge density.  
- Open GPG/ED как отдельная идея — лучше **tool внутри #1/#3**, не отдельная ставка.
