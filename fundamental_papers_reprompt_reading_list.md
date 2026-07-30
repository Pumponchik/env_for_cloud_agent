# Подборка фундаментальных работ по re-prompt / prompt enhancement для T2I

**Дата:** 2026-07-30  
**Принцип отбора:** как в партшколе — берём работы, которые **сами хорошо объясняют тему**, и пересказываем **что утверждает статья**, а не мою трактовку.  
**В конце:** краткая история области и отдельно помеченное **моё видение**.

Охват этого файла: **~65 позиций** (статьи + tech reports + ключевые product docs).  
Связанные файлы: [`report_reprompt_system_architecture_2026.md`](./report_reprompt_system_architecture_2026.md), [`papers_catalog_reprompt.md`](./papers_catalog_reprompt.md).

---

## Как читать

| Уровень | Зачем |
|--------|--------|
| **A. Ядро (~15)** | Если читать мало — только это. Статьи, которые задают язык области. |
| **B. Расширение** | Больше методов, IR, evaluation, labs. |
| **C. История + видение** | Куда шла область и куда, на мой взгляд, идёт. |

В карточках формат: **Проблема / Метод / Результат** — близко к формулировкам авторов.

---

# A. Ядро — фундаментальные работы, которые хорошо рассказывают тему

### A1. Promptist — Optimizing Prompts for Text-to-Image Generation
**Ссылка:** https://arxiv.org/abs/2212.09611 · NeurIPS 2023 · Microsoft Research  

**Проблема (слова статьи):** performant prompts «often model-specific and misaligned with user input».  
**Метод:** framework *prompt adaptation* — SFT языковой модели на manually engineered prompts, затем RL; reward поощряет aesthetics при сохранении user intentions.  
**Результат:** на Stable Diffusion лучше manual prompt engineering по automatic metrics и human preference; RL особенно помогает на out-of-domain prompts.  
**Почему в ядре:** первая чёткая постановка «адаптировать user input → model-preferred prompt».

---

### A2. Improving Image Generation with Better Captions (DALL·E 3)
**Ссылка:** https://cdn.openai.com/papers/dall-e-3.pdf · OpenAI  

**Проблема:** модели плохо следуют детальным описаниям; гипотеза — noisy/inaccurate training captions.  
**Метод:** свой captioner → recaption датасета; DALL·E 3 учится на смеси **95% synthetic / 5% ground truth**. В §3.5: GPT-4 «upsample» коротких captions в highly descriptive.  
**Результат:** улучшение prompt following; сравнение Drawbench/CLIP vs DALL·E 2 и SDXL в отчёте.  
**Почему в ядре:** индустриальный источник тезиса «длинные synthetic captions → нужен upsample на инференсе».

---

### A3. BeautifulPrompt
**Ссылка:** https://arxiv.org/abs/2311.06752 · EMNLP 2023 · SCUT + Alibaba  

**Проблема:** «multiple passes of prompt engineering by humans» для приемлемого результата.  
**Метод:** генеративная модель short→high-quality prompts; затем RL with Visual AI Feedback по PickScore + Aesthetic Scores.  
**Результат:** авторы сообщают существенный рост качества prompts и images; интеграция в cloud AI platform.  
**Почему в ядре:** канон эстетического RL-rewriter’а (позже часто используют как baseline).

---

### A4. Prompt Expansion for Adaptive Text-to-Image Generation
**Ссылка:** https://arxiv.org/abs/2312.16720 · ACL 2024 · Google Research  

**Проблема:** модели мощные, но сложны в использовании; выходы часто repetitive.  
**Метод:** один query → **набор** expanded prompts; датасет через invert high-aesthetic images → text + few-shot; PaLM 2; iterative re-fine-tune.  
**Результат:** human study — более aesthetic и diverse, чем baselines.  
**Почему в ядре:** явно ставит **diversity** как цель expansion, не только «длиннее».

---

### A5. OPT2I — Improving Text-to-Image Consistency via Automatic Prompt Optimization
**Ссылка:** https://arxiv.org/abs/2403.17804 · TMLR · Meta FAIR / Mila  

**Проблема:** слабости по quantities, relations, attributes; fine-tuning и локальный поиск дают плохие trade-offs.  
**Метод:** optimization-by-prompting: LLM итеративно правит prompt, максимизируя consistency score.  
**Результат:** до **+24.9% DSG** на PartiPrompts при сохранении FID и росте recall.  
**Почему в ядре:** training-free iterative loop как отдельное семейство.

