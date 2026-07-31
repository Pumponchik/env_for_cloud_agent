# User→Generator Bridge Methods: Taxonomy Beyond Textual Re-Prompt

**Дата:** 2026-07-31  
**Вопрос:** как закрыть gap между коротким/недоспецифицированным user prompt и тем, что реально потребляет T2I/T2V генератор — *не только* текстовым re-prompter’ом.  
**Метод:** 4 параллельных literature-агента (embeddings · layout · schema/endogenous/action · citation trees) + уже собранный корпус PE + arXiv/Semantic Scholar.  
**Артефакты:** [`research/bridge-methods/`](./research/bridge-methods/) · companion: [`report_reprompt_system_architecture_2026.md`](./report_reprompt_system_architecture_2026.md), [`fundamental_papers_reprompt_reading_list.md`](./fundamental_papers_reprompt_reading_list.md)

> **Важный gap поля:** dedicated survey именно по *bridge methods* (текст + embeddings + layout + schema + endogenous) **не существует**. Ближайшие обзоры — Controllable T2I (`2403.04279`), APO (`2502.16923` / `2502.11560`), Multimodal TTS (`2606.08231`), Multimodal CoT (`2503.12605`). Ниже — синтез primary papers.

---

## 0. Прямой ответ

Gap один, рычагов много. Общий пайплайн:

```
user_prompt  x
      │
      ▼
  bridge B(x)  →  wire artifact  y
      │
      ▼
  generator G(y) → image
```

**Wire artifact `y`** — вот что реально различает методы:

| Семья | Что уходит в генератор | Типичные якоря |
|-------|------------------------|----------------|
| **F1 Textual rewrite** | Новый prose prompt | APE, PromptEnhancer, Wan/Seed/Cosmos PE |
| **F2 Embedding / adapter** | Векторы LLM/CLIP/soft prompts | ELLA, SUR-adapter, DimFusion, PEZ, IP-Adapter |
| **F3 Layout / plan** | Боксы, регионы, граф, draft, код | LMD, RPG, GLIGEN, GoT, DraCo, ATLAS |
| **F4 Schema / JSON** | Typed fields (+ числа) | FIBO, Ideogram 4, BBQ, Structured Captions |
| **F5 Endogenous CoT** | Внутренние thinking-токены модели | T2I-R1, SEER, HunyuanImage 3 |
| **F6 Non-text action** | Attention / weights / timesteps / noise / mixed ops | Attend-and-Excite, PAE, PromptLoop, RAISE |

Они **не взаимоисключающие**. Граф цитирований показывает композицию: LMD нуждается в GLIGEN (F3→executor), RPG цитирует LMD+Attend-and-Excite, APE цитирует FIBO как target format, ATLAS/RAISE уже гибриды.

**Решающий эмпирический результат (SCoT `2602.11980`):** при фиксированном генераторе  
- Text CoT даёт почти весь *reasoning* gain;  
- boxes дают почти весь *compositional* (GenEval) gain.  
**Дополняют, не заменяют.**

---

## 1. Почему bridge вообще нужен (шесть формулировок gap)

| # | Gap | Кто формулирует | Какой bridge отвечает лучше |
|---|-----|-----------------|------------------------------|
| G1 | Train captions ≠ user text | Wan, Seedance, Cosmos, TIPO | F1 (distribution align) |
| G2 | Underspecification → произвольное додумывание | FIBO | F4 schema / F1 controlled expand |
| G3 | Spatial / count / binding failures | LMD, RPG, PromptEnhancer taxonomy | F3 layout / F6 attention |
| G4 | Слабый text encoder / окно CLIP | ELLA, LI-DiT | F2 connector / stronger encoder |
| G5 | Parametric control (точные bbox, RGB) | BBQ, Rich Text, Ideogram | F4 numeric schema |
| G6 | Understanding≠generation (Cognitive Gap) | SEER | F5 endogenous |

Текстовый PE закрывает в основном **G1–G2**. Остальное — другие семьи.

---

## 2. Семьи методов: идея, механизм, плюсы/минусы

### F1 — Внешний текстовый re-prompter

**Идея.** Пользователь пишет коротко. Отдельный LLM/VLM пишет длинный/структурный caption в духе training distribution. Генератор (часто frozen) ест prose.

**Как работает.** SFT short→long (± CoT) → RL (DPO/GRPO) по visual rewards; или zero-shot system prompt; или retrieval modifiers (RAPO++).

