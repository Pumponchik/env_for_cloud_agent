# Современный взгляд: закрытие gap между user prompt и входом генератора

**Дата:** 2026-07-30  
**Фокус:** только работы, которые **сами объясняют**, как превратить короткий/недоспецифицированный user prompt во вход, который ожидает T2I/T2V модель.  
**Описания:** Problem / Method / Result — близко к формулировкам авторов, без моей трактовки.  
**Старые работы (2023–24):** вынесены в §D «Развитие области» — для контекста и citation trees, не для текущего ядра.

Проверено сабагентами по большому корпусу arXiv 2025–2026 + tech reports ключевых лабораторий + citation descendants PromptEnhancer / Input-Side Scaling / APE / Wan.

Связанные файлы: [`report_reprompt_system_architecture_2026.md`](./report_reprompt_system_architecture_2026.md).

---

## Как устроена область сейчас (структура)

Современные системы закрывают gap тремя разными способами (это видно из самих работ, не из интерпретации):

| Тип bridge | Что делают авторы | Примеры |
|------------|-------------------|---------|
| **External rewriter** | Отдельный LLM/VLM переписывает prompt; генератор frozen | APE, PromptEnhancer, Input-Side Scaling, RePrompt, Wan/Qwen/Seed PE |
| **Structured interface** | Вход генератора = schema (JSON / fields / boxes), short text → заполнить schema | FIBO, Ideogram 4, BBQ, Structured Captions |
| **Native / endogenous** | Rewrite/thinking внутри генератора (CoT tokens) | HunyuanImage 3, T2I-R1, SEER, Z-Image PE-aware SFT |

Общий мотив в текстах лабораторий: **user prompt ≠ training caption distribution** → нужен модуль, который приводит вход к тому, на чём модель училась.

---

# A. Ядро P0 — читать в первую очередь

Работы главных игроков и/или наиболее чётко структурированные статьи про gap.

### 1. APE — Agentic Prompt Enhancer · **NVIDIA**
https://arxiv.org/abs/2606.00204 · 2026 · NVIDIA + UMichigan · https://research.nvidia.com/labs/sil/projects/ape/

**Проблема:** visual systems «highly sensitive to prompt formulation»; сильные enhancers зависят от proprietary LLM → cost/latency/deployment dependence; enhancement как «trainable component rather than a peripheral user choice».  
**Метод:** post-train small LMs. **SAPE** — one-pass rewrite. **MAPE** — router → rewriter → composer для objects/attributes/spatial/edits. GRPO/GDPO; visual model frozen.  
**Результат:** small post-trained enhancers лучше base; сужают gap к closed-source; MAPE сильнее на compositional.  
**Gap:** trainable deployable rewriter без гигантского LLM.

---

### 2. PromptEnhancer · **Tencent Hunyuan**
https://arxiv.org/abs/2509.04545 · 2025 · CVPR 2026

**Проблема:** attribute binding, negation, compositional relationships → mismatch user intent vs output.  
**Метод:** universal CoT rewriter; AlignEvaluator по taxonomy **24 key points**; SFT→RL; веса генератора не трогают.  
**Результат:** улучшение alignment на HunyuanImage 2.1; новый human preference benchmark.  
**Gap:** decoupled rewriter + fine-grained failure taxonomy.

---

### 3. Qwen-Image-2.0 · Prompt Enhancer · **Alibaba Qwen**
https://arxiv.org/abs/2605.10730 · 2026 · §3.3

**Проблема:** для posters/infographics/typography качество зависит от layout/hierarchy в prompt; user prompts «vary substantially in granularity».  
**Метод:** PE переписывает в structured detail-rich prompts; data = reverse-engineering (fine → degrade → short) → (P_short, CoT, P_fine); Qwen3.5-9B SFT→GRPO через frozen generator.  
**Результат:** авторы: PE improves generation quality, prompt following, reasoning; data flywheel имеет отдельный «prompt engineering track».  
**Gap:** явная инверсия caption→user prompt как обучение rewrite.

---

### 4. Seedream 2.0 / 4.0 · PE · **ByteDance Seed**
- 2.0: https://arxiv.org/abs/2503.07703 · §4.4  
- 4.0: https://arxiv.org/abs/2509.20427  

**Проблема (2.0, слова отчёта):** user prompt «simple and uncluttered»; diffusion trained on high-quality captions «much more complicated» → «recalibrate user prompts to match the model's preferences».  
**Метод 2.0:** SFT bilingual LLM на ⟨u, r⟩ + PE RLHF (SimPO) по aesthetics/alignment.  
**Результат 2.0:** ~+30% aesthetic, ~+5% alignment, рост diversity (по отчёту).  
**Метод 4.0:** VLM PE на Seed1.5-VL: task routing + rewrite (auto-thinking) + aspect ratio; AdaCoT budgets.  
**Gap:** каноническая lab-формулировка mismatch train captions vs user text.