---

### A6. TIPO — Text to Image with Text Presampling for Prompt Optimization
**Ссылка:** https://arxiv.org/abs/2411.08127 · ICLR 2026  

**Проблема/метод (слова статьи):** лёгкая pretrained-модель расширяет prompts, семплируя refined prompts из targeted sub-distribution semantic space, «preserving the original intent». Альтернатива тяжёлым LLM/RL.  
**Результат:** stronger text alignment, fewer artifacts, higher human preference; акцент на **distribution-aligned prompt engineering**.  
**Почему в ядре:** формализует цель «выровнять к train distribution», не «максимизировать verbosity».

---

### A7. RePrompt — Reasoning-Augmented Reprompting via RL
**Ссылка:** https://arxiv.org/abs/2505.17540 · Microsoft / Xiamen  

**Проблема:** короткие prompts; LLM-enhancement часто даёт stylistic/unrealistic content без visual grounding.  
**Метод:** LM учится генерировать structured self-reflective prompts через RL на image-level outcomes (preference, semantic alignment, visual composition); без human-annotated data.  
**Результат:** SOTA-заявления на GenEval и T2I-CompBench по spatial/compositional.  
**Почему в ядре:** reasoning + RL как современный шаблон.

---

### A8. PromptEnhancer (Tencent Hunyuan)
**Ссылка:** https://arxiv.org/abs/2509.04545 · CVPR 2026 camera-ready retitled *Taming Your Rewriter…*  

**Проблема:** attribute binding, negation, compositional relationships.  
**Метод:** model-agnostic CoT rewriter; AlignEvaluator по taxonomy **24 key points**; SFT → RL (GRPO); генератор не трогают.  
**Результат:** улучшение alignment на HunyuanImage 2.1; новый human preference benchmark.  
**Почему в ядре:** лучшая публичная fine-grained reward taxonomy для PE.

---

### A9. Improving T2I with Input-Side Inference-Time Scaling
**Ссылка:** https://arxiv.org/abs/2510.12041 · UMD + ByteDance  

**Проблема:** underspecified prompts → плохие alignment/aesthetics/quality.  
**Метод:** LLM rewriter; iterative DPO **без SFT**; composite rewards.  
**Результат:** улучшения alignment/quality/aesthetics; transferability между backbones; scaling с размером rewriter LLM.  
**Почему в ядре:** называет PE **input-side inference-time scaling** и измеряет transfer/scaling.

---

### A10. APE — Agentic Prompt Enhancer (**NVIDIA**)
**Ссылка:** https://arxiv.org/abs/2606.00204 · Project: https://research.nvidia.com/labs/sil/projects/ape/ · NVIDIA + UMichigan  

**Проблема (слова статьи):** visual systems «highly sensitive to prompt formulation»; сильные enhancers опираются на proprietary LLM (ChatGPT/Gemini) → cost, latency, deployment dependence. Prompt enhancement предлагается как **trainable component**, не «peripheral user choice».  
**Метод:** post-train **small** LMs as agents. **SAPE** — one-pass rewrite. **MAPE** — router → rewriter → composer для compositional constraints (objects, attributes, spatial, edits). Task-aware rewards; GRPO / GDPO. Downstream visual model **frozen**.  
**Результат:** post-trained small enhancers лучше base counterparts и сужают gap к closed-source enhancers; MAPE сильнее на complex compositional.  
**Почему в ядре:** одна из самых чётко описанных современных системных работ; прямо отвечает «как строить trainable PE без гигантского LLM».

---

### A11. FaithRewriter — Seeing is Believing
**Ссылка:** https://arxiv.org/abs/2606.08492  

**Проблема:** intent–generation gap; text-only polish без visual grounding → over-infer missing details.  
**Метод:** image from original prompt as visual cue → LLM grounded augmentation → distill в small LLM.  
**Результат:** prompts more faithful / visually plausible vs strong baselines.  
**Почему в ядре:** статья сама формулирует опасность «слепого» expansion.

---

### A12. VisualPrompter
**Ссылка:** https://arxiv.org/abs/2506.23138 · ICLR 2026  

