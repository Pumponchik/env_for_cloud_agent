# Идеи для статьи: text conditioning / PE / NL↔SP в T2I

Документ по инструкции этапа ideas (структура 1–4 → ранжирование → план проверки лучшей).  
Контекст: разбор Seed `2607.29679` (Context Scaling), FIBO, PromptEnhancer, SoftREPA и аудит open problems в репо.

---

## Часть I. Пять идей

### Идея 1. Info-matched NL ↔ SP: честный формат без «лишних деталей» в JSON

**(1) В чём идея?**  
Провести controlled сравнение **natural-language** и **structured prompt (JSON/schema)** при **одинаковой realized information** (matched ED/GPG и/или matched attribute set), а не при matched train budget с заведомо более плотным SP, как в Seed. Цель сетапа — ответить: выигрыш SP — это формат/организация или просто больше деталей? И какой IR лучше класть в **VLM/text conditioner** дальше (dense prose / JSON / layout-hybrid).

**(2) Какая цель?**  
Улучшить **научную валидность выбора conditioning IR** для следующего VLM-эмбеддера:  
- отделить **structure effect** от **information effect**;  
- дать recipe: «при равной информации что учить в text encoder / DiT»;  
- снизить риск построить весь pipeline на JSON только потому, что в Seed SP был информативнее NL.

**(3) Мотивация?**  
В `2607.29679` Dense NL L10 имеет ED≈0.75 / GPG≈112, Structured L10 — ED≈0.83 / GPG≈210; matched NL control — matched **train**, не matched **info**. Примеры SP (schema_room, pineapple PE) показывают либо denser grounded dump, либо явное дозаполнение. Значит текущий вердикт «SP ≫ NL» confounded. Cosmology/FIBO (`2511.06876`) тоже сравнивает long structured vs **short** captions. Observation DetailMaster/LongT2I: длина ≠ alignment. Если выровнять информацию, останется чистый эффект организации — критично для дизайна VLM embedder.

**(4) Почему новая?**  
Проверено: Seed Matched NL, FIBO long-JSON vs short, Cosmos field recall — **нет** публикации с hard attribute/ED/GPG-matched NL↔SP на одном backbone + явным выводом для conditioner design. Близко: Seed (matched train), FIBO (length confound). Разница: **info-matching protocol** + downstream рекомендация под VLM embedder, не ещё один end-to-end SOTA chase.

---

### Идея 2. Рецепт обучения prompter’а: zero-shot vs SFT vs cold-start vs RL vs agentic loop

**(1) В чём идея?**  
На **фиксированном** diffuser + фиксированном schema/IR провести factorial: нужен ли task-specific training prompter’а вообще, и какой stage даёт ROI (SFT / cold-start / GRPO / OPSD / multi-turn loop), при **cost-normalized** сравнении (latency, $API, GPU-hours).

**(2) Какая цель?**  
Улучшить **promptability training efficiency**: когда платить за LoRA/RFT, когда хватает frozen LLM + 1–2 round judge, когда always-on PE вреден. Практический deliverable — Pareto: quality vs cost для PE stack.

**(3) Мотивация?**  
Seed показывает: SFT даёт главный structure jump; OPSD лучше GRPO; Base@8 rounds < Trained@1 shot; loop saturates к ~2–4 rounds. PromptEnhancer/APE показывают RFT/agents, но **нет** общей cost-normalized карты «учить vs крутить loop». Продукты (Ideogram Magic Prompt, Qwen PE) часто always-on без oracle. Нужна карта, а не ещё один rewriter.

**(4) Почему новая?**  
Есть stage ablations внутри одной paper (Seed Table 4/5; PromptEnhancer; APE). Нет **cross-recipe bakeoff** с единым harness, eval vs **original** user prompt, и явным «do we need to train at all?» при matched inference budget. Отличие: meta-study + decision rule, не новый reward model.

---

### Идея 3. Oracle-gap predictive PE gating

**(1) В чём идея?**  
Построить benchmark и предиктор: для каждого user prompt оценить \(\Delta = \mathrm{score}(G(\mathrm{PE}(p))) - \mathrm{score}(G(p))\) и решить **enhance / skip / cheap-rewrite** *до* генерации. Репортить gap: always-skip / always-enhance / oracle / learned gate / cost-adjusted gate.

**(2) Какая цель?**  
Улучшить **utility PE при меньшей цене и меньшем intent drift**: не всегда раздувать промпт; включать PE там, где oracle показывает выигрыш (composition/count/layout), пропускать на простых aesthetic prompts.

