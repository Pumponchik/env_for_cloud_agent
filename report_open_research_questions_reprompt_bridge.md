# Куда копать: открытые вопросы T2I captions, re-prompt и bridge

**Дата:** 2026-08-03  
**Вход:** твоя подборка (Brack-цитаты, UniFusion, i1, ISS, FIBO, Think-Then-Generate, APE, VisualPrompter, TARA, DALL·E 3, RECAP, …) + вся база репо + свежий arXiv/HTML разбор limitations/future work ключевых papers.  
**Цель:** не ещё один список статей, а **карта незакрытых вопросов** — за что можно ухватиться в ресёрче.  
**Важно:** где казалось «дырка», но ответ уже есть — помечено отдельно.

Связанные отчёты: [`report_bridge_methods_taxonomy.md`](./report_bridge_methods_taxonomy.md) · [`reading_list_reprompter_latent_and_alt_channels.md`](./reading_list_reprompter_latent_and_alt_channels.md) · [`fundamental_papers_reprompt_reading_list.md`](./fundamental_papers_reprompt_reading_list.md)

---

## 0. Короткий вердикт

Поле **не** «всё уже сделали labs». Наоборот: три конкурирующих рецепта длины (рандомизация Brack / long-train+rewrite i1 / schema FIBO), **ноль** честного head-to-head; PE иногда **вредит** (GenEval 2, AtelierEval), а теории «когда пропускать» нет; structure vs length в conditioning **не разведены**; bias от rewrite уже измерен для prose, но **не** для JSON-schema expanders; latent re-prompter vs text PE на frozen DiT — почти пусто.

Ниже — 12 сквозных тем, затем ранжированные направления «куда копать», затем «казалось открытым → нашлось».

---

## 1. Сквозные незакрытые темы

### T1. Три рецепта длины — ни одного честного сравнения

| Рецепт | Источник | Суть |
|--------|----------|------|
| A | Brack `2506.16679` | На обучении **рандомизировать** длину/density → устойчивость к short prompts + diversity |
| B | i1 `2606.11289` | Учить на **длинных**, на инференсе rewrite/удлинять (GenEval 0.17 → 0.49 repeat×12 → 0.73 rewrite) |
| C | FIBO `2511.06876` | Учить на **длинных structured** + VLM→JSON translator |

**Твоя заметка про i1 верна:** правый столбец — про *инференс* на GenEval, не про обучение. Вывод labs: long-train + PE.  
**Дырка:** никто не сравнил A vs B vs C при matched backbone/data/FLOPs. Это самый чистый эксперимент в области caption design.

SEER (`2601.20305`) ещё спорит: выигрывает на **~23 словах** и ругает verbosity — противоречит i1/FIBO. **Никто не примирил** short-realizable vs long-distribution-matched.

---

### T2. Mismatch «переехал», не исчез

Каждый PE переносит train↔user gap в rewriter. Тогда вопрос становится: *лежит ли rewrite внутри realizable set генератора?*

- SEER: external rewriter → «linguistically valid but visually unrealizable» (representation mismatch).  
- APE: после RL **оптимальная длина model-specific** (FLUX короче, Z-Image длиннее).  
- ISS: сильный transfer rewriter’ов — но гипотеза «похожие caption distributions» **не проверена**.  
- UniFusion: in-model rewrite снижает shift, но VLM **ломает spelling** в text rendering.

**Дырка:** нет метрики *до* генерации: «этот revised prompt реализуем этим G?»

---

### T3. Когда PE включать — нет теории (есть сильная эмпирика «иногда вредит»)

Уже измерено:

- GenEval 2: rewrite **понижает** human alignment на 4/6 rewriting-trained models (−2.5%), поднимает на Qwen/Gemini (+3.3%).  
- AtelierEval (`2605.22645`): на системе с сильным internal middleware внешний MLLM-prompt **роняет** accuracy 69.6% → 45–49%; на Flux Pro без middleware — помогает.  
- PromptEnhancer: регрессии Text Layout / Interaction.  
- i1: механизм = train/infer length match.

Локальные заглушки (не теория): TARA accept-or-revert, APE `no_rewrite` router, RAISE adaptive budget, CRAFT stop, Ideogram AUTO.

**Дырка:** predict expected gain(prompt features, G, train caption law) → enhance | skip; oracle gap benchmark.

---

### T4. Structure vs length в conditioning — не разведены