**Проблема:** prior PE улучшает style/aesthetics, но neglect semantic alignment → «visually appealing but content-wise unsatisfying».  
**Метод:** training-free; self-reflection находит absent concepts; target-specific atomic repair; deconstruct → insert → reassemble.  
**Результат:** SOTA на text–image alignment benchmarks; plug-and-play.  
**Почему в ядре:** atomic semantic repair vs holistic rewrite.

---

### A13. TARA — One Rewrite to Fix Them All?
**Ссылка:** https://arxiv.org/abs/2607.18724  

**Проблема:** optimizers «absorb heterogeneous failures into one uniform prompt expansion», хотя каждому типу нужна своя repair language.  
**Метод:** atomic repair allocation; type-conditioned operators; diagnosis → allocation → compilation → semantic repair gate (accept-or-revert). Training-free.  
**Результат:** best semantic accuracy во всех 8 cells DSG/TIFA × 4 generators; +5.6 DSG / +2.6 TIFA vs VisualPrompter; 16.0s vs 20.0s.  
**Почему в ядре:** самая прямая критика «одного rewrite на всё».

---

### A14. FIBO — Generating an Image From 1,000 Words
**Ссылка:** https://arxiv.org/abs/2511.06876 · BRIA AI  

**Проблема:** модели map short prompts → detailed images → gap; missing details filled arbitrarily, bias to average preferences.  
**Метод:** open T2I trained on **long structured captions** с одним набором fine-grained attributes; DimFusion; TaBR protocol.  
**Результат:** SOTA prompt alignment среди open-source (по заявлению авторов); weights public.  
**Почему в ядре:** показывает путь **JSON/schema как train+infer interface**, не только prose rewrite.

---

### A15. Wan — Prompt Alignment (§ tech report)
**Ссылка:** https://arxiv.org/abs/2503.20314 · Alibaba  

**Проблема (слова отчёта):** user prompts «significantly shorter than the training captions» → distribution mismatch.  
**Метод:** rewrite к distribution training captions; принципы: details without altering meaning; natural motion; структура style → abstract → detailed; Qwen2.5-Plus.  
**Результат:** авторы: LLMs with strong instruction-following generate suitable prompts that enhance video generation.  
**Почему в ядре:** самая прямая lab-формулировка цели PE = align to training captions.

---

### A16. Brack et al. — How to Train Your Text-to-Image Model
**Ссылка:** https://arxiv.org/abs/2506.16679 · Adobe / TU Darmstadt  

**Проблема:** synthetic captions популярны, но design choices плохо изучены.  
**Метод:** systematic variation of synthetic captioning strategies.  
**Результат:** dense high-quality captions → alignment↑, aesthetics/diversity trade-offs; **randomized lengths** → balanced improvements без collapse diversity.  
**Почему в ядре:** контролируемый ответ, *какое* caption distribution должен целиться rewriter.

---

### A17. GenEval 2
**Ссылка:** https://arxiv.org/abs/2512.16853 · Meta FAIR et al.  

**Проблема:** benchmark drift; GenEval saturated.  
**Результат по rewriting (слова статьи):** across 6 models с rewriting techniques, rewritten prompts **decrease human alignment for 4 models** by ~2.5% avg; increase for 2 by ~3.3%. Protocol: evaluate image against **original** prompt.  
**Почему в ядре:** показывает, что rewrite — не безусловное благо; нужна per-backbone проверка.

---

### A18. RECAP
**Ссылка:** https://arxiv.org/abs/2310.16656 · Google  

**Проблема:** web alt-text captions low quality.  
**Метод:** automatic recaptioning + train T2I on recaptioned data.  
**Результат:** FID 14.84 vs 17.87; +64.3% faithful generation (human); лучше object/counting/position metrics. Claim: reduces train–inference discrepancy и повышает sample efficiency.  
**Почему в ядре:** training-side близнец inference PE.

---

# B. Расширенный каталог (больше охвата)

## B1. Методы PE / rewrite (ещё)