**Плюсы**
- Портативность: один rewriter → много API/бэкбонов (Input-Side Scaling).
- Человекочитаемый артефакт: можно показать `revised_prompt`, дать Off/Auto/On.
- Зрелая индустриальная практика (OpenAI, Wan, Seed, Qwen, FLUX, Cosmos).
- Не требует переобучения генератора.

**Минусы**
- Не умеет *числа* (точный bbox/RGB) — «слева» остаётся словами.
- Textual hallucination (FaithRewriter: fluent but unrealizable).
- GenEval 2: rewrite может *понизить* human alignment.
- Uniform expansion загрязняет intent; нужен gating (TARA / APE `no_rewrite`).
- Два мозга → representation mismatch (SEER).

**Когда правильно:** frozen third-party generator; нужен UX с видимым текстом; gap ≈ train↔user captions.  
**Когда неправильно:** нужна pixel-precise layout; бренд-критичный audit без дрейфа; уже есть сильный native CoT.

**Якоря:** PromptEnhancer `2509.04545`, APE `2606.00204`, RePrompt `2505.17540`, Input-Side Scaling `2510.12041`, TARA `2607.18724`, FaithRewriter `2606.08492`.

---

### F2 — Embeddings / adapters / soft prompts

**Идея.** Не печатать длинный текст. Взять смысл из LLM (или image encoder) и **прокинуть векторами** в cross-attention / conditioner генератора.

#### Подтипы

| Подтип | Суть | Примеры |
|--------|------|---------|
| A. Connector в frozen generator | Учить только adapter | ELLA, SUR-adapter, LLM4GEN, GlueGen |
| B. LLM-native conditioner | Генератор учится под LLM states | Imagen/T5, ParaDiffusion, SANA, Qwen-Image, DimFusion |
| C. Soft / test-time embedding opt | Оптимизировать векторы prompt | Textual Inversion, PEZ, DPO-Diff, IPGO, PEO |
| D. Image-as-prompt | Картинка вместо описания | IP-Adapter, Prompt-Free Diffusion |
| E. Prior text→image emb | Как DALL·E 2 | unCLIP, ECLIPSE |

**ELLA (`2403.05135`)** — канон connector’а: Timestep-Aware Semantic Connector динамически достаёт условия из LLM; U-Net/LLM frozen; совместим с LoRA/ControlNet; дал DPG-Bench.

**SUR-adapter (`2305.05189`)** — ранняя явная постановка: короткий casual prompt должен работать *без* выдачи rewritten string пользователю.

**LI-DiT (`2406.11831`) — важный негатив:** наивная замена CLIP на decoder-only LLM **ухудшает** prompt following (NTP≠discriminative features + positional bias). Нужны refiners / instruction prefix / снятие causal mask.

**DimFusion (в FIBO):** сливает слои LLM **по embedding-dimension**, не раздувая token length — ответ на стоимость длинных captions.

**Плюсы**
- Обходит лимит «красивых слов» и CLIP-77 truncation.
- Дешёвый plug-in путь (ELLA учит только connector).
- Переносит то, что текстом плохо сказать (style/ID → IP-Adapter).
- Test-time embedding opt может бить rewrite без обучения (PEO claims).

**Минусы**
- Плохая editability/audit: пользователь не правит векторы.
- Слабая переносимость soft prompts между моделями (PEZ сам это формулирует).
- Потолок = capacity frozen U-Net/DiT.
- Interpretability / adversarial density embedding space (`2406.07506`).
- Наивный LLM-encoder ломается (LI-DiT).

**Когда правильно:** свой или controllable stack; dense prompts + weak CLIP; нужен image prompt.  
**Когда неправильно:** нужен показываемый revised text; чужой closed API без embedding access.

---

### F3 — Layout / plan side-channel

**Идея.** Многие провалы — не «мало прилагательных», а **геометрия**: кто где, сколько, какие атрибуты к кому. Bridge выдаёт план сцены.

#### Что едет по проводу (по возрастанию конкретности)

prose → linguistic structure → **boxes+captions** → region partitions → blobs → masks → scene graphs → semantic panels → depth/3D → draft image → **executable code** → native positional tokens

**LMD (`2305.13655`):** LLM → captioned boxes → layout-conditioned generate (часто на GLIGEN). Negation 28%→100%, spatial 28%→79%.  
**Главный факт:** layouts сами ~**99%** correct, images только **76–86%** → bottleneck в renderer, не в planner.

**RPG (`2401.11708`):** Recaption → Plan regions → Generate — **гибрид** F1+F3. Spatial на T2I-CompBench почти удваивается.

**Эволюция 2025–26:** GoT/ATLAS (coordinates в reasoning), DraCo (draft-as-CoT), CoCo (code-as-CoT, verifiable), MetaCanvas (plan в latent space), SCoT (ablation text vs boxes).

