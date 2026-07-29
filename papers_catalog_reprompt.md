# Каталог статей: системы re-prompt / prompt enhancement для T2I

Дата: 2026-07-29  
Корпус: arXiv-поиск (~213 уникальных → 91 релевантных → 52 строго PE) + citation trees ключевых семян + отчёты OpenAI / Google / BFL / Qwen / Wan / Seedream / Seedance / Hunyuan / Ideogram / Midjourney / Stability + 4 параллельных web-search агента.

Цель каталога — быстро понять, **о чём статья** и **нужно ли её читать**, чтобы разобраться, как правильно строить систему репромпта.  
Итоговый синтез — в [`report_reprompt_systems.md`](./report_reprompt_systems.md).

Легенда приоритета:
- **P1** — must-read для понимания области
- **P2** — сильный контекст / важный метод
- **P3** — периферия / смежное / осторожно с релевантностью

---

## 0. Как читать это поле (карта)

Две независимые «корневые» линии, которые потом сошлись:

1. **Promptist (NeurIPS 2023)** — метод: SFT → RL, награда = эстетика + relevance.  
2. **DALL·E 3 Better Captions** — теория: модель учится на длинных synthetic captions → короткий user prompt = OOD → нужен upsample.

Почти все современные PE-системы — рекомбинация этих двух линий с разным reward, feedback (text-only vs image-grounded) и политикой длины.

---

## 1. Must-read (P1)

### 1.1. Теория разрыва train↔user

