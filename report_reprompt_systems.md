# Как устроена система re-prompt: академический разбор

**Дата:** 2026-07-29  
**Объект:** inference-time (и смежный training-time) prompt rewrite / enhancement / upsampling для text-to-image  
**Вопрос:** какую проблему решает эта система, какими методами, почему она выглядит именно так, и как делать правильно  
**Сопровождение:** см. также более детальные разборы в под-разделах/архитектурных отчётах в этом репозитории.

---

## 1. Короткий вердикт

**Re-prompt (PE) — это не «сделать промпт красивее».**  
Это механизм закрытия разрыва между:

- тем, **на каких текстах учился генератор** (часто длинные, плотные, synthetic captions), и  
- тем, **что реально пишет пользователь** (коротко, недоспецифицировано, разностилево).

Поэтому продакшн-системы выглядят похоже: отдельный LLM/VLM перед генератором, который разворачивает короткий ввод в «model-preferred caption». Академически правильная формулировка цели:

> Выровнять вход к **обучающему распределению captions** генератора, сохранив **исходный intent**, и чинить только те failure modes, которые реально ломают картинку — не максимизировать verbosity и не максимизировать aesthetic score любой ценой.

Если тренировка уже с **вариативной длиной** captions (Brack / RECAP), нужность always-on PE падает. Если тренировка на длинных dense captions (DALL·E 3 / Wan / Seedance), PE почти обязателен.

---

## 2. Какую проблему решает система

### 2.1. Главный разрыв: train ↔ user

Формулировки в литературе сходятся:

| Источник | Формулировка |
|---|---|
| **DALL·E 3** | Модель, обученная на длинных descriptive captions, плохо семплится из коротких user prompts (OOD). GPT upsample «возвращает» вход в train distribution. |
| **Wan** | «Distribution mismatch… users prefer concise prompts… significantly shorter than the training captions… objective is to align refined prompts with the distribution of training captions.» |
| **Seedance** | Тексты для DiT — dense video captions → LLM обязан конвертировать user prompt в caption format. |
| **Promptist** | «Performant prompts are often model-specific and misaligned with user input.» |
| **HunyuanVideo** | Адаптировать user prompt к **model-preferred prompt**. |

Это **не** та же задача, что training-time recaptioning (RECAP, Recap-DataComp, Better Captions captioner), но методы родственны: оба двигают текст к «хорошему» caption law. Разница:

- **Recaption** меняет обучающие пары image↔text.  
- **Re-prompt** меняет только inference input.

### 2.2. Вторичные проблемы, которые PE тоже тащат на себя

1. **Композиционные слабости генератора** — attribute binding, negation, counting, spatial (PromptEnhancer taxonomy).  
2. **Эстетика / «киношность»** — BeautifulPrompt, magic suffixes («Ultra HD, 4K…»), Master-mode Hunyuan.  
3. **Safety / policy** — явно у OpenAI; у других чаще отдельные классификаторы.  
4. **Язык и формат** — перевод, quoting in-image text, JSON schemas (Ideogram 4 / FIBO).  
5. **Task routing** — Seedream 4: PE = rewrite + aspect ratio + thinking budget.

Важно: (1) и (2) **конфликтуют**. Input-Side Scaling показывает это численно: aesthetics reward ↑0.48→0.82 при alignment ↓0.56→0.42. BeautifulPrompt у третьих сторон роняет T2I-CompBench на ~20 пунктов. Значит «одна кнопка Enhance» без цели — плохой дизайн.

### 2.3. Что PE *не* решает

- Не заменяет хороший text encoder / LLM conditioner (ELLA, native long-context VLM).  
- Не чинит truncated CLIP-77, если rewrite всё равно длиннее окна (GenEval 2).  
- Не увеличивает «alignment к словам пользователя» выше верхней границы raw prompt в embedding-смысле (Google Prompt Expansion) — зато может поднять **image–original-prompt consistency**, компенсируя слабости генератора (PromptEnhancer / RePrompt).

---

## 3. Почему системы выглядят именно так

Исторически сложились **два ствола**, которые потом слились:

```
HCI / community modifiers (2021–22)
        \                      NLP APE / RLHF (2021–22)
         \                            \
          → Promptist (SFT+PPO)        \
                 \                      \
                  └──── modern PE ←──── DALL·E 3 (long synthetic captions + GPT upsample)
```

Почти все современные системы — вариации одного скелета:

```
user_prompt
   → [optional gate: rewrite?]
   → rewriter (LLM / VLM / small LM)
        ├─ maybe CoT / reasoning
        ├─ maybe retrieve exemplars
        └─ maybe look at a draft image (visual feedback)
   → rewritten_prompt  (~ train caption length/style)
   → frozen T2I generator
   → [optional: score & accept-or-revert]
```

Почему именно так:

1. **Дешевле трогать текст, чем переобучать генератор** (model-agnostic PE, Input-Side Scaling).  
2. **Train distribution уже «длинная»** — проще подтянуть inference, чем переразметить всё и переучить.  
3. **LLM умеет говорить на языке captions** — особенно после distillation от GPT/Gemini/DeepSeek.  
4. **Разделение обязанностей**: генератор рисует, rewriter интерпретирует intent и заполняет недосказанное.

Три поколения архитектур (видно по лабораториям):

| Поколение | Примеры | Смысл |
|---|---|---|
| External zero-shot LLM | DALL·E 3 GPT-4, ранний Qwen polish, FLUX OpenRouter | Дешёвый старт, слабый контроль faithfulness |
| Purpose-trained PE | PromptEnhancer, Seedance SFT+DPO, Qwen-Image-2.0 PE, BeautifulPrompt | SFT (+ RL) под reward / caption format |
| Internalized CoT / thinking | HunyuanImage 3 Instruct, Nano Banana Pro thinking, wan2.7 `thinking_mode` вместо `prompt_extend` | Rewriter растворяется в генераторе |

---

## 4. Методы: таксономия

### 4.1. По источнику supervision

| Семья | Суть | Примеры | Риск |
|---|---|---|---|
| **Zero-shot LLM rewrite** | System prompt «сделай детальнее» | DALL·E Appendix C, FLUX system messages, Qwen polish | Hallucination, style injection |
| **SFT short→long** | Пары (user, model-preferred) | Promptist SFT, BeautifulPrompt SFT, PromptEnhancer SFT, Seedance | Учит verbosity; качество пар = потолок |
| **Reverse-engineered pairs** | Из fine caption синтезировать короткий user prompt | Qwen-Image-2.0 PE | Лучшая data story для реализма user inputs |
| **RL / preference** | PPO/GRPO/DPO по image rewards | Promptist, BeautifulPrompt, RePrompt, PromptEnhancer, Input-Side Scaling | Reward hacking → aesthetics↑ semantics↓ |
| **Retrieval-augmented** | Достать modifiers из training prompts | RAPO, RAPO++ | Model-specific, но data-grounded |
| **Distribution presampling** | Маленький LM учится на caption law датасета | TIPO | Эстетика/corruption↓, семантика может просесть |
| **Closed-loop visual** | Сгенерировать → оценить → чинить | OPT2I, Idea2Img, VisualPrompter, FaithRewriter, TARA, PRISM | Дорого (extra generations), зато grounded |
| **Structured / schema** | JSON fields / layout / DSG atoms | FIBO, Ideogram JSON, LMD/RPG | Контролируемость↑, verbosity риск если schema огромная |
| **Internalized** | CoT внутри генератора | T2I-R1, Hunyuan native thinking | Нет отдельного PE-сервиса |

### 4.2. По feedback modality (главный водораздел 2025–26)

1. **Text-only** — rewriter не видит картинку.  
2. **Image-grounded** — видит draft / visual anchor.  
3. **Latent-grounded** — видит промежуточные denoising states (PromptLoop).  
4. **Reward-model-only** — видит только scalar/pairwise scores.

Поле движется от (1)+(4) к (2), потому что text-only «додумывает» физически невозможное (FaithRewriter: «glass of water upside down»).

### 4.3. По политике срабатывания

| Политика | Кто | Смысл |
|---|---|---|
| Always-on | OpenAI DALL·E 3 | Максимальный quality/safety, минимум контроля |
| Default-on, switchable | Google Imagen, DashScope Qwen | Компромисс продукта |
| Optional / opt-in | FLUX.2, Wan open weights | Для power users и простых промптов |
| Length-adaptive | Ideogram AUTO, Vertex «<30 words return» | Короткие усиливать, длинные трогать слабо |
| Failure-gated | TARA τ≈0.72, accept-or-revert | Академически правильнее всего |

---

## 5. Чему учит эмпирика (не инженерия «на вкус»)

### 5.1. Длина — прокси, не цель

| Факт | Источник |
|---|---|
| DALL·E upsample prompt: 15–80 слов | Appendix C |
| Wan: ~80–100 слов | system prompts |
| FLUX I2I: 50–80 (~30 для brief) | system messages |
| Qwen polish: <200 words | prompt_utils |
| RePrompt hard-cap 15–77 tokens | paper |
| TARA: stay under ~70 words | paper |
| DetailMaster: слишком длинные промпты ухудшают binding/spatial | `2505.16915` |
| Brack: **вариативность** длины на train лучше «всегда длинно» | `2506.16679` |
| UF-FGTG: для SD оптимальный append ≈ 6 tokens, не «максимум» | `2402.12760` |

**Норматив:** целевая длина PE ≈ **закон обучающих captions** данного генератора (±окно encoder), не «как можно длиннее».

