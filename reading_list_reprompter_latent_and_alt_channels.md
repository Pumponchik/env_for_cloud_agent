# Статьи: нетекстовый / латентный re-prompter → генератор

**Фокус:** как обогатить вход T2I **без** (или не главным образом через) текстовый rewrite.  
**Не про:** latent communication между LLM-агентами (LatentMAS / Interlat / Beyond Tokens) — это другая задача.

Канал, о котором речь:

```
user prompt → [re-prompter / bridge] → ??? → generator
                              ↑
                    текст | векторы | schema | layout | внутри модели | action
```

---

## 1. Латентный / векторный re-prompter (читать первым)

Идея: enrichment в **embedding / hidden / soft-prompt** space; генератор ест векторы, не новый абзац.

| # | Статья | arXiv | Что делает |
|---|--------|-------|------------|
| 1 | **ELLA** | [`2403.05135`](https://arxiv.org/abs/2403.05135) | LLM → Timestep-Aware Semantic Connector → continuous conditioning; U-Net frozen. Канон «векторного» bridge. |
| 2 | **SUR-adapter** | [`2305.05189`](https://arxiv.org/abs/2305.05189) | Короткий casual prompt → adapter embeddings **без** выдачи rewritten string. |
| 3 | **LaVi-Bridge** | [`2403.07860`](https://arxiv.org/abs/2403.07860) | Произвольный LM × vision model через adapter/LoRA; continuous bridge. |
| 4 | **LLM4GEN** | [`2407.00737`](https://arxiv.org/abs/2407.00737) | Cross-Adapter: CLIP + LLM features fused → diffusion. |
| 5 | **Think-Then-Generate** | [`2601.10332`](https://arxiv.org/abs/2601.10332) | Есть reasoning, но в DiT идут **embeddings** (не текстовый продукт rewrite). Ближе всего к «latent re-prompt». |
| 6 | **LI-DiT** | [`2406.11831`](https://arxiv.org/abs/2406.11831) | Naive LLM-as-encoder **ломает** alignment — обязателен до дизайна connector. |
| 7 | **DimFusion** (в FIBO) | [`2511.06876`](https://arxiv.org/abs/2511.06876) | Длинный LLM context → компактные vectors (fusion по embedding-dim). |
| 8 | **Semantic Routing** | [`2602.03510`](https://arxiv.org/abs/2602.03510) | Какой слой LLM отдавать в conditioner (не static single layer). |
| 9 | **PEO** | [`2510.02599`](https://arxiv.org/abs/2510.02599) | Training-free **embedding-space** prompt enhancement (vs textual rewrite). |
| 10 | **IPGO** | [`2503.21812`](https://arxiv.org/abs/2503.21812) | Continuous injections в prompt embedding + constraints. |
| 11 | **Manipulating Embeddings of SD Prompts** | [`2308.12059`](https://arxiv.org/abs/2308.12059) | Прямая оптимизация embedding, не текста. |
| 12 | **PEZ** | [`2302.03668`](https://arxiv.org/abs/2302.03668) | Soft continuous opt → project to hard tokens; граница soft/hard. |
| 13 | **DPO-Diff** | [`2407.01606`](https://arxiv.org/abs/2407.01606) | Gradient discrete prompt opt в diffusion (часто через embedding relaxation). |
| 14 | **TextCraftor** | [`2403.18978`](https://arxiv.org/abs/2403.18978) | Reward-tune **text encoder** (векторный путь), U-Net frozen. |
| 15 | **GlueGen** | [`2303.10056`](https://arxiv.org/abs/2303.10056) | Align произвольный encoder → latent space T2I (GlueNet). |

**Минимум:** 1 ELLA → 2 SUR-adapter → 5 Think-Then-Generate → 6 LI-DiT → 9 PEO → 7 DimFusion.

---

## 2. Другие способы передачи (не latent-векторы)

### 2.1 Schema / structured wire (форма, не «красивый prompt»)

| # | Статья | arXiv | Канал |
|---|--------|-------|-------|
| 16 | **FIBO** | [`2511.06876`](https://arxiv.org/abs/2511.06876) | JSON schema → generator |
| 17 | **BBQ-to-Image** | [`2602.20672`](https://arxiv.org/abs/2602.20672) | Numeric bbox + RGB в structured text |
| 18 | **Structured Captions 19M** | [`2507.05300`](https://arxiv.org/abs/2507.05300) | Фиксированный порядок полей |
| 19 | **Ideogram 4** | [docs](https://github.com/ideogram-oss/ideogram4/blob/main/docs/prompting.md) | Exclusive JSON + Magic Prompt compiler |
| 20 | **Rich Text** | [`2304.06720`](https://arxiv.org/abs/2304.06720) | Атрибуты (цвет, вес) вне plain text |

### 2.2 Layout / plan (геометрия)

| # | Статья | arXiv | Канал |
|---|--------|-------|-------|
| 21 | **LMD** | [`2305.13655`](https://arxiv.org/abs/2305.13655) | Boxes |
| 22 | **RPG** | [`2401.11708`](https://arxiv.org/abs/2401.11708) | Regions + (опц.) recaption |
| 23 | **SCoT** | [`2602.11980`](https://arxiv.org/abs/2602.11980) | Text CoT vs boxes — разные gains |
| 24 | **GLIGEN** | [`2301.07093`](https://arxiv.org/abs/2301.07093) | Grounded box conditioning |
| 25 | **MetaCanvas** | [`2512.11464`](https://arxiv.org/abs/2512.11464) | Plan в spatial latent |
| 26 | **ATLAS** | [`2607.16409`](https://arxiv.org/abs/2607.16409) | Layout как shared IR |

### 2.3 Внутри генератора (endogenous «re-prompt»)

Нет внешнего текстового PE-сервиса — enrichment в весах/CoT модели.

| # | Статья | arXiv | Канал |
|---|--------|-------|-------|
| 27 | **T2I-R1** | [`2505.00703`](https://arxiv.org/abs/2505.00703) | Semantic + token CoT внутри |
| 28 | **SEER** | [`2601.20305`](https://arxiv.org/abs/2601.20305) | Endogenous self-aligned descriptors |
| 29 | **HunyuanImage 3** | [`2509.23951`](https://arxiv.org/abs/2509.23951) | Native CoT rewrite |
| 30 | **Z-Image PE-aware SFT** | [`2511.22699`](https://arxiv.org/abs/2511.22699) | Generator учится на выходах PE (co-adapt) |
| 31 | **ShortCoTI** | [`2510.05593`](https://arxiv.org/abs/2510.05593) | Длинный CoT может вредить |

### 2.4 Action space (рычаг не «сообщение», а sampler)

| # | Статья | arXiv | Канал |
|---|--------|-------|-------|
| 32 | **PromptLoop** | [`2510.00430`](https://arxiv.org/abs/2510.00430) | Refine от **latent states** denoising |
| 33 | **PAE** | [`2404.04095`](https://arxiv.org/abs/2404.04095) | Token weights + timesteps |
| 34 | **Attend-and-Excite** | [`2301.13826`](https://arxiv.org/abs/2301.13826) | Attention nursing без rewrite |
| 35 | **RAISE** | [`2603.00483`](https://arxiv.org/abs/2603.00483) | Rewrite ∪ resample ∪ edit |
| 36 | **ReNO** | [`2406.04312`](https://arxiv.org/abs/2406.04312) | Optimize initial noise |

### 2.5 Текстовый re-prompter (для контраста)

| # | Статья | arXiv |
|---|--------|-------|
| 37 | PromptEnhancer | [`2509.04545`](https://arxiv.org/abs/2509.04545) |
| 38 | APE (NVIDIA) | [`2606.00204`](https://arxiv.org/abs/2606.00204) |
| 39 | TARA | [`2607.18724`](https://arxiv.org/abs/2607.18724) |
| 40 | GenEval 2 | [`2512.16853`](https://arxiv.org/abs/2512.16853) |

---

## 3. Как это ложится на твою гипотезу

Ты хочешь убрать middle hop `… → текст → encode → vectors`.

Ближайшие ответы **именно про re-prompter→G**:

| Подход | Middle hop |
|--------|------------|
| ELLA / SUR / LaVi / Think-Then-Generate | LLM states → connector → vectors (текст не обязателен как продукт) |
| PEO / IPGO / Manipulating Embeddings | Optimise уже в embedding space |
| DimFusion / Semantic Routing | Какие continuous features отдать G |
| Endogenous (T2I-R1 / SEER) | Нет внешнего re-prompter |
| Schema / layout | Другой дискретный канал (не prose), не latent |

Полная таксономия: [`report_bridge_methods_taxonomy.md`](./report_bridge_methods_taxonomy.md).