---

### 5. Seedance 1.0 · PE · **ByteDance Seed**
https://arxiv.org/abs/2506.09113 · §2.4

**Проблема:** DiT texts = dense video captions → LLM must convert user prompts to caption format.  
**Метод:** Qwen2.5-14B; SFT на (user, dense caption); затем DPO из‑за hallucinations после SFT.  
**Результат:** «precise… rephrased results in video caption format, consistent with DiT training».  
**Gap:** gap как **format translation** user→training caption.

---

### 6. Wan · Prompt Alignment / `prompt_extend` · **Alibaba**
https://arxiv.org/abs/2503.20314 · repo Wan2.1 · DashScope `prompt_extend` default true

**Проблема:** users prefer concise prompts «significantly shorter than the training captions».  
**Метод:** rewrite к distribution training captions; структура style → abstract → detailed; Qwen2.5-Plus; CLI `--use_prompt_extend`.  
**Результат:** manual evaluation — after extension лучше; API включает extend by default.  
**Gap:** прямое align to training caption distribution + целевая schema rewrite.

---

### 7. NVIDIA Cosmos · Prompt Upsampler
https://arxiv.org/abs/2501.03575 · HF `Cosmos-1.0-Prompt-Upsampler-12B-Text2World`

**Проблема (слова paper):** training prompts from VLM «follow a different distribution of human descriptions» → domain gap.  
**Метод:** Mistral-NeMo-12B-based upsampler: human text → preferred by diffusion WFMs; default on; skip если уже длинный (`word_limit_to_skip_upsampler`).  
**Результат:** documented pipeline stage; enriched consistent structure before generation.  
**Gap:** shipped default-on converter human→model-preferred.

---

### 8. HunyuanImage 3.0 · native CoT rewrite · **Tencent**
https://arxiv.org/abs/2509.23951

**Проблема/метод:** automated CoT: interpret prompt → intermediate thinking (refinement/rewriting) → synthesize; T2T + T2TI data.  
**Результат:** native CoT «improves multimodal performance significantly»; open 80B MoE.  
**Gap:** rewrite **внутри** генератора, не внешний сервис.

---

### 9. Input-Side Inference-Time Scaling
https://arxiv.org/abs/2510.12041 · 2025 · ByteDance/TikTok + UMD

**Проблема:** underspecified prompts → suboptimal alignment/aesthetics/quality.  
**Метод:** LLM rewriter; iterative DPO **без SFT**; composite rewards.  
**Результат:** improves alignment/quality/aesthetics; transfer across backbones; gains scale with rewriter LLM size.  
**Gap:** PE как portable **input-side scaling**.

---

### 10. RePrompt · **Microsoft**
https://arxiv.org/abs/2505.17540 · 2025

**Проблема:** short/under-specified prompts; prior LLM enhancement → stylistic/unrealistic without visual grounding.  
**Метод:** RL на image-level outcomes; structured self-reflective prompts; rewards: preference, semantic alignment, visual composition.  
**Результат:** SOTA claims на GenEval / T2I-CompBench spatial & compositional.  
**Gap:** reasoning+RL против short prompts, не aesthetic-only.

---

### 11. FIBO · **BRIA AI**
https://arxiv.org/abs/2511.06876 · 2025

**Проблема:** short prompts → detailed images gap; missing details filled arbitrarily, bias to average preferences.  
**Метод:** T2I trained on long **structured** captions (same fine-grained attributes); DimFusion; TaBR.  
**Результат:** SOTA open-source prompt alignment (по авторам); public weights.  
**Gap:** bridge = fill fixed attribute schema, не «писать красивее».

---

### 12. Ideogram 4 · JSON + Magic Prompt · **Ideogram**
docs + OSS `ideogram4`

**Проблема (слова docs):** trained exclusively on structured JSON; plain text «will not work»; plain → Magic Prompt → JSON.  
**Метод:** schema (`high_level_description`, `style_description`, `compositional_deconstruction` + bbox/colors); Magic Prompt LLM default.  
**Результат:** training and inference share one prompt format.  
**Gap:** rewriter обязателен как compiler в schema.

---

### 13. FLUX.2 · Prompt Upsampling · **Black Forest Labs**
https://github.com/black-forest-labs/flux2/blob/main/docs/flux2_with_prompt_upsampling.md

**Метод:** VLM expand/enrich before generation; modes none/local/openrouter; preserve intent; separate T2I vs I2I system messages.  
**Scope (слова docs):** особенно для reasoning-heavy / text-in-image / image instructions; для «a red car» — little benefit.  
**Gap:** optional, scoped upsampling с явным when/when-not.

---

### 14. TARA — One Rewrite to Fix Them All?
https://arxiv.org/abs/2607.18724 · 2026

