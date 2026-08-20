# Автономный аудит открытых проблем: captions · PE · bridges · length

**Дата аудита:** 2026-08-03  
**Метод:** полный проход по отчётам репо (`prompt-length`, `reprompt-systems`, `bridge-methods`, latent/alt channels, taxonomy F1–F6) + параллельный web/arXiv search по 5 веткам + ручная сверка «закрыто / частично / открыто».  
**Правило честности:** не объявлять тему CLOSED, если есть лишь эвристика после генерации, один backbone или confounded ablation.  
**Короткий companion:** [`report_open_research_questions_reprompt_bridge.md`](./report_open_research_questions_reprompt_bridge.md)

---

## 0. Вердикт аудита

Поле **не** закрыто. С середины 2025 до июля 2026 появились сильные *частичные* ответы:

| Тезис | Статус после аудита |
|-------|---------------------|
| Длина NL ≠ информация | **Сильно закрыт** (`2607.29679` GPG/ED; Caption Detailness `2505.15172`) |
| Structure confounded с length | **Частично закрыт** Matched NL control в `2607.29679` (SP ≫ matched-train NL); **не** универсальный закон на всех DiT |
| PE иногда вредит | **Закрыт эмпирически** (GenEval 2, AtelierEval, PromptEnhancer regressions) |
| Predictive PE gating *до* generate | **Открыт** (есть post-hoc accept/revert: TARA/VisualPrompter; нет oracle-gap) |
| Head-to-head Brack vs i1 vs FIBO | **Открыт** — ни одного matched tournament |
| Schema expander bias | **Открыт** (FairPro закрыл prose) |
| Latent re-prompter vs text PE @ matched FLOPs на frozen DiT | **Открыт** (SoftREPA/IPGO/DATE/PromptLoop/LatentMorph — разные оси) |
| Realizability до generate | **Частично** (FaithRewriter offline anchors; SEER endogenous; нет cheap pre-filter) |

Ниже: карта областей → статус старых T1–T12 → **24 новые проблемы** → ранжированный backlog → чеклист «не начинать».

---

## 1. Карта областей ресерча в репо

```
A. Prompt / caption length & train–infer match
   └─ Brack · i1 · Hunyuan broadband · RECAP · DetailMaster · LongT2I · TIIF · SEER ~23w

B. Textual prompt enhancement (F1)
   └─ PromptEnhancer · ISS · APE/MAPE · FaithRewriter · RAISE · CRAFT · Ideogram Magic Prompt

C. Structured / schema bridges (F4)
   └─ FIBO · BBQ · Ideogram tree · Cosmos JSON · context-scaling SP · Reve layout IR

D. Embedding / latent bridges (F2)
   └─ ELLA · SUR · Think-Then-Generate · RISE-T2V · DATE · SoftREPA · IPGO · UniFusion VERIFI · LatentMorph

E. Layout / geometry / action (F3, F6)
   └─ SCoT · GLIGEN-line · EPIC · CoCo · DesignAsCode · GenClaw

F. Endogenous / typed repair (F5)
   └─ SEER · VisualPrompter · TARA · PromptLoop

G. Evaluation / judges / protocols
   └─ GenEval 2 · AtelierEval · FaithT2I · TaBR · MagicBench · DPG · WISE · CoReBench

H. Bias / diversity / safety (смежное)
   └─ FairPro · Brack diversity · PromptMoG · PE injection (почти пусто)
```

---

## 2. Статус прежних сквозных тем (T1–T12) — переаудит

### T1. Три рецепта длины — head-to-head  
**Статус: ОТКРЫТ ★★★★★**

Никто не сравнил на matched backbone/data/compute:

| Рецепт | Paper | Суть |
|--------|-------|------|
| A | Brack `2506.16679` | randomize length/density |
| B | i1 `2606.11289` | 100% long train + inference rewrite |
| C | FIBO `2511.06876` | long structured + VLM→JSON |
| D | Hunyuan `2509.23951` | hierarchical ~30–1000 |
| E | context-scaling `2607.29679` | SP train + trained prompter (новый «рецепт E») |

