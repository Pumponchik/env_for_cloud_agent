# Reading List: Latent Transfer & Other Bridge Channels

**Дата:** 2026-07-31  
**Запрос:** убрать текстовый bottleneck (latent reasoning / latent re-prompt / vector messages между модулями); затем — другие способы передачи.  
**Связано:** [`report_bridge_methods_taxonomy.md`](./report_bridge_methods_taxonomy.md)

---

## A. Сначала это — латентная передача (твой фокус)

Читать **в этом порядке**.

### A1. Фундамент: зачем убирать текст

| # | Работа | Ссылка | Зачем |
|---|--------|--------|-------|
| 1 | **Beyond Tokens** — survey latent communication in LLM MAS | [`2606.05711`](https://arxiv.org/abs/2606.05711) | Карта поля: WHAT/WHICH/HOW; ~18 методов; trade-offs capacity vs audit |
| 2 | **Coconut** — Chain of Continuous Thought | [`2412.06769`](https://arxiv.org/abs/2412.06769) | Latent reasoning *внутри* одной LLM: last hidden → снова input embedding, без decode в слово |
| 3 | **LatentMAS** — Latent Collaboration in Multi-Agent Systems | [`2511.20639`](https://arxiv.org/abs/2511.20639) | Агенты думают и обмениваются в latent space (hidden + KV working memory); training-free |
| 4 | **Interlat** — Enabling Agents to Communicate Entirely in Latent Space | ACL 2026 · [PDF](https://aclanthology.org/2026.acl-long.1248.pdf) · [code](https://github.com/XiaoDu-flying/Interlat) | «Telepathy» между агентами: last hidden states + compression; до 24× faster |
| 4b | **DiffMAS** — Learning to Communicate | [`2604.21794`](https://arxiv.org/abs/2604.21794) | Latent KV-канал как **обучаемый** компонент (не fixed protocol) |
| 4c | **Cache-to-Cache** | [`2510.03215`](https://arxiv.org/abs/2510.03215) | Прямая semantic communication через KV между LLM |
| 4d | **Thought Communication** | [`2510.20733`](https://arxiv.org/abs/2510.20733) | Обмен «мыслями» (hidden), не словами |
| 4e | **LatentSeek** | [`2505.13308`](https://arxiv.org/abs/2505.13308) | Test-time policy gradient в latent space (рядом с Coconut) |

### A2. Латентный мост к генератору картинок (тот же принцип, другой receiver)

| # | Работа | Ссылка | Зачем |
|---|--------|--------|-------|
| 5 | **ELLA** | [`2403.05135`](https://arxiv.org/abs/2403.05135) | LLM → continuous conditioning → frozen diffusion (векторный «репромптер») |
| 6 | **SUR-adapter** | [`2305.05189`](https://arxiv.org/abs/2305.05189) | Короткий prompt → adapter embeddings *без* выдачи rewritten text |
| 7 | **Think-Then-Generate** | [`2601.10332`](https://arxiv.org/abs/2601.10332) | Reasoning есть, но в DiT идут **embeddings** rewrite, не строка как продукт |
| 8 | **LI-DiT** | [`2406.11831`](https://arxiv.org/abs/2406.11831) | Важно: naive LLM-as-encoder *ломает* alignment — читать до дизайна connector |
| 9 | **DimFusion** (в FIBO) | [`2511.06876`](https://arxiv.org/abs/2511.06876) | Длинный LLM context → компактные vectors по embedding-dim |
| 10 | **MetaCanvas** | [`2512.11464`](https://arxiv.org/abs/2512.11464) | Plan прямо в spatial/spatiotemporal **latent**, не в text plan |

### A3. Soft / continuous prompt optimization (латентный opt без агентов)

| # | Работа | Ссылка | Зачем |
|---|--------|--------|-------|
| 11 | **PEZ** | [`2302.03668`](https://arxiv.org/abs/2302.03668) | Soft vs hard; оптимизация в continuous, project в tokens |
| 12 | **PEO** | [`2510.02599`](https://arxiv.org/abs/2510.02599) | Training-free embedding-space prompt enhancement |
| 13 | **IPGO** | [`2503.21812`](https://arxiv.org/abs/2503.21812) | Continuous injections в prompt embedding с constraints |
| 14 | **Manipulating Embeddings of SD Prompts** | [`2308.12059`](https://arxiv.org/abs/2308.12059) | Прямая манипуляция embedding, не текста |

**Минимум на вечер:** 1 → 2 → 3 → 5 → 7 → 8.

---

## B. Потом — другие способы передачи (не latent-only)

Когда поймёшь latent-канал, сравни с альтернативами.

### B1. Текстовый канал (классический bottleneck, но зрелый)

| # | Работа | Ссылка | Канал |
|---|--------|--------|-------|
| 15 | **APE** (NVIDIA) | [`2606.00204`](https://arxiv.org/abs/2606.00204) | Text rewrite agents (SAPE/MAPE) |
| 16 | **PromptEnhancer** | [`2509.04545`](https://arxiv.org/abs/2509.04545) | External CoT rewriter |
| 17 | **TARA** | [`2607.18724`](https://arxiv.org/abs/2607.18724) | Typed text repair + gate |
| 18 | **GenEval 2** | [`2512.16853`](https://arxiv.org/abs/2512.16853) | Text rewrite может *вредить* |

### B2. Schema / числа (дискретный, но не «проза»)

| # | Работа | Ссылка | Канал |
|---|--------|--------|-------|
| 19 | **FIBO** | [`2511.06876`](https://arxiv.org/abs/2511.06876) | JSON schema wire |
| 20 | **BBQ-to-Image** | [`2602.20672`](https://arxiv.org/abs/2602.20672) | Numeric bbox + RGB в structured text |
| 21 | **Structured Captions 19M** | [`2507.05300`](https://arxiv.org/abs/2507.05300) | Порядок полей = сигнал |
| 22 | Ideogram 4 docs | [prompting](https://github.com/ideogram-oss/ideogram4/blob/main/docs/prompting.md) | Exclusive JSON |

### B3. Layout / plan (геометрический канал)

| # | Работа | Ссылка | Канал |
|---|--------|--------|-------|
| 23 | **LMD** | [`2305.13655`](https://arxiv.org/abs/2305.13655) | Boxes |
| 24 | **RPG** | [`2401.11708`](https://arxiv.org/abs/2401.11708) | Recaption + region plan |
| 25 | **SCoT** | [`2602.11980`](https://arxiv.org/abs/2602.11980) | Ablation: text CoT vs boxes — **разные gains** |
| 26 | **ATLAS** | [`2607.16409`](https://arxiv.org/abs/2607.16409) | Layout как shared representation |

### B4. Endogenous (обогащение внутри генератора)

| # | Работа | Ссылка | Канал |
|---|--------|--------|-------|
| 27 | **T2I-R1** | [`2505.00703`](https://arxiv.org/abs/2505.00703) | Internal semantic + token CoT |
| 28 | **SEER** | [`2601.20305`](https://arxiv.org/abs/2601.20305) | Endogenous reprompt; Cognitive Gap |
| 29 | **ShortCoTI** | [`2510.05593`](https://arxiv.org/abs/2510.05593) | Длинный CoT может вредить |

### B5. Action space (не сообщение, а рычаг sampler)

| # | Работа | Ссылка | Канал |
|---|--------|--------|-------|
| 30 | **Attend-and-Excite** | [`2301.13826`](https://arxiv.org/abs/2301.13826) | Attention nursing |
| 31 | **RAISE** | [`2603.00483`](https://arxiv.org/abs/2603.00483) | Mixed: rewrite ∪ resample ∪ edit |
| 32 | **PromptLoop** | [`2510.00430`](https://arxiv.org/abs/2510.00430) | Prompt refine от latent states denoising |
| 33 | **PAE** | [`2404.04095`](https://arxiv.org/abs/2404.04095) | Token weights + timesteps |

---

## C. Как читать под твою гипотезу

Гипотеза: *любой дискретный middle hop = потеря; лучше latent.*

| Читать | Что проверяет |
|--------|----------------|
| Beyond Tokens + LatentMAS + Interlat | Гипотеза в **агентах** — да, линия реальная |
| Coconut | Latent reasoning без второго агента |
| ELLA + Think-Then-Generate + LI-DiT | Тот же принцип для **T2I conditioner** |
| SCoT + BBQ | Где latent/text **не** хватает — нужны boxes/числа |
| GenEval 2 + ShortCoTI | Дискретный/длинный канал иногда хуже, не всегда лучше latent-by-default |

**Вывод для дизайна:**  
1) для enrichment смысла — смотри **A (latent)**;  
2) для spatial/parametric — **B2/B3** не заменяются latent prose-encoder;  
3) audit/UX — оставь тонкий text side-channel (hybrid из survey agenda).

---

## Полные отчёты в репо

- Таксономия всех bridge: [`report_bridge_methods_taxonomy.md`](./report_bridge_methods_taxonomy.md)  
- Каталог: [`papers_catalog_bridge_methods.md`](./papers_catalog_bridge_methods.md)  
- Textual PE ядро: [`fundamental_papers_reprompt_reading_list.md`](./fundamental_papers_reprompt_reading_list.md)
