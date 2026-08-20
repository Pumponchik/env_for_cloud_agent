# Text Diffusion — Deep Research Report

Items: **18** · Source: `research/text-diffusion/results/`

## Table of contents

1. [Block Diffusion BD3-LM](#block-diffusion-bd3-lm) — 2025 | hybrid AR x diffusion
2. [CFG for Masked Diffusion](#cfg-for-masked-diffusion) — 2025 | guidance and control
3. [D3PM](#d3pm) — 2021 | discrete foundation
4. [DiffuLLaMA and AR Adaptation](#diffullama-and-ar-adaptation) — 2025 | scaled diffusion LLM
5. [Diffusion-LM](#diffusion-lm) — 2022 | continuous embedding diffusion
6. [Diffusion Multimodal LLaDA-V Dimple](#diffusion-multimodal-llada-v-dimple) — 2025 | multimodal diffusion LM
7. [Distillation and Few-Step dLLMs](#distillation-and-few-step-dllms) — 2026 | inference acceleration
8. [Dream 7B](#dream-7b) — 2025 | scaled diffusion LLM
9. [Fast-dLLM and Unmasking Policies](#fast-dllm-and-unmasking-policies) — 2025 | inference acceleration
10. [Gemini Diffusion](#gemini-diffusion) — 2025 | industrial system
11. [LLaDA](#llada) — 2025 | scaled diffusion LLM
12. [MD4 and GenMD4](#md4-and-genmd4) — 2024 | masked diffusion
13. [MDLM](#mdlm) — 2024 | masked diffusion
14. [Mercury](#mercury) — 2025 | industrial system
15. [RADD and Absorbing Theory](#radd-and-absorbing-theory) — 2024 | masked diffusion
16. [Remasking and Self-Correction](#remasking-and-self-correction) — 2026 | inference acceleration
17. [SEDD](#sedd) — 2023 | discrete foundation
18. [Surveys Discrete Diffusion LLM 2025](#surveys-discrete-diffusion-llm-2025) — 2025 | survey

---

## Block Diffusion BD3-LM

### Identity
- **name**: Block Diffusion BD3-LM
- **year**: 2025
- **organization**: Cornell / Kuleshov group (Arriola et al.)
- **model_type**: hybrid AR x diffusion
- **paper_or_source**: Block Diffusion: Interpolating Between Autoregressive and Diffusion Language Models
- **arxiv_id**: 2503.09573
- **primary_url**: https://arxiv.org/abs/2503.09573

### Representation
- **state_space**: discrete tokens
- **corruption_process**: discrete denoising diffusion within blocks (BD3 builds on D3PM/MDLM-style discrete diffusion)
- **time_formulation**: block-wise diffusion objective with efficient training; discrete diffusion inside blocks
- **noise_or_mask_schedule**: data-driven clipped noise schedules to reduce gradient variance
- **absorbing_token**: yes (masked discrete diffusion within blocks)

### Training
- **parameterization**: block-conditional discrete diffusion / masked predictors within block
- **training_objective**: block diffusion likelihood objective; estimators of gradient variance; specialized efficient training algorithm
- **architecture_backbone**: Transformer with block structure enabling KV caching across completed blocks
- **init_from_ar**: no required; block_size=1 recovers AR-like limit
- **scale_params**: OWT-scale research models; SOTA among diffusion LMs on LM benchmarks at that scale
- **conditioning_mechanism**: autoregressive conditioning on previous blocks; diffusion fills current block

### Inference
- **sampling_algorithm**: decode block-by-block; parallel token sampling inside block; KV cache for prior blocks
- **typical_num_steps**: depends on block size and within-block diffusion steps; tunes quality/efficiency tradeoff
- **unmasking_or_remasking_policy**: within-block diffusion unmasking; interacts with later confidence heuristics
- **guidance_methods**: not the headline contribution
- **claimed_throughput**: improved inference efficiency vs prior diffusion LMs via cache + parallel within-block sampling

### Evidence
- **reported_benchmarks**: SOTA likelihood among diffusion LMs; closes gap toward AR PPL; arbitrary-length generation
- **strengths_claimed**: flexible length; KV cache; interpolates AR↔diffusion via block size; variance-aware schedules
- **known_failure_modes**: block size is a hyperparameter; pure parallel benefits shrink as blocks shrink toward AR
- **isolation_quality**: strong for block-size interpolation narrative; still system recipe with multiple co-designed pieces

### DOF relevance
- **primary_dofs_touched**: block size hybrid; context length; KV cache; train schedule; steps
- **sota_claim_summary**: Canonical hybrid showing block size as first-class Pareto knob between AR and diffusion.
- **remaining_ambiguity**: Optimal block size by task (code/chat/long-context) not fully mapped; interaction with Fast-dLLM policies understudied in original.
- **suggested_followup_experiment**: Factorial block_size × confidence-unmask policy on fixed backbone; plot quality vs tokens/sec.
- **practical_takeaway**: If you need length + cache, prefer block diffusion over naive full-sequence MDM.

### Uncertain fields
- bits_per_byte

---

## CFG for Masked Diffusion

### Identity
- **name**: CFG for Masked Diffusion
- **year**: 2025
- **organization**: multiple theory/systems groups
- **model_type**: guidance and control
- **paper_or_source**: Improving Classifier-Free Guidance in Masked Diffusion; Commitment Before Realization: When CFG Becomes Unnecessary in Masked Diffusion Language Models; guidance+trajectory distillation works
- **arxiv_id**: 2507.08965; 2608.08082
- **primary_url**: https://arxiv.org/abs/2507.08965

### Representation
- **state_space**: discrete tokens
- **corruption_process**: masked diffusion with conditional and unconditional score/logit estimates
- **time_formulation**: guidance applied across denoising/unmasking trajectory
- **noise_or_mask_schedule**: interacts with guidance — naive CFG can unmask too fast early
- **absorbing_token**: yes

### Training
- **parameterization**: conditional vs unconditional mask predictors; logits combination with scale γ
- **training_objective**: train with condition dropout for CFG; distillation can remove dual forward
- **architecture_backbone**: standard MDM backbones
- **init_from_ar**: n/a
- **scale_params**: theory papers use low-dim + high-dim; systems evals up to multi-B / 8B class in distill works
- **conditioning_mechanism**: classifier-free guidance is the mechanism

### Inference
- **sampling_algorithm**: two forwards per step (cond+uncond) unless distilled; schedule-dependent γ(t)
- **typical_num_steps**: inherits base sampler; CFG doubles NFE unless distilled
- **unmasking_or_remasking_policy**: CFG can distort unmasking speed; improved CFG formulations stabilize transport
- **guidance_methods**: CFG with constant/late/adaptive schedules; commitment-horizon switching off CFG
- **claimed_throughput**: distill papers claim large speedups (up to ~16× in conditional settings) retaining quality

### Evidence
- **reported_benchmarks**: conditional generation quality; constraint satisfaction; theory explains early-vs-late guidance
- **strengths_claimed**: CFG transfers to discrete MDM; schedule theory; prompt-specific commitment horizons
- **known_failure_modes**: early high guidance harms; some prompts get no benefit or are hurt; always-on CFG wastes NFE
- **isolation_quality**: theory paper relatively clean on schedule effects; product systems still confound CFG with sampler

### DOF relevance
- **primary_dofs_touched**: guidance; steps/NFE; train-infer mismatch via distill
- **sota_claim_summary**: CFG works in masked diffusion but needs time/prompt-aware schedules; can be turned off after commitment.
- **remaining_ambiguity**: Automatic per-prompt commitment detectors that are cheap and reliable.
- **suggested_followup_experiment**: Prompt-stratified constant-γ vs late-only vs commit-horizon switch; measure constraint success and NFE.
- **practical_takeaway**: Do not ship constant CFG; prefer late/adaptive schedules and distill if latency matters.

---

## D3PM

### Identity
- **name**: D3PM
- **year**: 2021
- **organization**: Google Research / academic coauthors
- **model_type**: discrete foundation
- **paper_or_source**: Structured Denoising Diffusion Models in Discrete State-Spaces (D3PM)
- **arxiv_id**: 2107.03006
- **primary_url**: https://arxiv.org/abs/2107.03006

### Representation
- **state_space**: discrete categorical tokens (also applied to discrete images)
- **corruption_process**: Markov transition matrices Q_t: uniform, absorbing, and nearest-neighbor structured corruption
- **time_formulation**: discrete-time DDPM-style with categorical transitions
- **noise_or_mask_schedule**: scheduled transition matrices over T steps; absorbing variant concentrates mass on MASK
- **absorbing_token**: yes (absorbing-state variant)

### Training
- **parameterization**: parameterize reverse categorical transitions / predict clean or posterior
- **training_objective**: variational bound for discrete diffusion (ELBO)
- **architecture_backbone**: task-dependent networks; Transformer-style for text experiments in follow-on literature
- **init_from_ar**: no
- **conditioning_mechanism**: primarily unconditional / class-conditional setups in original scope

### Inference
- **sampling_algorithm**: ancestral discrete reverse sampling with learned transitions
- **unmasking_or_remasking_policy**: absorbing variant implies progressive unmasking; original paper does not use modern confidence remasking
- **guidance_methods**: limited relative to modern CFG-for-MDM literature
- **claimed_throughput**: not a throughput-focused system

### Evidence
- **reported_benchmarks**: likelihood / sample quality on discrete data; later papers use D3PM absorb as baseline vs SEDD/MDLM/MD4
- **strengths_claimed**: general discrete diffusion framework; absorbing/uniform/structured Q_t design space
- **known_failure_modes**: early objectives/parameterizations later argued suboptimal vs simplified masked CE (MDLM/MD4)
- **isolation_quality**: strong as foundational framework paper; not an isolated modern LLM-scale ablation

### DOF relevance
- **primary_dofs_touched**: corruption family; time formulation; parameterization; training objective
- **sota_claim_summary**: Foundational discrete diffusion recipe; absorbing corruption becomes the ancestor of modern masked diffusion LMs.
- **remaining_ambiguity**: Which Q_t family is optimal depends on domain and scale; D3PM itself does not settle LLM-scale defaults.
- **suggested_followup_experiment**: Re-run absorbing vs uniform vs mixture Q_t at fixed modern MDM architecture and data budget.
- **practical_takeaway**: Use D3PM as conceptual root; for text LM prefer absorbing/masked simplifications unless studying general Q_t.

### Uncertain fields
- bits_per_byte
- open_source_status
- scale_params
- typical_num_steps

---

## DiffuLLaMA and AR Adaptation

### Identity
- **name**: DiffuLLaMA and AR Adaptation
- **year**: 2025
- **organization**: HKUNLP / collaborators
- **model_type**: scaled diffusion LLM
- **paper_or_source**: Scaling Diffusion Language Models via Adaptation from Autoregressive Models
- **arxiv_id**: 2410.17891
- **primary_url**: https://arxiv.org/abs/2410.17891

### Representation
- **state_space**: discrete tokens
- **corruption_process**: diffusion objectives applied after adapting AR models (DiffuGPT/DiffuLLaMA)
- **time_formulation**: discrete diffusion sampling after continual pretraining adaptation
- **absorbing_token**: yes in masked diffusion adaptation setups

### Training
- **parameterization**: repurpose AR Transformer into diffusion denoiser via continual pretraining
- **training_objective**: continual pretraining with diffusion-style objectives from AR init
- **architecture_backbone**: GPT-2 and LLaMA family backbones (127M–7B reported)
- **init_from_ar**: yes — core contribution
- **scale_params**: 127M to 7B (DiffuLLaMA); later works cite extensions to larger scales (e.g., RND1 30B mentions)
- **conditioning_mechanism**: standard prompted LM after adaptation

### Inference
- **sampling_algorithm**: diffusion iterative decoding on adapted model
- **unmasking_or_remasking_policy**: compatible with later Fast-dLLM-class methods
- **claimed_throughput**: scaling/efficiency of training path more than tok/s product claims

### Evidence
- **reported_benchmarks**: demonstrates competitive diffusion LMs by adapting AR checkpoints rather than training from scratch
- **strengths_claimed**: sample-efficient path to scaled dLLMs; reuses AR ecosystem weights/tokenizers
- **known_failure_modes**: may retain AR inductive biases; not a pure test of diffusion-from-scratch hypothesis
- **isolation_quality**: strong as scaling recipe paper; comparisons to from-scratch need careful compute matching

### DOF relevance
- **primary_dofs_touched**: architecture/init; data/alignment stack; scaling path
- **sota_claim_summary**: Establishes AR→diffusion continual pretraining as a primary scaling strategy.
- **remaining_ambiguity**: When from-scratch beats adaptation at equal total compute — still open.
- **suggested_followup_experiment**: Equal token budget: random-init MDM vs AR-init adaptation; scale sweep 1B–8B; downstream + sample efficiency.
- **practical_takeaway**: Want a dLLM quickly? Adapt a strong AR model; reserve from-scratch for scientific controls.

### Uncertain fields
- bits_per_byte
- cfg_schedule
- guidance_methods
- noise_or_mask_schedule
- remask_policy
- typical_num_steps

---

## Diffusion-LM

### Identity
- **name**: Diffusion-LM
- **year**: 2022
- **organization**: Stanford / academic coauthors
- **model_type**: continuous embedding diffusion
- **paper_or_source**: Diffusion-LM Improves Controllable Text Generation
- **arxiv_id**: 2205.14217
- **primary_url**: https://arxiv.org/abs/2205.14217

### Representation
- **state_space**: continuous word embeddings in R^d with rounding back to discrete tokens
- **corruption_process**: Gaussian noise on continuous embeddings (continuous diffusion)
- **time_formulation**: continuous / DDPM-style discrete timesteps on embedding space
- **noise_or_mask_schedule**: standard continuous diffusion noise schedule on embeddings
- **absorbing_token**: no (continuous path; rounding replaces absorbing MASK)

### Training
- **parameterization**: denoising network predicting clean embeddings / noise
- **training_objective**: continuous diffusion denoising score/noise matching objectives adapted to embeddings
- **architecture_backbone**: Transformer operating on continuous latent sequences
- **scale_params**: research-scale (~80M class in later comparison tables); not LLM-scale
- **conditioning_mechanism**: classifier / gradient-based control in continuous latent space; plug-and-play constraints

### Inference
- **sampling_algorithm**: iterative continuous denoising then rounding to tokens
- **unmasking_or_remasking_policy**: n/a (not masked discrete); rounding errors are the discrete commitment mechanism
- **guidance_methods**: gradient-based control / classifiers in continuous space — historical strength
- **claimed_throughput**: not positioned as throughput SOTA

### Evidence
- **reported_benchmarks**: controllable generation success vs prior controllable LM methods; later cited with weaker LM PPL than modern MDM
- **strengths_claimed**: fine-grained controllability via continuous gradients; global planning in latent space
- **known_failure_modes**: rounding error; embedding geometry issues; generally lags discrete masked diffusion on likelihood at later GPT-2-scale bakeoffs
- **isolation_quality**: strong for controllability demos; not a modern matched rival to LLaDA-class systems

### DOF relevance
- **primary_dofs_touched**: representation; guidance; continuous vs discrete path
- **sota_claim_summary**: Landmark continuous embedding diffusion LM showing gradient control; foundational alternative path to discrete MDM.
- **remaining_ambiguity**: Whether a modern continuous path with better rounding/tokenizers could close the gap to MDM at 1B+ is largely untested.
- **suggested_followup_experiment**: Matched 1B bakeoff: continuous embedding diffusion vs absorbing MDM on identical data/tokenizer; report bits/byte + control suite.
- **practical_takeaway**: Reach for Diffusion-LM-style continuous control when constraints need gradients; for raw LM quality prefer masked discrete diffusion.

### Uncertain fields
- bits_per_byte
- init_from_ar
- typical_num_steps

---

## Diffusion Multimodal LLaDA-V Dimple

### Identity
- **name**: Diffusion Multimodal LLaDA-V Dimple
- **year**: 2025
- **organization**: ML-GSAI and other dMLLM groups
- **model_type**: multimodal diffusion LM
- **paper_or_source**: LLaDA-V: Large Language Diffusion Models with Visual Instruction Tuning; related dMLLMs (Dimple, LaViDa, MMaDA)
- **arxiv_id**: 2505.16933
- **primary_url**: https://arxiv.org/abs/2505.16933

### Representation
- **state_space**: discrete text tokens + continuous/visual embeddings projected into language space
- **corruption_process**: masked diffusion on language tokens; vision via encoder+MLP connector (LLaDA-V)
- **time_formulation**: same MDM reverse process on language side with visual conditioning
- **noise_or_mask_schedule**: inherits LLaDA-style masking; multimodal SFT packing
- **absorbing_token**: yes on language tokens

### Training
- **parameterization**: mask predictor over text tokens conditioned on visual features
- **training_objective**: visual instruction tuning / multimodal alignment on dLLM backbone
- **architecture_backbone**: LLaDA-like diffusion LM + vision encoder + MLP projector
- **init_from_ar**: no for LLaDA-V (from diffusion LM); some dMLLMs use hybrid AR-diffusion strategies
- **scale_params**: ~8B language backbone class for LLaDA-V
- **conditioning_mechanism**: vision tokens/features as conditioning context for diffusion language decode

### Inference
- **sampling_algorithm**: masked diffusion generation of textual responses given images
- **unmasking_or_remasking_policy**: inherits text dLLM samplers; multimodal-specific policies underexplored
- **claimed_throughput**: not the primary claim; competitiveness on multimodal understanding benchmarks

### Evidence
- **reported_benchmarks**: competitive with LLaMA3-V under same instruction data; SOTA among diffusion/hybrid diffusion MLLMs in paper claims
- **strengths_claimed**: shows dLLM backbones transfer to multimodal; good data scalability
- **known_failure_modes**: base text model may trail strong AR text peers; multimodal still early vs mature VLMs
- **isolation_quality**: system multimodal recipe; isolates diffusion backbone vs AR backbone under matched instruction data in parts

### DOF relevance
- **primary_dofs_touched**: conditioning interface; architecture; data/alignment; multimodal extension of DOFs
- **sota_claim_summary**: Establishes dMLLM line: diffusion LMs are viable multimodal backbones.
- **remaining_ambiguity**: Which text-side inference DOFs (unmask/CFG) transfer unchanged to multimodal.
- **suggested_followup_experiment**: Same LLaDA-V checkpoint: Fast-dLLM vs remask vs CFG schedules on multimodal benchmarks + latency.
- **practical_takeaway**: Multimodal is a natural next surface after text dLLM scale-up; reuse text inference lessons carefully.

### Uncertain fields
- block_size
- cfg_schedule
- guidance_methods
- remask_policy
- typical_num_steps

---

## Distillation and Few-Step dLLMs

### Identity
- **name**: Distillation and Few-Step dLLMs
- **year**: 2026
- **organization**: multiple groups
- **model_type**: inference acceleration
- **paper_or_source**: Few-Step Diffusion Language Models via Trajectory Self-Distillation; dual guidance+trajectory distillation; CDLM consistency diffusion LMs; Infinite Mask few-step distillation
- **arxiv_id**: 2602.12262; 2605.10518
- **primary_url**: https://arxiv.org/abs/2602.12262

### Representation
- **state_space**: discrete tokens
- **corruption_process**: inherits teacher MDM corruption; student learns short trajectories
- **time_formulation**: collapse long denoising chains into few-step generation
- **noise_or_mask_schedule**: student trained on teacher rollout / consistency targets rather than only random masks
- **absorbing_token**: yes

### Training
- **parameterization**: often same mean-field token-factorized MDM head; distillation fights factorization error at low steps
- **training_objective**: trajectory self-distillation; guidance distillation; consistency / within-block temporal consistency (CDLM)
- **architecture_backbone**: student MDM, sometimes switched to block-causal masks for KV cache (CDLM)
- **init_from_ar**: usually init from teacher dLLM / AR-adapted dLLM
- **scale_params**: up to multi-B / 8B teachers in reported distill frameworks
- **conditioning_mechanism**: conditional MDLMs; can distill CFG into single forward

### Inference
- **sampling_algorithm**: few-step parallel unmasking / consistency sampling with optional block cache
- **typical_num_steps**: aggressive few-step regimes (single-digit to low tens) vs teacher long chains
- **unmasking_or_remasking_policy**: often confidence-thresholded within blocks after distill
- **guidance_methods**: guidance distilled so inference avoids dual CFG forwards
- **claimed_throughput**: large speedups (order-of-magnitude NFE cuts in conditional distill reports)

### Evidence
- **reported_benchmarks**: conditional generation quality under tight NFE; math/coding maintained in CDLM-style reports
- **strengths_claimed**: attacks mean-field error and train-infer mismatch; practical unlock for dLLM latency
- **known_failure_modes**: distill can overfit teacher pathologies; evaluation often conditional-task specific
- **isolation_quality**: medium — often jointly distills guidance and trajectory

### DOF relevance
- **primary_dofs_touched**: steps/distill; train-infer mismatch; guidance; block size
- **sota_claim_summary**: Few-step/distill is the systems unlock after open dLLM quality became competitive.
- **remaining_ambiguity**: Standard few-step bakeoff protocol across LLaDA/Dream with public Pareto curves still sparse.
- **suggested_followup_experiment**: Same teacher: trajectory-only distill vs guidance+trajectory vs consistency; steps {1,2,4,8,16}; fixed eval suite.
- **practical_takeaway**: If latency matters, plan a distill stage; do not expect raw multi-step MDM to win product bakeoffs.

---

## Dream 7B

### Identity
- **name**: Dream 7B
- **year**: 2025
- **organization**: HKU NLP / collaborators
- **model_type**: scaled diffusion LLM
- **paper_or_source**: Dream 7B: Diffusion Large Language Models
- **arxiv_id**: 2508.15487
- **primary_url**: https://arxiv.org/abs/2508.15487

### Representation
- **state_space**: discrete tokens
- **corruption_process**: masked/discrete diffusion adapted from AR initialization
- **time_formulation**: discrete masked diffusion sampling with context-adaptive noise rescheduling
- **noise_or_mask_schedule**: context-adaptive noise rescheduling (distinctive Dream ingredient)
- **absorbing_token**: yes

### Training
- **parameterization**: diffusion head/objective over sequences initialized from AR weights
- **training_objective**: diffusion adaptation / continual training from AR checkpoint (Qwen-2.5 family narrative)
- **architecture_backbone**: AR Transformer adapted to diffusion (shift-operation characteristics retained per public summaries)
- **init_from_ar**: yes — adapted from Qwen-2.5
- **scale_params**: ~7B
- **conditioning_mechanism**: instruction/prompted generation in diffusion paradigm

### Inference
- **sampling_algorithm**: diffusion unmasking with adaptive scheduling
- **unmasking_or_remasking_policy**: compatible with modern confidence/block samplers; paper emphasizes adaptive noise
- **claimed_throughput**: quality-focused open model; not Mercury throughput headline

### Evidence
- **reported_benchmarks**: strong among open dLLMs on math/general reasoning in secondary summaries; competitive with AR-adapted peers
- **strengths_claimed**: AR-to-diffusion adaptation path; context-adaptive noise; strong reasoning relative to open dLLMs
- **known_failure_modes**: inherits AR tokenizer/data biases; adaptation details less 'pure' than LLaDA from-scratch story
- **isolation_quality**: system claim for adaptation recipe; adaptive noise not always isolated from other training choices

### DOF relevance
- **primary_dofs_touched**: architecture/init from AR; train schedule; scaling path
- **sota_claim_summary**: Leading open AR-adapted diffusion LLM example beside DiffuLLaMA/LLaDA.
- **remaining_ambiguity**: How much of Dream's gains are adaptive noise vs Qwen init vs data — needs ablation.
- **suggested_followup_experiment**: Same Qwen init: fixed schedule vs Dream adaptive noise only; equal tokens; math/code suite.
- **practical_takeaway**: If you already have a strong AR checkpoint, Dream-style adaptation is the pragmatic path to a dLLM.

### Uncertain fields
- bits_per_byte
- block_size
- cfg_schedule
- guidance_methods
- open_source_status
- remask_policy
- training_data_notes
- typical_num_steps

---

## Fast-dLLM and Unmasking Policies

### Identity
- **name**: Fast-dLLM and Unmasking Policies
- **year**: 2025
- **organization**: NVIDIA / academic follow-ons
- **model_type**: inference acceleration
- **paper_or_source**: Fast-dLLM: Training-free Acceleration of Diffusion LLM by Enabling KV Cache and Parallel Decoding; Learning Unmasking Policies for Diffusion Language Models
- **arxiv_id**: 2505.22618; 2512.09106
- **primary_url**: https://arxiv.org/abs/2505.22618

### Representation
- **state_space**: discrete tokens (applies to existing MDM checkpoints like LLaDA)
- **corruption_process**: inherits checkpoint's masked diffusion process
- **time_formulation**: inference-time decoding over diffusion steps / unmask rounds
- **noise_or_mask_schedule**: inference unmask schedule replaces naive fixed-k random unmasking
- **absorbing_token**: yes

### Training
- **parameterization**: uses frozen dLLM mask predictor logits/confidences
- **training_objective**: training-free for Fast-dLLM; learned policies add a policy-learning stage (2512.09106)
- **architecture_backbone**: works with existing bidirectional / block-wise dLLM architectures
- **init_from_ar**: n/a (inference method)
- **scale_params**: demonstrated on ~7–8B class open dLLMs
- **conditioning_mechanism**: compatible with prompted generation

### Inference
- **sampling_algorithm**: confidence-thresholded parallel unmasking; KV cache enabling tricks; optional semi-AR blocks
- **typical_num_steps**: variable — unmask all positions above confidence λ each round; often fewer effective steps than fixed schedules
- **unmasking_or_remasking_policy**: confidence threshold λ (+ at-least-one heuristics); learned unmasking policies as upgrade
- **guidance_methods**: orthogonal; can combine with CFG
- **claimed_throughput**: reports higher token throughput than similarly sized LLaMA under competitive quality in Fast-dLLM narrative

### Evidence
- **reported_benchmarks**: throughput and task accuracy on LLaDA-like models; later papers treat Fast-dLLM as strong baseline
- **strengths_claimed**: training-free speedups; practicalizes open dLLM inference; establishes confidence unmasking as default
- **known_failure_modes**: λ and block length brittle; heuristics often need semi-AR blocks; comparisons sensitive to baseline schedule choice
- **isolation_quality**: high as inference-only intervention on frozen weights; hyperparameters still confounded with block settings

### DOF relevance
- **primary_dofs_touched**: unmasking policy; steps/NFE; KV cache; block size interaction
- **sota_claim_summary**: De facto open-source inference baseline for accelerating masked diffusion LLMs.
- **remaining_ambiguity**: Whether learned policies dominate confidence thresholds under fixed wall-clock across models/tasks.
- **suggested_followup_experiment**: Latin-square of {random-k, threshold λ grid, learned policy} × {BL=8,32,128} at fixed wall-clock on one checkpoint.
- **practical_takeaway**: Before inventing a new sampler, beat Fast-dLLM under matched latency.

---

## Gemini Diffusion

### Identity
- **name**: Gemini Diffusion
- **year**: 2025
- **organization**: Google
- **model_type**: industrial system
- **paper_or_source**: Gemini Diffusion (industrial discrete diffusion LM; cited in 2025 surveys)
- **primary_url**: https://arxiv.org/abs/2506.13759

### Representation
- **state_space**: discrete tokens (reported as discrete diffusion LLM)
- **time_formulation**: parallel diffusion decoding (public narrative)

### Inference
- **sampling_algorithm**: parallel diffusion generation per public discussions/surveys
- **claimed_throughput**: surveys cite large speedups / ~1000 tok/s class alongside Mercury

### Evidence
- **reported_benchmarks**: surveys claim AR-competitive quality on code/math-style evaluations; primary detailed public report limited
- **strengths_claimed**: industrial validation that discrete diffusion LMs scale inside a major lab
- **known_failure_modes**: extreme opacity; cannot scientifically attribute DOFs
- **isolation_quality**: very low

### DOF relevance
- **primary_dofs_touched**: industrial systems existence proof
- **sota_claim_summary**: Important closed landmark cited with Mercury as commercial/industrial dLLM moment.
- **remaining_ambiguity**: Almost all technical DOFs.
- **suggested_followup_experiment**: Cannot ablate; track future technical reports; use open proxies for science.
- **practical_takeaway**: Treat as existence proof only; do not overfit research agenda to rumored details.

### Uncertain fields
- absorbing_token
- architecture_backbone
- arxiv_id
- bits_per_byte
- block_size
- cfg_schedule
- conditioning_mechanism
- corruption_process
- guidance_methods
- init_from_ar
- nfe_vs_quality_notes
- noise_or_mask_schedule
- parameterization
- remask_policy
- scale_params
- train_infer_mask_mismatch
- training_data_notes
- training_objective
- typical_num_steps
- unmask_policy_name
- unmasking_or_remasking_policy

---

## LLaDA

### Identity
- **name**: LLaDA
- **year**: 2025
- **organization**: ML-GSAI / Renmin University & collaborators
- **model_type**: scaled diffusion LLM
- **paper_or_source**: Large Language Diffusion Models
- **arxiv_id**: 2502.09992
- **primary_url**: https://arxiv.org/abs/2502.09992

### Representation
- **state_space**: discrete tokens
- **corruption_process**: masked/absorbing diffusion (random mask ratio t ~ U[0,1] in pretraining)
- **time_formulation**: masked diffusion with principled likelihood lower bound; sampling as iterative unmasking from t=1 to t=0
- **noise_or_mask_schedule**: random masking by continuous-time-like ratio t; flexible remasking at inference
- **absorbing_token**: yes

### Training
- **parameterization**: Transformer mask predictor predicting masked tokens (x0-style)
- **training_objective**: variational lower bound / masked diffusion ELBO under pretrain + SFT paradigm
- **architecture_backbone**: bidirectional Transformer; later MoE variant (LLaDA-MoE)
- **init_from_ar**: no — trained from scratch (contrast Dream/DiffuLLaMA)
- **scale_params**: 8B dense; MoE 7B-A1B follow-up; smaller scaling curve models in paper
- **conditioning_mechanism**: prompt/context with diffusion over response; instruction tuning after SFT

### Inference
- **sampling_algorithm**: parallel mask prediction each step with flexible remasking
- **unmasking_or_remasking_policy**: flexible remasking supported; later Fast-dLLM-style policies applied by community on LLaDA
- **guidance_methods**: instruction following via SFT; later LLaDA 1.5 adds VRPO preference alignment
- **claimed_throughput**: not the headline vs Mercury; focus on quality/scalability vs AR

### Evidence
- **reported_benchmarks**: competitive with self-constructed AR baselines; LLaDA 8B competitive with LLaMA3 8B on ICL; strong reversal poem completion vs GPT-4o claim
- **strengths_claimed**: shows LLM capabilities without AR; scaling trends; mitigates reversal curse; open weights
- **known_failure_modes**: system-level comparison confounders (data/tokenizer); inference cost without acceleration; multimodal follow-ups note pure-text still can trail strong AR peers
- **isolation_quality**: strong existence proof for from-scratch dLLM; many factors jointly scaled

### DOF relevance
- **primary_dofs_touched**: architecture/init path; objective at scale; conditioning/SFT packing; remasking
- **sota_claim_summary**: Flagship open from-scratch 8B masked diffusion LLM challenging 'LLM = AR' assumption.
- **remaining_ambiguity**: Matched-data AR vs LLaDA remains debated; optimal inference policy not settled in original paper.
- **suggested_followup_experiment**: Freeze LLaDA-8B-Instruct; factorial sweep unmask policy × steps × CFG/remask; publish Pareto curves.
- **practical_takeaway**: Best open reference for from-scratch diffusion LLMs; pair with Fast-dLLM-class samplers for practical speed.

### Uncertain fields
- bits_per_byte
- cfg_schedule
- typical_num_steps

---

## MD4 and GenMD4

### Identity
- **name**: MD4 and GenMD4
- **year**: 2024
- **organization**: Google DeepMind
- **model_type**: masked diffusion
- **paper_or_source**: Simplified and Generalized Masked Diffusion for Discrete Data
- **arxiv_id**: 2406.04329
- **primary_url**: https://arxiv.org/abs/2406.04329

### Representation
- **state_space**: discrete tokens (also discrete pixel experiments)
- **corruption_process**: masked/absorbing diffusion; GenMD4 allows state-dependent masking schedules
- **time_formulation**: continuous-time variational objective simplified to weighted integral of cross-entropy
- **noise_or_mask_schedule**: linear masking schedule preferred for text; GenMD4 state-dependent schedules improve likelihood
- **absorbing_token**: yes

### Training
- **parameterization**: clean-data prediction via CE parameterization (avoids fragile score parameterization issues noted vs SEDD)
- **training_objective**: continuous-time ELBO as weighted CE integral; generalized ELBO for state-dependent schedules
- **architecture_backbone**: Transformer LMs at GPT-2 small/medium scales in text experiments
- **init_from_ar**: no
- **scale_params**: GPT-2 small/medium class
- **conditioning_mechanism**: primarily unconditional LM experiments

### Inference
- **sampling_algorithm**: masked diffusion reverse sampling consistent with continuous-time formulation
- **unmasking_or_remasking_policy**: schedule-driven masking/unmasking; not Fast-dLLM-style confidence policies
- **guidance_methods**: not primary focus
- **claimed_throughput**: not throughput-first

### Evidence
- **reported_benchmarks**: OWT-trained models surpass prior diffusion LMs; zero-shot PPL beats SEDD and GPT-2 on 4/5 tasks at medium scale (tables in paper)
- **strengths_claimed**: simple general framework; clearer theory linking perspectives; GenMD4 gains; strong discrete image bpd too
- **known_failure_modes**: still not AR-parity on every zero-shot set (e.g., LAMBADA often second-best); scale below modern dLLM
- **isolation_quality**: high for objective/schedule theory; reimplemented SEDD for fairer comparison

### DOF relevance
- **primary_dofs_touched**: training objective; train schedule; parameterization; time formulation
- **sota_claim_summary**: DeepMind simplification proving masked diffusion ELBO can be literally weighted CE; GenMD4 opens state-dependent schedules.
- **remaining_ambiguity**: Transfer of GenMD4 schedules to 7–8B instruct models largely unproven in public literature.
- **suggested_followup_experiment**: Train matched MDM with linear vs GenMD4 state-dependent schedules at 1B; transfer schedules zero-shot to a new domain.
- **practical_takeaway**: If implementing MDM training, start from MD4-style weighted CE; treat GenMD4 as the schedule upgrade knob.

### Uncertain fields
- typical_num_steps

---

## MDLM

### Identity
- **name**: MDLM
- **year**: 2024
- **organization**: Cornell / academic coauthors (Sahoo et al.)
- **model_type**: masked diffusion
- **paper_or_source**: Simple and Effective Masked Diffusion Language Models
- **arxiv_id**: 2406.07524
- **primary_url**: https://arxiv.org/abs/2406.07524

### Representation
- **state_space**: discrete tokens
- **corruption_process**: absorbing/mask diffusion (focus; argues absorbing outperforms general Q_t on text)
- **time_formulation**: discrete-time friendly; objectives derived without requiring full CTMC machinery
- **noise_or_mask_schedule**: masking schedules compatible with weighted mixture of MLM losses
- **absorbing_token**: yes

### Training
- **parameterization**: mask predictor / x0 token prediction on masked positions
- **training_objective**: Rao-Blackwellized masked diffusion objective as mixture of classical masked LM losses
- **architecture_backbone**: encoder-only / bidirectional Transformer LM
- **init_from_ar**: no (trained as diffusion LM; compared to retrained AR Transformers)
- **scale_params**: ~110M class in main LM1B/OWT comparisons
- **conditioning_mechanism**: primarily unconditional LM; supports semi-AR generation of arbitrary lengths

### Inference
- **sampling_algorithm**: iterative unmasking / efficient samplers including semi-autoregressive generation
- **unmasking_or_remasking_policy**: schedule-based unmasking; precursor to later confidence-threshold literature
- **guidance_methods**: not the paper's primary contribution
- **claimed_throughput**: emphasizes efficient samplers vs prior discrete diffusion; not Mercury-class tok/s claims

### Evidence
- **reported_benchmarks**: LM1B PPL competitive among diffusion (e.g., <=23.00 at 327B tokens vs AR ~20.86); zero-shot PPL often beats SEDD and sometimes AR on OOD sets
- **strengths_claimed**: simpler tighter objectives; absorbing focus; strong diffusion LM likelihoods; OOD robustness hypothesis
- **known_failure_modes**: still trails strong AR on some in-domain PPL; gen-PPL evaluation pitfalls noted in later critique literature
- **isolation_quality**: strong on objective/corruption simplification vs prior discrete diffusion; not LLM-scale

### DOF relevance
- **primary_dofs_touched**: corruption family; training objective; parameterization; sampling
- **sota_claim_summary**: Key 2024 simplification making masked diffusion competitive and practical at GPT-2 scale.
- **remaining_ambiguity**: How far MDLM-style CE training alone goes without AR init at 7B+; inference policy not yet first-class.
- **suggested_followup_experiment**: Hold MDLM objective fixed and sweep only unmasking policies + NFE on a frozen checkpoint.
- **practical_takeaway**: Default training recipe for open masked diffusion LMs before scaling tricks.

### Uncertain fields
- bits_per_byte
- typical_num_steps

---

## Mercury

### Identity
- **name**: Mercury
- **year**: 2025
- **organization**: Inception Labs
- **model_type**: industrial system
- **paper_or_source**: Mercury: Ultra-Fast Language Models Based on Diffusion
- **arxiv_id**: 2506.17298
- **primary_url**: https://arxiv.org/abs/2506.17298

### Representation
- **state_space**: discrete tokens (commercial dLLM)
- **corruption_process**: diffusion language modeling with parallel multi-token prediction (exact forward process details partially proprietary)
- **time_formulation**: iterative parallel denoising rather than token-by-token AR

### Training
- **parameterization**: Transformer-parameterized diffusion LLM
- **training_objective**: trained to predict multiple tokens in parallel; full objective details partially closed
- **architecture_backbone**: Transformer diffusion architecture with proprietary denoiser upgrades (Mercury refreshed blog)
- **scale_params**: Mercury Coder Mini and Small (sizes not always given as open param counts)
- **conditioning_mechanism**: coding assistants, FIM/infill, instruction following via product API

### Inference
- **sampling_algorithm**: parallel diffusion decoding optimized for latency
- **claimed_throughput**: Artificial Analysis: Mini ~1109 tok/s, Small ~737 tok/s on H100; up to ~10× vs speed-optimized frontiers at comparable quality

### Evidence
- **reported_benchmarks**: code benchmarks across languages; Copilot Arena — high quality rank and fastest overall in reported snapshot
- **strengths_claimed**: commercial-scale dLLM; extreme throughput; strong coding/FIM; API+playground
- **known_failure_modes**: closed details block scientific isolation; hard to attribute gains to diffusion vs systems engineering
- **isolation_quality**: low for science — strong existence proof for productized dLLM speed/quality frontier

### DOF relevance
- **primary_dofs_touched**: steps/distill/systems; industrial stack; conditioning for code/FIM
- **sota_claim_summary**: Flagship industrial evidence that diffusion LMs can win the speed-quality frontier for coding.
- **remaining_ambiguity**: Which DOFs (architecture, schedule, distill, hardware kernels) drive the 10× — unknown publicly.
- **suggested_followup_experiment**: Cannot reproduce Mercury; instead build open proxy: Dream/LLaDA + few-step distill + Fast-dLLM and measure tok/s vs HumanEval-class suites on H100.
- **practical_takeaway**: Treat Mercury as proof of product viability, not as an ablatable open baseline.

### Uncertain fields
- absorbing_token
- bits_per_byte
- block_size
- cfg_schedule
- guidance_methods
- init_from_ar
- noise_or_mask_schedule
- remask_policy
- train_infer_mask_mismatch
- typical_num_steps
- unmask_policy_name
- unmasking_or_remasking_policy

---

## RADD and Absorbing Theory

### Identity
- **name**: RADD and Absorbing Theory
- **year**: 2024
- **organization**: academic (Ou et al. and related absorbing MDM theory)
- **model_type**: masked diffusion
- **paper_or_source**: Your Absorbing Discrete Diffusion Secretly Models the Conditional Distributions of Clean Data (RADD lineage / absorbing theory)
- **arxiv_id**: 2406.03736
- **primary_url**: https://arxiv.org/abs/2406.03736

### Representation
- **state_space**: discrete tokens
- **corruption_process**: absorbing discrete diffusion
- **time_formulation**: theoretical equivalence results bridging diffusion time and conditional clean-data distributions
- **noise_or_mask_schedule**: absorbing schedules analyzed theoretically
- **absorbing_token**: yes

### Training
- **parameterization**: shows connections implying mask predictors model clean conditionals
- **training_objective**: justifies simplified training/sampling viewpoints used by later MDM practice
- **architecture_backbone**: architecture-agnostic theory; empirically with Transformer MDMs
- **init_from_ar**: n/a
- **scale_params**: theory + modest empirical scales
- **conditioning_mechanism**: conditional clean-data viewpoint clarifies prompting/masking semantics

### Inference
- **sampling_algorithm**: supports understanding of ancestral unmasking as sampling clean conditionals
- **unmasking_or_remasking_policy**: informs why remasking/unmasking policies act on estimated clean conditionals
- **guidance_methods**: indirect — clarifies what is being guided
- **claimed_throughput**: n/a

### Evidence
- **reported_benchmarks**: theoretical results with supporting experiments; heavily cited by LLaDA/MDM line
- **strengths_claimed**: conceptual simplification: absorbing diffusion ≈ modeling clean conditionals
- **known_failure_modes**: theory assumptions may not cover all practical sampler hacks
- **isolation_quality**: high as theory contribution

### DOF relevance
- **primary_dofs_touched**: corruption family; parameterization; training objective; sampling semantics
- **sota_claim_summary**: Key theoretical reason modern MDM training looks like masked conditional modeling.
- **remaining_ambiguity**: How remasking policies interact with the conditional-clean interpretation under distribution shift.
- **suggested_followup_experiment**: Measure divergence between model clean conditionals on random masks vs confidence-sampler masks.
- **practical_takeaway**: When debugging samplers, think 'am I sampling the right clean conditionals under this mask set?'

### Uncertain fields
- training_data_notes
- typical_num_steps

---

## Remasking and Self-Correction

### Identity
- **name**: Remasking and Self-Correction
- **year**: 2026
- **organization**: multiple groups (WINO, STaRR, re-eval papers)
- **model_type**: inference acceleration
- **paper_or_source**: STaRR responsive remasking; WINO-style confidence remasking; Re-evaluating Confidence Remasking in Masked Diffusion Language Models
- **arxiv_id**: 2601.04205; 2606.12232
- **primary_url**: https://arxiv.org/abs/2601.04205

### Representation
- **state_space**: discrete tokens
- **corruption_process**: inherits MDM absorbing process; remask re-introduces MASK on committed tokens
- **time_formulation**: inference-time correction loops over denoising trajectory
- **noise_or_mask_schedule**: dynamic remask thresholds; STaRR uses temporal variance + spatial deviance
- **absorbing_token**: yes

### Training
- **parameterization**: uses base dLLM confidences/logits; usually training-free
- **training_objective**: typically training-free post-hoc; some edit-refinement variants may fine-tune
- **architecture_backbone**: frozen open dLLMs (LLaDA-class etc.)
- **init_from_ar**: n/a
- **scale_params**: evaluated on open 7–8B dLLMs in representative papers
- **conditioning_mechanism**: standard prompted decode

### Inference
- **sampling_algorithm**: unmask then conditionally remask low-confidence / dynamically selected tokens and resample
- **typical_num_steps**: adds extra NFE versus pure unmasking; speedup claims (e.g., STaRR) depend on avoiding unnecessary remasks
- **unmasking_or_remasking_policy**: remasking is the DOF — when/which tokens revert to MASK
- **guidance_methods**: orthogonal
- **claimed_throughput**: STaRR reports large speedups with maintained quality vs static thresholds; contested vs strong Fast-dLLM baselines

### Evidence
- **reported_benchmarks**: task accuracy + latency; re-eval finds WINO gains often <0.5% at BL=32 vs Fast-dLLM, larger only when baseline decode is weak (e.g., BL=128)
- **strengths_claimed**: fixes early commitment errors; helps under stochastic decoding; adaptive remask reduces waste
- **known_failure_modes**: can be a patch for bad block/unmask settings; latency overhead; benefits setting-dependent
- **isolation_quality**: improving — re-eval paper explicitly stresses matched Fast-dLLM baselines

### DOF relevance
- **primary_dofs_touched**: remasking; stochasticity interaction; steps/NFE budget; block length
- **sota_claim_summary**: Remasking is real but not magic; value is conditional on decode settings and must be NFE-normalized.
- **remaining_ambiguity**: Standard remask budget protocol still missing across papers.
- **suggested_followup_experiment**: Matched Fast-dLLM baseline; remask on/off × greedy/sample × BL; report accuracy vs extra NFE.
- **practical_takeaway**: Try remasking after tuning unmask/block; do not treat it as automatic free quality.

---

## SEDD

### Identity
- **name**: SEDD
- **year**: 2023
- **organization**: academic (Lou et al. / Traverso lineage cited as Score Entropy Discrete Diffusion)
- **model_type**: discrete foundation
- **paper_or_source**: Discrete Diffusion Modeling by Estimating the Ratios of the Data Distribution (SEDD)
- **arxiv_id**: 2310.16834
- **primary_url**: https://arxiv.org/abs/2310.16834

### Representation
- **state_space**: discrete tokens
- **corruption_process**: continuous-time discrete corruption; Absorb and Uniform variants commonly compared
- **time_formulation**: continuous-time CTMC / score-entropy framework
- **noise_or_mask_schedule**: CTMC rate schedules; Absorb often strongest on text among SEDD variants
- **absorbing_token**: yes for Absorb variant

### Training
- **parameterization**: concrete score / ratio parameterization (score entropy)
- **training_objective**: score entropy loss — discrete analogue of score matching
- **architecture_backbone**: Transformer discrete diffusion LMs at GPT-2-comparable scales in follow-on comparisons
- **init_from_ar**: no
- **scale_params**: ~100M class in common bakeoffs
- **conditioning_mechanism**: primarily unconditional LM in core comparisons

### Inference
- **sampling_algorithm**: CTMC-inspired discrete diffusion samplers
- **unmasking_or_remasking_policy**: Absorb path relates to unmasking; pre-confidence-threshold era
- **guidance_methods**: not the modern CFG-MDM focus
- **claimed_throughput**: not throughput-first

### Evidence
- **reported_benchmarks**: strong diffusion LM likelihoods for its time; later MD4/MDLM report better PPL with simpler objectives
- **strengths_claimed**: principled discrete score matching; bridges continuous score theory to tokens
- **known_failure_modes**: training complexity/stability vs simplified CE masked diffusion; mixed-precision issues noted in MD4 reimplementation discussion
- **isolation_quality**: high for introducing score-entropy discrete diffusion; later papers argue parameterization/objective suboptimal vs MD4

### DOF relevance
- **primary_dofs_touched**: time formulation; parameterization; training objective; corruption family
- **sota_claim_summary**: Landmark CTMC/score-entropy discrete diffusion LM; intellectual bridge to modern masked diffusion.
- **remaining_ambiguity**: Whether CTMC solvers still win at equal NFE on modern 7–8B MDMs.
- **suggested_followup_experiment**: Take a modern MDM checkpoint and compare ancestral unmasking vs CTMC-style solvers at equal NFE.
- **practical_takeaway**: Read SEDD for theory; implement MD4/MDLM-style CE unless you need CTMC tooling.

### Uncertain fields
- bits_per_byte
- typical_num_steps

---

## Surveys Discrete Diffusion LLM 2025

### Identity
- **name**: Surveys Discrete Diffusion LLM 2025
- **year**: 2025
- **organization**: Multiple survey groups
- **model_type**: survey
- **paper_or_source**: Discrete Diffusion in Large Language and Multimodal Models: A Survey; A Survey on Diffusion Language Models
- **arxiv_id**: 2506.13759; 2508.10875
- **primary_url**: https://arxiv.org/abs/2506.13759

### Representation
- **state_space**: surveys cover discrete tokens primarily; also discuss continuous/hybrid mentions
- **corruption_process**: taxonomizes absorbing/mask, uniform, and related discrete corruptions
- **time_formulation**: covers discrete-time and continuous-time discrete diffusion formulations
- **noise_or_mask_schedule**: reviews schedule choices across cited models
- **absorbing_token**: yes as dominant modern pattern in surveyed dLLMs

### Training
- **parameterization**: reviews x0 prediction, score/ratio, and related parameterizations
- **training_objective**: reviews ELBO, score entropy, masked CE, SFT/preference for dLLMs
- **architecture_backbone**: catalogues bidirectional Transformers, AR-adapted models, multimodal extensions
- **init_from_ar**: surveys both from-scratch and AR-adaptation paths
- **scale_params**: covers models from early small LMs through ~7–8B open dLLMs and industrial systems
- **conditioning_mechanism**: reviews prompt conditioning, CFG, multimodal connectors

### Inference
- **sampling_algorithm**: taxonomizes unmasking, remasking, block decode, distillation samplers
- **typical_num_steps**: surveys report wide ranges; industrial claims emphasize reduced effective latency rather than a single step count
- **unmasking_or_remasking_policy**: identifies inference policies as a major 2025 theme
- **guidance_methods**: covers CFG and related conditional controls
- **claimed_throughput**: cites Mercury/Gemini Diffusion class claims (~1000 tok/s / large speedups)

### Evidence
- **reported_benchmarks**: aggregates LM, code, math, multimodal benchmarks from cited works
- **strengths_claimed**: provides unified map of modeling, training, generation, multimodal, and trustworthiness threads
- **known_failure_modes**: surveys inherit uncertainty from closed industrial details and rapidly moving inference literature
- **isolation_quality**: high as maps; low as causal evidence — not substitute for controlled ablations

### DOF relevance
- **primary_dofs_touched**: all major DOFs at taxonomy level
- **sota_claim_summary**: Best entry-point taxonomies for 2025 dLLM/dMLLM landscape; situate Mercury/Gemini Diffusion alongside LLaDA/Dream.
- **remaining_ambiguity**: Surveys cannot resolve contested inference claims (remasking, CFG schedules) without new experiments.
- **suggested_followup_experiment**: Use survey taxonomy to build a factorial bakeoff matrix (corruption × unmask × CFG × block_size) on one open 7–8B checkpoint.
- **practical_takeaway**: Start with these surveys for orientation, then dive into MDLM/MD4/LLaDA/BD3/Fast-dLLM for actionable DOFs.

---