FIBO: long structured ≫ short — но structure **confounded** с length.  
Structured Captions 19M (`2507.05300`): порядок полей помогает при том же контенте — маленький масштаб.  
«Format Tax» (`2604.03616`) в LLM: JSON constraints могут **вредить** reasoning — знак эффекта для T2I conditioning **неизвестен**.

**Дырка:** matched compute: (a) long JSON, (b) length-matched prose той же информации, (c) short. Один результат валидирует или хоронит JSON-native парадигму (FIBO/Ideogram/BBQ).

---

### T5. Нет стандарта schema / interoperability

FIBO fields ≠ Ideogram tree (key **order** load-bearing) ≠ BBQ numeric.  
Ты правильно отметил: Ideogram/FIBO — разные диалекты «промежуточного языка».

**Дырка:** superset schema + round-trip loss FIBO↔Ideogram↔BBQ; эффект нарушения key-order.

---

### T6. Нет professional single-attribute controllability benchmark

TaBR только у BRIA (FIBO/BBQ), без независимой репликации.  
PaintBench / Qwen-Image-Bench — другое.  
Disentanglement у FIBO — качественные картинки, не leakage metric.

**Дырка:** seed-matched counterfactuals по lighting/DoF/focal/… + leakage на нецелевые поля.

---

### T7. Faithfulness / audit revised prompts и endogenous CoT

CRAFT / CoIG трогают interpretability шагов.  
**Не сделано:** является ли revised_prompt / `<think>` *каузальным* объяснением картинки (perturb clause → consistent image change)?  
Методы есть в LLM CoT faithfulness (`2607.29062`, `2607.27304`) — **не портированы** на T2I PE.

GenEval 2: production rewriting methods **не open-sourced** — инфраструктурный audit gap.

---

### T8. Latent / vector re-prompter vs textual PE — почти пусто на frozen DiT

Близко:

