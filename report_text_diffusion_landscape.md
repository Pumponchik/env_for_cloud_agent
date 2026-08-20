# Ландшафт исследования: диффузионные модели для текста

Дата среза: **2026-08-20**.  
Связано с: [`how_text_diffusion_works.md`](./how_text_diffusion_works.md), [`take_text_diffusion_dofs.md`](./take_text_diffusion_dofs.md), [`research/text-diffusion/`](./research/text-diffusion/).

---

## 1. Короткий вердикт

К 2025–2026 text diffusion перестала быть «игрушечной альтернативой AR»:

- математика **masked / absorbing discrete diffusion** упрощена до практически CE-обучения (MDLM, MD4, RADD);
- появились **open 7–8B dLLM** (LLaDA from scratch, Dream / DiffuLLaMA из AR);
- **индустрия** заявила продуктный scale (Mercury, Gemini Diffusion) с упором на throughput;
- центр тяжести сместился с «можно ли?» на **inference DOFs**: unmasking order, remasking, CFG schedule, distillation, block/hybrid KV-cache.

Ниже — карта областей, что уже «закрыто», что горячо, и куда смотреть.

---

## 2. Таксономия областей

```
Text diffusion
├── A. Foundations (что такое шум и objective)
│   ├── continuous embedding diffusion (Diffusion-LM lineage)
│   ├── discrete D3PM-style (uniform / absorbing / structured Q_t)
│   ├── continuous-time CTMC / score entropy (SEDD)
│   └── simplified masked ELBO (MDLM, MD4, GenMD4, RADD)
├── B. Scaling recipes (как получить LLM-класс)
│   ├── train from scratch MDM (LLaDA, Scaling MDM)
│   ├── adapt AR → diffusion (DiffuLLaMA, Dream, RND1, …)
│   └── MoE / larger scales (LLaDA-MoE, LLaDA2.0 mentions)
├── C. Hybridization with AR
│   ├── block diffusion / semi-AR (BD3-LM)
│   └── any-order / soft-mask / generation-order unification
├── D. Inference systems
│   ├── parallel unmasking + confidence thresholds (Fast-dLLM)
│   ├── remasking / self-correction (WINO, STaRR, edit refinement)
│   ├── learned unmasking policies
│   └── few-step distillation / consistency (CDLM, traj. distill)
├── E. Guidance & control
│   ├── CFG for masked diffusion (+ schedules)
│   ├── constraints / FIM / structured decode
│   └── preference / VRPO / alignment for dLLM
├── F. Multimodal dMLLM
│   └── LLaDA-V, Dimple, LaViDa, MMaDA, …
└── G. Evaluation & critique
    ├── PPL vs sample quality / precision artifacts
    ├── AR bakeoffs under matched data/compute
    └── «why mask diffusion fails» style stress tests
```

---

## 3. Хронология якорей

| Период | Что произошло | Примеры |
|--------|---------------|---------|
| 2021–2022 | Foundations | D3PM; Diffusion-LM; early seq diffusion |
| 2023 | CTMC / score path | SEDD; discrete flow theory |
| 2024 | Masked diffusion «simplifies» | MDLM; MD4/GenMD4; Scaling MDM ~1B |
| early 2025 | LLM-scale open models | LLaDA 8B; DiffuLLaMA; Dream; BD3-LM (ICLR’25 Oral) |
| mid 2025 | Industry + surveys | Mercury; Gemini Diffusion (cited); surveys 2506.13759, 2508.10875 |
| late 2025–2026 | Inference arms race | Fast-dLLM; remasking debates; CFG theory; few-step distill; dMLLM; MoE dLLM |

---

## 4. Что активно развивается (2025–2026)

### 4.1 Inference: порядок раскрытия и remasking — **самый горячий фронт**

После появления сильных open dLLM выяснилось: качество сильно зависит не только от весов, но от **политики unmasking**.

