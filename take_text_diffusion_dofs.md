# Степени свободы text diffusion — разбор по алгоритму

Связано с [`how_text_diffusion_works.md`](./how_text_diffusion_works.md), [`report_text_diffusion_landscape.md`](./report_text_diffusion_landscape.md), [`research/text-diffusion/`](./research/text-diffusion/).

**Объект:** генерация / моделирование текста диффузионной (обычно masked/discrete) LM.  
**Вопрос:** что можно варьировать в определении модели и семплирования, и как это влияет на качество (likelihood, downstream, latency, controllability).

Ниже — не эссе, а проход по алгоритму:

1. выделить основные степени свободы  
2. по каждой: если изучена — SOTA + поризонить; если нет — выделить и предложить эксперимент  
3. список утверждений к обсуждению  
4. что улучшить в самом разборе  

---

# ШАГ 1. Выделить основные степени свободы

Рабочий критерий: фактор меняет **определение forward/reverse процесса, архитектуры или политики семплирования**, а не просто «другую задачу». Качество = fluency + adequacy + (часто) tokens/sec.

## 1. Пространство состояний (representation)

Токены как категории; непрерывные эмбеддинги + rounding; сжатый continuous latent. Меняет весь math и тип guidance.

## 2. Семейство порчи (corruption / forward process)

Absorbing MASK vs uniform jump vs mixture vs Gaussian-on-embeddings. Определяет, *какой* шум модель учится снимать.

## 3. Временна́я формулировка

Discrete-time цепочка \(Q_t\) vs continuous-time CTMC / continuous ELBO. Влияет на objective, солверы и переносимость schedule.

## 4. Расписание шума / маскирования (train)

Линейное, cosine, spindle, data-driven, state-dependent (GenMD4). Согласование train schedule с inference — отдельный риск.

## 5. Параметризация reverse-модели

\(x_0\)-logits, concrete score/rates, прямой posterior mean. Связана с стабильностью обучения и тем, что можно guidance’ить.

## 6. Training objective

ELBO / score entropy / Rao–Blackwellized masked CE / consistency / preference (VRPO). «Тот же MDM» с разным loss ≠ тот же optima.

## 7. Архитектура и inductive bias

Full bidirectional; AR-init + adaptation; block-causal; MoE. Определяет KV-cache, length, перенос AR знаний.

## 8. Число шагов семплирования (NFE) и distillation

Сколько denoising/unmasking steps; student few-step. Прямой tradeoff quality ↔ latency.

## 9. Политика unmasking (порядок и сколько токенов за шаг)

Random fixed-k; confidence threshold; learned policy; block-wise semi-AR. Сейчас один из главных рычагов open dLLM.

## 10. Remasking / self-correction

Можно ли вернуть токен в MASK и переписать; пороги; spatial-temporal rules. Отдельно от первого unmasking.

## 11. Stochasticity / temperature / nucleus при unmask

Greedy argmax vs sample from logits; interaction с confidence heuristics.

## 12. Guidance (CFG и др.)

Scale, schedule во времени, когда выключать; classifier/reward guidance; structured constraints.

## 13. Conditioning interface

Clean prompt prefix; mask-only response (SFT); bidirectional condition; length/FIM spans.

## 14. Токенизация и словарь

BPE vs char; vocab size; multilingual token inflation — меняет «сложность» одной позиции.

## 15. Длина контекста и блочность

Fixed length MDM vs block diffusion vs sliding; packing; EOS handling.

## 16. Гибридность AR×diffusion (block size и родственные)

`block_size=1` ≈ AR; большой блок ≈ parallel diffusion. Явная интерполяция двух парадигм.

## 17. Данные и alignment stack

Pretrain mix, SFT masking policy (только response), preference/RL for diffusion.

## 18. Train–infer mismatch по промежуточным состояниям

Train: random masks. Infer: confidence / block heuristics. Отдельная DOF «насколько распределение intermediate states совпадает».

---

# ШАГ 2. По каждой степени свободы: изучена или нет?

Типы доказательств (не путать):

1. **Theory / small-scale isolation** — чистая абляция на GPT-2 scale / synthetic.  
2. **Scaled system claim** — LLaDA/Dream/Mercury: сильный результат, но много факторов сразу.  
3. **Inference-only** — тот же checkpoint, меняется только sampler/guidance.  

System-level показывает потолок системы, но **плохо изолирует** одну DOF.