**(3) Мотивация?**  
Наивная длина вредит (Seed Fig.1; DetailMaster). Always-on Magic Prompt часто «льёт воду». Есть post-hoc accept/revert (TARA-класс) и toxicity gates (PromptSafe), но **нет** predictive utility gate с oracle-gap protocol. GRACE/gated refinement — про LLM prompt optimization, не T2I PE utility. Если gap большой, а learned gate его закрывает — сильный systems paper; если gap мал — тоже результат (always-on ок).

**(4) Почему новая?**  
Поиск: PromptSafe (safety), GRACE (NLP APO), product heuristics (длина &lt; N слов). В нашем аудите T3/N03 помечены OPEN: нет oracle-gap PE utility benchmark. Отличие от post-hoc repair: решение **до** generate; метрика — gap to oracle, не только absolute score.

---

### Идея 4. Bridge bakeoff: text IR vs soft/latent conditioning @ matched FLOPs

**(1) В чём идея?**  
На **frozen** DiT сравнить каналы обогащения условия при одном latency/FLOPs budget: (a) textual rewrite/NL, (b) JSON/SP fill, (c) soft tokens / continuous PE (SoftREPA-класс), (d) опционально layout tokens. Вопрос: нужен ли читаемый текст как PE, или VLM/embedder-side continuous bridge лучше при том же compute?

**(2) Какая цель?**  
Улучшить **выбор канала для следующего VLM-эмбеддера**: текст-as-API vs soft conditioning. Закрыть путаницу papers, где каждый канал хвалят на своём сетапе.

**(3) Мотивация?**  
Seed/FIBO тянут всё в JSON text. SoftREPA (`2503.08250`) показывает soft tokens на frozen SD без textual PE. PromptLoop/latent methods — другие оси. Для «дальнейшего VLM embedder» критично: учить модель читать JSON или учить continuous bridge от user intent? Matched-FLOPs bakeoff даёт ответ.

**(4) Почему новая?**  
SoftREPA, IPGO, DATE, PromptLoop существуют по отдельности; **нет** head-to-head text-PE vs soft vs schema @ matched FLOPs, eval vs original prompt, один G. Отличие: systems bakeoff + decision для conditioner design, не новый soft-token objective.

---

### Идея 5. Open caption-information metrics + pre-train screening

**(1) В чём идея?**  
Сделать воспроизводимые open GPG/ED (или наследников) на 7–32B VLM без Gemini/GPT monopoly; показать, что ranking caption configs предсказывает relative train loss / gen quality; выпустить screener «стоит ли учить DiT на этом caption recipe».

**(2) Какая цель?**  
Улучшить **кост исследования caption recipes**: дешёвый filter до multi-GPU FT; общий yardstick для Ideи 1 (info-match).

**(3) Мотивация?**  
Seed показал, что GPG/ED предсказывают loss, но judges закрытые/огромные. Caption Detailness (`2505.15172`) — родственник ED. Без open metric идея 1 и recipe tournament плохо воспроизводимы. Science contribution + tool.

**(4) Почему новая?**  
GPG/ED в Seed; Detailness отдельно. Нет open calibrated release с proven rank-stability на публичных DiT и protocol для info-matching. Отличие: engineering+validation paper с release, не новая теория MI.

---

## Ранжирование и выбор лучшей

| Rank | Идея | Novelty | Impact | Feasibility | Стратегическая ценность |
|------|------|---------|--------|-------------|-------------------------|
| **1** | **#1 Info-matched NL↔SP** | высокая (дыра Seed) | очень высокий | средняя (нужен FT, но LoRA/1 DiT) | напрямую ведёт к VLM embedder |
| 2 | #3 Oracle-gap PE gating | высокая | высокий | высокая (меньше train) | systems + benchmark |
| 3 | #4 Bridge bakeoff text/soft | высокая | высокий | средне-высокая | стык с embedder |
| 4 | #2 Prompter training recipe | средняя | высокий | средняя | полезно, но secondary |
| 5 | #5 Open GPG/ED | средняя | высокий как tool | высокая | лучше как **side contrib** к #1 |

### Почему лучшая — Идея 1