| Работа | Ссылка | О чём говорит статья |
|--------|--------|----------------------|
| **PAE** | `2404.04095` | Автоматизирует не только текст, но **weights и injection timesteps**; RL на aesthetic/consistency/preference. |
| **RAPO** | `2504.11739` | T2V: dual branches — relation-graph modifiers + LLM rewrite; выбор лучшего. |
| **RAPO++** | `2510.20206` | Три стадии: data-aligned refine → test-time SSPO → fine-tune rewriter LLM. |
| **Parrot** | `2401.05675` | Joint multi-reward RL T2I + prompt expansion; original-prompt-centered guidance. |
| **UF-FGTG** | `2402.12760` | Coarse–fine prompt dataset; user-friendly automated optimization; +~5% aesthetic metrics. |
| **NeuroPrompts** | `2311.12229` | Constrained decoding под human-engineered style; user control via constraints. |
| **Idea2Img** | `2310.08541` | GPT-4V iterative self-refine с memory quirks модели. |
| **Self-Rewarding LVLMs** | `2505.16763` | Один LVLM = solver + reward; AI feedback; iterative RL. |
| **PromptLoop** | `2510.00430` | Step-wise prompt refine по latent feedback; plug-and-play RL. |
| **RATTPO** | `2506.16853` | Reward-agnostic test-time prompt search; 4.8× faster vs naive. |
| **PRISM** | `2607.24353` | Image-grounded self-rewarding; hybrid ideal-point/Chebyshev. |
| **PRIS** | `2512.03534` | Adaptive prompt redesign при inference-time scaling; +15% VBench 2.0. |
| **GenPilot** | `2510.07217` | Multi-agent test-time APO; до +16.9% DPG-bench. |
| **PromptSculptor** | `2509.12446` | Multi-agent short→rich prompt; CoT + self-eval. |
| **T2I-Copilot** | `2507.20536` | Training-free multi-agent: interpret / generate / evaluate. |
| **CAPR** | `2403.19716` | Reformulation из user logs с учётом user capability. |
| **Tailored Visions** | `2310.08129` | Personalized rewrite из истории (~300k prompts). |
| **POSI** | `2402.10882` | Prompt optimizer для **safety** (toxic→clean) в black-box T2I. |
| **PEZ** | `2302.03668` | Gradient hard-prompt discovery (interpretable discrete). |
| **DPO-Diff** | `2407.01606` | Discrete prompt optimization через diffusion gradients. |

## B2. Структура / IR / альтернативы prose rewrite

| Работа | Ссылка | О чём говорит статья |
|--------|--------|----------------------|
| **Structured Captions (Re-LAION 19M)** | `2507.05300` | Один template: subject / setting / aesthetics / camera; structured > shuffled на VQA alignment. |
| **LMD** | `2305.13655` | LLM → layout (captioned boxes) → controller diffusion; +accuracy на numeracy/spatial. |
| **RPG** | `2401.11708` | Recaption → Plan → regional generate; MLLM planner. |
| **ELLA** | `2403.05135` | LLM adapter для dense prompts без rewrite prose; DPG-Bench. |
| **T2I-R1** | `2505.00703` | Bi-level CoT **внутри** генератора (semantic + token); RL. |
| **SEER / Endogenous Reprompting** | `2601.20305` | Cognitive Gap в UMM; endogenous descriptors; RLVR→RLMT на 300 samples. |
| **BBQ-to-Image** | `2602.20672` | Numeric boxes + RGB в structured text; «intent → intermediate structured language → renderer». |
| **SCOPE** | `2605.08043` | Evolving structured specification + skill orchestration; EGIP 0.60. |
| **Oppenlaender taxonomy** | `2204.13988` | 6 типов prompt modifiers из ethnography community. |

## B3. Lab / product PE (как описывают авторы)

| Система | Источник | Что говорит документация/отчёт |
|---------|----------|--------------------------------|
| **NVIDIA APE** | `2606.00204` | см. A10 |
| **NVIDIA Cosmos Prompt Upsampler** | HF `Cosmos-1.0-Prompt-Upsampler-12B` + docs | LLM превращает human prompts в detailed, training-preferred; default on; max 512 tokens |
| **Qwen-Image-2.0 PE** | `2605.10730` §3.3 | reverse-engineering degradation → (short, CoT, fine); SFT→GRPO; rewards: consistency + aesthetics + rules |
| **Seedance PE** | `2506.09113` | Qwen2.5-14B; SFT затем DPO из‑за hallucinations после SFT |
| **Seedream 4.0 PE** | `2509.20427` | VLM на Seed1.5-VL: routing + rewrite + aspect ratio; AdaCoT budgets |
| **HunyuanImage 3.0** | `2509.23951` | Native CoT: interpret → thinking/rewrite → synthesize; T2T+T2TI data |
| **OpenAI DALL·E 3 API** | Cookbook | GPT-4 rewrite always-on; `revised_prompt`; нельзя выключить |
| **Google Vertex Imagen** | Cloud docs | `enhancePrompt` default on; rewrite в ответе если input <30 words |
| **FLUX.2 upsampling** | BFL docs | VLM expand; optional; полезно для reasoning-heavy; для «a red car» — мало пользы |
| **Ideogram 4** | docs + OSS | trained exclusively on JSON; Magic Prompt plain→JSON; plain text «will not work» |