---

## 1. Пространство состояний

- **Статус: ИЗУЧЕНА (как развилка), но не «закрыта».**
- **SOTA.** На language modeling доминирует **discrete absorbing/masked** (MDLM, MD4, LLaDA, Dream). Continuous embedding path (Diffusion-LM и наследники) жив для controllable / seq2seq, но не лидирует как LLM-backbone. Latent continuous — чаще conditional generation.
- **Поризонить.** Почти нет современного matched bakeoff: один и тот же data/compute budget, discrete MDM vs continuous embedding diffusion vs latent, одинаковый eval. «Discrete победил» = исторический path dependence + engineering, не обязательно теорема.
- **Что улучшить.** Matched 1B-scale bakeoff трёх representation при фиксированном tokenizer и data; метрики: PPL bound, gen PPL, downstream, controllability suite.

## 2. Семейство порчи

- **Статус: ИЗУЧЕНА.**
- **SOTA.** Absorbing/mask стабильно лучше uniform на тексте в линии D3PM → SEDD Absorb → MDLM/MD4. Поэтому modern dLLM ≈ MDM.
- **Поризонить.** Сравнения часто на маленьком scale; mixture / soft-mask / edit-based corruption снова всплывают в 2025–2026 («soft-masked», edit refinement). «Mask всегда оптимален» для reasoning/code не доказано.
- **Эксперимент.** На одном backbone: absorbing vs uniform vs 10/30/50% uniform-mixture vs soft-mask; одинаковый NFE budget; отдельно LM PPL и code/math.

## 3. Временна́я формулировка

- **Статус: ЧАСТИЧНО.**
- **SOTA.** Continuous-time ELBO для masked diffusion упрощён до weighted CE (MD4); SEDD даёт CTMC score path. На практике large models часто живут в discrete unmasking steps с continuous-motivated loss.
- **Поризонить.** Discrete vs continuous *solver* при том же trained model редко изолирован. Выигрыш CTMC solvers vs простой ancestral unmasking на 8B почти не стандартизирован.
- **Эксперимент.** Зафиксировать MD4/LLaDA-style checkpoint; сравнить ancestral discrete steps vs CTMC/τ-leaping-style solvers при equal NFE.

## 4. Train noise / mask schedule

- **Статус: ЧАСТИЧНО.**
- **SOTA.** MD4: linear хорошо для текста; GenMD4 state-dependent улучшает likelihood. BD3-LM: data-driven clipped schedules ↓ gradient variance. DiffusionBERT spindle — frequency-aware (ранний).
- **Поризонить.** Schedule почти всегда joint-tuned с architecture. Мало transfer: schedule от OWT-GPT2 → 8B instruct.
- **Эксперимент.** Grid schedule families на фиксированной модели; отдельно перенос schedule без retune при смене domain (code vs prose).

## 5. Параметризация reverse-модели

- **Статус: ЧАСТИЧНО → почти консенсус для MDM.**
- **SOTA.** Для absorbing: **mask-token \(x_0\) prediction + CE** доминирует (MDLM/MD4/LLaDA). SEDD score parameterization сильнее в CTMC-рамке, но сложнее и менее стабильна в части сравнений.
- **Поризонить.** Путают parameterization и objective. Мало абляций «тот же ELBO, другая head».
- **Эксперимент.** Shared trunk, heads: x0 logits vs score/rates vs posterior; identical compute; train curves + sample quality.

## 6. Training objective

- **Статус: ИЗУЧЕНА на foundations, открыта на alignment.**
- **SOTA.** Simplified masked ELBO / mixture-of-MLM (MDLM, MD4) — default pretrain. Preference/VRPO (LLaDA 1.5) — ранняя линия alignment. Consistency / traj distillation — post-train objectives для few-step.
- **Поризонить.** Gen-PPL и ELBO могут врать (precision, diversity tradeoffs). «Лучший ELBO ⇒ лучший chat» не показано systematically.
- **Что улучшить.** Multi-objective Pareto: ELBO / gen quality / instruction / diversity при смене только loss weights.

## 7. Архитектура и inductive bias