Добавить в tournament как минимум A/B/C/E. SEER (`2601.20305`) про **inference** ~23 слова, не про train caption law — примирение только через ось *executability × information*, не short vs long.

### T2. Realizability / mismatch переехал в rewriter  
**Статус: ЧАСТИЧНО**

- **FaithRewriter** `2606.08492`: simulate-then-distill с visual anchors; hard negatives против verbosity hacking; FaithT2I. Закрывает «нужен visual grounding при обучении rewriter», но **не** cheap filter без offline image generation.  
- SEER: endogenous, shared space.  
- **Дырка:** `P(realizable | revised, G)` *до* generate для disjoint PE (APE/PromptEnhancer).

### T3. Когда PE включать  
**Статус: ОТКРЫТ (теория); ЧАСТИЧНО (эвристики)**

Закрыто «can hurt». Не закрыто predictive decision:

| Метод | Что делает | Почему не закрывает T3 |
|-------|------------|------------------------|
| TARA `2607.18724` | accept-or-revert после repair | post-generation |
| VisualPrompter | skip если нет missing concepts | нужен visual diagnose |
| APE | router `no_rewrite` на editing | не calibrated gain predictor |
| RAISE/CRAFT | adaptive budget loops | после первых renders |
| SPOT `2602.00616` | selective rewrite | safety, не visual gain |
| Ideogram AUTO | product heuristic | непрозрачно |

**Нужно:** `E[Δscore | prompt, G, caption-law]` + oracle-gap benchmark: always-skip / always-enhance / oracle / learned gate / cost-adjusted.

### T4. Structure ⊥ length  
**Статус: ЧАСТИЧНО ЗАКРЫТ `2607.29679`**

Matched NL control (те же images, budget, prompter stages; только NL vs SP interface) → SP сильно выше (GenEval2 GM ~72.5 vs ~36).  
Плюс Caption Detailness `2505.15172`: length — плохой proxy; ICR/AOD лучше.  
Structured Captions `2507.05300`: порядок полей при том же контенте.

**Всё ещё открыто:** multi-backbone/multi-seed replication; JSON vs graph/layout/prose IR при *matched information* (не только matched tokens); open reproducible GPG/ED judges.

### T5. Schema interoperability  
**Статус: ОТКРЫТ ★★★★**

FIBO ≠ Ideogram (key-order load-bearing) ≠ BBQ numeric ≠ Cosmos temporal ≠ Reve HTML/SVG-like ≠ Seed SP.  
Нет round-trip loss, нет compiler IR.

### T6. Single-attribute controllability + leakage  
**Статус: ОТКРЫТ**

TaBR у BRIA; BizGenEval/ServImage — commercial-ish, не leakage protocol. Нужны seed-matched counterfactuals + non-target preservation.

### T7. Faithfulness revised_prompt / CoT  
**Статус: ОТКРЫТ**

FaithRewriter/PRISM трогают intent; **нет** port LLM CoT faithfulness (perturb clause → image change). Нет provenance ledger: user-specified vs inferred vs hallucinated fields.

### T8. Latent / soft / embedding PE vs text @ matched FLOPs  
**Статус: ОТКРЫТ ★★★★**

Новые точки на карте (не bakeoff):

| Paper | Канал | Почему не закрывает |
|-------|-------|---------------------|
| SoftREPA `2503.08250` | soft tokens, frozen backbone | alignment fine-tune, не re-prompter user→cond |
| AGSM `2605.30038` | soft tokens + score matching | чинит SoftREPA counting |
| IPGO | continuous prefix/suffix | reward prompt tuning |
| DATE `2510.23974` | dynamic embeddings during sampling | training-free |
| PromptLoop `2510.00430` | latent feedback rewrite loop | не matched vs strong textual PE |
| LatentMorph `2602.02227` | latent thoughts | AR UMM, не DiT connector |
| Think-Then-Generate / RISE / ELLA / UniFusion VERIFI | mixed | разные цели |