**Плюсы**
- Лучший рычаг на spatial / count / multi-object.
- Редактируемость: «сдвинь бокс на 20%» (Ranni panel, SLD ops).
- Sample-efficient TTS (ReFocus: 0.84 GenEval при N=4 vs Reflect-DiT 0.81 при N=20).
- Verifiability (особенно code/draft).

**Минусы**
- Renderer bottleneck (LMD 99 vs 76).
- Fidelity/aesthetics trade-off (RealCompo существует именно поэтому).
- Spatial может **подавить** text (ReGround на GLIGEN).
- Boxes — бедный примитив (occlusion, pose, soft location → нужны depth/masks/blobs).
- LLM spatial reasoning слаб на сложных layout’ах (постеры; Uni-RS «spatial reversal curse»).
- Latency ≥ 2 model calls; adapter churn под каждый backbone.
- Долгосрочно SPRIGHT: часть gap чинится data (spatial captions), не inference bridge.

**Когда правильно:** composition/count/position — главный KPI.  
**Когда неправильно:** aesthetic-first short prompts; нет доступа к layout conditioner; base model уже силён на GenEval Position.

---

### F4 — Schema / JSON-native interface

**Идея.** Генератор учится **только** (или преимущественно) на фиксированной схеме атрибутов. Bridge = заполнить форму, не «написать красивее».

**FIBO (`2511.06876`):** ~1000-token JSON fields; DimFusion; TaBR (round-trip controllability).  
**Ideogram 4:** exclusive JSON; CaptionVerifier hard-reject; Magic Prompt = compiler plain→JSON; typed text elements.  
**BBQ (`2602.20672`):** numeric bbox + RGB внутри structured text — «parametric gap»; UI: drag & color picker.  
**Structured Captions (`2507.05300`):** shuffled vs ordered — **структура сама** улучшает adherence.

**Плюсы**
- Disentangled control: поменять одно поле.
- Числа нативно (bbox, hex).
- Diffable / versionable / reproducible artifact.
- Train↔infer format parity максимальная.

**Минусы**
- Нужен **свой** pretraining (дорого).
- Три несовместимых диалекта (FIBO ≠ Ideogram ≠ BBQ) — нет стандарта.
- Casual user всё равно нужен VLM-bridge → его ошибки.
- Нет professional-control benchmark (кроме TaBR).
- Ideogram 4 — vendor blog без peer-reviewed paper.

**Когда правильно:** design tool, brand pipeline, typography, «поменяй только свет».  
**Когда неправильно:** только API чужого prose-модели; нет бюджета на co-train.

---

### F5 — Endogenous CoT (внутри генератора)

**Идея.** Не ставить внешний PE-сервис. Научить checkpoint: подумать/уточнить → нарисовать.

**T2I-R1:** semantic-level CoT + token-level CoT; BiCoT-GRPO.  
**SEER:** Cognitive Gap; self-aligned descriptors; RLVR→RLMT на **~300** samples.  
**HunyuanImage 3:** native CoT schema; T2T / T2TI recipes.  
**Z-Image:** не fully endogenous — PE-aware SFT (генератор учится *на выходах* frozen PE).  
**ShortCoTI:** «visual overthinking» — длинный CoT может **вредить**.

**Плюсы**
- Один деплой; нет рассинхрона двух моделей.
- Capability часто latent → дёшево unlock’ается (SEER, Hunyuan «small specialized set»).
- Хорошо стыкуется с unified MLLM.

**Минусы**
- Нужен post-train генератора (дорого, если не ваш).
- Opacity: Wan `prompt_extend=true` — rewrite невидимый (плохо для audit).
- Visual overthinking / reward hacking.
- Token-level CoT плохо переносится на pure diffusion без AR backbone.
- Не даёт numeric UI само по себе.

**Когда правильно:** владеете training UMM/AR generator.  
**Когда неправильно:** только black-box API; нужен editable intermediate.

---

### F6 — Non-text action space

**Идея.** Рычаг — не новый текст, а **как** conditioning входит в sampler.

| Рычаг | Примеры |
|-------|---------|
| Cross-attention nursing | Attend-and-Excite, SynGen, Predicated Diffusion |
| Token weights + timesteps | PAE |
| Latent-conditioned stepwise prompts | PromptLoop |
| Mixed: rewrite ∪ resample ∪ edit | RAISE |
| Noise / trajectory | ReNO, Noise Projection, CARINOX |
| Negative prompting auto | NPC |

