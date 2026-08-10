# Как учили в ByteDance *Scaling Properties of Text Conditioning*

Источник: [arxiv 2607.29679](https://arxiv.org/pdf/2607.29679), project page [heheyas.github.io/context-scaling](https://heheyas.github.io/context-scaling/). Ниже — сжатое, но точное описание их обучающего пайплайна по тексту статьи и Appendix C, без нашей интерпретации «что чинить».

В статье учат **две разные вещи**, и их нельзя смешивать:

1. **Diffuser** — модель генерации картинки из текстового conditioning (structured prompt или NL).
2. **Prompter** — LLM, который на inference из короткого user prompt пишет structured prompt для diffuser.

Плюс отдельно, ещё до обучения diffuser, идёт **annotation pipeline**: из картинки собирают полный L10 SP. Это не обучение нейросети на градиентах, а frozen-инференс VLM и perception-экспертов, который производит train-labels.

---

## Общая схема

На train у каждого изображения есть пиксели и исходный caption (его потом часто трактуют как «user prompt»). Annotation pipeline по картинке строит полный structured prompt уровня L10. Из него детерминированно получают более бедные уровни L5–L9 маскированием групп полей. Diffuser учится паре «текст conditioning → изображение». Prompter учится отображению «user prompt → SP» (на inference картинки нет).

Итог на тесте в single-shot режиме: user prompt → обученный prompter → SP → обученный diffuser → картинка.

---

## 1. Annotation: откуда берутся structured prompts

Пайплайн пятистадийный (Figure 8, §3.3, Appendix C.2). Все модели в нём **заморожены**, градиентов нет.

**Stage 1 — глобальная сцена.** VLM Seed-VL смотрит целое изображение и выдаёт intent, atmosphere, style, lighting, photography, блок scene (setting + background), а также инвентарь элементов с id и bounding boxes, упорядоченный по композиционной важности.

**Stage 2 — по элементам.** Каждый объект кропается; VLM заново описывает caption, атрибуты (цвет, материал, поверхность и т.д.) и действия (pose, gesture, expression, gaze). Для людей Sapiens предсказывает 133 keypoints; keypoints **рисуют overlay** для следующего VLM-прохода, но **сырые точки в SP не пишут** — в схему идёт текстовое понимание позы.

**Stage 3 — геометрия.** DepthAnything V2 даёт относительную глубину элемента (0 ближайший … 255 дальний, иначе поле опускают). SAM 2.1 даёт маски и признаки occlusion. Boxes, masks и depth поддерживают геометрические relations (overlap, containment, порядок по глубине).

**Stage 4 — сборка.** Второй VLM-проход склеивает всё в валидный L10 JSON по схеме. Выходы экспертов **ограничивают** аннотацию, а не копируются сырьём.

**Stage 5 — degradation / field ladder.** Из одного L10 получают L9…L5, выключая группы полей (Table 1):

| Уровень | Средн. токены | Что добавляется относительно предыдущего |
|---------|---------------|------------------------------------------|
| L5 | 447 | base fields |
| L6 | 542 | bounding boxes |
| L7 | 647 | scene context |
| L8 | 803 | dynamic attributes |
| L9 | 1062 | depth & relationships |
| L10 | 1374 | photography |

Одна деградация на L10 переиспользуется во всех training cells. Схема полей — Table 10: обязательные `intent`, `scene`, `elements`; опциональные `relationships`, `atmosphere`, `photography`, `style`, `lighting`. Поле `ratio` пишет только prompter на inference (выбор canvas), в image-to-SP его нет.

**Matched NL controls** для end-to-end сравнения делают не «сплющиванием JSON», а из того же stage-1–3 evidence bundle: NL-verbalizer получает те же VLM-описания, Sapiens overlay, depth и SAM cues и пишет прозу под целевой токенный бюджет. Длина растёт **elaboration и связками**, без доступа к новым фактам аннотации.

Корпус картинок в статье **внутренний** (in-house); публично отдан не размер датасета целиком, а процедура и схема. Примеры схемы/кейсов есть на project page.

---

## 2. Обучение diffuser

Учат два backbone’а под разные вопросы.

### 2.1 BAGEL — scaling sweep (§3.2)

Зачем: показать, что converged diffusion loss предсказывается информацией в caption (GPG, ED), а не длиной. Собирают **15 caption-конфигураций** из одних и тех же полных аннотаций: три NL controls разной длины, шесть nested SP уровней L5–L10, три spatial-grid варианта, три field ablations. На **каждую** конфигурацию — **отдельный** training run.

Инициализация: in-house continued-training checkpoint BAGEL (не публичный релиз): Qwen2.5-7B с MoT-слоями, SigLIP2, frozen Flux KL-VAE.

Что размораживают: **full-parameter finetune** LLM, vision encoder и projection/embedding; **VAE заморожен**.

Рецепт (Table 11):

- packed sequence length 32 768 (не больше 16 384 токенов на один sample);
- LR \(5\times10^{-5}\), linear warmup 1k steps, потом constant;
- AdamW \(\beta_1=0.9\), \(\beta_2=0.95\), \(\epsilon=10^{-15}\), weight decay 0;
- grad clip 1.0, EMA 0.999;
- objective: rectified flow / v-prediction, timestep shift 4.0;
- bf16 compute, fp32 optimizer moments;
- 192 GPU, FSDP HYBRID_SHARD → ~6.3M tokens/step;
- CFG через conditioning dropout на train (text 0.1; reference-image VAE dropout 0.1);
- multi-aspect 512–1024 px.

Бюджет сравнения: все cells доводят до **одних и тех же** \(2.84\times10^{10}\) cumulative **image tokens**; на этой точке читают «converged» MSE для fits GPG/ED.

Текстовый conditioning: SP сериализуют в компактный single-quote JSON, чтобы экономить токены. Токенизатор — Qwen2.5-7B BPE.

### 2.2 Qwen-Image — основная end-to-end система (§3.4, §4)

Зачем: один сильный diffuser под structured interface + промптерные абляции. Учат **один раз**, потом **фиксируют** и меняют только prompter.

Инициализация: публичный **Qwen-Image-2512** — 60-layer DiT, text encoder **Qwen2.5-VL-7B заморожен**, **KL-VAE заморожен**.

Что учат: **full finetune DiT** (не LoRA на diffuser).

Рецепт (Table 12):

- packed sequence length 32 768;
- LR \(1\times10^{-4}\), linear warmup 2k steps, потом constant;
- AdamW те же \(\beta\), weight decay 0, clip 1.0;
- EMA 0.9999;
- flow matching / v-prediction; timestep shift зависит от длины последовательности (от ~0.5 при 256 токенах до ~0.9 при 8192);
- 512 GPU → ~16.8M tokens/step;
- text dropout 0.1, reference-image VAE dropout 0.3;
- multi-aspect 768–1536 px;
- длительность: **500 000 steps** (бюджет задан шагами, не тем же image-token cutoff, что у BAGEL sweep).

Данные conditioning: **смесь SP уровней и NL captions**, чтобы один backbone переваривал разные структуры и плотности. Токенизатор — Qwen2.5-VL (словарь 152 064).

Matched NL control для Table 2: тот же Qwen-Image init, те же картинки, тот же diffusion recipe и budget, но conditioning и цели — free-form NL вместо SP; prompter тоже matched по бюджету стадий, только цели NL.

---

## 3. Обучение prompter

База: **Qwen3.5-397B-A17B**, веса базы **всегда заморожены**. Учат только **LoRA rank 128** (\(\alpha=256\)), target — all linear modules. Три стадии подряд: SFT → Cold-start → RFT (verifier-gated OPSD). Appendix C.5, Table 13.

### Stage 1 — SFT

Задача: научить распределение SP, которое видит diffuser.

Данные: ~333k примеров, ~0.97B tokens, token-balanced mixture:

- примерно треть — core task: **original caption картинки как user prompt → image-derived SP** (+ reverse image-to-JSON);
- две трети — reasoning/instruction replay (EN/ZH CoT, VLM reasoning, dialogue, небольшой identity-anchor), чтобы не забыть базу.

Важно: target SP считают **одним правдоподобным** visual completion user prompt, а не восстанавливаемым ground-truth layout. Loss — CE только по assistant tokens; thinking block в SFT пустой и из loss выкинут. Один epoch, ~740 steps. Packed length 20 480, LR \(1\times10^{-5}\), cosine, warmup 0.1, weight decay 0.1, global batch 64. Инфра: Megatron / ms-swift, TP=PP=EP=4.

### Stage 2 — Cold-start

Задача: научить рассуждать от caption к детальному SP **без картинки на входе студента**.

Teacher (тот же Qwen3.5-397B в high-reasoning) видит caption **и** paired image, пишет long thinking trace + JSON. Gemini 3 Pro (validator v4) жёстко фильтрует утечки instance-specific деталей без обоснования, misalignment, reverse rationalization и т.п. Из 172 208 кандидатов принимают ~34%, после dedup остаётся **50 182** примера `(caption → thinking → SP)`.

Студент на train/inference картинки не видит. Loss — CE по thinking + JSON. ~8 epochs (два chained 4-epoch прогона). Packed 32 768, LR \(5\times10^{-5}\), cosine, warmup 5–10%, batch 128.

### Stage 3 — RFT / verifier-gated OPSD

Задача: on-policy улучшить image-free prompter сигналом от image-conditioned teacher, но только на rollout’ах, которые хорошо рисуются.

Данные: 10 003 original caption–image pairs. Студент (LoRA после SFT+Cold-start) image-free семплит rollout (T=1.0). Diffuser (уже обученный и **замороженный**) рендерит картинку. Gemini-verifier смотрит **только** user request и render (не SP); порог ≥6/10 по structure, alignment, aesthetics. На принятых rollout’ах считают OPSD: KL между next-token распределениями image-conditioned teacher и image-free student (top-64 logits teacher, clip divergence 5.0). Отдельного CE-auxiliary нет (`sft_alpha=0`).

Инфра RFT: DeepSpeed ZeRO-3, 8 GPU, colocated vLLM для rollout. Packed до 49 152, LR \(1\times10^{-4}\) / \(4\times10^{-5}\) по Table 13, batch 32.

Ablations в статье отдельно сравнивают verifier-only GRPO, OPSD-only без gate и полный gated OPSD.

---

## 4. Inference (как используют обученное)

Single-shot (основные таблицы): prompter greedy (T=0), до 16 384 new tokens → thinking + JSON; wrapper снимает thinking, читает `ratio`, убирает его, остальное SP отдаёт diffuser. Diffuser: Euler ODE, 50 steps; CFG 4.0 у Qwen-Image, 8.0 у BAGEL. Дефолт бенчмарков 1024².

Agentic loop (Table 5, не main single-shot): refine–render–judge, судья снова не видит SP, только user prompt и картинку; при FAIL критика возвращается в контекст prompter. Насыщение примерно на 2–3 раундах; обученный prompter за один проход сильнее длинного цикла у base.

---

## 5. Что важно не перепутать

| Компонент | Модель | Как учат | Заморожено |
|-----------|--------|----------|------------|
| Annotation | Seed-VL + Sapiens + DepthAnything V2 + SAM 2.1 | не учат, frozen inference | всё |
| Scaling diffuser | BAGEL CT (in-house) | full FT, 15 runs × matched \(2.84\times10^{10}\) image tokens | VAE |
| Main diffuser | Qwen-Image-2512 | full FT DiT, 500k steps, смесь SP+NL | text encoder + VAE |
| Prompter | Qwen3.5-397B-A17B | LoRA r=128, SFT→Cold-start→OPSD | вся база LLM |
| Matched NL control | тот же Qwen-Image + тот же LoRA-prompter | те же budget/stages, цели NL | как в SP-ветке |

Diffuserability поднимают annotation + обучением diffuser на SP. Promptability поднимают обучением prompter (и опционально agentic loop). End-to-end цифры в Table 2 — произведение обоих рычагов; ablations по prompter при фиксированном diffuser как раз и разводят вторую половину.