- **Статус: ЧАСТИЧНО (два сильных recipe).**
- **SOTA.** From-scratch bidirectional MDM: LLaDA 8B ~ LLaMA3-8B class claims. AR-adaptation: Dream, DiffuLLaMA — быстрый путь. MoE diffusion (LLaDA-MoE) — efficiency. Block-causal — для cache.
- **Поризонить.** From-scratch vs adapt **не matched** по data/tokenizer/compute. Industrial Mercury/Gemini — закрытые, нельзя атрибутировать архитектуре.
- **Эксперимент.** Один corpus, два init (random vs AR), одна MDM objective; scale sweep 1B→8B; измерить sample efficiency.

## 8. Число шагов / distillation

- **Статус: АКТИВНО ИЗУЧАЕТСЯ, не закрыта.**
- **SOTA.** Naive: quality растёт с steps до насыщения. Fast-dLLM / confidence parallel снижает effective steps. Distill/consistency/few-step papers 2025–2026 бьют по NFE (заявки до ~10×–16× в conditional settings).
- **Поризонить.** Curves steps↔quality редко публикуют для одного 7–8B на широком suite. Distill часто меняет и guidance. Mean-field factorization error растёт при агрессивном parallel unmask.
- **Эксперимент.** Pareto frontier: steps ∈ {1,2,4,8,16,32,64,128,256} × (base vs distilled) на фиксированных prompts; latency на одном GPU; accuracy + diversity.

## 9. Политика unmasking