## B4. Длина captions / evaluation / rewards / surveys

| Работа | Ссылка | О чём говорит статья |
|--------|--------|----------------------|
| **DetailMaster** | `2505.16915` | Long prompts avg ~285 tokens; ceiling ~50%; нужен **expanded limits + long-prompt training**. |
| **DSG** | `2310.18235` | Atomic QG/A dependency graphs для reliable T2I evaluation. |
| **TIFA** | `2303.11897` | VQA faithfulness metric; reference-free. |
| **ImageReward** | `2304.05977` | Human preference reward model; 137k comparisons. |
| **PickScore** | `2305.01569` | CLIP-based preference from real users; Pick-a-Pic. |
| **HPS v2** | `2306.09341` | Large preference dataset; HPS scoring. |
| **APO survey** | `2502.16923` | 5-part unifying APO framework (в основном LLM; T2I — ветка). |
| **APO optimization survey** | `2502.11560` | Discrete/continuous/hybrid prompt spaces. |
| **The Prompt Report** | `2406.06608` | Taxonomy 58 LLM + 40 multimodal techniques. |
| **VPO** | `2503.20491` | T2V: principles harmless / accurate / helpful; SFT + preference. |

---

# C. Краткая история области (факты по работам)

1. **2021–22:** community modifiers и HCI (Oppenlaender) — ручной craft.  
2. **2022–23:** Promptist задаёт SFT→RL; DALL·E 3 Better Captions — synthetic captions + GPT upsample; BeautifulPrompt — aesthetic RL.  
3. **2023–24:** OPT2I / Idea2Img — loops; LMD/RPG — layout вместо (или вместе с) prose; PAE — weights/timesteps; Prompt Expansion — diversity.  
4. **2025:** labs (Wan, Seedance/Seedream, Qwen, Hunyuan, FLUX, Cosmos) встраивают PE; академически — TIPO, RePrompt, PromptEnhancer, VisualPrompter, Input-Side Scaling, FIBO.  
5. **2026:** диагностика и gating (TARA, APE/NVIDIA, FaithRewriter); endogenous CoT (SEER, T2I-R1); GenEval 2 показывает, что rewrite может снижать human alignment.

---

# D. Моё видение (отдельно от пересказа статей)

Это **не** утверждения статей, а сжатое мнение после обзора:

1. Область ушла от «всегда удлинять» к **условному** enhancement (когда чинить / когда не трогать).  
2. «Правильный» выход PE — не универсальный JSON и не универсальный long prose, а **то, на чём учился ваш генератор** (prose caption law *или* schema, если модель JSON-native).  
3. Самые полезные «учебники темы» сейчас: **Promptist + DALL·E 3 + Wan** (зачем), **PromptEnhancer / Input-Side Scaling / APE** (как учить rewriter), **FaithRewriter / TARA / VisualPrompter** (как не ломать intent), **FIBO / Ideogram** (когда структура = интерфейс), **GenEval 2 / Brack** (как измерять и какой train distribution целиться).  
4. Отдельного survey «T2I re-prompt handbook» всё ещё нет — APO surveys закрывают только соседнюю полку. Имеет смысл читать **кластер P0 выше**, а не одну старую работу.

---

## Быстрый маршрут чтения (партшкола)

**Неделя 1 — зачем:** Promptist → DALL·E 3 PDF → Wan §prompt → Brack → RECAP  
**Неделя 2 — как учить PE:** BeautifulPrompt → PromptEnhancer → Input-Side Scaling → **APE (NVIDIA)** → Qwen-Image-2.0 §PE  
**Неделя 3 — как не вредить:** FaithRewriter → VisualPrompter → TARA → GenEval 2  
**Неделя 4 — структура:** FIBO → Structured Captions 19M → Ideogram JSON docs → LMD/RPG (альтернативы) → SEER/T2I-R1 (internalize)

---

*Если нужна следующая итерация — могу вынести только P0 в одностраничный «syllabus» или добавить цитатные деревья потомков именно от APE / PromptEnhancer / FaithRewriter.*
