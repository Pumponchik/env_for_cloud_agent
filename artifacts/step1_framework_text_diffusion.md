# Step 1 — Initial Framework: Text Diffusion Models

**Topic:** Diffusion models for text (discrete / continuous / hybrid generative language models)  
**Date:** 2026-08-20  
**Scope:** How they work; research landscape; degrees of freedom that affect quality.

---

## How they work (brief)

Text diffusion replaces left-to-right next-token prediction with a **forward corruption process** and a learned **reverse denoising process**.

1. **Forward process.** Start from clean text \(x_0\) (tokens or continuous embeddings). Gradually corrupt it toward a simple noise prior \(x_T\) (all-MASK, uniform random tokens, or Gaussian noise in embedding space).
2. **Reverse process.** A neural net (usually a bidirectional Transformer) predicts clean tokens / scores / denoised embeddings at each noise level \(t\), optionally conditioned on a prompt.
3. **Sampling.** Start from noise and iteratively denoise for \(T\) (or fewer distilled) steps. Unlike AR LM decoding, many positions can update **in parallel** each step.
4. **Key discrete design choice.** Because tokens are categorical, the continuous Gaussian diffusion recipe must be adapted: absorbing (mask) diffusion, uniform discrete diffusion, continuous-time Markov chains (CTMC), or embed-then-diffuse in \(\mathbb{R}^d\).

Quality is driven by the corruption family, parameterization, objective, architecture, sampling schedule, and guidance — these are the degrees of freedom explored below.

---

## Items List (research objects / families)

### Foundational continuous / embedding diffusion
1. **Diffusion-LM** — continuous diffusion over word embeddings; controllable generation via gradients.
2. **Latent Diffusion for Text / DiffuSeq lineage** — sequence-to-sequence continuous/latent diffusion.
3. **CDCD / continuous embedding diffusion variants** — self-conditioning, embedding geometry.

### Discrete diffusion foundations
4. **D3PM** — discrete denoising diffusion probabilistic models (uniform / absorbing / nearest-neighbor).
5. **Absorbing / Masked diffusion (MDLM, MD4, RADD)** — MASK corruption + simplified ELBO / cross-entropy.
6. **SEDD / CTMC score entropy** — continuous-time discrete diffusion via concrete score / ratio matching.
7. **Campbell / Lou discrete flow / CTMC samplers** — continuous-time discrete sampling theory.

### Modern diffusion LLMs (scale)
8. **LLaDA** — large language diffusion model; AR-competitive scaling claims.
9. **Dream / DiffuLLaMA / Mercury / Gemini Diffusion-class systems** — industrial / large open diffusion LMs.
10. **Block Diffusion / BD3-LM** — blockwise hybrid AR×diffusion for KV-cache and long context.
11. **AR-Diffusion / Any-Order / Semi-AR hybrids** — interpolate AR and full parallel diffusion.

### Sampling, distillation, acceleration
12. **Few-step / distilled text diffusion** — consistency-style or progressive distillation for text.
13. **Remasking / schedule / temperature / CFG for discrete LM** — inference knobs.

### Controllability, editing, reasoning
14. **Infilling / editing / constrained generation with diffusion** — fill masks, hard constraints.
15. **Planner / reasoner uses of diffusion LMs** — parallel revise, self-correction.
16. **Classifier-free / reward / energy guidance on discrete diffusion**.

### Benchmarks, theory, comparisons
17. **AR vs Diffusion LM bakeoffs** — perplexity, GenEval-style, coding, math, latency.
18. **Theory of discrete diffusion ELBO / score matching equivalence**.
19. **Tokenization / vocabulary / multilingual effects on discrete diffusion**.
20. **Surveys and taxonomies of text / discrete diffusion (2024–2026)**.

---

## Field Framework (dimensions to capture per item)

### Identity
- name, year, organization, paper_or_source, arxiv_id, primary_url, model_type

### Representation & Forward Process
- state_space (discrete tokens / continuous embeddings / latent)
- corruption_process (absorbing, uniform, Gaussian, mixture)
- time_formulation (discrete steps vs continuous-time CTMC)
- noise_schedule

### Reverse Model & Training
- parameterization (x0, score/ratio, mean, logits)
- training_objective
- architecture_backbone
- conditioning_mechanism
- scale_params_data

### Inference
- sampling_algorithm
- typical_steps
- guidance_methods
- remasking_or_redecode_policy
- latency_vs_ar

### Capabilities & Evidence
- reported_benchmarks
- strengths_claimed
- known_failure_modes
- open_source_status

### Degrees of Freedom Relevance
- primary_dofs_touched
- sota_claim_summary
- isolation_quality (how cleanly ablated)
- open_questions

### Activity Signal
- citation_or_followup_signal
- active_research_threads_2025_2026

uncertain: []