**Проблема:** heterogeneous failures absorbed into one uniform expansion, though each needs different repair language.  
**Метод:** atomic repair allocation; type-conditioned operators; diagnosis → allocation → compilation → accept-or-revert gate. Training-free.  
**Результат:** best DSG/TIFA во всех 8 cells; +5.6/+2.6 vs VisualPrompter; 16.0s vs 20.0s.  
**Gap:** typed repair вместо одного rewrite.

---

### 15. FaithRewriter — Seeing is Believing
https://arxiv.org/abs/2606.08492 · 2026

**Проблема:** intent–generation gap; polish без visual grounding → over-infer.  
**Метод:** image from raw prompt as visual cue → grounded augmentation → distill small LLM.  
**Результат:** more faithful / visually plausible vs strong baselines.  
**Gap:** visual anchor против textual hallucination.

---

### 16. Brack et al. — How to Train Your T2I Model
https://arxiv.org/abs/2506.16679 · 2025 · Adobe + TU Darmstadt

**Проблема:** synthetic captions популярны, design choices не изучены.  
**Метод:** systematic variation of captioning strategies.  
**Результат:** dense captions → alignment↑, aesthetics/diversity trade-offs; **randomized lengths** → balanced without diversity collapse.  
**Gap:** supply side — какой caption law должен целиться rewriter.

---

### 17. OpenAI Images · `revised_prompt`
Developer docs 2025–2026

**Метод:** mainline model (gpt-5.x / o-series) automatically revises prompt; image model renders; `revised_prompt` returned.  
**Gap:** largest-deployment instance: rewrite model ≠ render model.

---

# B. P1 — сильные современные (расширение ядра)

| Работа | Ссылка | О чём говорит статья (кратко) |
|--------|--------|-------------------------------|
| **VisualPrompter** | `2506.23138` | Gap user vs model-preferred; neglect semantics; training-free atomic repair of missing concepts. |
| **Wan-Image PE** | `2604.19858` | PE + selective activation (typography/posters/UI…); non-CoT vs CoT variants. |
| **Z-Image PE** | `2511.22699` | PE compensates small model; PE-aware SFT — generator trained on PE outputs. |
| **ERNIE-Image PE** | `2605.25347` | Lightweight PE: concise intent → structured visual descriptions; open weights. |
| **RAPO / RAPO++** | `2504.11739` / `2510.20206` | User prompts misaligned with training; retrieval modifiers + test-time SSPO + distill rewriter. |
| **VPO** | `2503.20491` | T2V: train detailed vs user concise; principles harmless/accurate/helpful. |
| **ReaDe (Kling)** | `2511.20563` | Reason-then-describe interpreter; ambiguity → actionable specs. |
| **PRIS** | `2512.03534` | Visual scaling plateaus if prompt fixed; redesign prompt from failure patterns. |
| **PromptRL** | `2602.01382` | Prompt overfitting in flow RL; trainable rewrite agent inside RL loop. |
| **SEER** | `2601.20305` | Cognitive Gap in UMM; endogenous self-aligned descriptors. |
| **T2I-R1** | `2505.00703` | Semantic-level CoT planning + token-level CoT; BiCoT-GRPO. |
| **BBQ** | `2602.20672` | Parametric gap; boxes+RGB in structured text; intent → structured language → renderer. |
| **SCOPE** | `2605.08043` | Conceptual Rift; evolving structured specification + conditional repair skills. |
| **PromptLoop** | `2510.00430` | Step-wise refine from latent states; not one feed-forward rewrite. |
| **PRISM (self-reward)** | `2607.24353` | Image-grounded diagnosis; hybrid multi-objective self-reward. |
| **GenPilot** | `2510.07217` | Multi-agent test-time APO; error analysis + memory. |
| **Maestro** | `2509.10704` | Self-critique + evolution; correct under-specification; preserve intent. |
| **Qwen-Image-Agent** | `2606.26907` | Context Gap; planning + grounding (search/memory/feedback). |
| **CRAFT** | `2512.20362` | Constraint-structured verify; targeted prompt updates only. |
| **RAISE** | `2603.00483` | Rewrite as one action among resampling/editing; requirement checklist. |
| **T2I-Copilot** | `2507.20536` | Input Interpreter → standardized report → generate → evaluate. |
| **Structured Captions 19M** | `2507.05300` | Fixed 4-part template > shuffled; structure improves adherence. |
| **Self-Rewarding LVLMs** | `2505.16763` | Unified solver+reward LVLM; AI feedback. |
| **Sem-DPO** | `2507.20133` | Bound semantic drift of preference-tuned prompt generators. |
| **PAG (GFlowNets)** | `2502.11477` | Mode collapse in RL rewrite; sample diverse prompts. |
| **VERIFI / UniFusion** | `2510.12789` | In-model VLM rewriting; condition on rewrite tokens. |
| **DetailMaster** | `2505.16915` | Long prompts (~285 tok); expansion alone insufficient without long-prompt training. |
| **GenEval 2** | `2512.16853` | Rewriting decreases human alignment on 4/6 models; evaluate vs original. |
| **MOVA** | `2602.08794` | Prompt enhancement as primary stage; with/without ablation. |
| **Kling-Omni PE** | `2512.16776` | PE bridges heterogeneous user inputs ↔ model representations. |
| **TIPO** | `2411.08127` | (Nov 2024 / ICLR 2026) distribution-aligned presampling — borderline; держать как мост к 2025. |