- **Статус: ИЗУЧЕНА ВЗРЫВНО, но не стабилизирована.**
- **SOTA.** Confidence-threshold parallel unmasking (Fast-dLLM) — de facto baseline ускорения open dLLM. Learned policies ([2512.09106](https://arxiv.org/abs/2512.09106)) целят лучше heuristic. Semi-AR blocks часто нужны, чтобы heuristics работали.
- **Поризонить.** Пороги λ, block length, «at least one token» rules — хрупкие. Сравнения легко выиграть выбором плохого baseline schedule. Переносимость policy между LLaDA и Dream неясна.
- **Эксперимент.** Latin-square: {random-k, top-k confidence, threshold λ grid, learned policy} × {BL=8,32,128} на одном checkpoint; фиксировать wall-clock.

## 10. Remasking / self-correction

- **Статус: ЧАСТИЧНО / СПОРНО.**
- **SOTA.** Много training-free remask методов (WINO, STaRR, …). Re-eval ([2606.12232](https://arxiv.org/abs/2606.12232)): выигрыш WINO над Fast-dLLM часто **маргинален** при стандартных коротких блоках; сильные цифры бывают patch’ем плохих decode settings.
- **Поризонить.** Remasking смешивают с изменением числа steps и stochasticity. Нет стандартного протокола «remask budget».
- **Эксперимент.** При полном matched Fast-dLLM baseline: remask on/off × greedy/sample × BL; абляция «только когда confidence упала» vs «всегда low-conf remask»; cost в extra NFE.

## 11. Stochasticity / temperature

- **Статус: НЕДОИЗУЧЕНА как изолированная DOF.**
- **Предлагаем выделить явно:** temperature/top-p при параллельном unmask ≠ temperature в AR; взаимодействует с confidence.
- **Почему мало литературы.** Часто greedy для бенчмарков; stochastic включают ad hoc.
- **Эксперимент.** Sweep T и top-p при fixed unmask policy; метрики: pass@k, diversity, contradiction rate; отдельно с/без remask (remask как antidote к noise).

## 12. Guidance (CFG и др.)

- **Статус: ЧАСТИЧНО.**
- **SOTA.** CFG помогает conditional MDM, но **schedule важен**: early high CFG вредит ([2507.08965](https://arxiv.org/abs/2507.08965)). Commitment-horizon: CFG можно выключить после точки commitment ([2608.08082](https://arxiv.org/abs/2608.08082)). Distill guidance → 1 forward.
- **Поризонить.** Оптимальный γ зависит от prompt; «γ=constant» почти наверняка suboptimal. Reward guidance в discrete менее зрелый, чем в continuous image.
- **Эксперимент.** Prompt-stratified: constant-γ vs late-only vs adaptive commit-horizon; измерять constraint success и NFE.

## 13. Conditioning interface

- **Статус: ЧАСТИЧНО.**
- **SOTA.** LLaDA SFT: маскировать только response. FIM / span infill — естественный выигрыш dLLM (Mercury coding narrative). Prefix-clean continuation — стандарт.
- **Поризонить.** Мало абляций: same data formatted as prefix-LM vs mask-response vs full-bidirectional condition. Multiturn chat packing для diffusion слабо стандартизирован.
- **Эксперимент.** Один SFT corpus, три packing schema; eval: single-turn, multiturn, FIM, reversal tasks.

## 14. Токенизация и словарь

- **Статус: НЕ ВЫДЕЛЕНА / НЕДОИЗУЧЕНА для dLLM.**
- **Предлагаем выделить:** vocab/tokenization как first-class DOF для diffusion (в AR изучена лучше).
- **Почему.** Mask diffusion loss живёт *по позициям токенов*; другой tokenizer меняет число шагов смысла на «позицию». Multilingual inflation может бить parallel decode иначе, чем AR.
- **Эксперимент.** Retrain small MDM на identical bytes с BPE-32k / BPE-100k / byte-level; equal wall-clock train; compare bits/byte, not only token PPL.

## 15. Длина контекста и блочность

- **Статус: ЧАСТИЧНО.**
- **SOTA.** Pure MDM часто fixed-length; BD3-LM даёт arbitrary length + cache. Long-context dLLM — активная инженерная зона (dynamic chunking и т.п.).
- **Поризонить.** Long-context quality claims редко с needle/Havre-style suites, matched к AR long-context.
- **Эксперимент.** Needle-in-haystack + long dependency tasks: pure MDM sliding vs BD3 vs AR; plot accuracy vs context length vs latency.

## 16. Гибридность / block size

- **Статус: ИЗУЧЕНА как идея, не исчерпана.**
- **SOTA.** BD3-LM: block size интерполирует AR↔diffusion; SOTA likelihood среди diffusion на LM benchmarks; KV cache.
- **Поризонить.** Оптимальный block size task-dependent (code vs chat). Interaction block size × confidence unmasking × remask — мало factorial designs.
- **Эксперимент.** Factorial: block_size ∈ {1,4,16,64,256} × unmask policy; Pareto quality/throughput.

## 17. Данные и alignment stack

- **Статус: ЧАСТИЧНО (наследует AR playbook).**
- **SOTA.** Pretrain+SFT работает для LLaDA; preference (VRPO) для LLaDA 1.5; industrial undisclosed stacks.
- **Поризонить.** Неясно, нужны ли *diffusion-specific* data curricula (например, больше noisy reconstructions) vs копировать AR data.
- **Эксперимент.** Curriculum: AR-style next-token data vs mask-reconstruction heavy mix; same tokens seen; downstream delta.

## 18. Train–infer intermediate-state mismatch

- **Статус: НЕДОИЗУЧЕНА, но уже названа в few-step работах.**
- **Предлагаем выделить явно** как DOF: расстояние между train mask distribution и inference mask distribution.
- **SOTA-намёк.** Trajectory self-distillation / training on teacher rollouts бьёт именно в mismatch ([2602.12262](https://arxiv.org/abs/2602.12262)).
- **Эксперимент.** Замерить TV/KL между train random-masks и masks от confidence sampler; fine-tune с imitation of infer masks; абляция «только mismatch fix» без уменьшения steps.

---

# ШАГ 3. Список степеней свободы и вложенных утверждений к обсуждению

Формат: **DOF → утверждения** (соглашаться / спорить / уточнять).

### DOF 1 — Representation
- D1.1 Discrete absorbing tokens — правильный default для LLM-scale text diffusion.
- D1.2 Continuous embedding diffusion интересен главным образом для guidance/control, не для raw LM quality.
- D1.3 Без matched bakeoff нельзя честно хоронить continuous path.

### DOF 2 — Corruption family
- D2.1 Mask ≫ uniform на open-web LM.
- D2.2 Для code/edit soft-mask или edit-corruption может обогнать hard absorbing.
- D2.3 Mixture corruption — недооценённый компромисс.

### DOF 3 — Time formulation
- D3.1 Continuous-time theory важна для вывода loss, не обязательна как runtime solver.
- D3.2 На 8B CTMC solvers не дают бесплатного quality при equal NFE (гипотеза).

### DOF 4 — Train schedule
- D4.1 Linear mask schedule достаточно силён для текста.
- D4.2 State-dependent / data-driven schedules — real gains, но хрупкий transfer.

### DOF 5 — Parameterization
- D5.1 \(x_0\) CE parameterization достаточна для SOTA MDM.
- D5.2 Score parameterization окупается только вместе с CTMC tooling.

### DOF 6 — Objective
- D6.1 Pretrain = masked ELBO/CE.
- D6.2 Chat quality требует отдельных preference objectives, не следует из PPL.
- D6.3 Distillation objectives — отдельный класс, не «ещё pretrain».

### DOF 7 — Architecture / init
- D7.1 AR-init ускощает путь к конкурентному dLLM.
- D7.2 From-scratch нужен, чтобы утверждать «LLM capabilities ≠ AR».
- D7.3 Block-causal attention — необходим для practical KV-cache.

### DOF 8 — Steps / distill
- D8.1 Open dLLM без distill обычно проигрывает AR по latency при matched quality.
- D8.2 Few-step distill — главный product unlock после scale.
- D8.3 Step–quality curve должна стать обязательным артефактом papers.

### DOF 9 — Unmasking policy
- D9.1 Confidence thresholding — необходимый baseline, не research novelty сам по себе.
- D9.2 Learned policies стоит сравнивать при fixed wall-clock, не fixed steps.
- D9.3 Semi-AR blocks часто «держат» heuristic unmasking.

### DOF 10 — Remasking
- D10.1 Remasking не универсальное улучшение; часто patch плохих settings.
- D10.2 Remask budget нужно нормализовать в extra NFE.
- D10.3 Remasking полезнее при stochastic decode, чем при greedy.

### DOF 11 — Stochasticity
- D11.1 Temperature в parallel unmask — отдельная наука от AR temperature.
- D11.2 Diversity метрики обязательны; иначе greedy завышает «качество».

### DOF 12 — Guidance
- D12.1 Constant CFG suboptimal; нужен time/prompt schedule.
- D12.2 CFG можно рано выключать после commitment.
- D12.3 Guidance distillation обязателен для production CFG.

### DOF 13 — Conditioning interface
- D13.1 Mask-only-response SFT — правильный default.
- D13.2 FIM/infill — killer app dLLM vs AR.
- D13.3 Multiturn packing для diffusion недоспецифицирован.

### DOF 14 — Tokenization
- D14.1 Отчётность в bits/byte обязательна при сравнении tokenizer.
- D14.2 Multilingual token inflation бьёт dLLM иначе, чем AR (гипотеза).

### DOF 15 — Context / length
- D15.1 Pure fixed-length MDM недостаточен как LLM product.
- D15.2 Long-context eval должен быть отдельным треком, не «ещё MMLU».

### DOF 16 — Block size hybrid
- D16.1 Block size — первоклассный Pareto-контроль quality/speed.
- D16.2 Оптимум task-dependent (код ≠ open chat).

### DOF 17 — Data / alignment
- D17.1 Копировать AR data pipeline — baseline, не оптимум.
- D17.2 Diffusion-specific curricula могут улучшить sample efficiency (гипотеза).

### DOF 18 — Train–infer mismatch
- D18.1 Random-mask train + confidence infer — структурный mismatch.
- D18.2 Training on infer-like trajectories — один из самых чистых unlock’ов few-step quality.

---

# ШАГ 4. Что улучшить в самом разборе

1. **Подтянуть deep JSON** по каждому item из `outline.yaml` (сейчас landscape+DOF опираются на surveys + selective reads).  
2. **Добавить citation trees** от MDLM/MD4/LLaDA/BD3/Fast-dLLM как в prompt-length research.  
3. **Разделить DOF на train-time vs infer-time** визуально (сейчас смешанный список — удобно для обсуждения, хуже для экспериментального планирования).  
4. **Ввести единый eval harness proposal** (tasks × metrics × latency protocol), иначе DOF-споры нерешаемы.  
5. **Отдельно пройти continuous embedding path** — в этом разборе он сознательно сжат, потому что центр массы ушёл в discrete MDM.

---

## Практический приоритет (если выбирать, что крутить первым)

| Приоритет | DOF | Почему |
|-----------|-----|--------|
| P0 | Unmasking policy (#9) + steps (#8) | максимальный impact на open checkpoints без retrain |
| P0 | Block size (#16) | явный Pareto + KV-cache |
| P1 | CFG schedule (#12) | дешёвый conditional unlock |
| P1 | Train–infer mismatch (#18) | фундамент для честного few-step |
| P2 | Remasking (#10) | проверить, не иллюзия ли выигрыша |
| P2 | Tokenization (#14) | долгосрочный, дорогой retrain |
| P3 | Representation (#1) revisit | нужен большой matched bakeoff |
