# Сравнение подходов к обучению re-prompter’ов: SFT, RL, agents

Заметка в том же духе, что сравнение NL vs Structured вокруг Seed ([`2607.29679`](https://arxiv.org/pdf/2607.29679)): там чиним confound формата; здесь — отсутствие честного bakeoff по **способу учить** переводчик user prompt → conditioning при фиксированном diffuser и фиксированном целевом IR.

---

## Короткий тейк (как у форматов)

**Сравнение различных подходов обучения re-prompter’ов: SFT, preference/RL, agentic loops**

Сейчас у каждой «школы» своя статья и свой diffuser, поэтому нельзя честно сказать, что покупает качество: данные, награда, многошаговый цикл или просто больший LLM. Хочется получить несмещённый вердикт по **методу обучения prompter’а** — такой, который можно перенести в выбор post-training бюджета.

Сделаем примерно то же, что Seed делает внутри одной лаборатории в Tables 4–5, только как отдельное исследование с открытыми якорями по лагерям. Фиксируем diffuser (полный FT под наш IR, как в плане с Qwen-Image) и целевой формат conditioning (после вердикта NL/SP). Учим один и тот же класс модели-rewriter’а — ориентир Seed: Qwen3.5 с LoRA rank 128, либо меньший открытый Qwen3.5 для методики — разными протоколами: чистый SFT; SFT→preference/RL (DPO / GRPO / OPSD); training-free или lightly-trained agentic refine–render–judge; при возможности гибрид SFT+агент. По итогу сравниваем quality против original user prompt, GPU-часы обучения и latency на запрос.

**Тейк.** SFT учит *распределение* хороших conditioning’ов и даёт главный скачок «уметь формат». RL учит *что переживает frozen diffuser и судья*, но легко награждается verbosity и эстетикой в ущерб верности запросу. Agents покупают качество за inference-compute и критику по картинке, но без обучения часто не догоняют обученный single-shot (у Seed base за 8 раундов не догоняет trained за 1). Пока их не поставить на одну ось cost–quality при одном IR и одном diffuser, выбор «SFT хватит / нужен RL / нужен агент» остаётся вкусом лаборатории.

---

## Базовые подходы (определения)

### 1. Supervised fine-tuning (SFT)

Rewriter учится next-token prediction на парах `(user prompt → target conditioning)`.

Target бывает разный:
- dense NL caption;
- structured JSON / SP (Seed);
- CoT + rewrite.

Данные часто синтетические: original caption как «user», annotation/SP как target; или reverse-engineering (fine → degrade → short), как у Qwen-Image PE.

**Что покупает:** грамматику формата, prior по объектам/атрибутам/layout, стиль, который видел diffuser на train.  
**Чего не покупает напрямую:** сигнал «эта перепись реально улучшила картинку относительно *исходного* запроса».

Якоря:
- [Promptist](https://arxiv.org/abs/2212.09611) (`2212.09611`) — классика SFT→RL для prompt adaptation  
- [Seed Context Scaling](https://arxiv.org/pdf/2607.29679) (`2607.29679`) — SFT на caption→SP, главный скачок structure  
- [Qwen-Image-2.0 PE](https://arxiv.org/abs/2605.10730) (`2605.10730`) — degrade→inverse CoT, потом GRPO  
- [Wan prompt extend](https://arxiv.org/abs/2503.20314) (`2503.20314`) — постановка mismatch user vs train captions  

### 2. Preference / RL на rewriter (при frozen generator)

После (или вместо) SFT rewriter оптимизируют под reward с картинки: Aesthetic, CLIP/VQA, ImageReward, fine-grained AlignEvaluator, verifier gates.

Алгоритмы в поле: PPO (Promptist), DPO / iterative DPO, GRPO/GDPO, SimPO, у Seed — verifier-gated **OPSD** (on-policy distillation от image-conditioned teacher), не «голый» GRPO.

**Что покупает:** выравнивание под то, что diffuser умеет нарисовать и что любит судья.  
**Риски:** reward hacking (длина, beauty↑ alignment↓ — ярко у Input-Side Scaling), зависимость от качества reward model, дорогой on-policy rollout (generate image на каждый sample).

Якоря:
- [PromptEnhancer](https://arxiv.org/abs/2509.04545) (`2509.04545`, CVPR 2026) — SFT→GRPO, AlignEvaluator по 24 failure modes  
- [APE](https://arxiv.org/abs/2606.00204) (`2606.00204`) — NVIDIA, GRPO/GDPO на small enhancers; SAPE/MAPE  
- [Input-Side Scaling](https://arxiv.org/abs/2510.12041) (`2510.12041`) — iterative DPO **без** SFT; scaling размера rewriter  
- [RePrompt](https://arxiv.org/abs/2505.17540) (`2505.17540`) — reasoning + GRPO; naive LLM rewrite часто вредит  
- [FaithRewriter](https://arxiv.org/abs/2606.08492) (`2606.08492`) — visual anchor → MLLM-диагноз → DPO; length-matched pairs  
- Seed (`2607.29679`) — cold-start + verifier-gated OPSD; в абляциях OPSD устойчивее GRPO  
- [Pref-GRPO](https://arxiv.org/abs/2508.20751) (`2508.20751`) — illusory advantage pointwise GRPO  

### 3. Agentic / multi-step inference (часто training-free или слабо дообученный)

Не один rewrite, а цикл: rewrite → render → judge/critique → refine (иногда plan/layout как промежуточный язык).

Варианты:
- **training-free agents** — LLM/VLM + frozen T2I, правила/инструменты;
- **learned router/composer** — как MAPE в APE (objects/attributes/spatial/edits);
- **field-level refine** — Seed agentic loop по failed SP fields.

**Что покупает:** использование пиксельного feedback на тесте, локальный ремонт ошибок.  
**Риски:** latency ×N, насыщение на 2–3 раундах, стоимость verifier на каждый запрос; без сильного base policy цикл «крутит воду».

Якоря:
- [VisualPrompter](https://arxiv.org/abs/2506.23138) (`2506.23138`) — training-free: атомы Entity/Attribute/Relation → вопросы → VLM по картинке → цикл правок  
- [TARA](https://arxiv.org/abs/2607.18724) (`2607.18724`) — type-aware repair; близкий цикл с более сильной схемой вопросов  
- [RPG](https://arxiv.org/abs/2401.11708) (`2401.11708`) — Recaption–Plan–Generate  
- [APE](https://arxiv.org/abs/2606.00204) — MAPE как agentic decomposition + post-train  
- [T2I-Copilot](https://arxiv.org/abs/2507.20536) (`2507.20536`) — training-free multi-agent  
- [OPT2I](https://arxiv.org/abs/2403.17804) (`2403.17804`) — iterative rewrite по decomposed scores, без обучения rewriter  
- Seed (`2607.29679`) Table 5 — refine–render–judge; trained single-shot бьёт длинный цикл base  
- [PRISM](https://arxiv.org/abs/2607.24353) (`2607.24353`) — один VLM = rewriter + judge, multi-objective  

### 4. Соседние, но не то же самое

| Подход | Суть | Якорь |
|--------|------|--------|
| Endogenous / native CoT | «Rewrite» внутри генератора, не внешний PE | [T2I-R1](https://arxiv.org/abs/2505.00703), HunyuanImage 3 |
| Thinking → embeddings | Думает/переписывает, в DiT идут эмбеддинги | [Think-Then-Generate](https://arxiv.org/abs/2601.10332) |
| VLM как единый encoder | Не external re-prompter; смена conditioning path | [UniFusion](https://arxiv.org/abs/2510.12789) |
| Retrieval + test-time | RAPO-стиль | [RAPO](https://arxiv.org/abs/2504.11739) / [RAPO++](https://arxiv.org/abs/2510.20206) |
| Always-on product PE | Закрытые API rewrite | DALL·E 3, Imagen enhancePrompt, Qwen prompt_extend |

Для bakeoff держим **external rewriter + frozen (уже FT) diffuser**, иначе смешаем с end-to-end generator RL. Подробный разбор вашего обзора: [`literature_notes_user_survey.md`](./literature_notes_user_survey.md).

---

## В чём проблема литературы (confound, как у NL/SP)

Лагеря почти не сравниваются head-to-head:

- разные целевые форматы (NL dense vs JSON SP vs CoT prose);
- разные diffuser’ы и разные train captions;
- разные судьи и разные eval (часто vs rewritten, а не vs original);
- RL-статьи редко показывают **чистый SFT ceiling** при тех же данных;
- agent-статьи редко показывают **тот же single-shot rewriter** при том же compute на запрос;
- Seed сравнивает стадии *внутри* своего стека, но не против PromptEnhancer/APE на общем IR.

Поэтому «RL лучше SFT» и «агент лучше single-shot» сейчас нельзя переносить в дизайн так же, как нельзя переносить «SP ≫ NL» без matched info.

---

## Что хочется сделать

Фиксируем:
1. Diffuser — полный FT под наш выбранный IR (после эксперимента про структурность).  
2. Целевой язык conditioning — один (SP или info-matched NL).  
3. База rewriter’а — одно семейство (Qwen3.5 + LoRA r=128 как у Seed, или меньший twin для дешевизны методики).  
4. Eval — GenEval2 / DPG / structure–alignment judges **против original user prompt**; плюс cost: GPU-h train и ms/query (с учётом числа render’ов).

Ветви обучения (накопительно и ортогонально):

| Ветвь | Протокол | Зачем |
|-------|----------|--------|
| Zero-shot / ICL | схема + few-shot, без градиентов | пол ли шкалы |
| SFT-only | caption→IR (+ replay) | потолок чистого supervised |
| SFT→DPO | preference pairs length-matched | дешёвый preference без on-policy image |
| SFT→GRPO | rollout→render→reward | лагерь PromptEnhancer/APE |
| SFT→cold-start→OPSD | лагерь Seed | privileged-image distillation + verifier gate |
| Agentic on base | refine–render–judge без FT | цена inference-only |
| Agentic on SFT / on full | цикл поверх обученного | докупает ли loop после обучения |
| MAPE-style | router→specialists→compose | decomposition vs monolithic rewrite |

Читаем трейдоф как в заметке про budget diffuser vs prompter: наклон Δquality / GPU-h и Δquality / latency, gaps до oracle-IR с картинки.

Ожидания заранее (чтобы не переинтерпретировать):
- SFT даёт основной скачок формата (как Table 4 Seed).  
- RL докупает, если reward не схлопывается в length/aesthetics; иначе alignment проседает (Input-Side Scaling).  
- Agentic на base не догоняет strong SFT single-shot при честном cost (Seed Table 5).  
- Agentic на уже обученном насыщается быстро — loop как complement, не замена training.  
- Если SFT-only при matched data догоняет SFT→RL на вашей метрике vs original — тяжёлый RL для продукта не обязателен.

---

## Как это стыкуется с тейком про NL vs структуру

Там гипотеза: NL несёт подсмыслы и внутреннюю структуру языка; схема облегчает базовые слоты. Проверка — matched facts + paraphrase.

Здесь зеркало на стороне prompter’а:
- SFT на SP учит *заполнять слоты*;
- SFT на dense NL учит *писать прозу с подтекстом*;
- RL награждает то, что diffuser реально съел — может предпочесть «плоский», но удобный для модели язык;
- агент чинит по пикселям и может восстанавливать подсмыслы итеративно.

Поэтому bakeoff методов обучения имеет смысл **после** (или совместно с) вердиктом по формату: иначе RL «под SP» и SFT «под NL» снова сравнят разные интерфейсы, а не разные алгоритмы.

---

## Шаблон (1)–(4) для этой идеи

**(1) Идея.** Честный bakeoff протоколов обучения external re-prompter’а (SFT / preference-RL / agentic / гибриды) при фиксированном diffuser, фиксированном IR и eval vs original prompt, с осями train-cost и serve-cost.

**(2) Цель.** Понять, куда класть post-training бюджет prompter’а и нужен ли inference-time агент; улучшить cost-aware выбор стадии, а не табличный SOTA одной лаборатории.

**(3) Мотивация.** Seed, PromptEnhancer, APE, Input-Side Scaling, RPG/OPT2I рассказывают несовместимые истории на разных стеках; внутри Seed SFT — главный скачок, OPSD > GRPO, агент насыщается рано — но без кросс-лагерного matched протокола это нельзя генерализовать. Reward hacking и eval vs rewritten делают «RL лучше» особенно хрупким выводом.

**(4) Новизна.** Есть ablations стадий внутри работ; нет стандартного open bakeoff «SFT vs DPO vs GRPO vs OPSD vs agentic» на одном IR/diffuser с двойной осью стоимости. Ближе всего Seed Tables 4–5 и разрозненные PE-papers выше — их и сводим на общий стенд.

Связанные файлы: [`ideas_t2i_conditioning_narrative.md`](./ideas_t2i_conditioning_narrative.md) (идея 5), [`training_bytedance_context_scaling.md`](./training_bytedance_context_scaling.md), [`fundamental_papers_reprompt_reading_list.md`](./fundamental_papers_reprompt_reading_list.md).