---

# C. Отрицательные / ограничивающие результаты (нужны)

| Работа | Ссылка | Claim авторов |
|--------|--------|---------------|
| **T2ICountBench** | `2503.06884` | Prompt refinement generally **cannot** fix counting. |
| **DialectGen** | `2510.14949` | Prompt rewriting helps dialects only slightly; may hurt SAE. |
| **Prompt complexity study** | `2510.19557` | Higher complexity ↓ diversity & consistency; expansion raises aesthetics/diversity vs baselines. |
| **GenEval 2** | `2512.16853` | Rewriting ≠ always better for humans. |

---

# D. Развитие области (2023–2024) — не ядро

Эти работы **не** в современном основном списке. Нужны чтобы видеть направление движения и искать потомков в citation trees.

| Год | Работа | Роль в развитии |
|-----|--------|-----------------|
| 2022–23 | **Promptist** `2212.09611` | Первая постановка: adapt user → model-preferred; SFT→RL. |
| 2023 | **DALL·E 3 Better Captions** PDF | Synthetic long captions + GPT upsample → индустриальный корень PE. |
| 2023 | **BeautifulPrompt** `2311.06752` | Aesthetic RL rewriter; позже baseline, часто бьёт семантику. |
| 2023 | **RECAP** `2310.16656` | Training-side recaption; train–inference discrepancy. |
| 2023 | **Idea2Img** `2310.08541` | VLM iterative self-refine. |
| 2023–24 | **LMD** `2305.13655` / **RPG** `2401.11708` | Layout/plan вместо (или рядом с) prose rewrite. |
| 2023–24 | **OPT2I** `2403.17804` | Training-free iterative consistency optimization. |
| 2023–24 | **Prompt Expansion** `2312.16720` | Diversity-oriented expansion (Google). |
| 2024 | **PAE** `2404.04095` | Weights + timesteps как action space. |
| 2024 | **Parrot** `2401.05675` | Multi-reward + original-prompt guidance. |
| 2024 | **UF-FGTG** `2402.12760` | Novice vs model-preferred length gap. |
| 2024 | **ELLA** `2403.05135` | Dense prompts через LLM adapter (альтернатива rewrite). |
| 2024 | **DSG / TIFA / ImageReward / PickScore / HPS** | Evaluation & reward substrate для поздних PE. |
| 2024 | **The Prompt Report** `2406.06608` | Общая taxonomy prompting (не T2I-PE handbook). |

**Куда шла область (по этим работам → 2025–26):**  
ручной craft → aesthetic RL rewrite → train на synthetic captions → **явный distribution alignment** → fine-grained / visual-grounded / typed repair → **schema-native generators** и **endogenous CoT**.

---

# E. Моё видение (отдельно)

Не утверждения статей:

1. Современный правильный вопрос не «как удлинить prompt», а **какой артефакт генератор был обучен потреблять** и как туда скомпилировать user intent.  
2. У больших игроков (NVIDIA, ByteDance, Alibaba, Tencent, BFL, Ideogram, OpenAI, Google Vertex/Cosmos) PE уже **именованный stage** — читать их tech reports важнее, чем старые NeurIPS-2023 baselines.  
3. Три живых ветки: external RL rewriter · JSON/schema interface · native CoT. Выбирать по контролю над training.  
4. Обязательные ограничители: GenEval 2, counting paper, DetailMaster — без них легко переоценить rewrite.

---

## Маршрут чтения (современный)

1. Seedream 2.0 §PE / Wan §prompt / Cosmos upsampler — **зачем** (словами labs)  
2. APE (NVIDIA) + PromptEnhancer + Qwen-Image-2.0 PE — **как учить external rewriter**  
3. FIBO + Ideogram 4 — **когда schema = вход**  
4. HunyuanImage 3 / T2I-R1 / SEER — **когда rewrite внутри модели**  
5. TARA + FaithRewriter + VisualPrompter — **как не ломать intent**  
6. Brack + GenEval 2 + DetailMaster — **закон train captions и метрики**

Старые 23–24 — только после этого, как предыстория / для citation crawl.