**Нужен bakeoff:** text rewrite · soft tokens · dynamic emb · latent thoughts · layout · schema · predicates — один frozen G, matched latency/FLOPs, eval vs **original** prompt.

### T9. Credit assignment RL-rewriter  
**Статус: ОТКРЫТ** (APE future work жив)

PRE-GRPO / Stepwise-Flow-GRPO — про diffusion trajectory, не prompter stages. Нет per-field/per-atom rewards для router→rewrite→compose.

### T10. VLM-as-judge drift  
**Статус: ЧАСТИЧНО**

GenEval 2 закрыл «старый GenEval сгнил». Открыто: continuous drift detection без full human re-study; anti-circular repair (не тот же VLM diagnose+reward+eval).

### T11. Prompt-addressable ceiling  
**Статус: ОТКРЫТ ★★★★**

TARA/VisualPrompter/SEER/T2ICountBench: часть fail’ов не чинится prompt’ом. Нет oracle decomposition: wording / schema / layout / verifier / generator-intrinsic.

### T12. Bias / diversity от PE  
**Статус: ЧАСТИЧНО**

FairPro `2512.04981` — prose. PromptMoG `2511.20251` — long prompts ↑fidelity ↓diversity.  
Открыто: schema expanders; cultural/aesthetic homogenization; PE style mode collapse.

---

## 3. Что `2607.29679` меняет в agenda (отдельно)

Статья Seed *Scaling Properties of Text Conditioning* — самый важный апдейт августа 2026 для этой карты.

**Добавляет в научный словарь:**

- **Diffusability** — потолок формата caption’а  
- **Promptability** — насколько prompter достигает потолка  
- **GPG / ED** — измерители image-grounded information  
- Scaling: loss ~ linear(GPG), power-law(ED)

**Закрывает как «гипотезу»:** «просто сделай NL длиннее» — нет.  
**Не закрывает:** tournament рецептов train; PE gating; bias schema; open cheap metrics; multi-backbone universality; когда agentic loop оправдан vs single-shot.

**Новые исследовательские объекты из неё:**

1. Независимый measurement diffusability vs promptability (предсказывать gain *до* full train).  
2. Open-source GPG/ED (без Gemini/GPT-as-judge monopoly).  
3. Format-tax-aware prompters: free CoT → затем schema emit (см. Format Tax `2604.03616`).  
4. Field-level edit leakage как стандартный тест SP-trained G.

---

## 4. Новые области проблем (придуманы + валидированы поиском)

Каждая: **статус · crisp question · якоря · почему дырка**.

### N01. Diffusability × Promptability как измеримый факторинг  
**OPEN ★★★★★** · `2607.29679`  
Можно ли независимо оценить потолок формата и качество prompter’а так, чтобы предсказывать end-to-end gain без полного joint train?

### N02. Test-time compute allocation  
**OPEN ★★★★★** · ISS, RAISE, PSP, context-scaling agentic  
При фиксированном budget: купить PE tokens / rewrite candidates / diffusion steps / seeds / agentic rounds? Политика как функция (prompt type, G, latency).

### N03. Oracle-gap PE gating benchmark  
**OPEN ★★★★★** · GenEval 2, AtelierEval, TARA  
Стандартный протокол: always-skip, always-enhance, per-prompt oracle, learned gate, cost-adjusted gate. Сейчас никто не репортит oracle gap.

### N04. Caption mixture laws как научный объект  
**OPEN ★★★★** · Brack, i1, Detailness, context-scaling  
Не «какой один caption», а mixture short/long/structured/synthetic → Pareto short-user vs long-enhanced. Factorial: length × coverage × redundancy × structure.

### N05. Information metrics без proprietary judges  
**OPEN ★★★★** · GPG/ED, Detailness ICR/AOD  
Нужны открытые, калиброванные, дешёвые proxies с uncertainty; иначе scaling laws невоспроизводимы.

### N06. Schema IR compiler + round-trip  
**OPEN ★★★★** · FIBO, Ideogram, BBQ, Cosmos, Reve, Seed SP  
Канонический scene IR → compile to prose / JSON / boxes / SVG / embeddings; metric round-trip loss + key-order brittleness.