| ID | Статья | О чём | Зачем читать |
|---|---|---|---|
| OpenAI PDF | [Improving Image Generation with Better Captions](https://cdn.openai.com/papers/dall-e-3.pdf) | Рекапшн датасета + GPT-4 upsample коротких промптов; 95% synthetic captions. Appendix C — текст системного промпта (15–80 слов). | Первичный индустриальный аргумент «почему репромпт вообще существует». |
| `2310.16656` | **RECAP** | Контролируемые абляции short vs long synthetic captions. | Академический open-world ответ: нужны **и** короткие, **и** длинные captions; длина — не «чем больше, тем лучше». |
| `2506.16679` | **Brack et al. How to Train…** | Дизайн synthetic training captions: плотность, вариативность длины. | Задаёт **целевое распределение**, на которое должен целиться rewriter. |
| `2503.20314` | **Wan** (prompt extend) | Самая прямая формулировка: user prompts короче training captions → mismatch → rewrite должен **выровнять распределение**. | Каноническая формулировка проблемы + 3 принципа rewrite (смысл / motion / структура caption). |
| `2605.10730` | **Qwen-Image-2.0** §Prompt Enhancer | PE из Qwen3.5-9B; reverse-engineering коротких промптов из fine annotations; SFT+GRPO. | Как современные лаборатории **конструируют данные** для PE (деградация → inverse CoT). |

### 1.2. Основания метода

| ID | Статья | О чём | Зачем читать |
|---|---|---|---|
| `2212.09611` | **Promptist** | SFT на human-engineered prompts + PPO; reward = LAION aesthetic + gated CLIP relevance. | Шаблон всего поля: «адаптировать промпт под модель». |
| `2311.06752` | **BeautifulPrompt** | Пары low→high quality prompts + RL с PickScore+Aesthetic. | Канонический пример **эстетического PE**, который потом ломает семантику (~−20 на T2I-CompBench у третьих сторон). |
| `2312.16720` | **Prompt Expansion** (Google, ACL 2024) | Один query → N expansions; оптимизация diversity+aesthetics. | Теоретический тезис: expansion **не может повысить** alignment к исходному query выше верхней границы raw prompt — цель = минимизировать падение alignment. |
| `2403.17804` | **OPT2I** | Training-free iterative rewrite по DSG / decomposed CLIPScore. | Первое чёткое: скалярный reward слишком груб; нужна декомпозиция. |
| `2404.04095` | **PAE** | Dynamic prompt optimizing: не только текст, но веса токенов и timesteps. | Показывает, что action space PE не обязан быть plain text. |

### 1.3. Современные ядра PE (2025–2026)

| ID | Статья | О чём | Зачем читать |
|---|---|---|---|
| `2411.08127` | **TIPO** | Лёгкий LM, text presampling: выравнивание к distribution training captions без большого LLM/RL. | Формализация distribution-aligned PE; предупреждение про OOD «просто длиннее». |
| `2505.17540` | **RePrompt** | Reasoning-augmented rewrite + RL (GRPO); ensemble ImageReward+VLM; length cap 15–77. | Naive LLM rewrite часто **ухудшает**; reasoning+RL даёт прирост. |
| `2509.04545` | **PromptEnhancer** | CoT rewriter + AlignEvaluator (24 keypoints) + SFT→GRPO; model-agnostic. | Лучшая articulation fine-grained failure taxonomy; CVPR 2026 camera-ready. |
| `2510.12041` | **Input-Side Scaling** | Iterative DPO без SFT; scaling по размеру rewriter LLM; transferability. | Чистая абляция: aesthetics reward поднимает beauty 0.48→0.82 и роняет alignment 0.56→0.42. |
| `2606.08492` | **FaithRewriter** («Seeing is Believing») | Visual anchor: сгенерировать картинку → MLLM-диагноз → rewrite → distill DPO. | Главный урок: preference pairs надо **length-match**, иначе учится verbosity. |
| `2506.23138` | **VisualPrompter** | Training-free: найти missing concepts по картинке и чинить только их. | Atomic targeted repair вместо holistic expansion. |
| `2607.18724` | **TARA** | Type-aware repair allocation + accept-or-revert gate + skip если уже хорошо (τ≈0.72). | Самый инженерно-правильный ответ на «когда НЕ репромптить». |
| `2510.20206` | **RAPO++** | Retrieval alignment + test-time scaling + distillation (T2V, но архитектурно центрально). | Синтез трёх стратегий поля в один pipeline. |
| `2504.11739` | **RAPO** | Retrieval-augmented prompt optimization из training-prompt relation graph. | Data-grounded distribution alignment через retrieval. |

### 1.4. Продуктовые / лабораторные системы (документация)

| Система | Орг | О чём | Зачем читать |
|---|---|---|---|
| DALL·E 3 API rewrite | OpenAI | Always-on GPT-4 rewrite; нельзя выключить; `revised_prompt`. | Always-on политика + safety как второй мотив. |
| Vertex Imagen `enhancePrompt` | Google | Default on; rewrite возвращается только если input <30 слов; ломает seed. | Самая жёсткая documented length-gating политика. |
| FLUX.2 prompt upsampling | BFL | Optional; local Mistral / OpenRouter; system messages с «preserve intent»; max_new_tokens=512. | Лучший публичный system prompt upsampler’а. |
| Qwen-Image `prompt_extend` / polish | Alibaba | Default on в API; <200 words; magic suffix Ultra HD/4K; editing нестабилен без rewrite. | Продакшн-дефолты + edit vs generate. |
| Wan `prompt_extend` | Alibaba | Optional off by default в open weights; 80–100 слов; fallback на оригинал при ошибке. | Канон train/user gap. |
| Seedance / Seedream PE | ByteDance | Dense caption format; SFT+DPO (Seedance); VLM PE с task routing (Seedream 4). | PE как стадия post-training / pipeline. |
| HunyuanImage / PromptEnhancer | Tencent | Native CoT self-rewrite + внешний DeepSeek PE; Normal vs Master modes (Video). | Два режима: intent vs cinematic quality. |
| Ideogram Magic Prompt | Ideogram | AUTO/ON/OFF; length-adaptive; JSON captions в 4.0. | Лучший UX-паттерн gating. |
| Midjourney / Stability | — | **Нет** always-on rewriter (MJ: conversational opt-in; Stability: user prompting). | Контрпримеры: когда PE сознательно не ставят. |

---

## 2. Сильный контекст (P2)

### 2.1. Visual-feedback / closed-loop

| ID | Статья | О чём |
|---|---|---|
| `2607.24353` | **PRISM** | Один VLM = rewriter + judge; multi-objective reward (semantic/aesthetic/preference). |
| `2310.08541` | **Idea2Img** | GPT-4V loop: generate → select → reflect; память quirks модели. |
| `2510.00430` | **PromptLoop** | Step-wise refinement внутри denoising по latent feedback; mitigation reward hacking. |
| `2505.16763` | Self-Rewarding LVLMs | Unified solver+reward; iterative DPO. |
| `2507.20536` | T2I-Copilot | Training-free multi-agent interpretation. |
| `2509.12446` | PromptSculptor | Multi-agent evaluator-guided optimization. |
| `2510.07217` | GenPilot | Multi-agent test-time prompt optimization. |

### 2.2. Agentic / structured / alternatives

| ID | Статья | О чём |
|---|---|---|
| `2606.00204` | **APE (Agentic Prompt Enhancer)** | SAPE/MAPE над semantic fields; GRPO/GDPO; small enhancers; explicit no-rewrite route. |
| `2511.06876` | **FIBO** | ~1000-word structured JSON captions; schema как target PE. |
| `2305.13655` | **LMD** | LLM выдаёт layout, не prose — другое intermediate representation. |
| `2401.11708` | **RPG** | Recaption → Plan → Generate. |
| `2505.00703` | **T2I-R1** | Internalized semantic CoT вместо внешнего rewriter. |
| `2601.20305` | Endogenous Reprompting | Self-aligned descriptors внутри unified multimodal model. |
| `2407.01606` | DPO-Diff | Gradient-based discrete prompt optimization. |
| `2302.03668` | PEZ | Hard prompts via gradient (pre-LLM baseline). |
| `2401.05675` | **Parrot** | Multi-reward RL + dual-condition на raw+expanded prompt. |
| `2402.12760` | UF-FGTG | Явный plot: DiffusionDB length vs novice users; optimal append ≈6 tokens для SD. |

### 2.3. Video / cross-modal transfer

| ID | Статья | О чём |
|---|---|---|
| `2503.20491` | **VPO** | Принципы harmless / accurate / helpful для T2V PE. |
| `2412.15156` | Prompt-A-Video | Failure modes: modality-inconsistency, cost-discrepancy, model-unaware. |

### 2.4. Evaluation / risk / length

| ID | Статья | О чём |
|---|---|---|
| `2505.16915` | DetailMaster | Long prompts → деградация attribute binding / spatial. |
| `2512.16853` | GenEval 2 | Rewriting **уменьшает** human alignment на 4/6 моделей; оценивать против **original** prompt. |
| `2601.03468` | Reward Hacking in T2I RL | Preference rewards ломают composition; ensemble не спасает полностью. |
| `2508.20751` | Pref-GRPO | «Illusory advantage» pointwise GRPO; pairwise лучше. |
| `2512.04981` | FairPro | LLM rewrite вливает демографические атрибуты в нейтральные промпты. |
| DSG / TIFA | Cho/Hu et al. | Atomic proposition / VQA evaluation substrate для PE. |

### 2.5. HCI / interactive lineage

| ID | Статья | О чём |
|---|---|---|
| `2109.06977` | Design Guidelines (CHI 2022) | Эмпирический origin «subject+style» и trial-and-error. |
| `2204.13988` | Taxonomy of prompt modifiers | Словарь community modifiers. |
| Promptify / PromptCharm / PromptMagician / CHI RePrompt | 2023–2024 | Human-in-the-loop: что пользователь хочет контролировать. |
| `2310.08129` | Tailored Visions | Personalized rewrite из истории. |
| `2403.19716` | CAPR | Capability-aware reformulation из user logs. |

---

## 3. Периферия / осторожно (P3)

Много arXiv-хитов содержат слова «prompt optimization», но это не inference PE:

- jailbreak / safety red-teaming T2I;
- personalization adapters («image prompt adapter»);
- inverse problems / EHR / Petri nets с «reprompt» в названии;
- pure architecture papers без rewrite stage.

В `research/reprompt-systems/corpus/arxiv_pe_strict.json` — 52 кандидата после фильтра; в итоговом чтении опираться на P1/P2 выше.

---

## 4. Дерево цитирований (сжатый вывод)

По Semantic Scholar (частично rate-limited; см. `research/reprompt-systems/citation_trees/`):

| Seed | Примерно cites (S2 sample) | Роль |
|---|---|---|
| Promptist `2212.09611` | высокий (trunk) | Метод-предок |
| OPT2I `2403.17804` | ~80 | Самый цитируемый sibling iterative loop |
| Prompt Expansion `2312.16720` | ~34 | Diversity/alignment theory |
| PromptEnhancer `2509.04545` | ~32 | Текущий hub fine-grained reward |
| RePrompt `2505.17540` | ~17 | Reasoning+RL hub |
| RAPO `2504.11739` | ~16 | Retrieval hub (T2V→T2I) |
| TIPO `2411.08127` | ~5 | Distribution-alignment formalization |
| VisualPrompter `2506.23138` | ~3 | Visual-feedback sibling |
| TARA / APE / FaithRewriter (2026) | ~0–few | Слишком новые; читать как frontier |

**Ключевой overlap:** почти все PE-семена цитируют **Promptist** и **DALL·E 3 Better Captions**. Это два ствола дерева.

---

## 5. Что читать по порядку (практический маршрут)

**День 1 — проблема и зачем PE выглядит так:**
1. DALL·E 3 Better Captions (особенно §3.5 + Appendix C)  
2. Wan §prompt extend (distribution mismatch)  
3. Brack `2506.16679` + RECAP  

**День 2 — методы:**
4. Promptist  
5. BeautifulPrompt (как cautionary tale)  
6. TIPO  
7. PromptEnhancer  
8. Input-Side Scaling  

**День 3 — как делать правильно:**
9. FaithRewriter (length-matched pairs, visual anchor)  
10. VisualPrompter / TARA (targeted repair + gating)  
11. GenEval 2 (evaluate vs original; rewriting can hurt)  
12. FLUX.2 / Qwen / Ideogram docs (продуктовые политики)

**День 4 — альтернативы и границы:**
13. Parrot (dual-condition)  
14. FIBO / LMD (schema/layout instead of prose)  
15. T2I-R1 / Endogenous Reprompting (internalize PE)  
16. FairPro + reward-hacking papers

---

## 6. Артефакты этого исследования

```
.                                      ← основные MD-отчёты в корне PR
  report_reprompt_systems.md
  papers_catalog_reprompt.md
research/reprompt-systems/             ← технические артефакты
  outline.yaml
  fields.yaml
  corpus/
    arxiv_pe_filtered.json             ← 91
    arxiv_pe_strict.json               ← 52
    curated_reading_list.json          ← 72
  citation_trees/
  raw_searches/arxiv_pe_search.json    ← сырой arXiv (213)
```

Связанный корпус по длине captions: `research/prompt-length/` + отчёты в корне.