1. **Самая острая дыра в главной paper области** (`2607.29679`): вердикт SP≫NL сейчас нельзя честно переносить на дизайн conditioner’а.  
2. **Прямой путь к вашей следующей задаче** (VLM embedder): ответ «при равной информации нужен JSON / prose / hybrid» определяет архитектуру.  
3. **Одна сильная статья**: protocol + ablations + recommendation; Idea 5 естественно вкладывается как metric appendix.  
4. Идеи 2–4 лучше делать *после*: иначе непонятно, *в каком IR* учить prompter/soft bridge.  
5. Риск compute управляем: не 15×BAGEL, а 2–3 caption arms × один open DiT (LoRA/continued FT).

Отличие от #3/#4: те отвечают «когда PE» и «какой канал», но оба предполагают, что мы уже знаем, *что* писать в conditioning. #1 отвечает на prior вопрос.

---

## Часть II. Лучшая идея подробно + план проверки

### Нарратив статьи

**Проблема.**  
Современный T2I упирается не только в размер DiT, но и в то, *как* текст отдаёт image-grounded информацию. Seed показал scaling law: loss следует GPG/ED, а не длине; structured prompts бьют NL. Индустрия и research начинают строить JSON prompters и SP-trained generators.

**Недостаток существующих решений.**  
Контроли «SP vs NL» смешивают формат с количеством деталей. В Seed длинный Dense NL не дотягивает по ED/GPG до L10 SP; FIBO сравнивает long JSON с short captions. Создаётся впечатление, что «структура побеждает», хотя могла победить **плотность аннотации**. Если так, следующий VLM-эмбеддер могут зря заточить под хрупкий JSON.

**Идея.**  
Построить **Info-Matched Conditioning Benchmark**: из одного image evidence собрать пакеты  
- SP-L10,  
- NL-matched (prose с hard check на тот же attribute/geometry set, ED/GPG в допуске),  
- NL-verbose (вода без новых фактов),  
- SP-sparse (те же факты, меньше полей/организации).  

Обучить / адаптировать **один** diffuser на каждом arm при matched compute и сравнить train loss + gen metrics. Дополнительно: frozen backbone probe (как Fig.3) и анализ, что лучше ест **VLM text encoder** (JSON tokens vs prose).

**Как станет лучше.**  
Если при matched info SP всё ещё выигрывает — structure реален, JSON/schema оправдан для embedder.  
Если gap схлопывается — приоритет **coverage annotation**, формат вторичен; embedder можно учить на dense NL + лёгкой разметке.  
Любой исход publishable и снимает confound у Seed/FIBO.

**Вывод статьи.**  
«Что масштабирует text conditioning — информация, организация или оба?» с честным протоколом и рекомендацией для VLM conditioner.

---

### Минимальный экспериментальный сетап

**Модель (diffuser):**  
- Основной: открытый DiT с нормальным text encoder — предпочтительно **Qwen-Image** (LoRA/continued FT DiT, text encoder frozen) *или* SD3.5/FLUX.dev если Qwen-FT недоступен по compute.  
- Для probe без retrain: один frozen checkpoint (официальный + при возможности SP-tuned).

**Данные:**  
- 50k–200k images с богатой сценой (не только COCO short).  
- Annotation pipeline (упрощённый Seed): VLM crop captions + SAM boxes (+ depth optional).  
- Из L10-like record детерминированно:  
  - **SP-full**  
  - **NL-matched**: verbalizer + **hard filter** (attribute recall ≥ τ vs SP; reject/retry)  
  - **NL-water**: matched entities, +50–100% tokens elaboration only  
  - **SP-ablate**: mask photography/relations (control organization)

**Метрики:**  
- Train: converged flow-matching MSE @ matched token budget.  
- Caption-side: open ED-proxy + GPG на Qwen2.5-VL-7B/32B (Idea 5 lite).  
- Gen: GenEval / GenEval2 subset, DPG-Bench subset, TIIF-short, GSB/VLM pairwise vs original short user prompts *и* vs reference caption.  
- Conditioner probe: DINOv3/SigLIP2/LPIPS reconstruction (Fig.3-style) на held-out.

**Минимальный compute target:**  
2–4 arms × LoRA-DiT 10k–50k steps на 8–32 GPU, не full Seed 500k×512.

---

### Бейзлайны

| Baseline | Реализация |
|----------|------------|
| Official model + short user prompt | HuggingFace pipeline as-is |
| Official PE / prompt_extend | Qwen/Ideogram-style expand если доступен; иначе GPT/Qwen rewrite |
| Seed-style SP train (info-unmatched) | наш SP-full arm — upper reference |
| FIBO-like long JSON vs short NL | short web caption vs SP-full (confounded control) |
| Matched-train NL без info gate | verbalizer без ED filter (как Seed) — показать, что info-gate меняет вывод |
| Zero-shot LLM→SP на frozen G | Gemini/Qwen fill schema, без FT diffuser |