**Attend-and-Excite:** «catastrophic neglect» — возбудить забытые subject tokens; без rewrite.  
**PAE:** online RL по весам слов и injection timesteps.  
**PromptLoop:** prompt обновляется от **latent states** denoising; portable across backbones; mitigates reward hacking.  
**RAISE:** checklist требований + heterogeneous actions; SOTA alignment при *меньшем* числе samples/VLM calls.

**Плюсы**
- Часто training-free / model-agnostic (RAISE, многие attention methods).
- Чинит failure modes, которые текст не выражает.
- Композируется с F1 (ортогонально).
- Не раздувает prompt.

**Минусы**
- Architecture-bound (SD cross-attn ≠ DiT; PAE плохо переносится).
- Per-prompt latency / compute.
- Нет persistent editable artifact.
- Нужен доступ к latents/attention (не все API).
- Be Decisive: внешний layout может конфликтовать с noise-induced prior.

**Когда правильно:** нет права учить генератор; нужен inference-time boost; failure = neglect/binding.  
**Когда неправильно:** нужен стабильный reproducible prompt для продакшн-ассетов.

---

## 3. Сводная таблица плюсов/минусов

| Измерение | F1 Text | F2 Embed | F3 Layout | F4 Schema | F5 Endogenous | F6 Action |
|-----------|---------|----------|-----------|-----------|---------------|-----------|
| Wire | prose | vectors | boxes/plan | JSON/fields | internal CoT | attn/noise/… |
| Портативность API | ★★★★★ | ★★ | ★★★ | ★ | ★ | ★★★★ |
| Human edit / audit | ★★★★★ | ★ | ★★★★ | ★★★★★ | ★ | ★ |
| Spatial/count | ★★ | ★★ | ★★★★★ | ★★★★ | ★★★ | ★★★ |
| Numeric (bbox/RGB) | ★ | ★ | ★★★★ | ★★★★★ | ★ | ★★ |
| Без retrain generator | ★★★★★ | ★★★★ | ★★★★ | ★ | ★ | ★★★★★ |
| Cost inference | низкий–средний | низкий | средний–высокий | низкий | низкий+CoT | высокий |
| Главный риск | intent drift | opacity | renderer bottleneck; text suppressed | schema lock-in | overthinking; opacity | latency; no persistence |

---

## 4. Как выбирать (decision tree)

```
Владеете pretraining генератора?
 ├─ YES, и нужен design-UI / числа  → F4 Schema (+ тонкий F1 compiler)
 ├─ YES, unified MLLM/AR            → F5 Endogenous (± layout tokens ATLAS)
 └─ NO
     Нужен только API prose-модели?
      ├─ Spatial/count критичны?
      │    ├─ YES, есть layout conditioner → F3 (+ optional F1 recaption)
      │    └─ YES, нет layout             → F1 typed repair (TARA) + F6 attention
      ├─ Нужен видимый текст / compliance → F1 с gating + показать revised
      ├─ Есть доступ к embeddings/latents → F2 connector или F6 PromptLoop/RAISE
      └─ Макс. портативность, минимум интеграции → F1 (APE/PromptEnhancer-class)
```

**Практический default 2026 для продукта на чужом генераторе:**  
`F1 gated rewriter` + опционально `F6 RAISE/attention` на сложных промптах.  

**Практический default если свой foundation model:**  
`F4 или F5` как основной bridge; F1 только как UX-компилятор в схему/CoT.

---

## 5. Главные результаты области (load-bearing facts)

1. **Bridge ≠ обязательный rewrite.** PEZ/ELLA/LMD/Attend-and-Excite доказали альтернативные action spaces ещё в 2023.
2. **Text CoT ≠ boxes** (SCoT): разные gains; стек выгоднее выбора «или».
3. **Planner ≫ renderer** в классическом LMD (99% vs 76%) — улучшать надо исполнение layout.
4. **Structure beats shuffled content** (Structured Captions) — порядок полей = сигнал.
5. **Naive LLM encoder hurts** (LI-DiT) — F2 требует careful connector design.
6. **Rewrite can hurt humans** (GenEval 2) — evaluate vs original; gate.
7. **Spatial channel can kill text channel** (ReGround).
8. **Endogenous is cheap to unlock** (SEER 300 samples; Hunyuan small CoT set) — но opaque.
9. **Mixed actions > single lever** (RAISE).
10. **Families compose** (citation graph): F4 needs F5 executor historically; F1 targets F4 schema in APE←FIBO; 2026 hybrids (ATLAS, RAISE) — куда идёт поле.
11. **No dedicated bridge survey** — taxonomy выше закрывает дыру для builders.
12. **Historical drift:** 2023 external/training-free → 2024 learned middle module → 2025–26 internalized CoT / agent loops.