### N07. Rewrite provenance ledger  
**OPEN ★★★★** · FaithRewriter, FIBO fields, context-scaling SP  
Каждая добавленная деталь: user-specified | world-knowledge | visual-inferred | style-prior | hallucinated. Audit отдельно.

### N08. World-knowledge PE vs compositional constraints  
**OPEN ★★★★** · WISE, World-To-Image, Think-Then-Generate, CoReBench  
Когда внешнее знание заполняет gaps, как не перетереть явные counts/layout/attributes?

### N09. Spelling / text-rendering vs rewrite  
**OPEN ★★★★** · UniFusion, TARA text type, FontFusion-line  
Как PE сохраняет exact strings (logos, UI, quotes) при enrichment вокруг типографики?

### N10. Multilingual PE / cross-lingual caption mismatch  
**OPEN ★★★★** · PMT2I `2501.07086`, CTA-Flux line  
Translate / bilingual-expand / culturally adapt / preserve native? English-centric train captions vs non-EN users.

### N11. T2I→T2V transfer laws для PE operators  
**OPEN ★★★★** · RAPO `2504.11739`, SCMAPR, RISE-T2V, APE future work  
Какие операторы T2I PE выживают требования motion / temporal consistency / causality?

### N12. Personalization of the enhancer (не только G)  
**OPEN ★★★** · APPO, preference adapters  
Маленькая user-model для стиля PE без вреда literal following и privacy.

### N13. PE как security boundary  
**OPEN ★★★★** · OWASP LLM01, почти пусто в T2I PE literature  
Injection через enhancer→generator: untrusted text управляет rewriter policy и visual semantics.

### N14. Synthetic PE style / diversity collapse  
**OPEN ★★★★** · PromptMoG, FairPro, Brack diversity, DAVE-line  
Стандартизированные rewriters схлопывают aesthetic/demographic/style distribution?

### N15. Negative prompting as compiled constraint satisfaction  
**OPEN ★★★** · ONG, NAG, CDG, Automated Negative Prompting `2512.07702`  
Compile negative constraints → positive / negative / attention controls с предсказуемыми tradeoffs; связать с PE gating.

### N16. Geometry-aware PE without brittle JSON  
**OPEN ★★★★** · SCoT, ConsistCompose, Format Tax  
Может ли prose(+soft structure) нести executable layout так же надёжно, как coordinate schemas?

### N17. Cacheable / amortized prompters  
**OPEN ★★★** · APE SLM, production PE cost  
Когда кешировать SP/rewrite по semantic similarity без заморозки intent/diversity?

### N18. Distillation survival curves huge→SLM prompter  
**OPEN ★★★** · APE, FaithRewriter distill, context-scaling prompter scale  
Что выживает: intent, grounding, multilinguality, safety, compositional repair?

### N19. CFG / guidance × PE length/structure  
**OPEN ★★★** · Prompt-aware CFG `2509.22728`  
Нужен ли другой guidance schedule для enhanced vs original prompt?

### N20. Soft-token / continuous PE как re-prompter (не alignment FT)  
**OPEN ★★★★** · SoftREPA, AGSM, IPGO  
Можно ли *на лету* из user prompt эмитить soft conditioning competitive с textual PE, без per-model soft-token training на captions?

### N21. Process rewards for PE reasoning  
**OPEN ★★★** · APE credit gap, PromptEnhancer keypoints  
Score intermediate CoT/layout/predicate *до* image; не только terminal reward.

### N22. Verifier-resistant refinement / judge gaming  
**OPEN ★★★★** · GenEval 2, VLM judges rank≠score  
Учится ли PE gaming VQA/MLLM judges? Нужны adversarial human-audited predicate suites.

### N23. Agentic vs single-shot: feature-conditioned policy  
**OPEN ★★★** (методы crowded, **политика** open) · CRAFT, RAISE, context-scaling Tmax  
При каких prompt features agentic оправдан? context-scaling: returns saturate ~4; training lifts start — количественная policy ещё нет.