---

### Какой код

| Компонент | Код |
|-----------|-----|
| DiT train/LoRA | DiffSynth-Studio / FlyMyAI qwen-image-lora / Musubi — адаптировать под JSON captions |
| Annotation | свой thin pipeline на Qwen2.5-VL + SAM2 (не Seed-VL internal) |
| Info-match filter | свой: attribute extract+match (open VLM) + retry verbalizer |
| Metrics GenEval/DPG | публичные evalkits; GSB — VLM judge prompts из Seed App.E (offline) |
| GPG/ED-lite | частичный port из `heheyas/context-scaling` evalkit + свой open judge |
| PE baselines | vLLM + system prompts; для SP — student prompt из их demo |

Свой glue: dataset build, arm configs, logging, tables. Не писать DiT с нуля.

---

### Ожидаемые результаты

1. **NL-water ≈ NL-matched** по loss/gen → подтверждение Seed «длина без info не помогает».  
2. **SP-full ≫ NL-unmatched** (репликация Seed confound).  
3. Главный fork:  
   - **A (structure real):** SP-full ≥ NL-matched на gen composition/layout на ≥X пунктов GenEval2 GM / GSB; loss gap остаётся.  
   - **B (info was confound):** gap SP-full vs NL-matched ≤ noise; SP-ablate ≈ NL-matched.  
4. Для VLM embedder: если A — рекомендовать schema-aware tokenization/fields; если B — dense NL + attribute coverage objective.  
Ожидаемый effect size при A: не Seed +16 GenEval2 GM over matched NL, а **меньший, но значимый** layout/count gain (порядка нескольких пунктов + GSB), потому что info выровнена.

---

### Sanity checks (корректность кода)

| Check | Ожидание |
|-------|----------|
| Tokenization SP vs NL lengths | SP не обязан быть длиннее; логировать |
| Info-match filter | ED(NL-matched) ∈ [ED(SP)−ε, ED(SP)+ε]; fail rate логировать |
| NL-water | ED flat vs NL-matched, tokens ↑ |
| Overfit one batch | loss падает на train batch для всех arms |
| Frozen probe identity | один seed, один image: metrics воспроизводимы |
| Shuffle attributes in NL-matched | gen/layout должны упасть → сигнал реально используется |
| Empty caption / CFG dropout | деградация как в baseline recipe |
| JSON syntax-only (ключи без values) | почти как weak caption → не «магия скобок» |

---

### Критерии успеха / неуспеха

**Развивать дальше (success), если:**  
- Info-match protocol стабилен (rank-stable ED across 2 judges);  
- Получен **чёткий** A или B с воспроизводимым gap;  
- Есть actionable recommendation для VLM embedder;  
- Side: open metric скрипт работает на 1k images.

**Пивот / отказ от идеи как main paper, если:**  
- Не удаётся свести ED NL к SP без разрушения fluent NL (verbalizer collapse) → тогда идея 5+annotation становится блокером, main переключается на Idea 3 (gating) или 4 (soft bridge);  
- Все arms в noise при доступном compute (LoRA слишком слаб) → нужен heavier FT или другой backbone; если и heavy FT даёт null без interpretability — идея слабая как empirical claim;  
- Обнаружится, что кто-то уже выложил info-matched SP↔NL с тем же выводом до submission — сохранить как replication+embedder angle или сузить на conditioner probing.

**Частичный успех (всё ещё paper):**  
Protocol + negative result «при matched info structure не помогает на open DiT X» — сильный corrective к Seed.

---

## Следующий шаг после успеха Ideи 1

1. Зафиксировать IR-победителя → Ideя 4 (soft vs text) на этом IR.  
2. Ideя 2 — training recipe prompter’а уже под выбранный IR.  
3. Ideя 3 — gating поверх лучшего PE.  
4. Ideя 5 — выпустить метрики вместе с Ideей 1.

---

## Краткие ссылки

- Seed / Context Scaling: arXiv `2607.29679`, https://heheyas.github.io/context-scaling/  
- FIBO: `2511.06876`  
- SoftREPA: `2503.08250`  
- PromptEnhancer: `2509.04545` / CVPR 2026  
- Caption Detailness: `2505.15172`  
- Аудит open problems: `report_open_problems_autonomous_audit.md`