- Fast-dLLM: confidence threshold + параллельный decode + KV-cache tricks ([2505.22618](https://arxiv.org/abs/2505.22618)).
- Learned unmasking policies ([2512.09106](https://arxiv.org/abs/2512.09106)).
- Remasking / self-correction (STaRR [2601.04205](https://arxiv.org/abs/2601.04205); WINO; re-eval [2606.12232](https://arxiv.org/abs/2606.12232) — benefit часто setting-dependent).
- Soft-masked / edit-based refinement, dynamic chunking (см. Awesome-DLMs timeline 2025–2026).

**Почему горячо:** это дешёвый рычаг без retrain; одновременно здесь максимум путаницы в сравнениях (разные block length, greedy vs stochastic).

### 4.2 Гибриды AR × diffusion (block size как DOF)

BD3-LM ([2503.09573](https://arxiv.org/abs/2503.09573)): AR между блоками, diffusion внутри → KV-cache + flexible length + интерполяция quality/parallelism через `block_size`.

Продолжения: Fast-dLLM v2 / SlowFast / consistency models с block-causal masks (CDLM).

### 4.3 Few-step / distillation

Проблема: чтобы rival AR quality, dLLM часто жжёт много NFE. Линия 2025–2026:

- dual distillation of **guidance + trajectory**;
- trajectory self-distillation ([2602.12262](https://arxiv.org/abs/2602.12262));
- infinite-mask few-step ([2605.10518](https://arxiv.org/abs/2605.10518));
- consistency-style CDLM.

### 4.4 CFG и conditional generation в discrete setting

CFG перенесён с картинок, но:

- early high guidance вредит, late помогает ([2507.08965](https://arxiv.org/abs/2507.08965));
- guidance может стать **избыточной после commitment horizon** ([2608.08082](https://arxiv.org/abs/2608.08082));
- CFG удваивает NFE → отдельно дистиллируют.

### 4.5 Scaling path: from-scratch vs AR-adaptation

Два лагеря:

| Path | Пример | Смысл |
|------|--------|-------|
| From scratch MDM | LLaDA | чистый тест «нужен ли AR inductive bias» |
| Adapt AR | Dream, DiffuLLaMA, многие industrial | быстрее догнать экосистему данных/весов |
| Hybrid scale | Block schemes, LLaDA2.0 mentions, MoE | инженерный pragmatic SOTA |

### 4.6 Multimodal / alignment / productization

- dMLLM: LLaDA-V, Dimple, …
- Preference for diffusion (VRPO / LLaDA 1.5)
- Mercury refreshed: coding + throughput product loop
- Tooling: dLLM frameworks unifying MDLM/BD3 training+eval ([2602.22661](https://arxiv.org/abs/2602.22661))

---

## 5. Что относительно «устаканилось»

Уже можно считать **рабочим консенсусом** (с оговорками):

1. **Absorbing / masked** corruption обычно сильнее uniform на language modeling (D3PM → MDLM/MD4 era).
2. Objective для masked diffusion **можно писать как weighted CE** — сложный CTMC score не обязателен, чтобы получить сильный MDM.
3. Bidirectional Transformer + mask predictor — default architecture для open dLLM.
4. Parallel decode **не бесплатен**: без умного schedule/блоков легко проиграть AR по latency *или* quality.
5. Controllability / FIM / mid-sequence edit — естественное преимущество vs causal AR.

Не консенсус (и не должно быть):

- «dLLM уже строго лучше AR» на matched compute;
- «больше steps всегда лучше»;
- «remasking всегда помогает»;
- «CFG always-on оптимален».

---

## 6. Карта ключевых объектов (для deep-research)

Полный список — в [`research/text-diffusion/outline.yaml`](./research/text-diffusion/outline.yaml). Ядра:

**Foundations:** D3PM, Diffusion-LM, SEDD, MDLM, MD4, RADD  
**Scale:** LLaDA, Dream, DiffuLLaMA, Mercury, Gemini Diffusion  
**Hybrid/Infer:** BD3-LM, Fast-dLLM, Remasking line, CFG line, Distill line  
**Meta:** surveys 2506.13759 & 2508.10875; Awesome-DLMs

---

## 7. Как это стыкуется с алгоритмом степеней свободы

Ландшафт отвечает: *какие рычаги люди крутят*.  
DOF-разбор ([`take_text_diffusion_dofs.md`](./take_text_diffusion_dofs.md)) отвечает: *какие рычаги реально изолированы, где SOTA, где нужен эксперимент*.

Практическая рекомендация для следующего шага исследования: не раздувать ещё модели «вообще», а выбрать **2–3 DOF** (например unmasking policy × num steps × CFG schedule) и гонять matched bakeoff на одном backbone.