### 5.2. Aesthetic rewards опасны как единственная цель

- BeautifulPrompt / PickScore+Aesthetic — семантика падает (PromptEnhancer Table 4; TARA).  
- Input-Side Scaling Table 10 — прямой tradeoff aesthetics↔alignment.  
- PickScore авторы сами: иногда выбирает красоту ценой faithfulness.  
- Reward-hacking literature: HPS → oversaturation, composition↓.

**Норматив:** либо **два режима** (faithful vs pretty), либо decomposed reward (keypoints / DSG), либо aesthetics только как soft secondary с жёстким faithfulness constraint.

### 5.3. Naive LLM rewrite часто бесполезен или вреден

RePrompt: сырой Qwen2.5-3B rewrite роняет counting 0.75→0.63; RL without reasoning ≈ naive.  
GenEval 2: на 4 из 6 моделей rewriting **снижает** human alignment.

**Норматив:** измерять PE **per backbone**, против **original** prompt, на compositional бенчмарках — не верить «стало красивее».

### 5.4. Чинить атомарно, не раздувать всё

VisualPrompter / TARA / OPT2I: decompose → fix failed propositions → не добавлять aesthetic filler.  
FaithRewriter: length-matched hard negatives, иначе DPO учит «пиши длиннее».

**Норматив:** expansion без диагноза = главный источник intent pollution.

### 5.5. Иногда лучше не репромптить

- Промпт уже длинный / structured (Ideogram JSON; DPG-Bench).  
- Draft уже хорош (TARA re-seed).  
- Artistic / style-first запросы (малые gains PromptEnhancer на Artistic Style).  
- Сильный генератор + короткий креативный запрос (Midjourney philosophy; FLUX docs: «a red car» не нуждается).  
- Нужен reproducible seed (Vertex: enhance ломает seed).

---

## 6. Как делать правильно: design principles

Ниже — нормативный чеклист, собранный из P1-литературы и лабораторных отчётов. Это не «один рецепт», а **пространство решений**, которое надо явно выбрать.

### P0. Зафиксировать цель PE

Выбрать одну primary objective:

1. **Distribution alignment** — подтянуть к train captions (Wan / TIPO / Seedance).  
2. **Compositional faithfulness** — чинить binding/counting/spatial (PromptEnhancer / FaithRewriter / TARA).  
3. **Aesthetics / diversity** — BeautifulPrompt / Prompt Expansion / Ideogram variety.  
4. **Safety / policy** — OpenAI-style.

Смешивать (2) и (3) в один scalar reward — системная ошибка.

### P1. Сначала понять train caption law

Без знания, на каких текстах учился генератор, PE гадает. Нужны:

- типичная длина / структура captions (style-first? JSON? prose?),  
- доля synthetic vs raw,  
- была ли **variability** длины (Brack).

Если train уже variable-length и user-like — PE default-off.  
Если train dense-long — PE default-on или gated.

### P2. Данные для rewriter

Предпочтительный pipeline (Qwen-Image-2.0 / PromptEnhancer / FaithRewriter):

1. Взять fine / model-preferred captions.  
2. Синтезировать реалистичные short user prompts (colloquialization, underspecification).  
3. Получить (short, CoT?, long) с **сохранением intent**.  
4. Для RL: preference pairs **length-matched** (оба expanded), win = более visually faithful.  
5. Отдельно держать hard negatives: over-specification, demographic injection, style spam.

### P3. Reward / objective

Минимум:

- **Faithfulness** к original prompt (DSG / keypoints / VQA / MLLM pairwise).  
- **Anti-hallucination** (no new objects; preserve correct atoms).  
- **Length / format** constraint под encoder budget.  
- Опционально aesthetics — отдельная голова или отдельная модель.

Избегать: голый PickScore / HPS / LAION Aesthetic как единственный reward.

### P4. Inference policy

Рекомендуемый продакшн-скелет:

```
if user_disabled_pe: use raw
elif prompt is already long/structured: light touch or skip
else:
   draft = maybe_generate(raw)          # optional, for gated systems
   if draft_score >= τ: keep raw (reseed if needed)
   else:
      candidates = rewrite(raw, feedback=draft?)
      pick best by faithfulness-to-original
      if score(new) <= score(raw): revert
```

UX-уровни как у Ideogram: **Off / Auto / On**, плюс показать `revised_prompt`.

### P5. Output contract rewriter’а

Повторяющиеся индустриальные правила (FLUX / Qwen / Wan):

- Preserve core subject and intent.  
- Quote in-image text literally; don’t translate it.  
- Turn negatives into positives («don’t change X» → «keep X») для editing.  
- Lead with subject & hard constraints; style в конце (на случай truncation).  
- No unrelated objects / generic quality filler.  
- Target length ≈ train caption law.  
- On failure: **fallback to original** (Wan).