- ELLA / SUR / Think-Then-Generate / RISE-T2V / DATE / UniFusion VERIFI — каналы embeddings.  
- **LatentMorph** `2602.02227` («Show, Don't Tell»): latent reasoning vs text decode на AR UMM; `w/o latent` ablation падает; −время/−tokens. **Частичный ответ**, но Janus-Pro AR, не frozen DiT connector.

**Дырка:** ELLA-style connector, который эмитит *enhanced conditioning*, vs textual PE при matched FLOPs на SD/FLUX/Qwen-Image.

Твоя заметка про UniFusion верна: основное — VLM как unified encoder; re-prompt там побочный (OCRewrite). Копать имеет смысл именно ветку «продолжение промпта внутри VLM → conditioning», не путать с «заменили VAE».

---

### T9. Credit assignment в RL-rewriter’ах

APE **явно**: GRPO/GDPO только final reward → future: finer-grained credit across stages.  
Think-Then-Generate / ISS / PromptEnhancer — terminal или coarse composite.  
MAPE иногда **хуже** one-shot при уже ясном промпте (error propagation).

**Дырка:** per-field / per-atom / per-stage rewards для router→rewrite→compose.

---

### T10. VLM-as-judge drift + circularity

GenEval 2: VQAScore alignment **гнил** для моделей новее судьи.  
VisualPrompter/TARA: судья = источник ошибок.  
SEER: internal judge на 300 samples.

**Дырка:** drift detection без полного human re-study; anti-circular repair (не тот же VLM diagnose+reward+eval).

---

### T11. Prompt-addressable ceiling

TARA / VisualPrompter / SEER независимо: часть failures **не чинится** prompt’ом (counting, rare pose, long text render, вне manifold).

**Дырка:** оценить долю remaining gap, которую ещё может закрыть input-side vs нужна weight update. Это решает, куда класть compute: PE vs train.

---

### T12. Bias / diversity от PE — слепое пятно (частично закрыто для prose)

**Нашлось (см. §3):** FairPro / «Aligned but Stereotypical?» `2512.04981` — rewrite **усиливает** demographic bias; alignment↔bias r≈0.948.

**Всё ещё открыто:**

- schema expanders (FIBO поля ethnicity/expression — slot-fill protected attrs by design);  
- cultural / aesthetic homogenization;  
- diversity collapse от rewriter style (Brack уже видел diversity↓ от dense captions на train-side).

Brack сам: caption→gender bias «complex, more research needed».

---

## 2. Ранжированные направления «за что ухватиться»

Оценка: novelty × impact × feasibility (лучше сверху).

### ★★★★★ 1. PE gating как decision problem + oracle-gap benchmark

**Вопрос:** когда enhance, когда skip, для какого G?  
**Почему сейчас:** GenEval 2 + AtelierEval + i1 уже дали эффект-сайзы.  
**Что сделать:** cheap predictor E[Δ | prompt, G, caption-law]; benchmark oracle skip-vs-enhance.  
**Риск низкий, публикабельность высокая.**

### ★★★★★ 2. Head-to-head: randomized-length train vs long-train+rewrite vs structured long

**Вопрос:** какой рецепт T1 правильный?  
**Почему:** Brack vs i1 vs FIBO — поле без арбитра.  
**Что сделать:** один backbone (i1 recipe открыт), три data regimes, eval: short/long/rewrite GenEval + aesthetics + diversity + human.  
**Это «лабораторный» paper, который цитировали бы все.**

### ★★★★☆ 3. Structure ⊥ length в conditioning

**Вопрос:** JSON помогает сам по себе или только потому что длинный?  
**Что сделать:** same content → JSON vs prose serialization vs short; matched tokens/FLOPs.  
**Связь с Format Tax:** исход непредсказуем — хорошо для novelty.

### ★★★★☆ 4. Intent + bias audit schema bridges (FIBO / Ideogram / BBQ)

**Вопрос:** VLM→JSON expander инжектит demography/style сильнее prose PE?  
**Почему:** FairPro закрыл prose; schema — дырка и опаснее (явные ethnicity fields).  
**Метод:** перенести `2512.04981` на Magic Prompt / FIBO expander.

### ★★★★☆ 5. Realizability filter: «этот rewrite G умеет нарисовать?»

**Вопрос:** как отсеять FaithRewriter-style hallucination *до* generate?  
**Стык:** SEER (нужен shared space) vs disjoint PE (APE/PromptEnhancer).  
**Что сделать:** predict visual realizability; reject/revise; сравнить endogenous vs external.

### ★★★☆☆ 6. Single-attribute controllability benchmark (+ leakage)

**Вопрос:** правда ли FIBO disentangled?  
**Что сделать:** counterfactual pairs + leakage metric; открытый бенч поверх TaBR.

### ★★★☆☆ 7. Latent re-prompter для frozen DiT vs text PE @ matched FLOPs

**Вопрос:** убрать text bottleneck в PE→G выгодно ли?  
**База:** ELLA, RISE-T2V, Think-Then-Generate, DATE; не путать с UniFusion-as-encoder.  
**Частичный ответ уже:** LatentMorph на AR — указать и отличиться diffusion connector’ом.

### ★★★☆☆ 8. Faithfulness audit revised_prompt / CoT

**Вопрос:** trace = объяснение или декорация?  
**Метод:** port CoT faithfulness; perturb clause.  
**Бонус:** проверить слух про PromptEnhancer SFT w/ CoT ≤ w/o CoT (числа на third-party notes, **не** в arXiv v3–v5 — нужно подтвердить camera-ready).

### ★★☆☆☆ 9. Prompt-addressable fraction of remaining errors

**Вопрос:** какой % fail’ов чинится typed repair / PE / layout, какой — только train?  
**Метод:** upper bound с oracle repairs + oracle layouts на DSG/TIFA/GenEval2.

### ★★☆☆☆ 10. Dedicated survey + open PE harness

Низкая novelty, высокая service value. GenEval 2 уже страдает от closed rewriters.  
Harness: единый rewrite protocol, eval vs **original** prompt, length-matched controls.

### ★★☆☆☆ 11. Per-stage credit assignment для MAPE-like PE

Прямой future work APE. Узко, но NVIDIA-adjacent.

### ★★☆☆☆ 12. Intermediate visual language / schema design science

FIBO future work: «which attributes, what granularity».  
Связать с BBQ parametric gap и Ideogram key-order brittleness.

---

## 3. Казалось открытым → нашёлся ответ (указывать в related work)

| Вопрос | Статус | Где ответ |
|--------|--------|-----------|
| Rewriting инжектит demographic bias? | **В основном закрыт** для prose PE | FairPro / Aligned but Stereotypical? `2512.04981` (r≈0.948 alignment–bias) |
| Существует ли endogenous reprompt без внешнего LLM? | **Да** | SEER `2601.20305` (300 samples) |
| Latent reasoning лучше text decode? | **Частично** (AR UMM, не DiT PE) | LatentMorph `2602.02227` |
| Нужен ли always-on rewrite? | Эмпирика «нет», теории нет | GenEval 2, AtelierEval, TARA/APE gates |
| Dedicated T2I-PE survey? | **Всё ещё нет** | Ближайшие: APO `2502.16923`, Controllable T2I `2403.04279` |
| Head-to-head JSON vs NL @ matched compute? | **Всё ещё нет** | FIBO confounds length; `2507.05300` tiny |
| Schema standard? | **Нет** | Три несовместимых диалекта |
| Professional attribute leakage bench? | **Нет** (TaBR только BRIA) | — |
| Counting чинится PE? | **Скорее нет** | T2ICountBench `2503.06884`; TARA residual |
| Train short to match users? | **Labs говорят нет** | i1 Finding 7; Wan/Seed/Cosmos — align to train |
| Captioner fingerprint в T2I? | Есть линия | `2602.22734` (из твоих цитат Brack) — копать потомков |
| VLM вместо T5+VAE? | Архитектурная линия, не PE | UniFusion `2510.12789` — твой разбор верен |

---

## 4. Как это стыкуется с твоими заметками

| Твоя заметка | Исследовательский вывод |
|--------------|-------------------------|
| UniFusion — не про re-prompt, а VLM encoder; интересно «continuation» | Верно. Отдельный вопрос: **in-model rewrite tokens → cond** (VERIFI) vs полный encoder swap. Не смешивать. |
| i1: учат long, eval rewrite — не «учат на rewrite» | Верно. Открытый вопрос: сравнить с Brack randomization. |
| ISS: DPO rewriter, длина растёт, додумывает | Известный failure: verbosity hacking; нет stopping rule → тема gating + length-matched DPO (FaithRewriter). |
| FIBO ~1000 tok + DimFusion | Архитектура под long — да; structure⊥length — нет. |
| Hunyuan broadband 30–1000 | Третий рецепт вариативности; сравнить с Brack/i1. |
| Think-Then-Generate: think→rewrite→**embeddings** + Dual-GRPO | Ближайший «latent re-prompt» с текстом как внутренним IR; сравнить с RISE (без emit string). |
| APE SLM+GRPO, MAPE decomposition | Decomposition не всегда помогает; credit assignment — их future work = твоя ниша. |
| VisualPrompter / TARA typed repair | Потолок generator-side; следующий шаг — измерить addressable fraction. |
| DALL·E 3 Better Captions | Индустриальный корень; «ничего про captioner architecture» — да, поэтому Brack/i1/FIBO важнее как science. |
| RECAP short/long/mix @ CLIP-77 | Старый CLIP-бюджет; сегодня пересмотреть при 256–1000 tok encoders (i1/FIBO). |

---

## 5. Практический совет: с чего начать ресёрч

Если один проект на квартал:

1. **Gating + oracle gap** — быстро, сильно цитируемо, опирается на GenEval 2.  
2. Или **Brack vs i1 vs FIBO-style data** на одном open recipe (i1) — «закрывает спор области».

Если интерес к **латентному re-prompter** (твой фокус раньше):

3. **RISE/ELLA/Think-Then-Generate vs PromptEnhancer/APE @ matched FLOPs** на одном G + eval vs original prompt (GenEval 2 discipline). Явно отделить от UniFusion encoder story.

Если интерес к **schema/control**:

4. **Structure⊥length** + **bias audit JSON expanders**.

Не начинать с: очередного always-on aesthetic rewriter; очередного agentic debate без gate; MAS latent messaging (другая область).

---

## 6. Чеклист «хорошего» paper в этой зоне (2026)

- Eval против **original** user prompt (GenEval 2).  
- Length-matched controls (FaithRewriter lesson).  
- Report skip-vs-enhance / when PE hurts.  
- Diversity + bias, не только alignment.  
- Назвать generator’s train caption law.  
- Если schema: ablate structure vs length.  
- Если latent: сравнить с strong textual PE при matched compute.  
- Open rewriter / seeds — иначе GenEval-2-style confusion.

---

## Источники (ядро)

Brack `2506.16679` · i1 `2606.11289` · GenEval 2 `2512.16853` · FIBO `2511.06876` · BBQ `2602.20672` · APE `2606.00204` · ISS `2510.12041` · Think-Then-Generate `2601.10332` · UniFusion `2510.12789` · VisualPrompter `2506.23138` · TARA `2607.18724` · PromptEnhancer `2509.04545` · SEER `2601.20305` · FairPro `2512.04981` · LatentMorph `2602.02227` · AtelierEval `2605.22645` · Format Tax `2604.03616` · RECAP `2310.16656` · DALL·E 3 Better Captions · RISE-T2V `2511.04317` · ELLA `2403.05135`

Полные citation trees / корпуса: `research/bridge-methods/`, `research/reprompt-systems/`, `research/prompt-length/`.