---

## 6. Citation map (сжато)

Полные деревья: [`research/bridge-methods/citation_trees/bridge_hubs.json`](./research/bridge-methods/citation_trees/bridge_hubs.json).

| Seed | Family | ~cites (S2, 2026-07) | Роль |
|------|--------|----------------------|------|
| GLIGEN `2301.07093` | layout executor | ~969 | backend для LMD+ |
| Attend-and-Excite `2301.13826` | F6 | ~871 | GSN / neglect |
| ELLA `2403.05135` | F2 | ~428 | LLM connector hub |
| PEZ `2302.03668` | F2 soft↔hard | ~429 | outlier→safety; T2I-ближе DPO-Diff |
| LMD `2305.13655` | F3 | ~269 | boxes bridge root |
| RPG `2401.11708` | F3+F1 | ~257 | hinge planning↔RL |
| T2I-R1 `2505.00703` | F5 | ~159 | endogenous RL |
| PAE `2404.04095` | F6 | ~54 | weights+timesteps |
| PromptEnhancer `2509.04545` | F1 | ~32 | textual hub→agents |
| FIBO `2511.06876` | F4 | ~11 | schema; cited by APE |
| SEER `2601.20305` | F5 | ~4 | Cognitive Gap |
| APE `2606.00204` | F1 | 0 | newest agentic PE |

**Cross-family hubs:** NPC `2512.07702` (8 seeds), GenArtist, SOAR, MetaPoint, SCoT.

**Сильные co-citation кластеры:** GLIGEN↔A&E↔LMD↔RPG — один разговор о compositionality; ELLA мост в LLM-encoder; T2I-R1 мост в RL.

---

## 7. Must-read маршрут (bridge-centric)

### День 1 — понять пространство
1. Этот отчёт §0–3  
2. SCoT `2602.11980` — ablation text vs boxes  
3. Controllable T2I survey `2403.04279`

### День 2 — F1 vs альтернативы
4. PromptEnhancer / APE (текстовый потолок)  
5. ELLA + LI-DiT (embeddings + ловушка)  
6. LMD + RPG (layout)

### День 3 — schema & endogenous
7. FIBO + BBQ + Structured Captions  
8. T2I-R1 + SEER + ShortCoTI  

### День 4 — action space & hybrids
9. Attend-and-Excite + RAISE + PromptLoop  
10. ATLAS / MetaCanvas (куда сходится поле)  
11. GenEval 2 + ReGround + Be Decisive (ограничители)

---

## 8. Открытые дыры (research + engineering)

1. **Нет head-to-head** JSON-native vs NL при matched backbone/data/token budget (кроме маленького `2507.05300`).  
2. **Нет schema standard** между FIBO / Ideogram / BBQ.  
3. **Нет professional-control benchmark** (single-attribute hold-out); TaBR почти одинок.  
4. **Auditability endogenous CoT** почти не исследована.  
5. **Dedicated bridge survey** отсутствует — это и есть novelty claim для обзора.  
6. Ideogram 4 — важнейший F4 data point без paper.

---

## 9. Норматив для builders (коротко)

1. Сначала назовите **какой gap** (G1–G6) — от этого семья.  
2. Wire = то, на чём учился генератор; не навязывайте JSON prose-модели.  
3. Структура внутри bridge полезна даже если наружу уходит prose.  
4. Не выбирайте «только текст» или «только boxes» — SCoT говорит стекать.  
5. Gating обязателен для F1; accept-or-revert для дорогих F3/F6.  
6. Если свой training и design-UI — инвестируйте в F4/F5, а не в вечный purple-prose rewriter.  
7. Оценивайте против **original** user prompt (GenEval 2).

---

## Источники и артефакты

- Корпус: [`research/bridge-methods/corpus/bridge_methods_corpus.json`](./research/bridge-methods/corpus/bridge_methods_corpus.json)  
- Citation trees: [`research/bridge-methods/citation_trees/bridge_hubs.json`](./research/bridge-methods/citation_trees/bridge_hubs.json)  
- Outline/fields: [`research/bridge-methods/outline.yaml`](./research/bridge-methods/outline.yaml), [`fields.yaml`](./research/bridge-methods/fields.yaml)  
- Каталог чтения: [`papers_catalog_bridge_methods.md`](./papers_catalog_bridge_methods.md)

Связанные предыдущие отчёты по textual PE остаются валидны как углубление **F1**; этот документ — карта **всех** семейств bridge.