### P6. Evaluation protocol

Обязательно:

1. Сравнивать image с **original** prompt (GenEval 2 / Parrot / Promptist).  
2. Репортить **Δ vs raw**, не только vs другие PE.  
3. Раздельно: compositional (GenEval/T2I-CompBench/DSG), dense-prompt regress (DPG-Bench), human pref, length stats.  
4. Per-backbone.  
5. После expansion — не забывать, что тестпоинты могли измениться (UniGenBench++ re-alignment).  
6. Смотреть bias/demographics (FairPro).

### P7. Когда PE не ставить

- Research API с требованием seed determinism.  
- Пользователь — prompt engineer / JSON schema.  
- Модель с сильным aesthetic prior и короткой train distribution (Midjourney-like).  
- Уже есть native thinking/CoT image model и он измерен лучше внешнего PE.

---

## 7. Минимальная «правильная» архитектура (если строить с нуля)

Практичный baseline 2026, согласованный с литературой:

1. **Малый/средний rewriter** (3B–14B), не обязательно GPT-класс в runtime (APE: post-trained small models догоняют).  
2. **SFT** на reverse-engineered (short→train-like) с CoT опционально.  
3. **RL stage** с decomposed faithfulness reward (keypoints/DSG/MLLM pairwise), length-matched DPO/GRPO.  
4. **Отдельный aesthetic mode**, не смешивать в один.  
5. **Gating**: skip если raw уже хорош / уже длинен; accept-or-revert.  
6. **Показать revised prompt**; дать Off/Auto/On.  
7. **Fallback** на raw при ошибке rewriter.  
8. Метрики: GenEval/T2I-CompBench/DSG + human vs **original**; следить за length и bias.

Альтернатива «ещё правильнее на train-side»: учить генератор на **variable-length / mixed** captions (Brack, RECAP, SD3 50/50), тогда PE становится тонкой опцией, а не костылём.

Альтернатива «ещё правильнее на model-side»: internalized semantic CoT (T2I-R1 / Hunyuan thinking) — PE как сервис исчезает, но нужна тяжёлая post-training генератора.

---

## 8. Открытые разломы поля (куда смотреть дальше)

1. **Reward specification** — taxonomy (PromptEnhancer) vs visual anchor (FaithRewriter) vs reward-agnostic (RATTPO) vs human prefs (APPO).  
2. **Feed-forward vs iterative vs internalized** — PromptEnhancer vs PromptLoop/TARA vs T2I-R1.  
3. **Uniform expansion vs typed repair** — TARA прямо атакует все Tier-1 seeds.  
4. **Нет dedicated survey** именно по T2I PE (есть общие APO surveys) — поле ещё не канонизировано.  
5. **Bias injection через rewrite** — недоисследовано относительно aesthetics papers.  
6. **Conditional length policy** end-to-end (модель сама решает, насколько расширять) — дырка; TIPO multi-task + TARA gate закрывают только половины.

---

## 9. Связь с предыдущим исследованием длины промптов

В отчётах по длине промпта (см. [`README.md`](./README.md)) уже показано:

- train–infer length match критичен;  
- variable length или long+PE — два рабочих режима;  
- PE должен целиться в train caption law, не в max verbosity.

Этот отчёт — следующий слой: **как именно устроен PE**, почему лаборатории делают always-on/default-on/opt-in, и какие академические результаты отделяют «инженерно привычное» от «правильно».

Совместная политика:

\[
(\mu_{\text{train}},\, L,\, g)
\]

где \(\mu_{\text{train}}\) — закон обучающих captions, \(L\) — бюджет encoder/API, \(g\) — политика gating PE.

---

## 10. Источники верхнего уровня

Ядро:

- Promptist `2212.09611`  
- DALL·E 3 Better Captions PDF  
- RECAP `2310.16656`, Brack `2506.16679`  
- BeautifulPrompt `2311.06752`, Prompt Expansion `2312.16720`  
- OPT2I `2403.17804`, TIPO `2411.08127`  
- RePrompt `2505.17540`, PromptEnhancer `2509.04545`, Input-Side Scaling `2510.12041`  
- RAPO/RAPO++ `2504.11739` / `2510.20206`  
- VisualPrompter `2506.23138`, FaithRewriter `2606.08492`, TARA `2607.18724`  
- Wan `2503.20314`, Qwen-Image-2.0 `2605.10730`, Seedance/Seedream, HunyuanImage 3, FLUX.2 docs, Ideogram Magic Prompt, Vertex Imagen rewriter  
- GenEval 2 `2512.16853`, DetailMaster `2505.16915`, FairPro `2512.04981`

Сырые корпуса и деревья: `research/reprompt-systems/corpus/`, `research/reprompt-systems/citation_trees/`.