### N24. Open PE harness + reproducibility  
**OPEN ★★★** (service, высокая ценность) · GenEval 2 closed rewriters complaint  
Единый harness: generators × judges × seeds × languages × cost; eval vs original; length-matched controls; open rewriter weights.

---

## 5. Ранжированный backlog «за что ухватиться»

Оценка: novelty × impact × feasibility × насколько дырка ещё жива после аудита.

| Rank | Проблема | Stars | Тип работы |
|------|----------|-------|------------|
| 1 | **Oracle-gap PE gating** (N03+T3) | ★★★★★ | benchmark + predictor |
| 2 | **Recipe tournament** A/B/C/E (T1+N04) | ★★★★★ | controlled train study |
| 3 | **Compute allocation** PE vs steps vs rounds (N02) | ★★★★★ | systems + theory |
| 4 | **Bridge bakeoff** text/soft/latent/layout/schema @ matched FLOPs (T8+N20) | ★★★★☆ | systems bakeoff |
| 5 | **Diffusability×Promptability** independent meters (N01) | ★★★★☆ | metric science |
| 6 | **Open GPG/ED** (N05) | ★★★★☆ | metric + release |
| 7 | **Schema IR + round-trip** (N06+T5) | ★★★★☆ | standards + eval |
| 8 | **Provenance ledger + faithfulness** (N07+T7) | ★★★★☆ | audit protocol |
| 9 | **Schema bias audit** (T12 schema) | ★★★★☆ | FairPro transfer |
| 10 | **Prompt-addressable ceiling** (T11) | ★★★★☆ | oracle study |
| 11 | **WK vs composition conflict** (N08) | ★★★★☆ | conflict bench |
| 12 | **Text-render vs rewrite** (N09) | ★★★★☆ | typed PE |
| 13 | **Multilingual PE policy** (N10) | ★★★★☆ | cross-lingual |
| 14 | **T2I→T2V PE transfer** (N11) | ★★★★☆ | transfer laws |
| 15 | **PE security / injection** (N13) | ★★★★☆ | red-team |
| 16 | **Diversity collapse of PE** (N14) | ★★★★☆ | measurement |
| 17 | **Geometry without JSON** (N16) | ★★★☆☆ | representation |
| 18 | **Realizability pre-filter** (T2) | ★★★☆☆ | predictor |
| 19 | **Attribute leakage bench** (T6) | ★★★☆☆ | benchmark |
| 20 | **CFG × PE** (N19) | ★★★☆☆ | ablations |
| 21 | **Process rewards / credit** (N21+T9) | ★★★☆☆ | RL |
| 22 | **Judge gaming** (N22+T10) | ★★★☆☆ | eval security |
| 23 | **Amortized/cached PE** (N17) | ★★☆☆☆ | systems |
| 24 | **SLM distillation survival** (N18) | ★★☆☆☆ | distillation |
| 25 | **Open harness** (N24) | ★★☆☆☆ | infra |

---

## 6. Казалось открытым → нашёлся ответ (обновлено)

| Вопрос | Статус | Где |
|--------|--------|-----|
| Длина NL масштабирует loss/качество? | **Нет** (saturates) | `2607.29679`, Fig.1/3; DetailMaster negative length corr. |
| Structure только из-за длины? | **Скорее нет** (Matched NL) | `2607.29679` |
| Нужны ли metrics информативности? | **Да, GPG/ED работают** | `2607.29679`; предки GPG `2403.14003` |
| PE can hurt? | **Да** | AtelierEval, GenEval 2, PromptEnhancer |
| Visual grounding для rewriter? | **Частично да** | FaithRewriter |
| Endogenous PE без внешнего LLM? | **Да** | SEER |
| Soft tokens помогают alignment? | **Да** (не PE bakeoff) | SoftREPA, AGSM |
| Bias prose PE? | **Да, усиливает** | FairPro |
| Always-on rewrite? | Эмпирика «нет» | GenEval 2 + gates |
| Head-to-head recipes? | **Всё ещё нет** | — |
| Predictive gating? | **Всё ещё нет** | — |
| Schema standard? | **Нет** | — |
| Latent vs text PE matched DiT? | **Нет** | — |
| Dedicated T2I-PE survey? | **Нет** | APO/controllable surveys смежные |

---

## 7. Ложные «закрытия» — не попадаться

Некоторые обзоры/заметки mid-2026 объявляют CLOSED то, что закрыто лишь узко:

| Заявление | Реальность |
|-----------|------------|
| «PE gating закрыт TARA/RAISE» | Закрыт *post-hoc repair*, не predictive utility |
| «Latent PE закрыт PromptLoop» | Есть метод; нет bakeoff vs textual PE |
| «Length recipes закрыты i1/Brack» | Есть отдельные рецепты; нет tournament |
| «Structure vs length закрыт» | Сильный Matched NL на одной линии Seed; нужна репликация |
| «Faithfulness закрыт FaithRewriter» | Лучший grounding pipeline; нет causal clause audit |
| «VLM drift закрыт GenEval 2» | Показан drift; continuous monitoring open |

---

## 8. Практические стартовые пакеты (1 проект)

**Пакет A — быстро цитируемо:** Oracle-gap gating benchmark на GenEval2/DPG + cheap predictor.  
**Пакет B — «закрывает спор области»:** Recipe tournament на i1 open recipe: random-length / long+rewrite / SP+prompter / mixture.  
**Пакет C — systems:** Matched-FLOPs bridge bakeoff на Qwen-Image или FLUX.  
**Пакет D — metrics:** Open GPG/ED + diffusability/promptability split.  
**Пакет E — risk:** Schema bias + PE injection + diversity collapse (одна «harm suite»).

Не начинать: очередной always-on aesthetic rewriter; agentic debate без gate/cost; MAS latent messaging (другая область).

---

## 9. Чеклист хорошего paper (аудит 2026-08)

- Eval vs **original** user prompt  
- Length- **and** information-matched controls  
- Report skip / enhance / oracle  
- Diversity + bias, не только alignment  
- Назвать generator’s **train caption law**  
- Schema: ablate structure vs length **and** vs matched-info prose  
- Latent/soft: сравнить с strong textual PE @ matched compute  
- Open rewriter / seeds / judge version pins  
- Если agentic: cost curves vs single-shot  
- Provenance: что добавил PE сверх user text  

---

## 10. Источники аудита (ядро + новые)

**Ядро репо:** Brack `2506.16679` · i1 `2606.11289` · FIBO `2511.06876` · GenEval 2 `2512.16853` · APE `2606.00204` · ISS `2510.12041` · PromptEnhancer `2509.04545` · SEER `2601.20305` · FairPro `2512.04981` · TARA `2607.18724` · VisualPrompter `2506.23138` · UniFusion `2510.12789` · Think-Then-Generate `2601.10332` · LatentMorph `2602.02227` · AtelierEval `2605.22645` · Format Tax `2604.03616` · BBQ `2602.20672` · ELLA `2403.05135` · RISE-T2V `2511.04317`

**Новые якоря аудита:** context-scaling `2607.29679` · FaithRewriter `2606.08492` · Caption Detailness `2505.15172` · SoftREPA `2503.08250` · AGSM `2605.30038` · PromptLoop `2510.00430` · DATE `2510.23974` · RAISE `2603.00483` · CRAFT `2512.20362` · PromptMoG `2511.20251` · Structured Captions `2507.05300` · LongT2IBench `2512.09271` · TIIF `2506.02161` · DetailMaster `2505.16915` · RAPO `2504.11739` · SCMAPR (ACL 2026) · PMT2I `2501.07086` · HunyuanImage 3.0 `2509.23951` · Fingerprints `2602.22734` · Automated Neg. Prompting `2512.07702` · Prompt-aware CFG `2509.22728` · SCoT `2602.11980`

Корпуса: `research/prompt-length/`, `research/reprompt-systems/`, `research/bridge-methods/`.
