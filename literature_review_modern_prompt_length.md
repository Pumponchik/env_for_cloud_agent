# Literature Review: Prompt / Caption Length for Modern Text-to-Image Models

*Generated: 2026-07-28 · Full catalog: 150 papers · Length-focused subset: 73*

## Scope and framing

This review covers the same questions as our earlier study (train length, inference length, re-prompt output length, and *why*), but recenters on **modern LLM/VLM text encoders**—Qwen-VLM-class, Gemma, Llama, Mistral, unified AR multimodal models—rather than CLIP-77 or classic frozen T5 as design targets. CLIP/T5 appear only when a result still generalizes.

**Questions:** (1) What length do recent systems use at train vs infer? (2) Fixed or variable? (3) What length should a re-prompt/PE model emit? (4) What is a fundamental (not only engineering) account of why one regime wins?

---

## Executive answers for a Qwen-VLM-class stack

| Regime | Train length | Infer length | Fixed vs variable | PE / re-prompt output |
|--------|--------------|--------------|-------------------|------------------------|
| Qwen-Image / FLUX.2 / Seedream-style | Dense/long inside ~**512** (API sometimes 800–1300) | Match train via **default-on PE** | Long-biased; some systems randomize | ≈ encoder budget (**~512** `max_new_tokens`) |
| Open recipe (i1) | Long-only, truncate **256** | Rewrite or repeat short prompts | Fixed long + infer expand | Expand toward train length law |
| Structured long (FIBO) | ~**1000 tokens** JSON-schema | Same structured regime | Fixed long structured | Schema-filling VLM |
| Wide-band (HunyuanImage 3.0) | **30–1000 words** sampled | Optional CoT rewrite | **Variable by design** | Content-fixing, not verbosity |
| No PE (transferable lesson) | Randomize/mix within budget | Native short+long | **Variable** | N/A |

**Practical recommendation:** choose a joint policy `(L, μ_train, g)` where `g` is the inference map (identity or PE). Either train variable length covering deployment, or train long and set PE default-on so `Law(g(c_user)) ≈ μ_train`. Do not optimize length alone; optimize **matched length + relevant semantic rate + faithfulness**.

---

## Fundamental problem statement

### How to break the task

Generator `p_θ(x|c)` with text program `c`:

- `c_train ~ μ_train` (captions / VLM recaptions)
- `c_user ~ μ_user` (short underspecified prompts)
- `c_infer = g(c_user)` (identity / rewrite / schema fill)
- encode with budget `L`: `E(c_infer[:L])`

The real decision is not a single integer. It is choosing **`μ_train`, `L`, and `g`** to maximize deployment utility under compute and faithfulness constraints.

### Three mismatches

1. **Capacity:** `len(c)>L` ⇒ truncation loss. Necessary to set `L` high enough; not sufficient (DetailMaster).
2. **Distributional length:** `μ_train` vs `Law(c_infer)` differ in length. Empirically huge (i1: 0.17→0.73 when length is aligned without new image supervision).
3. **Semantic rate:** tokens may be empty style/padding vs attribute-rich content (PromptEnhancer vs verbosity reward hacks; Padding Tone).

### Mathematical sketch

**Rate–distortion.** Length-`ℓ` captions are codes for image content. Useful information scales like `min(I(x; c_≤ℓ), C_model)`. Too short ⇒ under-coding. Past `C_model` ⇒ dilution / unused bits / overload.

**Covariate shift.** Risk under `μ_user` equals in-support risk under `μ_train` plus a shift term. Length is a major coordinate of that shift (prompt-repetition diagnostic keeps content fixed). Remedies: cover test lengths in `μ_train`, or transport via `g`.

**Mixtures.** Variable-length training is a non-degenerate mixture over length bins; fixed length is degenerate. If deployment is multi-modal, Bayes-optimal `μ_train` puts mass on those modes.

**Conceptual program:**

```
max_{μ_train, L, g}  E_{c~μ_dep} U( p_θ(·|E(g(c))) , c )
s.t. compute(E,L,g) ≤ B,
     Faithfulness(g(c), c) ≥ f_min,
     support(Law(g(c))) ⊆≈ support(μ_train) ∩ {len ≤ L}
```

There is no universal closed-form `L*`; there *is* a well-posed objective that tells you what to ablate and what “better length” means.

### How to attack this in a new project

1. Histogram lengths: train captions, users, PE outputs, each benchmark.
2. Set `L` from an upper quantile you refuse to truncate (+ chat-template overhead).
3. Choose `μ_train`: long-heavy+PE **or** wide-band mixture.
4. Choose `g` with faithfulness rewards; avoid pure length rewards.
5. Ablate short / repeat-short / rewritten / native-long.
6. Always report train–eval length delta with scores.

---

## Must-read modern subset (length & variability)

### M1. Qwen-Image-2.0 Technical Report

- **Link:** [https://arxiv.org/abs/2605.10730](https://arxiv.org/abs/2605.10730)
- **Date:** 2026-05-11
- **Tags:** LLM/VLM encoder

Qwen-Image-2.0 is a frontier open multimodal image generation system built around a Qwen-family VLM/LLM text pathway rather than CLIP or classic T5.

The report documents large effective prompt budgets (on the order of hundreds to ~1.3k tokens depending on API/version) with hard truncation past the limit.

Prompt extension is treated as a first-class component (default-on PE), so inference text is intentionally lengthened toward the training caption regime.

For a Qwen-VLM-class design, this is a primary reference for choosing encoder max length, PE max_new_tokens, and default rewrite policy.


### M2. Seedream 4.0: Toward Next-generation Multimodal Image Generation

- **Link:** [https://arxiv.org/abs/2509.20427](https://arxiv.org/abs/2509.20427)
- **Date:** 2025-09-24
- **Tags:** LLM/VLM encoder

Seedream 4.0 (ByteDance) is a next-generation multimodal image system whose prompt enhancement is a VLM with task routing and adaptive thinking budgets.

Re-prompt is not a shallow style expander: it can reason about the request and dynamically spend tokens (“auto-thinking”).

This matters because rewrite length becomes conditional on task difficulty rather than a single fixed expansion factor.

It generalizes the lesson that modern stacks couple a strong multimodal language model to the generator and control how much text that model emits before denoising.


### M3. HunyuanImage 3.0 Technical Report

- **Link:** [https://arxiv.org/abs/2509.23951](https://arxiv.org/abs/2509.23951)
- **Date:** 2025-09-28
- **Tags:** length / modern T2I

HunyuanImage 3.0 trains with Compositional Caption Synthesis, sampling caption fields to produce bilingual captions from about 30 to 1,000 words.

Length and pattern are deliberately variable during training, which is one of the clearest published “wide-band” caption policies.

Inference can use CoT think_recaption / rewrite modes to map short user text into the trained band.

This is strong evidence that for LLM/VLM-era models, varying train length across a wide range is a viable alternative to fixed-long-only training.


### M4. PromptEnhancer: A Simple Approach to Enhance Text-to-Image Models via Chain-of-Thought Prompt Rewriting

- **Link:** [https://arxiv.org/abs/2509.04545](https://arxiv.org/abs/2509.04545)
- **Date:** 2025-09-04
- **Tags:** re-prompt/recaption

PromptEnhancer is a model-agnostic CoT prompt rewriter trained with fine-grained RL against an AlignEvaluator covering many T2I failure modes.

The authors argue rewriting should change content to fix failures, not merely add stylistic verbosity.

That distinction is central to “how long should PE output be”: length is a side-effect of needed content, not the objective.

Use it as the conceptual template for PE rewards when you do not want reward-hacked overlong prompts.


### M5. Generating an Image From 1,000 Words: Enhancing Text-to-Image With Structured Captions

- **Link:** [https://arxiv.org/abs/2511.06876](https://arxiv.org/abs/2511.06876)
- **Date:** 2025-11-10
- **Tags:** long/dense preferred, discusses short prompts, LLM/VLM encoder

FIBO trains an open T2I model on long structured (JSON-schema) captions at roughly thousand-token scale (reported mean around 1160 tokens).

DimFusion fuses intermediate LLM states without growing token count, addressing the compute cost of long text.

Ablations show long structured captions converge faster and improve controllability versus short captions under the same backbone.

This is the extreme “fixed long + structure” pole of the design space for VLM/LLM-conditioned generators.


### M6. i1: A Simple and Fully Open Recipe for Strong Text-to-Image Models

- **Link:** [https://arxiv.org/abs/2606.11289](https://arxiv.org/abs/2606.11289)
- **Date:** 2026-06-01
- **Tags:** long/dense preferred, discusses short prompts, re-prompt/recaption, numeric token budget, LLM/VLM encoder

i1 is a fully open T2I recipe using a modern encoder (T5Gemma) with right truncation to 256 tokens and long synthetic captions.

Its decisive result is distributional: long-caption training scores 0.17 on short GenEval, 0.49 if the short prompt is repeated 12×, and 0.73 with LLM rewrite.

Authors recommend training long and lengthening inference prompts to match training, rather than training short to match users.

Even if you swap T5Gemma for Qwen-VLM, the length-alignment diagnostic remains the right experimental template.


### M7. DetailMaster: Can Your Text-to-Image Model Handle Long Prompts?

- **Link:** [https://arxiv.org/abs/2505.16915](https://arxiv.org/abs/2505.16915)
- **Date:** 2025-05-22
- **Tags:** long/dense preferred

DetailMaster is a long-prompt benchmark with average length ~284.89 tokens and fine-grained attribute/relation metrics.

It shows SOTA models still degrade as prompt length grows, and that dense long training matters more than merely raising token capacity.

CLIP-era limits are a baseline failure mode; T5/LLM models do better but do not saturate the benchmark.

Use it to stress-test any new Qwen-VLM stack at professional long-prompt lengths, not only short GenEval-like sets.


### M8. How to Train your Text-to-Image Model: Evaluating Design Choices for Synthetic Training Captions

- **Link:** [https://arxiv.org/abs/2506.16679](https://arxiv.org/abs/2506.16679)
- **Date:** 2025-06-20
- **Tags:** variable/mixed length

How to Train your Text-to-Image Model studies synthetic caption design and finds fixed long captions trade aesthetics/diversity against alignment.

Randomizing caption length per image removes that trade-off and yields the best overall PickScores in their setup.

Although experiments are on SD/CLIP budgets, the mixture principle transfers: cover the length modes you will serve.

This is the main citation for choosing variable train length when you may not ship a rewriter.


### M9. Playground v3: Improving Text-to-Image Alignment with Deep-Fusion Large Language Models

- **Link:** [https://arxiv.org/abs/2409.10695](https://arxiv.org/abs/2409.10695)
- **Date:** 2024-09-16
- **Tags:** LLM/VLM encoder

Playground v3 replaces CLIP/T5 with deep fusion from a Llama3-8B language model into the DiT, feeding every LLM layer.

Text conditioning is therefore native LLM hidden states, not a 77-token contrastive embedding.

The paper also emphasizes caption quality (CapsBench), tying generation quality to the text channel’s richness.

It is an early clear break from CLIP/T5 dual towers toward LLM-centric conditioning.


### M10. SANA: Efficient High-Resolution Image Synthesis with Linear Diffusion Transformers

- **Link:** [https://arxiv.org/abs/2410.10679](https://arxiv.org/abs/2410.10679)
- **Date:** 2024-10-01
- **Tags:** numeric token budget, LLM/VLM encoder

SANA uses a decoder-only Gemma LM as text encoder with an efficient linear-attention diffusion transformer.

Practical pipelines often set max_sequence_length around 300, and instruction templates consume part of that budget.

This shows modern systems must budget tokens for system/instruction wrappers, not only user text.

Relevant when designing chat-templated Qwen/Gemma encoders where template overhead shrinks usable user length.


### M11. Improving Text-to-Image Generation with Input-Side Inference-Time Scaling

- **Link:** [https://arxiv.org/abs/2510.12041](https://arxiv.org/abs/2510.12041)
- **Date:** 2025-10-14
- **Tags:** re-prompt/recaption, LLM/VLM encoder

Input-side inference-time scaling trains iterative prompt rewriters (e.g., DPO) without requiring SFT on the T2I backbone.

Gains are attributed to closing the train/user text distribution gap, and rewriters can transfer across generators.

Rewrite length should therefore be judged by distribution matching, not by a universal token target.

This supports PE as a portable layer in front of a Qwen-VLM-conditioned generator.


### M12. Seeing is Believing: Aligning Prompt Rewriting with Visual Anchors for Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2606.08492](https://arxiv.org/abs/2606.08492)
- **Date:** 2026-06-07
- **Tags:** re-prompt/recaption, LLM/VLM encoder

FaithRewriter warns that text-only prompt rewriters can hallucinate visually impossible details.

It anchors rewriting with an intermediate image so expansions stay visually faithful.

This constrains PE length: extra tokens are harmful if they invent unsupported content.

Any long-rewrite policy for modern models needs a faithfulness objective, not only a length target.


### M13. What If We Recaption Billions of Web Images with LLaMA-3?

- **Link:** [https://arxiv.org/abs/2406.08478](https://arxiv.org/abs/2406.08478)
- **Date:** 2024-06-12
- **Tags:** re-prompt/recaption, LLM/VLM encoder

Recap-DataComp-1B recaptions ~1B images with LLaVA-LLaMA3 using max_new_tokens=128, raising mean length from ~10 to ~49 tokens.

It is a concrete operating point for offline VLM recaption budgets at web scale.

Downstream T2I/representation models then train on mid-length dense text rather than raw alt-text.

Useful as a lower-bound modern recaption recipe before jumping to 512–1000 token regimes.


### M14. LongT2IBench: A Benchmark for Evaluating Long Text-to-Image Generation with Graph-structured Annotations

- **Link:** [https://arxiv.org/abs/2512.09271](https://arxiv.org/abs/2512.09271)
- **Date:** 2025-12-10
- **Tags:** long/dense preferred, discusses short prompts, LLM/VLM encoder

LongT2IBench provides large-scale long text–image evaluation with graph-structured annotations and balanced word-count bins.

It deliberately spans multiple length bins so evaluators and generators can be compared as length grows.

This is how the field should measure whether a new LLM/VLM stack actually uses long text.

Pair it with DetailMaster when validating length policies.


### M15. Long-Text-to-Image Generation via Compositional Prompt Decomposition

- **Link:** [https://arxiv.org/abs/2604.18258](https://arxiv.org/abs/2604.18258)
- **Date:** 2026-04-20
- **Tags:** long/dense preferred

PRISM / compositional prompt decomposition studies long-text T2I and reports length-extrapolation failures of segment methods trained mostly under ~300 tokens when tested above ~500.

Compositional modeling holds up better at extreme lengths than naive long-context patches.

The fundamental point: train support in length must cover deployment support.

Critical caution against claiming arbitrary long-context ability without training mass at those lengths.


### M16. Wan: Open and Advanced Large-Scale Video Generative Models

- **Link:** [https://arxiv.org/abs/2503.20314](https://arxiv.org/abs/2503.20314)
- **Date:** 2025-01-01
- **Tags:** hand-curated

Wan technical reporting on video generation states the train/infer text alignment principle plainly: dense captions in training, LLM rewriting at inference to match that distribution.

Even though the modality is video, the PE length logic is identical to modern T2I.

Default-on prompt extend is recommended in released tooling.

Cite it when arguing that PE length should track training caption law across modalities.


### M17. A Picture is Worth a Thousand Words: Principled Recaptioning Improves Image Generation

- **Link:** [https://arxiv.org/abs/2310.16656v1](https://arxiv.org/abs/2310.16656v1)
- **Date:** 2023-10-25
- **Tags:** long/dense preferred, re-prompt/recaption

"A Picture is Worth a Thousand Words: Principled Recaptioning Improves Image Generation" (2023) focuses on captioning/recaptioning data that feeds text-to-image training.

Text-to-image diffusion models achieved a remarkable leap in capabilities over the last few years, enabling high-quality and diverse synthesis of images from a textual prompt.

However, even the most advanced models often struggle to precisely follow all of the directions in their prompts.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M18. TULIP: Token-length Upgraded CLIP

- **Link:** [https://arxiv.org/abs/2410.10034v2](https://arxiv.org/abs/2410.10034v2)
- **Date:** 2024-10-13
- **Tags:** long/dense preferred, numeric token budget

"TULIP: Token-length Upgraded CLIP" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

We address the challenge of representing long captions in vision-language models, such as CLIP.

By design these models are limited by fixed, absolute positional encodings, restricting inputs to a maximum of 77 tokens and hindering performance on tasks requiring longer descriptions.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M19. Improving Long-Text Alignment for Text-to-Image Diffusion Models (LongAlign)

- **Link:** [https://arxiv.org/abs/2410.11817](https://arxiv.org/abs/2410.11817)
- **Date:** 2024-10-01
- **Tags:** long/dense preferred, numeric token budget

"Improving Long-Text Alignment for Text-to-Image Diffusion Models (LongAlign)" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Segment-level encoding for long prompts with CLIP and decomposed preference optimization.

Enables SD-class models to handle multi-sentence prompts beyond 77 tokens by splitting, encoding, and concatenating segments.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M20. Think-Then-Generate: Reasoning-Aware Text-to-Image Diffusion with LLM Encoders

- **Link:** [https://arxiv.org/abs/2601.10332v1](https://arxiv.org/abs/2601.10332v1)
- **Date:** 2026-01-15
- **Tags:** re-prompt/recaption, LLM/VLM encoder

"Think-Then-Generate: Reasoning-Aware Text-to-Image Diffusion with LLM Encoders" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Recent progress in text-to-image (T2I) diffusion models (DMs) has enabled high-quality visual synthesis from diverse textual prompts.

Yet, most existing T2I DMs, even those equipped with large language model (LLM)-based text encoders, remain text-pixel mappers -- they employ LLMs merely as text encoders, without leveraging their inherent reasoning capabilities to infer what should be visually depicted given the textual prompt.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M21. PromptEcho: Annotation-Free Reward from Vision-Language Models for Text-to-Image Reinforcement Learning

- **Link:** [https://arxiv.org/abs/2604.12652v2](https://arxiv.org/abs/2604.12652v2)
- **Date:** 2026-04-14
- **Tags:** long/dense preferred, numeric token budget, LLM/VLM encoder

"PromptEcho: Annotation-Free Reward from Vision-Language Models for Text-to-Image Reinforcement Learning" (2026) studies prompt rewriting, optimization, or prompt-side control for image generators.

Reinforcement learning (RL) can improve the prompt following capability of text-to-image (T2I) models, yet obtaining high-quality reward signals remains challenging: CLIP Score is too coarse-grained, while VLM-based reward models (e.g., RewardDance) require costly human-annotated preference data and additional fine-tuning.

We propose PromptEcho, a reward construction method that requires \emph{no} annotation and \emph{no} reward model training.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M22. CRAFT: Continuous Reasoning and Agentic Feedback Tuning for Multimodal Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2512.20362v2](https://arxiv.org/abs/2512.20362v2)
- **Date:** 2025-12-23
- **Tags:** re-prompt/recaption

"CRAFT: Continuous Reasoning and Agentic Feedback Tuning for Multimodal Text-to-Image Generation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Recent work has shown that inference-time reasoning and reflection can improve text-to-image generation without retraining.

However, existing approaches often rely on implicit, holistic critiques or unconstrained prompt rewrites, making their behavior difficult to interpret, control, or stop reliably.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M23. PromptMoG: Enhancing Diversity in Long-Prompt Image Generation via Prompt Embedding Mixture-of-Gaussian Sampling

- **Link:** [https://arxiv.org/abs/2511.20251v1](https://arxiv.org/abs/2511.20251v1)
- **Date:** 2025-11-25
- **Tags:** long/dense preferred, LLM/VLM encoder

"PromptMoG: Enhancing Diversity in Long-Prompt Image Generation via Prompt Embedding Mixture-of-Gaussian Sampling" (2025) studies prompt rewriting, optimization, or prompt-side control for image generators.

Recent advances in text-to-image (T2I) generation have achieved remarkable visual outcomes through large-scale rectified flow models.

However, how these models behave under long prompts remains underexplored.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M24. SPOT: Selective Prompt Projection via Total Variation for Inference-Only Safe Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2602.00616v3](https://arxiv.org/abs/2602.00616v3)
- **Date:** 2026-01-31
- **Tags:** re-prompt/recaption, LLM/VLM encoder

"SPOT: Selective Prompt Projection via Total Variation for Inference-Only Safe Text-to-Image Generation" (2026) studies prompt rewriting, optimization, or prompt-side control for image generators.

Text-to-Image (T2I) diffusion models enable high quality open ended synthesis, but practical use requires suppressing unsafe generations while preserving behavior on benign prompts.

We study this tension relative to the frozen generator, using its prompt conditioned distribution as the preservation reference.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M25. Multi-Resolution Flow Matching: Training-Free Diffusion Acceleration via Staged Sampling

- **Link:** [https://arxiv.org/abs/2607.01642v1](https://arxiv.org/abs/2607.01642v1)
- **Date:** 2026-07-02
- **Tags:** re-prompt/recaption, LLM/VLM encoder

"Multi-Resolution Flow Matching: Training-Free Diffusion Acceleration via Staged Sampling" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Hardware-agnostic strategies for accelerating text-to-image diffusion, such as timestep distillation and feature caching, can reduce inference time without custom kernels or system-level optimization.

Among them, multi-resolution generation strategies have recently received broad attention, attaining more than 5x speedup without any training.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M26. ITIScore: An Image-to-Text-to-Image Rating Framework for the Image Captioning Ability of MLLMs

- **Link:** [https://arxiv.org/abs/2604.03765v2](https://arxiv.org/abs/2604.03765v2)
- **Date:** 2026-04-04
- **Tags:** long/dense preferred, discusses short prompts, LLM/VLM encoder

"ITIScore: An Image-to-Text-to-Image Rating Framework for the Image Captioning Ability of MLLMs" (2026) focuses on captioning/recaptioning data that feeds text-to-image training.

Recent advances in multimodal large language models (MLLMs) have greatly improved image understanding and captioning capabilities.

However, existing image captioning benchmarks typically suffer from limited diversity in caption length, the absence of recent advanced MLLMs, and insufficient human annotations, which potentially introduces bias and limits the ability to comprehensively assess the performance of modern MLLMs.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M27. RePrompt: Reasoning-Augmented Reprompting for Text-to-Image Generation via Reinforcement Learning

- **Link:** [https://arxiv.org/abs/2505.17540v1](https://arxiv.org/abs/2505.17540v1)
- **Date:** 2025-05-23
- **Tags:** re-prompt/recaption, LLM/VLM encoder

"RePrompt: Reasoning-Augmented Reprompting for Text-to-Image Generation via Reinforcement Learning" (2025) studies prompt rewriting, optimization, or prompt-side control for image generators.

Despite recent progress in text-to-image (T2I) generation, existing models often struggle to faithfully capture user intentions from short and under-specified prompts.

While prior work has attempted to enhance prompts using large language models (LLMs), these methods frequently generate stylistic or unrealistic content due to insufficient grounding in visual semantics and real-world composition.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M28. RICO: Improving Accuracy and Completeness in Image Recaptioning via Visual Reconstruction

- **Link:** [https://arxiv.org/abs/2505.22613v1](https://arxiv.org/abs/2505.22613v1)
- **Date:** 2025-05-28
- **Tags:** re-prompt/recaption, LLM/VLM encoder

"RICO: Improving Accuracy and Completeness in Image Recaptioning via Visual Reconstruction" (2025) focuses on captioning/recaptioning data that feeds text-to-image training.

Image recaptioning is widely used to generate training datasets with enhanced quality for various multimodal tasks.

Existing recaptioning methods typically rely on powerful multimodal large language models (MLLMs) to enhance textual descriptions, but often suffer from inaccuracies due to hallucinations and incompleteness caused by missing fine-grained details.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M29. UniGenBench++: A Unified Semantic Evaluation Benchmark for Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2510.18701v2](https://arxiv.org/abs/2510.18701v2)
- **Date:** 2025-10-21
- **Tags:** variable/mixed length, LLM/VLM encoder

"UniGenBench++: A Unified Semantic Evaluation Benchmark for Text-to-Image Generation" (2025) introduces or expands evaluation for text-conditioned image generation, often under long or compositional prompts.

Recent progress in text-to-image (T2I) generation underscores the importance of reliable benchmarks in evaluating how accurately generated images reflect the semantics of their textual prompt.

However, (1) existing benchmarks lack the diversity of prompt scenarios and multilingual support, both essential for real-world applicability; (2) they offer only coarse evaluations across primary dimensions, covering a narrow range of sub-dimensions, and fall short in fine-grained sub-dimension assessment.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M30. Omni-Dish: Photorealistic and Faithful Image Generation and Editing for Arbitrary Chinese Dishes

- **Link:** [https://arxiv.org/abs/2504.09948v3](https://arxiv.org/abs/2504.09948v3)
- **Date:** 2025-04-14
- **Tags:** re-prompt/recaption

"Omni-Dish: Photorealistic and Faithful Image Generation and Editing for Arbitrary Chinese Dishes" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Dish images play a crucial role in the digital era, with the demand for culturally distinctive dish images continuously increasing due to the digitization of the food industry and e-commerce.

In general cases, existing text-to-image generation models excel in producing high-quality images; however, they struggle to capture diverse characteristics and faithful details of specific domains, particularly Chinese dishes.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M31. Qwen-Image-Layered: Towards Inherent Editability via Layer Decomposition

- **Link:** [https://arxiv.org/abs/2512.15603v1](https://arxiv.org/abs/2512.15603v1)
- **Date:** 2025-12-17
- **Tags:** LLM/VLM encoder

"Qwen-Image-Layered: Towards Inherent Editability via Layer Decomposition" (2025) is a modern system/report in the LLM/VLM-conditioned image generation line.

Recent visual generative models often struggle with consistency during image editing due to the entangled nature of raster images, where all visual content is fused into a single canvas.

In contrast, professional design tools employ layered representations, allowing isolated edits while preserving consistency.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M32. Reason2Attack: Jailbreaking Text-to-Image Models via LLM Reasoning

- **Link:** [https://arxiv.org/abs/2503.17987v3](https://arxiv.org/abs/2503.17987v3)
- **Date:** 2025-03-23
- **Tags:** LLM/VLM encoder

"Reason2Attack: Jailbreaking Text-to-Image Models via LLM Reasoning" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Text-to-Image(T2I) models typically deploy safety filters to prevent the generation of sensitive images.

Unfortunately, recent jailbreaking attack methods manually design instructions for the LLM to generate adversarial prompts, which effectively bypass safety filters while producing sensitive images, exposing safety vulnerabilities of T2I models.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M33. Harnessing Caption Detailness for Data-Efficient Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2505.15172v1](https://arxiv.org/abs/2505.15172v1)
- **Date:** 2025-05-21
- **Tags:** long/dense preferred

"Harnessing Caption Detailness for Data-Efficient Text-to-Image Generation" (2025) focuses on captioning/recaptioning data that feeds text-to-image training.

Training text-to-image (T2I) models with detailed captions can significantly improve their generation quality.

Existing methods often rely on simplistic metrics like caption length to represent the detailness of the caption in the T2I training set.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M34. BlindSight: Harnessing Sparsity for Efficient Vision-Language Models

- **Link:** [https://arxiv.org/abs/2507.09071v3](https://arxiv.org/abs/2507.09071v3)
- **Date:** 2025-07-11
- **Tags:** numeric token budget, LLM/VLM encoder

"BlindSight: Harnessing Sparsity for Efficient Vision-Language Models" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Large vision-language models (VLMs) enable joint processing of text and images.

However, incorporating vision data significantly increases the prompt length, resulting in a longer time to first token (TTFT).

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M35. Understanding-in-Generation: Reinforcing Generative Capability of Unified Model via Infusing Understanding into Generation

- **Link:** [https://arxiv.org/abs/2509.18639v3](https://arxiv.org/abs/2509.18639v3)
- **Date:** 2025-09-23
- **Tags:** long/dense preferred

"Understanding-in-Generation: Reinforcing Generative Capability of Unified Model via Infusing Understanding into Generation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Recent works have made notable advancements in enhancing unified models for text-to-image generation through the Chain-of-Thought (CoT).

However, these reasoning methods separate the processes of understanding and generation, which limits their ability to guide the reasoning of unified models in addressing the deficiencies of their generative capabilities.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M36. Synth$^2$: Boosting Visual-Language Models with Synthetic Captions and Image Embeddings

- **Link:** [https://arxiv.org/abs/2403.07750v2](https://arxiv.org/abs/2403.07750v2)
- **Date:** 2024-03-12
- **Tags:** LLM/VLM encoder

"Synth$^2$: Boosting Visual-Language Models with Synthetic Captions and Image Embeddings" (2024) focuses on captioning/recaptioning data that feeds text-to-image training.

The creation of high-quality human-labeled image-caption datasets presents a significant bottleneck in the development of Visual-Language Models (VLMs).

In this work, we investigate an approach that leverages the strengths of Large Language Models (LLMs) and image generation models to create synthetic image-text pairs for efficient and effective VLM training.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M37. TIIF-Bench: How Does Your T2I Model Follow Your Instructions?

- **Link:** [https://arxiv.org/abs/2506.02161v3](https://arxiv.org/abs/2506.02161v3)
- **Date:** 2025-06-02
- **Tags:** LLM/VLM encoder

"TIIF-Bench: How Does Your T2I Model Follow Your Instructions?" (2025) introduces or expands evaluation for text-conditioned image generation, often under long or compositional prompts.

The rapid advancements of Text-to-Image (T2I) models have ushered in a new phase of AI-generated content, marked by their growing ability to interpret and follow user instructions.

However, existing T2I model evaluation benchmarks fall short in limited prompt diversity and complexity, as well as coarse evaluation metrics, making it difficult to evaluate the fine-grained alignment performance between textual instructions and generated images.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M38. Efficient Scaling of Diffusion Transformers for Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2412.12391v1](https://arxiv.org/abs/2412.12391v1)
- **Date:** 2024-12-16
- **Tags:** long/dense preferred

"Efficient Scaling of Diffusion Transformers for Text-to-Image Generation" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

We empirically study the scaling properties of various Diffusion Transformers (DiTs) for text-to-image generation by performing extensive and rigorous ablations, including training scaled DiTs ranging from 0.3B upto 8B parameters on datasets up to 600M images.

We find that U-ViT, a pure self-attention based DiT model provides a simpler design and scales more effectively in comparison with cross-attention based DiT variants, which allows straightforward expansion for extra conditions and other modalities.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M39. JoyAI-Image: Awaking Spatial Intelligence in Unified Multimodal Understanding and Generation

- **Link:** [https://arxiv.org/abs/2605.04128v2](https://arxiv.org/abs/2605.04128v2)
- **Date:** 2026-05-05
- **Tags:** LLM/VLM encoder

"JoyAI-Image: Awaking Spatial Intelligence in Unified Multimodal Understanding and Generation" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

We present JoyAI-Image, a unified multimodal foundation model for visual understanding, text-to-image generation, and instruction-guided image editing.

JoyAI-Image couples a spatially enhanced Multimodal Large Language Model (MLLM) with a Multimodal Diffusion Transformer (MMDiT), allowing perception and generation to interact through a shared multimodal interface.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M40. Mastering Text-to-Image Diffusion: Recaptioning, Planning, and Generating with Multimodal LLMs

- **Link:** [https://arxiv.org/abs/2401.11708v3](https://arxiv.org/abs/2401.11708v3)
- **Date:** 2024-01-22
- **Tags:** re-prompt/recaption, LLM/VLM encoder

"Mastering Text-to-Image Diffusion: Recaptioning, Planning, and Generating with Multimodal LLMs" (2024) focuses on captioning/recaptioning data that feeds text-to-image training.

Diffusion models have exhibit exceptional performance in text-to-image generation and editing.

However, existing methods often face challenges when handling complex text prompts that involve multiple objects with multiple attributes and relationships.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M41. TeleStyle V2: Beyond Content-Preserving Style Transfer with Self-Distillation and Distribution-Matching-Distillation

- **Link:** [https://arxiv.org/abs/2606.20709v1](https://arxiv.org/abs/2606.20709v1)
- **Date:** 2026-06-16
- **Tags:** re-prompt/recaption, LLM/VLM encoder

"TeleStyle V2: Beyond Content-Preserving Style Transfer with Self-Distillation and Distribution-Matching-Distillation" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Given a content reference and a style reference, content-preserving style transfer requires the model to generate stylized outputs with content and style consistency.

We introduced TeleStyle V1 to tackle this problem.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M42. Prompting for products: Investigating design space exploration strategies for text-to-image generative models

- **Link:** [https://arxiv.org/abs/2408.03946v1](https://arxiv.org/abs/2408.03946v1)
- **Date:** 2024-07-22
- **Tags:** length / modern T2I

"Prompting for products: Investigating design space exploration strategies for text-to-image generative models" (2024) studies prompt rewriting, optimization, or prompt-side control for image generators.

Text-to-image models are enabling efficient design space exploration, rapidly generating images from text prompts.

However, many generative AI tools are imperfect for product design applications as they are not built for the goals and requirements of product design.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M43. PiD: Fast and High-Resolution Latent Decoding with Pixel Diffusion

- **Link:** [https://arxiv.org/abs/2605.23902v1](https://arxiv.org/abs/2605.23902v1)
- **Date:** 2026-05-22
- **Tags:** re-prompt/recaption, numeric token budget

"PiD: Fast and High-Resolution Latent Decoding with Pixel Diffusion" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Most practical high-resolution text-to-image systems, including latent diffusion and autoregressive models, perform generation in a compact latent space, and a decoder maps the generated latents back to pixels.

Yet the latent-to-pixel decoder is reconstruction-oriented, optimized to invert the encoder rather than synthesize more details, and becomes increasingly costly at megapixel scale.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M44. Reflect-DiT: Inference-Time Scaling for Text-to-Image Diffusion Transformers via In-Context Reflection

- **Link:** [https://arxiv.org/abs/2503.12271v1](https://arxiv.org/abs/2503.12271v1)
- **Date:** 2025-03-15
- **Tags:** length / modern T2I

"Reflect-DiT: Inference-Time Scaling for Text-to-Image Diffusion Transformers via In-Context Reflection" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

The predominant approach to advancing text-to-image generation has been training-time scaling, where larger models are trained on more data using greater computational resources.

While effective, this approach is computationally expensive, leading to growing interest in inference-time scaling to improve performance.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M45. QwenStyle: Content-Preserving Style Transfer with Qwen-Image-Edit

- **Link:** [https://arxiv.org/abs/2601.06202v1](https://arxiv.org/abs/2601.06202v1)
- **Date:** 2026-01-08
- **Tags:** long/dense preferred, LLM/VLM encoder

"QwenStyle: Content-Preserving Style Transfer with Qwen-Image-Edit" (2026) is a modern system/report in the LLM/VLM-conditioned image generation line.

Content-Preserving Style transfer, given content and style references, remains challenging for Diffusion Transformers (DiTs) due to its internal entangled content and style features.

In this technical report, we propose the first content-preserving style transfer model trained on Qwen-Image-Edit, which activates Qwen-Image-Edit's strong content preservation and style customization capability.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M46. LumiGen: An LVLM-Enhanced Iterative Framework for Fine-Grained Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2508.04732v1](https://arxiv.org/abs/2508.04732v1)
- **Date:** 2025-08-05
- **Tags:** re-prompt/recaption, LLM/VLM encoder

"LumiGen: An LVLM-Enhanced Iterative Framework for Fine-Grained Text-to-Image Generation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Text-to-Image (T2I) generation has made significant advancements with diffusion models, yet challenges persist in handling complex instructions, ensuring fine-grained content control, and maintaining deep semantic consistency.

Existing T2I models often struggle with tasks like accurate text rendering, precise pose generation, or intricate compositional coherence.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M47. LSSGen: Leveraging Latent Space Scaling in Flow and Diffusion for Efficient Text to Image Generation

- **Link:** [https://arxiv.org/abs/2507.16154v1](https://arxiv.org/abs/2507.16154v1)
- **Date:** 2025-07-22
- **Tags:** re-prompt/recaption

"LSSGen: Leveraging Latent Space Scaling in Flow and Diffusion for Efficient Text to Image Generation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Flow matching and diffusion models have shown impressive results in text-to-image generation, producing photorealistic images through an iterative denoising process.

A common strategy to speed up synthesis is to perform early denoising at lower resolutions.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M48. LPNSR: Optimal Noise-Guided Diffusion Image Super-Resolution Via Learnable Noise Prediction

- **Link:** [https://arxiv.org/abs/2603.21045v5](https://arxiv.org/abs/2603.21045v5)
- **Date:** 2026-03-22
- **Tags:** re-prompt/recaption

"LPNSR: Optimal Noise-Guided Diffusion Image Super-Resolution Via Learnable Noise Prediction" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Diffusion-based image super-resolution (SR) aims to reconstruct high-resolution (HR) images from low-resolution (LR) observations.

However, the inherent randomness injected during the reverse diffusion process causes the performance of diffusion-based SR models to vary significantly across different sampling runs, particularly when the sampling trajectory is compressed into a limited number of steps.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M49. Factorized-Dreamer: Training A High-Quality Video Generator with Limited and Low-Quality Data

- **Link:** [https://arxiv.org/abs/2408.10119v1](https://arxiv.org/abs/2408.10119v1)
- **Date:** 2024-08-19
- **Tags:** long/dense preferred, re-prompt/recaption

"Factorized-Dreamer: Training A High-Quality Video Generator with Limited and Low-Quality Data" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Text-to-video (T2V) generation has gained significant attention due to its wide applications to video generation, editing, enhancement and translation, \etc.

However, high-quality (HQ) video synthesis is extremely challenging because of the diverse and complex motions existed in real world.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M50. One Rewrite to Fix Them All? Type-Aware Repair Allocation for Text-to-Image Prompt Optimization

- **Link:** [https://arxiv.org/abs/2607.18724v1](https://arxiv.org/abs/2607.18724v1)
- **Date:** 2026-07-21
- **Tags:** re-prompt/recaption

"One Rewrite to Fix Them All? Type-Aware Repair Allocation for Text-to-Image Prompt Optimization" (2026) studies prompt rewriting, optimization, or prompt-side control for image generators.

Text-to-image (T2I) generators often fail to follow their prompts faithfully, producing wrong counts, swapped attributes, ambiguous relations, and illegible text.

Prompt optimization repairs such failures by rewriting the user prompt, requiring no generator retraining, and has yielded promising results.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M51. On the Feasibility of Poisoning Text-to-Image AI Models via Adversarial Mislabeling

- **Link:** [https://arxiv.org/abs/2506.21874v1](https://arxiv.org/abs/2506.21874v1)
- **Date:** 2025-06-27
- **Tags:** long/dense preferred, LLM/VLM encoder

"On the Feasibility of Poisoning Text-to-Image AI Models via Adversarial Mislabeling" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Today's text-to-image generative models are trained on millions of images sourced from the Internet, each paired with a detailed caption produced by Vision-Language Models (VLMs).

This part of the training pipeline is critical for supplying the models with large volumes of high-quality image-caption pairs during training.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M52. TIT-Score: Evaluating Long-Prompt Based Text-to-Image Alignment via Text-to-Image-to-Text Consistency

- **Link:** [https://arxiv.org/abs/2510.02987v1](https://arxiv.org/abs/2510.02987v1)
- **Date:** 2025-10-03
- **Tags:** discusses short prompts, LLM/VLM encoder

"TIT-Score: Evaluating Long-Prompt Based Text-to-Image Alignment via Text-to-Image-to-Text Consistency" (2025) studies prompt rewriting, optimization, or prompt-side control for image generators.

With the rapid advancement of large multimodal models (LMMs), recent text-to-image (T2I) models can generate high-quality images and demonstrate great alignment to short prompts.

However, they still struggle to effectively understand and follow long and detailed prompts, displaying inconsistent generation.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M53. Multimodal Prompt Decoupling Attack on the Safety Filters in Text-to-Image Models

- **Link:** [https://arxiv.org/abs/2509.21360v1](https://arxiv.org/abs/2509.21360v1)
- **Date:** 2025-09-21
- **Tags:** re-prompt/recaption, LLM/VLM encoder

"Multimodal Prompt Decoupling Attack on the Safety Filters in Text-to-Image Models" (2025) studies prompt rewriting, optimization, or prompt-side control for image generators.

Text-to-image (T2I) models have been widely applied in generating high-fidelity images across various domains.

However, these models may also be abused to produce Not-Safe-for-Work (NSFW) content via jailbreak attacks.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M54. LLMs can see and hear without any training

- **Link:** [https://arxiv.org/abs/2501.18096v1](https://arxiv.org/abs/2501.18096v1)
- **Date:** 2025-01-30
- **Tags:** re-prompt/recaption, LLM/VLM encoder

"LLMs can see and hear without any training" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

We present MILS: Multimodal Iterative LLM Solver, a surprisingly simple, training-free approach, to imbue multimodal capabilities into your favorite LLM.

Leveraging their innate ability to perform multi-step reasoning, MILS prompts the LLM to generate candidate outputs, each of which are scored and fed back iteratively, eventually generating a solution to the task.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M55. Low-hallucination Synthetic Captions for Large-Scale Vision-Language Model Pre-training

- **Link:** [https://arxiv.org/abs/2504.13123v2](https://arxiv.org/abs/2504.13123v2)
- **Date:** 2025-04-17
- **Tags:** numeric token budget

"Low-hallucination Synthetic Captions for Large-Scale Vision-Language Model Pre-training" (2025) focuses on captioning/recaptioning data that feeds text-to-image training.

In recent years, the field of vision-language model pre-training has experienced rapid advancements, driven primarily by the continuous enhancement of textual capabilities in large language models.

However, existing training paradigms for multimodal large language models heavily rely on high-quality image-text pairs.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M56. ELLA: Equip Diffusion Models with LLM for Enhanced Semantic Alignment

- **Link:** [https://arxiv.org/abs/2403.05135v1](https://arxiv.org/abs/2403.05135v1)
- **Date:** 2024-03-08
- **Tags:** LLM/VLM encoder

"ELLA: Equip Diffusion Models with LLM for Enhanced Semantic Alignment" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Diffusion models have demonstrated remarkable performance in the domain of text-to-image generation.

However, most widely used models still employ CLIP as their text encoder, which constrains their ability to comprehend dense prompts, encompassing multiple objects, detailed attributes, complex relationships, long-text alignment, etc.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M57. Automated Prompt Generation for Creative and Counterfactual Text-to-image Synthesis

- **Link:** [https://arxiv.org/abs/2509.21375v1](https://arxiv.org/abs/2509.21375v1)
- **Date:** 2025-09-23
- **Tags:** re-prompt/recaption

"Automated Prompt Generation for Creative and Counterfactual Text-to-image Synthesis" (2025) studies prompt rewriting, optimization, or prompt-side control for image generators.

Text-to-image generation has advanced rapidly with large-scale multimodal training, yet fine-grained controllability remains a critical challenge.

Counterfactual controllability, defined as the capacity to deliberately generate images that contradict common-sense patterns, remains a major challenge but plays a crucial role in enabling creativity and exploratory applications.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M58. EditID: Training-Free Editable ID Customization for Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2503.12526v1](https://arxiv.org/abs/2503.12526v1)
- **Date:** 2025-03-16
- **Tags:** long/dense preferred

"EditID: Training-Free Editable ID Customization for Text-to-Image Generation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

We propose EditID, a training-free approach based on the DiT architecture, which achieves highly editable customized IDs for text to image generation.

Existing text-to-image models for customized IDs typically focus more on ID consistency while neglecting editability.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M59. Progressive Prompt Detailing for Improved Alignment in Text-to-Image Generative Models

- **Link:** [https://arxiv.org/abs/2503.17794v4](https://arxiv.org/abs/2503.17794v4)
- **Date:** 2025-03-22
- **Tags:** long/dense preferred

"Progressive Prompt Detailing for Improved Alignment in Text-to-Image Generative Models" (2025) studies prompt rewriting, optimization, or prompt-side control for image generators.

Text-to-image generative models often struggle with long prompts detailing complex scenes, diverse objects with distinct visual characteristics and spatial relationships.

In this work, we propose SCoPE (Scheduled interpolation of Coarse-to-fine Prompt Embeddings), a training-free method to improve text-to-image alignment by progressively refining the input prompt in a coarse-to-fine-grained manner.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M60. EditIDv2: Editable ID Customization with Data-Lubricated ID Feature Integration for Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2509.05659v1](https://arxiv.org/abs/2509.05659v1)
- **Date:** 2025-09-06
- **Tags:** long/dense preferred

"EditIDv2: Editable ID Customization with Data-Lubricated ID Feature Integration for Text-to-Image Generation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

We propose EditIDv2, a tuning-free solution specifically designed for high-complexity narrative scenes and long text inputs.

Existing character editing methods perform well under simple prompts, but often suffer from degraded editing capabilities, semantic understanding biases, and identity consistency breakdowns when faced with long text narratives containing multiple semantic layers, temporal logic, and complex contextual relationships.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M61. CAHS-Attack: CLIP-Aware Heuristic Search Attack Method for Stable Diffusion

- **Link:** [https://arxiv.org/abs/2511.21180v1](https://arxiv.org/abs/2511.21180v1)
- **Date:** 2025-11-26
- **Tags:** long/dense preferred

"CAHS-Attack: CLIP-Aware Heuristic Search Attack Method for Stable Diffusion" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Diffusion models exhibit notable fragility when faced with adversarial prompts, and strengthening attack capabilities is crucial for uncovering such vulnerabilities and building more robust generative systems.

Existing works often rely on white-box access to model gradients or hand-crafted prompt engineering, which is infeasible in real-world deployments due to restricted access or poor attack effect.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M62. A Little More Like This: Text-to-Image Retrieval with Vision-Language Models Using Relevance Feedback

- **Link:** [https://arxiv.org/abs/2511.17255v1](https://arxiv.org/abs/2511.17255v1)
- **Date:** 2025-11-21
- **Tags:** LLM/VLM encoder

"A Little More Like This: Text-to-Image Retrieval with Vision-Language Models Using Relevance Feedback" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Large vision-language models (VLMs) enable intuitive visual search using natural language queries.

However, improving their performance often requires fine-tuning and scaling to larger model variants.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M63. Self-Rewarding Large Vision-Language Models for Optimizing Prompts in Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2505.16763v2](https://arxiv.org/abs/2505.16763v2)
- **Date:** 2025-05-22
- **Tags:** re-prompt/recaption, LLM/VLM encoder

"Self-Rewarding Large Vision-Language Models for Optimizing Prompts in Text-to-Image Generation" (2025) studies prompt rewriting, optimization, or prompt-side control for image generators.

Text-to-image models are powerful for producing high-quality images based on given text prompts, but crafting these prompts often requires specialized vocabulary.

To address this, existing methods train rewriting models with supervision from large amounts of manually annotated data and trained aesthetic assessment models.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M64. Dynamic Optimization and Safety Indicator Injection for Jailbreaking Text-to-Image Models with Multimodal Safety Filters

- **Link:** [https://arxiv.org/abs/2505.18979v2](https://arxiv.org/abs/2505.18979v2)
- **Date:** 2025-05-25
- **Tags:** re-prompt/recaption, LLM/VLM encoder

"Dynamic Optimization and Safety Indicator Injection for Jailbreaking Text-to-Image Models with Multimodal Safety Filters" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Text-to-image (T2I) models can generate not-safe-for-work (NSFW) content, motivating multi-stage safety pipelines with both text and image filters.

Newer LLM-based filters detect latent intent beyond keywords, making token-level perturbation attacks unreliable.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M65. Visual Autoregressive Modelling for Monocular Depth Estimation

- **Link:** [https://arxiv.org/abs/2512.22653v1](https://arxiv.org/abs/2512.22653v1)
- **Date:** 2025-12-27
- **Tags:** re-prompt/recaption

"Visual Autoregressive Modelling for Monocular Depth Estimation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

We propose a monocular depth estimation method based on visual autoregressive (VAR) priors, offering an alternative to diffusion-based approaches.

Our method adapts a large-scale text-to-image VAR model and introduces a scale-wise conditional upsampling mechanism with classifier-free guidance.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M66. StrandDesigner: Towards Practical Strand Generation with Sketch Guidance

- **Link:** [https://arxiv.org/abs/2508.01650v1](https://arxiv.org/abs/2508.01650v1)
- **Date:** 2025-08-03
- **Tags:** re-prompt/recaption

"StrandDesigner: Towards Practical Strand Generation with Sketch Guidance" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Realistic hair strand generation is crucial for applications like computer graphics and virtual reality.

While diffusion models can generate hairstyles from text or images, these inputs lack precision and user-friendliness.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M67. ERNIE-Image Technical Report

- **Link:** [https://arxiv.org/abs/2605.25347v1](https://arxiv.org/abs/2605.25347v1)
- **Date:** 2026-05-25
- **Tags:** re-prompt/recaption

"ERNIE-Image Technical Report" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

We introduce ERNIE-Image, an open-source text-to-image generation model built upon an 8B single-stream DiT architecture.

ERNIE-Image aims to bridge the gap between current open-source models and leading closed-source systems through more effective mining of large-scale pre-training data and improved supervision quality throughout training.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M68. PG-MAP: Joint MAP Optimization for Inference-Time Alignment of Diffusion and Flow-Matching Models

- **Link:** [https://arxiv.org/abs/2606.22958v1](https://arxiv.org/abs/2606.22958v1)
- **Date:** 2026-06-22
- **Tags:** length / modern T2I

"PG-MAP: Joint MAP Optimization for Inference-Time Alignment of Diffusion and Flow-Matching Models" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Inference-time alignment of pretrained text-to-image models is typically performed along a single control axis, such as classifier-free guidance, attention editing, or reward-based latent perturbations.

This limitation prevents modeling joint dependencies between conditioning and latent variables and hinders transfer across generative transports.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M69. An Empirical Study and Analysis of Text-to-Image Generation Using Large Language Model-Powered Textual Representation

- **Link:** [https://arxiv.org/abs/2405.12914v2](https://arxiv.org/abs/2405.12914v2)
- **Date:** 2024-05-21
- **Tags:** numeric token budget, LLM/VLM encoder

"An Empirical Study and Analysis of Text-to-Image Generation Using Large Language Model-Powered Textual Representation" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

One critical prerequisite for faithful text-to-image generation is the accurate understanding of text inputs.

Existing methods leverage the text encoder of the CLIP model to represent input prompts.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M70. Red-Teaming Text-to-Image Models via In-Context Experience Replay and Semantic-Preserving Prompt Rewriting

- **Link:** [https://arxiv.org/abs/2411.16769v3](https://arxiv.org/abs/2411.16769v3)
- **Date:** 2024-11-25
- **Tags:** re-prompt/recaption, LLM/VLM encoder

"Red-Teaming Text-to-Image Models via In-Context Experience Replay and Semantic-Preserving Prompt Rewriting" (2024) studies prompt rewriting, optimization, or prompt-side control for image generators.

Understanding the capabilities of text-to-image (T2I) models in harmful content generation is essential to safety and compliance.

However, human red-teaming is costly and inconsistent, driving the need for automatic tools that simulate realistic misuse attempts.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M71. Edify Image: High-Quality Image Generation with Pixel Space Laplacian Diffusion Models

- **Link:** [https://arxiv.org/abs/2411.07126v1](https://arxiv.org/abs/2411.07126v1)
- **Date:** 2024-11-11
- **Tags:** re-prompt/recaption

"Edify Image: High-Quality Image Generation with Pixel Space Laplacian Diffusion Models" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

We introduce Edify Image, a family of diffusion models capable of generating photorealistic image content with pixel-perfect accuracy.

Edify Image utilizes cascaded pixel-space diffusion models trained using a novel Laplacian diffusion process, in which image signals at different frequency bands are attenuated at varying rates.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M72. Spectral Image Tokenizer

- **Link:** [https://arxiv.org/abs/2412.09607v2](https://arxiv.org/abs/2412.09607v2)
- **Date:** 2024-12-12
- **Tags:** re-prompt/recaption

"Spectral Image Tokenizer" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Image tokenizers map images to sequences of discrete tokens, and are a crucial component of autoregressive transformer-based image generation.

The tokens are typically associated with spatial locations in the input image, arranged in raster scan order, which is not ideal for autoregressive modeling.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### M73. RubiCap: Rubric-Guided Reinforcement Learning for Dense Image Captioning

- **Link:** [https://arxiv.org/abs/2603.09160v1](https://arxiv.org/abs/2603.09160v1)
- **Date:** 2026-03-10
- **Tags:** LLM/VLM encoder

"RubiCap: Rubric-Guided Reinforcement Learning for Dense Image Captioning" (2026) focuses on captioning/recaptioning data that feeds text-to-image training.

Dense image captioning is critical for cross-modal alignment in vision-language pretraining and text-to-image generation, but scaling expert-quality annotations is prohibitively expensive.

While synthetic captioning via strong vision-language models (VLMs) is a practical alternative, supervised distillation often yields limited output diversity and weak generalization.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


---

## Full catalog (150 papers)

Title, link, and four sentences each. Sorted with hand-prioritized modern systems first, then relevance-ranked corpus papers from arXiv (2023–2026 emphasis).

### 1. Wan: Open and Advanced Large-Scale Video Generative Models

- **Link:** [https://arxiv.org/abs/2503.20314](https://arxiv.org/abs/2503.20314)
- **Published:** 2025-01-01

Wan technical reporting on video generation states the train/infer text alignment principle plainly: dense captions in training, LLM rewriting at inference to match that distribution.

Even though the modality is video, the PE length logic is identical to modern T2I.

Default-on prompt extend is recommended in released tooling.

Cite it when arguing that PE length should track training caption law across modalities.


### 2. Improving Text-to-Image Generation with Input-Side Inference-Time Scaling

- **Link:** [https://arxiv.org/abs/2510.12041](https://arxiv.org/abs/2510.12041)
- **Published:** 2025-10-14

Input-side inference-time scaling trains iterative prompt rewriters (e.g., DPO) without requiring SFT on the T2I backbone.

Gains are attributed to closing the train/user text distribution gap, and rewriters can transfer across generators.

Rewrite length should therefore be judged by distribution matching, not by a universal token target.

This supports PE as a portable layer in front of a Qwen-VLM-conditioned generator.


### 3. PromptEnhancer: A Simple Approach to Enhance Text-to-Image Models via Chain-of-Thought Prompt Rewriting

- **Link:** [https://arxiv.org/abs/2509.04545](https://arxiv.org/abs/2509.04545)
- **Published:** 2025-09-04

PromptEnhancer is a model-agnostic CoT prompt rewriter trained with fine-grained RL against an AlignEvaluator covering many T2I failure modes.

The authors argue rewriting should change content to fix failures, not merely add stylistic verbosity.

That distinction is central to “how long should PE output be”: length is a side-effect of needed content, not the objective.

Use it as the conceptual template for PE rewards when you do not want reward-hacked overlong prompts.


### 4. i1: A Simple and Fully Open Recipe for Strong Text-to-Image Models

- **Link:** [https://arxiv.org/abs/2606.11289](https://arxiv.org/abs/2606.11289)
- **Published:** 2026-06-01

i1 is a fully open T2I recipe using a modern encoder (T5Gemma) with right truncation to 256 tokens and long synthetic captions.

Its decisive result is distributional: long-caption training scores 0.17 on short GenEval, 0.49 if the short prompt is repeated 12×, and 0.73 with LLM rewrite.

Authors recommend training long and lengthening inference prompts to match training, rather than training short to match users.

Even if you swap T5Gemma for Qwen-VLM, the length-alignment diagnostic remains the right experimental template.


### 5. LongT2IBench: A Benchmark for Evaluating Long Text-to-Image Generation with Graph-structured Annotations

- **Link:** [https://arxiv.org/abs/2512.09271](https://arxiv.org/abs/2512.09271)
- **Published:** 2025-12-10

LongT2IBench provides large-scale long text–image evaluation with graph-structured annotations and balanced word-count bins.

It deliberately spans multiple length bins so evaluators and generators can be compared as length grows.

This is how the field should measure whether a new LLM/VLM stack actually uses long text.

Pair it with DetailMaster when validating length policies.


### 6. Generating an Image From 1,000 Words: Enhancing Text-to-Image With Structured Captions

- **Link:** [https://arxiv.org/abs/2511.06876](https://arxiv.org/abs/2511.06876)
- **Published:** 2025-11-10

FIBO trains an open T2I model on long structured (JSON-schema) captions at roughly thousand-token scale (reported mean around 1160 tokens).

DimFusion fuses intermediate LLM states without growing token count, addressing the compute cost of long text.

Ablations show long structured captions converge faster and improve controllability versus short captions under the same backbone.

This is the extreme “fixed long + structure” pole of the design space for VLM/LLM-conditioned generators.


### 7. DetailMaster: Can Your Text-to-Image Model Handle Long Prompts?

- **Link:** [https://arxiv.org/abs/2505.16915](https://arxiv.org/abs/2505.16915)
- **Published:** 2025-05-22

DetailMaster is a long-prompt benchmark with average length ~284.89 tokens and fine-grained attribute/relation metrics.

It shows SOTA models still degrade as prompt length grows, and that dense long training matters more than merely raising token capacity.

CLIP-era limits are a baseline failure mode; T5/LLM models do better but do not saturate the benchmark.

Use it to stress-test any new Qwen-VLM stack at professional long-prompt lengths, not only short GenEval-like sets.


### 8. What If We Recaption Billions of Web Images with LLaMA-3?

- **Link:** [https://arxiv.org/abs/2406.08478](https://arxiv.org/abs/2406.08478)
- **Published:** 2024-06-12

Recap-DataComp-1B recaptions ~1B images with LLaVA-LLaMA3 using max_new_tokens=128, raising mean length from ~10 to ~49 tokens.

It is a concrete operating point for offline VLM recaption budgets at web scale.

Downstream T2I/representation models then train on mid-length dense text rather than raw alt-text.

Useful as a lower-bound modern recaption recipe before jumping to 512–1000 token regimes.


### 9. Qwen-Image-2.0 Technical Report

- **Link:** [https://arxiv.org/abs/2605.10730](https://arxiv.org/abs/2605.10730)
- **Published:** 2026-05-11

Qwen-Image-2.0 is a frontier open multimodal image generation system built around a Qwen-family VLM/LLM text pathway rather than CLIP or classic T5.

The report documents large effective prompt budgets (on the order of hundreds to ~1.3k tokens depending on API/version) with hard truncation past the limit.

Prompt extension is treated as a first-class component (default-on PE), so inference text is intentionally lengthened toward the training caption regime.

For a Qwen-VLM-class design, this is a primary reference for choosing encoder max length, PE max_new_tokens, and default rewrite policy.


### 10. Seeing is Believing: Aligning Prompt Rewriting with Visual Anchors for Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2606.08492](https://arxiv.org/abs/2606.08492)
- **Published:** 2026-06-07

FaithRewriter warns that text-only prompt rewriters can hallucinate visually impossible details.

It anchors rewriting with an intermediate image so expansions stay visually faithful.

This constrains PE length: extra tokens are harmful if they invent unsupported content.

Any long-rewrite policy for modern models needs a faithfulness objective, not only a length target.


### 11. Seedream 4.0: Toward Next-generation Multimodal Image Generation

- **Link:** [https://arxiv.org/abs/2509.20427](https://arxiv.org/abs/2509.20427)
- **Published:** 2025-09-24

Seedream 4.0 (ByteDance) is a next-generation multimodal image system whose prompt enhancement is a VLM with task routing and adaptive thinking budgets.

Re-prompt is not a shallow style expander: it can reason about the request and dynamically spend tokens (“auto-thinking”).

This matters because rewrite length becomes conditional on task difficulty rather than a single fixed expansion factor.

It generalizes the lesson that modern stacks couple a strong multimodal language model to the generator and control how much text that model emits before denoising.


### 12. Long-Text-to-Image Generation via Compositional Prompt Decomposition

- **Link:** [https://arxiv.org/abs/2604.18258](https://arxiv.org/abs/2604.18258)
- **Published:** 2026-04-20

PRISM / compositional prompt decomposition studies long-text T2I and reports length-extrapolation failures of segment methods trained mostly under ~300 tokens when tested above ~500.

Compositional modeling holds up better at extreme lengths than naive long-context patches.

The fundamental point: train support in length must cover deployment support.

Critical caution against claiming arbitrary long-context ability without training mass at those lengths.


### 13. Playground v3: Improving Text-to-Image Alignment with Deep-Fusion Large Language Models

- **Link:** [https://arxiv.org/abs/2409.10695](https://arxiv.org/abs/2409.10695)
- **Published:** 2024-09-16

Playground v3 replaces CLIP/T5 with deep fusion from a Llama3-8B language model into the DiT, feeding every LLM layer.

Text conditioning is therefore native LLM hidden states, not a 77-token contrastive embedding.

The paper also emphasizes caption quality (CapsBench), tying generation quality to the text channel’s richness.

It is an early clear break from CLIP/T5 dual towers toward LLM-centric conditioning.


### 14. How to Train your Text-to-Image Model: Evaluating Design Choices for Synthetic Training Captions

- **Link:** [https://arxiv.org/abs/2506.16679](https://arxiv.org/abs/2506.16679)
- **Published:** 2025-06-20

How to Train your Text-to-Image Model studies synthetic caption design and finds fixed long captions trade aesthetics/diversity against alignment.

Randomizing caption length per image removes that trade-off and yields the best overall PickScores in their setup.

Although experiments are on SD/CLIP budgets, the mixture principle transfers: cover the length modes you will serve.

This is the main citation for choosing variable train length when you may not ship a rewriter.


### 15. HunyuanImage 3.0 Technical Report

- **Link:** [https://arxiv.org/abs/2509.23951](https://arxiv.org/abs/2509.23951)
- **Published:** 2025-09-28

HunyuanImage 3.0 trains with Compositional Caption Synthesis, sampling caption fields to produce bilingual captions from about 30 to 1,000 words.

Length and pattern are deliberately variable during training, which is one of the clearest published “wide-band” caption policies.

Inference can use CoT think_recaption / rewrite modes to map short user text into the trained band.

This is strong evidence that for LLM/VLM-era models, varying train length across a wide range is a viable alternative to fixed-long-only training.


### 16. SANA: Efficient High-Resolution Image Synthesis with Linear Diffusion Transformers

- **Link:** [https://arxiv.org/abs/2410.10679](https://arxiv.org/abs/2410.10679)
- **Published:** 2024-10-01

SANA uses a decoder-only Gemma LM as text encoder with an efficient linear-attention diffusion transformer.

Practical pipelines often set max_sequence_length around 300, and instruction templates consume part of that budget.

This shows modern systems must budget tokens for system/instruction wrappers, not only user text.

Relevant when designing chat-templated Qwen/Gemma encoders where template overhead shrinks usable user length.


### 17. A Picture is Worth a Thousand Words: Principled Recaptioning Improves Image Generation

- **Link:** [https://arxiv.org/abs/2310.16656v1](https://arxiv.org/abs/2310.16656v1)
- **Published:** 2023-10-25

"A Picture is Worth a Thousand Words: Principled Recaptioning Improves Image Generation" (2023) focuses on captioning/recaptioning data that feeds text-to-image training.

Text-to-image diffusion models achieved a remarkable leap in capabilities over the last few years, enabling high-quality and diverse synthesis of images from a textual prompt.

However, even the most advanced models often struggle to precisely follow all of the directions in their prompts.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 18. TULIP: Token-length Upgraded CLIP

- **Link:** [https://arxiv.org/abs/2410.10034v2](https://arxiv.org/abs/2410.10034v2)
- **Published:** 2024-10-13

"TULIP: Token-length Upgraded CLIP" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

We address the challenge of representing long captions in vision-language models, such as CLIP.

By design these models are limited by fixed, absolute positional encodings, restricting inputs to a maximum of 77 tokens and hindering performance on tasks requiring longer descriptions.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 19. PixArt-Σ: Weak-to-Strong Training of Diffusion Transformer for 4K Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2403.04692v2](https://arxiv.org/abs/2403.04692v2)
- **Published:** 2024-03-07

"PixArt-Σ: Weak-to-Strong Training of Diffusion Transformer for 4K Text-to-Image Generation" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

In this paper, we introduce PixArt-Σ, a Diffusion Transformer model~(DiT) capable of directly generating images at 4K resolution.

PixArt-Σrepresents a significant advancement over its predecessor, PixArt-α, offering images of markedly higher fidelity and improved alignment with text prompts.

Keep it as background on modern generation/evaluation; use only if its data or metrics inform caption-length decisions.


### 20. Improving Long-Text Alignment for Text-to-Image Diffusion Models (LongAlign)

- **Link:** [https://arxiv.org/abs/2410.11817](https://arxiv.org/abs/2410.11817)
- **Published:** 2024-10-01

"Improving Long-Text Alignment for Text-to-Image Diffusion Models (LongAlign)" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Segment-level encoding for long prompts with CLIP and decomposed preference optimization.

Enables SD-class models to handle multi-sentence prompts beyond 77 tokens by splitting, encoding, and concatenating segments.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 21. TIPO: Text to Image with Text Presampling for Prompt Optimization

- **Link:** [https://arxiv.org/abs/2411.08127v6](https://arxiv.org/abs/2411.08127v6)
- **Published:** 2024-11-12

"TIPO: Text to Image with Text Presampling for Prompt Optimization" (2024) studies prompt rewriting, optimization, or prompt-side control for image generators.

TIPO (Text-to-Image Prompt Optimization) introduces an efficient approach for automatic prompt refinement in text-to-image (T2I) generation.

Starting from simple user prompts, TIPO leverages a lightweight pre-trained model to expand these prompts into richer and more detailed versions.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 22. Think-Then-Generate: Reasoning-Aware Text-to-Image Diffusion with LLM Encoders

- **Link:** [https://arxiv.org/abs/2601.10332v1](https://arxiv.org/abs/2601.10332v1)
- **Published:** 2026-01-15

"Think-Then-Generate: Reasoning-Aware Text-to-Image Diffusion with LLM Encoders" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Recent progress in text-to-image (T2I) diffusion models (DMs) has enabled high-quality visual synthesis from diverse textual prompts.

Yet, most existing T2I DMs, even those equipped with large language model (LLM)-based text encoders, remain text-pixel mappers -- they employ LLMs merely as text encoders, without leveraging their inherent reasoning capabilities to infer what should be visually depicted given the textual prompt.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 23. TextAlign: Preference Alignment for Text Rendering with Hierarchical Rewards

- **Link:** [https://arxiv.org/abs/2605.19320v2](https://arxiv.org/abs/2605.19320v2)
- **Published:** 2026-05-19

"TextAlign: Preference Alignment for Text Rendering with Hierarchical Rewards" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Faithful text rendering remains a persistent weakness of large text-to-image generative models, as it requires both semantic instruction following and fine-grained glyph-level structure.

Prior methods often improve this ability through architecture-specific modules or encoder modifications, which complicate deployment across foundation models.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 24. PromptEcho: Annotation-Free Reward from Vision-Language Models for Text-to-Image Reinforcement Learning

- **Link:** [https://arxiv.org/abs/2604.12652v2](https://arxiv.org/abs/2604.12652v2)
- **Published:** 2026-04-14

"PromptEcho: Annotation-Free Reward from Vision-Language Models for Text-to-Image Reinforcement Learning" (2026) studies prompt rewriting, optimization, or prompt-side control for image generators.

Reinforcement learning (RL) can improve the prompt following capability of text-to-image (T2I) models, yet obtaining high-quality reward signals remains challenging: CLIP Score is too coarse-grained, while VLM-based reward models (e.g., RewardDance) require costly human-annotated preference data and additional fine-tuning.

We propose PromptEcho, a reward construction method that requires \emph{no} annotation and \emph{no} reward model training.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 25. VLM-Guided Adaptive Negative Prompting for Creative Generation

- **Link:** [https://arxiv.org/abs/2510.10715v1](https://arxiv.org/abs/2510.10715v1)
- **Published:** 2025-10-12

"VLM-Guided Adaptive Negative Prompting for Creative Generation" (2025) studies prompt rewriting, optimization, or prompt-side control for image generators.

Creative generation is the synthesis of new, surprising, and valuable samples that reflect user intent yet cannot be envisioned in advance.

This task aims to extend human imagination, enabling the discovery of visual concepts that exist in the unexplored spaces between familiar domains.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 26. CRAFT: Continuous Reasoning and Agentic Feedback Tuning for Multimodal Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2512.20362v2](https://arxiv.org/abs/2512.20362v2)
- **Published:** 2025-12-23

"CRAFT: Continuous Reasoning and Agentic Feedback Tuning for Multimodal Text-to-Image Generation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Recent work has shown that inference-time reasoning and reflection can improve text-to-image generation without retraining.

However, existing approaches often rely on implicit, holistic critiques or unconstrained prompt rewrites, making their behavior difficult to interpret, control, or stop reliably.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 27. PromptMoG: Enhancing Diversity in Long-Prompt Image Generation via Prompt Embedding Mixture-of-Gaussian Sampling

- **Link:** [https://arxiv.org/abs/2511.20251v1](https://arxiv.org/abs/2511.20251v1)
- **Published:** 2025-11-25

"PromptMoG: Enhancing Diversity in Long-Prompt Image Generation via Prompt Embedding Mixture-of-Gaussian Sampling" (2025) studies prompt rewriting, optimization, or prompt-side control for image generators.

Recent advances in text-to-image (T2I) generation have achieved remarkable visual outcomes through large-scale rectified flow models.

However, how these models behave under long prompts remains underexplored.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 28. Lumina-mGPT 2.0: Stand-Alone AutoRegressive Image Modeling

- **Link:** [https://arxiv.org/abs/2507.17801v1](https://arxiv.org/abs/2507.17801v1)
- **Published:** 2025-07-23

"Lumina-mGPT 2.0: Stand-Alone AutoRegressive Image Modeling" (2025) is a modern system/report in the LLM/VLM-conditioned image generation line.

We present Lumina-mGPT 2.0, a stand-alone, decoder-only autoregressive model that revisits and revitalizes the autoregressive paradigm for high-quality image generation and beyond.

Unlike existing approaches that rely on pretrained components or hybrid architectures, Lumina-mGPT 2.0 is trained entirely from scratch, enabling unrestricted architectural design and licensing freedom.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 29. TexTailor: Inference-Time Textual Guidance Tailoring for Multimodal Diffusion Transformers

- **Link:** [https://arxiv.org/abs/2601.02211v2](https://arxiv.org/abs/2601.02211v2)
- **Published:** 2026-01-05

"TexTailor: Inference-Time Textual Guidance Tailoring for Multimodal Diffusion Transformers" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Recent breakthroughs of transformer-based diffusion models, particularly with Multimodal Diffusion Transformers (MMDiT) driven models like FLUX and Qwen Image, have facilitated thrilling experiences in visual generation.

However, these models rely only on the interactions between textual conditions and visual features to produce semantically aligned images.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 30. SPOT: Selective Prompt Projection via Total Variation for Inference-Only Safe Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2602.00616v3](https://arxiv.org/abs/2602.00616v3)
- **Published:** 2026-01-31

"SPOT: Selective Prompt Projection via Total Variation for Inference-Only Safe Text-to-Image Generation" (2026) studies prompt rewriting, optimization, or prompt-side control for image generators.

Text-to-Image (T2I) diffusion models enable high quality open ended synthesis, but practical use requires suppressing unsafe generations while preserving behavior on benign prompts.

We study this tension relative to the frozen generator, using its prompt conditioned distribution as the preservation reference.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 31. HiDream-O1-Image: A Natively Unified Image Generative Foundation Model with Pixel-level Unified Transformer

- **Link:** [https://arxiv.org/abs/2605.11061v1](https://arxiv.org/abs/2605.11061v1)
- **Published:** 2026-05-11

"HiDream-O1-Image: A Natively Unified Image Generative Foundation Model with Pixel-level Unified Transformer" (2026) is a modern system/report in the LLM/VLM-conditioned image generation line.

The evolution of visual generative models has long been constrained by fragmented architectures relying on disjoint text encoders and external VAEs.

In this report, we present HiDream-O1-Image, a natively unified generative foundation model via pixel-space Diffusion Transformer, that pioneers a paradigm shift from modular architectures to an end-to-end in-context visual generation engine.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 32. MMCORE: MultiModal COnnection with Representation Aligned Latent Embeddings

- **Link:** [https://arxiv.org/abs/2604.19902v1](https://arxiv.org/abs/2604.19902v1)
- **Published:** 2026-04-21

"MMCORE: MultiModal COnnection with Representation Aligned Latent Embeddings" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

We present MMCORE, a unified framework designed for multimodal image generation and editing.

MMCORE leverages a pre-trained Vision-Language Model (VLM) to predict semantic visual embeddings via learnable query tokens, which subsequently serve as conditioning signals for a diffusion model.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 33. ROVI: A VLM-LLM Re-Captioned Dataset for Open-Vocabulary Instance-Grounded Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2508.01008v1](https://arxiv.org/abs/2508.01008v1)
- **Published:** 2025-08-01

"ROVI: A VLM-LLM Re-Captioned Dataset for Open-Vocabulary Instance-Grounded Text-to-Image Generation" (2025) focuses on captioning/recaptioning data that feeds text-to-image training.

We present ROVI, a high-quality synthetic dataset for instance-grounded text-to-image generation, created by labeling 1M curated web images.

Our key innovation is a strategy called re-captioning, focusing on the pre-detection stage, where a VLM (Vision-Language Model) generates comprehensive visual descriptions that are then processed by an LLM (Large Language Model) to extract a flat list of potential categories for OVDs (Open-Vocabulary Detectors) to detect.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 34. Multi-Resolution Flow Matching: Training-Free Diffusion Acceleration via Staged Sampling

- **Link:** [https://arxiv.org/abs/2607.01642v1](https://arxiv.org/abs/2607.01642v1)
- **Published:** 2026-07-02

"Multi-Resolution Flow Matching: Training-Free Diffusion Acceleration via Staged Sampling" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Hardware-agnostic strategies for accelerating text-to-image diffusion, such as timestep distillation and feature caching, can reduce inference time without custom kernels or system-level optimization.

Among them, multi-resolution generation strategies have recently received broad attention, attaining more than 5x speedup without any training.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 35. ITIScore: An Image-to-Text-to-Image Rating Framework for the Image Captioning Ability of MLLMs

- **Link:** [https://arxiv.org/abs/2604.03765v2](https://arxiv.org/abs/2604.03765v2)
- **Published:** 2026-04-04

"ITIScore: An Image-to-Text-to-Image Rating Framework for the Image Captioning Ability of MLLMs" (2026) focuses on captioning/recaptioning data that feeds text-to-image training.

Recent advances in multimodal large language models (MLLMs) have greatly improved image understanding and captioning capabilities.

However, existing image captioning benchmarks typically suffer from limited diversity in caption length, the absence of recent advanced MLLMs, and insufficient human annotations, which potentially introduces bias and limits the ability to comprehensively assess the performance of modern MLLMs.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 36. Query-Kontext: An Unified Multimodal Model for Image Generation and Editing

- **Link:** [https://arxiv.org/abs/2509.26641v1](https://arxiv.org/abs/2509.26641v1)
- **Published:** 2025-09-30

"Query-Kontext: An Unified Multimodal Model for Image Generation and Editing" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Unified Multimodal Models (UMMs) have demonstrated remarkable performance in text-to-image generation (T2I) and editing (TI2I), whether instantiated as assembled unified frameworks which couple powerful vision-language model (VLM) with diffusion-based generator, or as naive Unified Multimodal Models with an early fusion of understanding and gene...

We contend that in current unified frameworks, the crucial capability of multimodal generative reasoning which encompasses instruction understanding, grounding, and image referring for identity preservation and faithful reconstruction, is intrinsically entangled with high-fidelity synthesis.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 37. LaDe: Unified Multi-Layered Graphic Media Generation and Decomposition

- **Link:** [https://arxiv.org/abs/2603.17965v1](https://arxiv.org/abs/2603.17965v1)
- **Published:** 2026-03-18

"LaDe: Unified Multi-Layered Graphic Media Generation and Decomposition" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Media design layer generation enables the creation of fully editable, layered design documents such as posters, flyers, and logos using only natural language prompts.

Existing methods either restrict outputs to a fixed number of layers or require each layer to contain only spatially continuous regions, causing the layer count to scale linearly with design complexity.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 38. CIDER: A Causal Cure for Brand-Obsessed Text-to-Image Models

- **Link:** [https://arxiv.org/abs/2509.15803v1](https://arxiv.org/abs/2509.15803v1)
- **Published:** 2025-09-19

"CIDER: A Causal Cure for Brand-Obsessed Text-to-Image Models" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Text-to-image (T2I) models exhibit a significant yet under-explored "brand bias", a tendency to generate contents featuring dominant commercial brands from generic prompts, posing ethical and legal risks.

We propose CIDER, a novel, model-agnostic framework to mitigate bias at inference-time through prompt refinement to avoid costly retraining.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 39. RePrompt: Reasoning-Augmented Reprompting for Text-to-Image Generation via Reinforcement Learning

- **Link:** [https://arxiv.org/abs/2505.17540v1](https://arxiv.org/abs/2505.17540v1)
- **Published:** 2025-05-23

"RePrompt: Reasoning-Augmented Reprompting for Text-to-Image Generation via Reinforcement Learning" (2025) studies prompt rewriting, optimization, or prompt-side control for image generators.

Despite recent progress in text-to-image (T2I) generation, existing models often struggle to faithfully capture user intentions from short and under-specified prompts.

While prior work has attempted to enhance prompts using large language models (LLMs), these methods frequently generate stylistic or unrealistic content due to insufficient grounding in visual semantics and real-world composition.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 40. RICO: Improving Accuracy and Completeness in Image Recaptioning via Visual Reconstruction

- **Link:** [https://arxiv.org/abs/2505.22613v1](https://arxiv.org/abs/2505.22613v1)
- **Published:** 2025-05-28

"RICO: Improving Accuracy and Completeness in Image Recaptioning via Visual Reconstruction" (2025) focuses on captioning/recaptioning data that feeds text-to-image training.

Image recaptioning is widely used to generate training datasets with enhanced quality for various multimodal tasks.

Existing recaptioning methods typically rely on powerful multimodal large language models (MLLMs) to enhance textual descriptions, but often suffer from inaccuracies due to hallucinations and incompleteness caused by missing fine-grained details.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 41. UniGenBench++: A Unified Semantic Evaluation Benchmark for Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2510.18701v2](https://arxiv.org/abs/2510.18701v2)
- **Published:** 2025-10-21

"UniGenBench++: A Unified Semantic Evaluation Benchmark for Text-to-Image Generation" (2025) introduces or expands evaluation for text-conditioned image generation, often under long or compositional prompts.

Recent progress in text-to-image (T2I) generation underscores the importance of reliable benchmarks in evaluating how accurately generated images reflect the semantics of their textual prompt.

However, (1) existing benchmarks lack the diversity of prompt scenarios and multilingual support, both essential for real-world applicability; (2) they offer only coarse evaluations across primary dimensions, covering a narrow range of sub-dimensions, and fall short in fine-grained sub-dimension assessment.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 42. Omni-Dish: Photorealistic and Faithful Image Generation and Editing for Arbitrary Chinese Dishes

- **Link:** [https://arxiv.org/abs/2504.09948v3](https://arxiv.org/abs/2504.09948v3)
- **Published:** 2025-04-14

"Omni-Dish: Photorealistic and Faithful Image Generation and Editing for Arbitrary Chinese Dishes" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Dish images play a crucial role in the digital era, with the demand for culturally distinctive dish images continuously increasing due to the digitization of the food industry and e-commerce.

In general cases, existing text-to-image generation models excel in producing high-quality images; however, they struggle to capture diverse characteristics and faithful details of specific domains, particularly Chinese dishes.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 43. Qwen-Image-Layered: Towards Inherent Editability via Layer Decomposition

- **Link:** [https://arxiv.org/abs/2512.15603v1](https://arxiv.org/abs/2512.15603v1)
- **Published:** 2025-12-17

"Qwen-Image-Layered: Towards Inherent Editability via Layer Decomposition" (2025) is a modern system/report in the LLM/VLM-conditioned image generation line.

Recent visual generative models often struggle with consistency during image editing due to the entangled nature of raster images, where all visual content is fused into a single canvas.

In contrast, professional design tools employ layered representations, allowing isolated edits while preserving consistency.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 44. Reason2Attack: Jailbreaking Text-to-Image Models via LLM Reasoning

- **Link:** [https://arxiv.org/abs/2503.17987v3](https://arxiv.org/abs/2503.17987v3)
- **Published:** 2025-03-23

"Reason2Attack: Jailbreaking Text-to-Image Models via LLM Reasoning" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Text-to-Image(T2I) models typically deploy safety filters to prevent the generation of sensitive images.

Unfortunately, recent jailbreaking attack methods manually design instructions for the LLM to generate adversarial prompts, which effectively bypass safety filters while producing sensitive images, exposing safety vulnerabilities of T2I models.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 45. Harnessing Caption Detailness for Data-Efficient Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2505.15172v1](https://arxiv.org/abs/2505.15172v1)
- **Published:** 2025-05-21

"Harnessing Caption Detailness for Data-Efficient Text-to-Image Generation" (2025) focuses on captioning/recaptioning data that feeds text-to-image training.

Training text-to-image (T2I) models with detailed captions can significantly improve their generation quality.

Existing methods often rely on simplistic metrics like caption length to represent the detailness of the caption in the T2I training set.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 46. BlindSight: Harnessing Sparsity for Efficient Vision-Language Models

- **Link:** [https://arxiv.org/abs/2507.09071v3](https://arxiv.org/abs/2507.09071v3)
- **Published:** 2025-07-11

"BlindSight: Harnessing Sparsity for Efficient Vision-Language Models" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Large vision-language models (VLMs) enable joint processing of text and images.

However, incorporating vision data significantly increases the prompt length, resulting in a longer time to first token (TTFT).

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 47. Understanding-in-Generation: Reinforcing Generative Capability of Unified Model via Infusing Understanding into Generation

- **Link:** [https://arxiv.org/abs/2509.18639v3](https://arxiv.org/abs/2509.18639v3)
- **Published:** 2025-09-23

"Understanding-in-Generation: Reinforcing Generative Capability of Unified Model via Infusing Understanding into Generation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Recent works have made notable advancements in enhancing unified models for text-to-image generation through the Chain-of-Thought (CoT).

However, these reasoning methods separate the processes of understanding and generation, which limits their ability to guide the reasoning of unified models in addressing the deficiencies of their generative capabilities.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 48. Synth$^2$: Boosting Visual-Language Models with Synthetic Captions and Image Embeddings

- **Link:** [https://arxiv.org/abs/2403.07750v2](https://arxiv.org/abs/2403.07750v2)
- **Published:** 2024-03-12

"Synth$^2$: Boosting Visual-Language Models with Synthetic Captions and Image Embeddings" (2024) focuses on captioning/recaptioning data that feeds text-to-image training.

The creation of high-quality human-labeled image-caption datasets presents a significant bottleneck in the development of Visual-Language Models (VLMs).

In this work, we investigate an approach that leverages the strengths of Large Language Models (LLMs) and image generation models to create synthetic image-text pairs for efficient and effective VLM training.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 49. TIIF-Bench: How Does Your T2I Model Follow Your Instructions?

- **Link:** [https://arxiv.org/abs/2506.02161v3](https://arxiv.org/abs/2506.02161v3)
- **Published:** 2025-06-02

"TIIF-Bench: How Does Your T2I Model Follow Your Instructions?" (2025) introduces or expands evaluation for text-conditioned image generation, often under long or compositional prompts.

The rapid advancements of Text-to-Image (T2I) models have ushered in a new phase of AI-generated content, marked by their growing ability to interpret and follow user instructions.

However, existing T2I model evaluation benchmarks fall short in limited prompt diversity and complexity, as well as coarse evaluation metrics, making it difficult to evaluate the fine-grained alignment performance between textual instructions and generated images.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 50. Efficient Scaling of Diffusion Transformers for Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2412.12391v1](https://arxiv.org/abs/2412.12391v1)
- **Published:** 2024-12-16

"Efficient Scaling of Diffusion Transformers for Text-to-Image Generation" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

We empirically study the scaling properties of various Diffusion Transformers (DiTs) for text-to-image generation by performing extensive and rigorous ablations, including training scaled DiTs ranging from 0.3B upto 8B parameters on datasets up to 600M images.

We find that U-ViT, a pure self-attention based DiT model provides a simpler design and scales more effectively in comparison with cross-attention based DiT variants, which allows straightforward expansion for extra conditions and other modalities.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 51. SANA: Efficient High-Resolution Image Synthesis with Linear Diffusion Transformers

- **Link:** [https://arxiv.org/abs/2410.10629v3](https://arxiv.org/abs/2410.10629v3)
- **Published:** 2024-10-14

"SANA: Efficient High-Resolution Image Synthesis with Linear Diffusion Transformers" (2024) is a modern system/report in the LLM/VLM-conditioned image generation line.

We introduce Sana, a text-to-image framework that can efficiently generate images up to 4096$\times$4096 resolution.

Sana can synthesize high-resolution, high-quality images with strong text-image alignment at a remarkably fast speed, deployable on laptop GPU.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 52. No Caption, No Problem: Caption-Free Membership Inference via Model-Fitted Embeddings

- **Link:** [https://arxiv.org/abs/2602.22689v1](https://arxiv.org/abs/2602.22689v1)
- **Published:** 2026-02-26

"No Caption, No Problem: Caption-Free Membership Inference via Model-Fitted Embeddings" (2026) focuses on captioning/recaptioning data that feeds text-to-image training.

Latent diffusion models have achieved remarkable success in high-fidelity text-to-image generation, but their tendency to memorize training data raises critical privacy and intellectual property concerns.

Membership inference attacks (MIAs) provide a principled way to audit such memorization by determining whether a given sample was included in training.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 53. Qwen-Image-2.0-RL Technical Report

- **Link:** [https://arxiv.org/abs/2606.27608v1](https://arxiv.org/abs/2606.27608v1)
- **Published:** 2026-06-25

"Qwen-Image-2.0-RL Technical Report" (2026) is a modern system/report in the LLM/VLM-conditioned image generation line.

We present Qwen-Image-2.0-RL, a post-training pipeline that applies reinforcement learning from human feedback (RLHF) and on-policy distillation (OPD) to improve both the visual quality and instruction-following capability of the Qwen-Image-2.0 diffusion model.

To provide reliable reward signals, we construct task-specific composite reward models by fine-tuning vision-language models with a pointwise scoring paradigm and chain-of-thought reasoning.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 54. High-Fidelity Text-to-Image Generation from Pre-Trained Vision-Language Models via Distribution-Conditioned Diffusion Decoding

- **Link:** [https://arxiv.org/abs/2603.13389v1](https://arxiv.org/abs/2603.13389v1)
- **Published:** 2026-03-11

"High-Fidelity Text-to-Image Generation from Pre-Trained Vision-Language Models via Distribution-Conditioned Diffusion Decoding" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Recent large-scale vision-language models (VLMs) have shown remarkable text-to-image generation capabilities, yet their visual fidelity remains constrained by the discrete image tokenization, which poses a major challenge.

Although several studies have explored continuous representation modeling to enhance visual quality, adapting pre-trained VLM models to such representations requires large-scale data and training costs comparable to the original pre-training.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 55. RAISE: Requirement-Adaptive Evolutionary Refinement for Training-Free Text-to-Image Alignment

- **Link:** [https://arxiv.org/abs/2603.00483v1](https://arxiv.org/abs/2603.00483v1)
- **Published:** 2026-02-28

"RAISE: Requirement-Adaptive Evolutionary Refinement for Training-Free Text-to-Image Alignment" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Recent text-to-image (T2I) diffusion models achieve remarkable realism, yet faithful prompt-image alignment remains challenging, particularly for complex prompts with multiple objects, relations, and fine-grained attributes.

Existing training-free inference-time scaling methods rely on fixed iteration budgets that cannot adapt to prompt difficulty, while reflection-tuned models require carefully curated reflection datasets and extensive joint fine-tuning of diffusion and vision-language models, often overfitting to reflection paths data and lacking transferability a...

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 56. Amber-Image: Efficient Compression of Large-Scale Diffusion Transformers

- **Link:** [https://arxiv.org/abs/2602.17047v1](https://arxiv.org/abs/2602.17047v1)
- **Published:** 2026-02-19

"Amber-Image: Efficient Compression of Large-Scale Diffusion Transformers" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Diffusion Transformer (DiT) architectures have significantly advanced Text-to-Image (T2I) generation but suffer from prohibitive computational costs and deployment barriers.

To address these challenges, we propose an efficient compression framework that transforms the 60-layer dual-stream MMDiT-based Qwen-Image into lightweight models without training from scratch.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 57. JoyAI-Image: Awaking Spatial Intelligence in Unified Multimodal Understanding and Generation

- **Link:** [https://arxiv.org/abs/2605.04128v2](https://arxiv.org/abs/2605.04128v2)
- **Published:** 2026-05-05

"JoyAI-Image: Awaking Spatial Intelligence in Unified Multimodal Understanding and Generation" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

We present JoyAI-Image, a unified multimodal foundation model for visual understanding, text-to-image generation, and instruction-guided image editing.

JoyAI-Image couples a spatially enhanced Multimodal Large Language Model (MLLM) with a Multimodal Diffusion Transformer (MMDiT), allowing perception and generation to interact through a shared multimodal interface.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 58. ImagenWorld: Stress-Testing Image Generation Models with Explainable Human Evaluation on Open-ended Real-World Tasks

- **Link:** [https://arxiv.org/abs/2603.27862v1](https://arxiv.org/abs/2603.27862v1)
- **Published:** 2026-03-29

"ImagenWorld: Stress-Testing Image Generation Models with Explainable Human Evaluation on Open-ended Real-World Tasks" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Advances in diffusion, autoregressive, and hybrid models have enabled high-quality image synthesis for tasks such as text-to-image, editing, and reference-guided composition.

Yet, existing benchmarks remain limited, either focus on isolated tasks, cover only narrow domains, or provide opaque scores without explaining failure modes.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 59. Auto-Rubric as Reward: From Implicit Preferences to Explicit Multimodal Generative Criteria

- **Link:** [https://arxiv.org/abs/2605.08354v1](https://arxiv.org/abs/2605.08354v1)
- **Published:** 2026-05-08

"Auto-Rubric as Reward: From Implicit Preferences to Explicit Multimodal Generative Criteria" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Aligning multimodal generative models with human preferences demands reward signals that respect the compositional, multi-dimensional structure of human judgment.

Prevailing RLHF approaches reduce this structure to scalar or pairwise labels, collapsing nuanced preferences into opaque parametric proxies and exposing vulnerabilities to reward hacking.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 60. Make VLM Recognize Visual Hallucination on Cartoon Character Image with Pose Information

- **Link:** [https://arxiv.org/abs/2403.15048v4](https://arxiv.org/abs/2403.15048v4)
- **Published:** 2024-03-22

"Make VLM Recognize Visual Hallucination on Cartoon Character Image with Pose Information" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Leveraging large-scale Text-to-Image (TTI) models have become a common technique for generating exemplar or training dataset in the fields of image synthesis, video editing, 3D reconstruction.

However, semantic structural visual hallucinations involving perceptually severe defects remain a concern, especially in the domain of non-photorealistic rendering (NPR) such as cartoons and pixelization-style character.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 61. AutoRubric-T2I: Robust Rule-Based Reward Model for Text-to-Image Alignment

- **Link:** [https://arxiv.org/abs/2605.17602v2](https://arxiv.org/abs/2605.17602v2)
- **Published:** 2026-05-17

"AutoRubric-T2I: Robust Rule-Based Reward Model for Text-to-Image Alignment" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Aligning Text-to-Image (T2I) generation models with human preferences increasingly relies on image reward models that score or rank generated images according to prompt alignment and perceptual quality.

Existing reward models are commonly trained as Bradley-Terry (BT) preference models on large-scale human preference corpora, making them costly to train, difficult to adapt, and opaque in their evaluation criteria.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 62. UniFusion: Vision-Language Model as Unified Encoder in Image Generation

- **Link:** [https://arxiv.org/abs/2510.12789v1](https://arxiv.org/abs/2510.12789v1)
- **Published:** 2025-10-14

"UniFusion: Vision-Language Model as Unified Encoder in Image Generation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Although recent advances in visual generation have been remarkable, most existing architectures still depend on distinct encoders for images and text.

This separation constrains diffusion models' ability to perform cross-modal reasoning and knowledge transfer.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 63. UltraFlux: Data-Model Co-Design for High-quality Native 4K Text-to-Image Generation across Diverse Aspect Ratios

- **Link:** [https://arxiv.org/abs/2511.18050v1](https://arxiv.org/abs/2511.18050v1)
- **Published:** 2025-11-22

"UltraFlux: Data-Model Co-Design for High-quality Native 4K Text-to-Image Generation across Diverse Aspect Ratios" (2025) is a modern system/report in the LLM/VLM-conditioned image generation line.

Diffusion transformers have recently delivered strong text-to-image generation around 1K resolution, but we show that extending them to native 4K across diverse aspect ratios exposes a tightly coupled failure mode spanning positional encoding, VAE compression, and optimization.

Tackling any of these factors in isolation leaves substantial quality on the table.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 64. Lumina-mGPT: Illuminate Flexible Photorealistic Text-to-Image Generation with Multimodal Generative Pretraining

- **Link:** [https://arxiv.org/abs/2408.02657v3](https://arxiv.org/abs/2408.02657v3)
- **Published:** 2024-08-05

"Lumina-mGPT: Illuminate Flexible Photorealistic Text-to-Image Generation with Multimodal Generative Pretraining" (2024) is a modern system/report in the LLM/VLM-conditioned image generation line.

We present Lumina-mGPT, a family of multimodal autoregressive models capable of various vision and language tasks, particularly excelling in generating flexible photorealistic images from text descriptions.

By initializing from multimodal Generative PreTraining (mGPT), we demonstrate that decoder-only Autoregressive (AR) model can achieve image generation performance comparable to modern diffusion models with high efficiency through Flexible Progressive Supervised Fine-tuning (FP-SFT).

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 65. ViHOI: Human-Object Interaction Synthesis with Visual Priors

- **Link:** [https://arxiv.org/abs/2603.24383v1](https://arxiv.org/abs/2603.24383v1)
- **Published:** 2026-03-25

"ViHOI: Human-Object Interaction Synthesis with Visual Priors" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Generating realistic and physically plausible 3D Human-Object Interactions (HOI) remains a key challenge in motion generation.

One primary reason is that describing these physical constraints with words alone is difficult.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 66. Mastering Text-to-Image Diffusion: Recaptioning, Planning, and Generating with Multimodal LLMs

- **Link:** [https://arxiv.org/abs/2401.11708v3](https://arxiv.org/abs/2401.11708v3)
- **Published:** 2024-01-22

"Mastering Text-to-Image Diffusion: Recaptioning, Planning, and Generating with Multimodal LLMs" (2024) focuses on captioning/recaptioning data that feeds text-to-image training.

Diffusion models have exhibit exceptional performance in text-to-image generation and editing.

However, existing methods often face challenges when handling complex text prompts that involve multiple objects with multiple attributes and relationships.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 67. Towards Robust Text-to-Image Person Retrieval: Multi-View Reformulation for Semantic Compensation

- **Link:** [https://arxiv.org/abs/2604.18376v1](https://arxiv.org/abs/2604.18376v1)
- **Published:** 2026-04-20

"Towards Robust Text-to-Image Person Retrieval: Multi-View Reformulation for Semantic Compensation" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

In text-to-image person retrieval tasks, the diversity of natural language expressions and the implicitness of visual semantics often lead to the problem of Expression Drift, where semantically equivalent texts exhibit significant feature discrepancies in the embedding space due to phrasing variations, thereby degrading the robustness of image-t...

This paper proposes a semantic compensation framework (MVR) driven by Large Language Models (LLMs), which enhances cross-modal representation consistency through multi-view semantic reformulation and feature compensation.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 68. RealGen: Photorealistic Text-to-Image Generation via Detector-Guided Rewards

- **Link:** [https://arxiv.org/abs/2512.00473v1](https://arxiv.org/abs/2512.00473v1)
- **Published:** 2025-11-29

"RealGen: Photorealistic Text-to-Image Generation via Detector-Guided Rewards" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

With the continuous advancement of image generation technology, advanced models such as GPT-Image-1 and Qwen-Image have achieved remarkable text-to-image consistency and world knowledge However, these models still fall short in photorealistic image generation.

Even on simple T2I tasks, they tend to produce " fake" images with distinct AI artifacts, often characterized by "overly smooth skin" and "oily facial sheens".

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 69. CycleCap: Improving VLMs Captioning Performance via Self-Supervised Cycle Consistency Fine-Tuning

- **Link:** [https://arxiv.org/abs/2603.18282v2](https://arxiv.org/abs/2603.18282v2)
- **Published:** 2026-03-18

"CycleCap: Improving VLMs Captioning Performance via Self-Supervised Cycle Consistency Fine-Tuning" (2026) focuses on captioning/recaptioning data that feeds text-to-image training.

Visual-Language Models (VLMs) have achieved remarkable progress in image captioning, visual question answering, and visual reasoning.

Yet they remain prone to vision-language misalignment, often producing overly generic or hallucinated descriptions.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 70. ELDiff: When Evidential Learning Meets Text-to-Image Diffusion

- **Link:** [https://arxiv.org/abs/2606.20924v1](https://arxiv.org/abs/2606.20924v1)
- **Published:** 2026-06-18

"ELDiff: When Evidential Learning Meets Text-to-Image Diffusion" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

In multi-object text-to-image (T2I) diffusion, ensuring semantic consistency between textual prompts and generated visual content is crucial for image synthesis.

However, such consistency constraint is often underemphasized in the denoising process of diffusion models.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 71. TeleStyle V2: Beyond Content-Preserving Style Transfer with Self-Distillation and Distribution-Matching-Distillation

- **Link:** [https://arxiv.org/abs/2606.20709v1](https://arxiv.org/abs/2606.20709v1)
- **Published:** 2026-06-16

"TeleStyle V2: Beyond Content-Preserving Style Transfer with Self-Distillation and Distribution-Matching-Distillation" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Given a content reference and a style reference, content-preserving style transfer requires the model to generate stylized outputs with content and style consistency.

We introduced TeleStyle V1 to tackle this problem.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 72. Qwen-Image-VAE-2.0 Technical Report

- **Link:** [https://arxiv.org/abs/2605.13565v1](https://arxiv.org/abs/2605.13565v1)
- **Published:** 2026-05-13

"Qwen-Image-VAE-2.0 Technical Report" (2026) is a modern system/report in the LLM/VLM-conditioned image generation line.

We present Qwen-Image-VAE-2.0, a suite of high-compression Variational Autoencoders (VAEs) that achieve significant advances in both reconstruction fidelity and diffusability.

To address the reconstruction bottlenecks of high compression, we adopt an improved architecture featuring Global Skip Connections (GSC) and expanded latent channels.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 73. Agentic Flow Steering and Parallel Rollout Search for Spatially Grounded Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2603.18627v1](https://arxiv.org/abs/2603.18627v1)
- **Published:** 2026-03-19

"Agentic Flow Steering and Parallel Rollout Search for Spatially Grounded Text-to-Image Generation" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Precise Text-to-Image (T2I) generation has achieved great success but is hindered by the limited relational reasoning of static text encoders and the error accumulation in open-loop sampling.

Without real-time feedback, initial semantic ambiguities during the Ordinary Differential Equation trajectory inevitably escalate into stochastic deviations from spatial constraints.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 74. CritiFusion: Semantic Critique and Spectral Alignment for Faithful Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2512.22681v2](https://arxiv.org/abs/2512.22681v2)
- **Published:** 2025-12-27

"CritiFusion: Semantic Critique and Spectral Alignment for Faithful Text-to-Image Generation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Recent text-to-image diffusion models have achieved remarkable visual fidelity but often struggle with semantic alignment to complex prompts.

We introduce CritiFusion, a novel inference-time framework that integrates a multimodal semantic critique mechanism with frequency-domain refinement to improve text-to-image consistency and detail.

Keep it as background on modern generation/evaluation; use only if its data or metrics inform caption-length decisions.


### 75. Discovering Divergent Representations between Text-to-Image Models

- **Link:** [https://arxiv.org/abs/2509.08940v1](https://arxiv.org/abs/2509.08940v1)
- **Published:** 2025-09-10

"Discovering Divergent Representations between Text-to-Image Models" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

In this paper, we investigate when and how visual representations learned by two different generative models diverge.

Given two text-to-image models, our goal is to discover visual attributes that appear in images generated by one model but not the other, along with the types of prompts that trigger these attribute differences.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 76. Prompting for products: Investigating design space exploration strategies for text-to-image generative models

- **Link:** [https://arxiv.org/abs/2408.03946v1](https://arxiv.org/abs/2408.03946v1)
- **Published:** 2024-07-22

"Prompting for products: Investigating design space exploration strategies for text-to-image generative models" (2024) studies prompt rewriting, optimization, or prompt-side control for image generators.

Text-to-image models are enabling efficient design space exploration, rapidly generating images from text prompts.

However, many generative AI tools are imperfect for product design applications as they are not built for the goals and requirements of product design.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 77. PiD: Fast and High-Resolution Latent Decoding with Pixel Diffusion

- **Link:** [https://arxiv.org/abs/2605.23902v1](https://arxiv.org/abs/2605.23902v1)
- **Published:** 2026-05-22

"PiD: Fast and High-Resolution Latent Decoding with Pixel Diffusion" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Most practical high-resolution text-to-image systems, including latent diffusion and autoregressive models, perform generation in a compact latent space, and a decoder maps the generated latents back to pixels.

Yet the latent-to-pixel decoder is reconstruction-oriented, optimized to invert the encoder rather than synthesize more details, and becomes increasingly costly at megapixel scale.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 78. Reflect-DiT: Inference-Time Scaling for Text-to-Image Diffusion Transformers via In-Context Reflection

- **Link:** [https://arxiv.org/abs/2503.12271v1](https://arxiv.org/abs/2503.12271v1)
- **Published:** 2025-03-15

"Reflect-DiT: Inference-Time Scaling for Text-to-Image Diffusion Transformers via In-Context Reflection" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

The predominant approach to advancing text-to-image generation has been training-time scaling, where larger models are trained on more data using greater computational resources.

While effective, this approach is computationally expensive, leading to growing interest in inference-time scaling to improve performance.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 79. QwenStyle: Content-Preserving Style Transfer with Qwen-Image-Edit

- **Link:** [https://arxiv.org/abs/2601.06202v1](https://arxiv.org/abs/2601.06202v1)
- **Published:** 2026-01-08

"QwenStyle: Content-Preserving Style Transfer with Qwen-Image-Edit" (2026) is a modern system/report in the LLM/VLM-conditioned image generation line.

Content-Preserving Style transfer, given content and style references, remains challenging for Diffusion Transformers (DiTs) due to its internal entangled content and style features.

In this technical report, we propose the first content-preserving style transfer model trained on Qwen-Image-Edit, which activates Qwen-Image-Edit's strong content preservation and style customization capability.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 80. Noise Projection: Closing the Prompt-Agnostic Gap Behind Text-to-Image Misalignment in Diffusion Models

- **Link:** [https://arxiv.org/abs/2510.14526v1](https://arxiv.org/abs/2510.14526v1)
- **Published:** 2025-10-16

"Noise Projection: Closing the Prompt-Agnostic Gap Behind Text-to-Image Misalignment in Diffusion Models" (2025) studies prompt rewriting, optimization, or prompt-side control for image generators.

In text-to-image generation, different initial noises induce distinct denoising paths with a pretrained Stable Diffusion (SD) model.

While this pattern could output diverse images, some of them may fail to align well with the prompt.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 81. MLLM-Guided VLM Fine-Tuning with Joint Inference for Zero-Shot Composed Image Retrieval

- **Link:** [https://arxiv.org/abs/2505.19707v1](https://arxiv.org/abs/2505.19707v1)
- **Published:** 2025-05-26

"MLLM-Guided VLM Fine-Tuning with Joint Inference for Zero-Shot Composed Image Retrieval" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Existing Zero-Shot Composed Image Retrieval (ZS-CIR) methods typically train adapters that convert reference images into pseudo-text tokens, which are concatenated with the modifying text and processed by frozen text encoders in pretrained VLMs or LLMs.

While this design leverages the strengths of large pretrained models, it only supervises the adapter to produce encoder-compatible tokens that loosely preserve visual semantics.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 82. LumiGen: An LVLM-Enhanced Iterative Framework for Fine-Grained Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2508.04732v1](https://arxiv.org/abs/2508.04732v1)
- **Published:** 2025-08-05

"LumiGen: An LVLM-Enhanced Iterative Framework for Fine-Grained Text-to-Image Generation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Text-to-Image (T2I) generation has made significant advancements with diffusion models, yet challenges persist in handling complex instructions, ensuring fine-grained content control, and maintaining deep semantic consistency.

Existing T2I models often struggle with tasks like accurate text rendering, precise pose generation, or intricate compositional coherence.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 83. LSSGen: Leveraging Latent Space Scaling in Flow and Diffusion for Efficient Text to Image Generation

- **Link:** [https://arxiv.org/abs/2507.16154v1](https://arxiv.org/abs/2507.16154v1)
- **Published:** 2025-07-22

"LSSGen: Leveraging Latent Space Scaling in Flow and Diffusion for Efficient Text to Image Generation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Flow matching and diffusion models have shown impressive results in text-to-image generation, producing photorealistic images through an iterative denoising process.

A common strategy to speed up synthesis is to perform early denoising at lower resolutions.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 84. LPNSR: Optimal Noise-Guided Diffusion Image Super-Resolution Via Learnable Noise Prediction

- **Link:** [https://arxiv.org/abs/2603.21045v5](https://arxiv.org/abs/2603.21045v5)
- **Published:** 2026-03-22

"LPNSR: Optimal Noise-Guided Diffusion Image Super-Resolution Via Learnable Noise Prediction" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Diffusion-based image super-resolution (SR) aims to reconstruct high-resolution (HR) images from low-resolution (LR) observations.

However, the inherent randomness injected during the reverse diffusion process causes the performance of diffusion-based SR models to vary significantly across different sampling runs, particularly when the sampling trajectory is compressed into a limited number of steps.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 85. Factorized-Dreamer: Training A High-Quality Video Generator with Limited and Low-Quality Data

- **Link:** [https://arxiv.org/abs/2408.10119v1](https://arxiv.org/abs/2408.10119v1)
- **Published:** 2024-08-19

"Factorized-Dreamer: Training A High-Quality Video Generator with Limited and Low-Quality Data" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Text-to-video (T2V) generation has gained significant attention due to its wide applications to video generation, editing, enhancement and translation, \etc.

However, high-quality (HQ) video synthesis is extremely challenging because of the diverse and complex motions existed in real world.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 86. One Rewrite to Fix Them All? Type-Aware Repair Allocation for Text-to-Image Prompt Optimization

- **Link:** [https://arxiv.org/abs/2607.18724v1](https://arxiv.org/abs/2607.18724v1)
- **Published:** 2026-07-21

"One Rewrite to Fix Them All? Type-Aware Repair Allocation for Text-to-Image Prompt Optimization" (2026) studies prompt rewriting, optimization, or prompt-side control for image generators.

Text-to-image (T2I) generators often fail to follow their prompts faithfully, producing wrong counts, swapped attributes, ambiguous relations, and illegible text.

Prompt optimization repairs such failures by rewriting the user prompt, requiring no generator retraining, and has yielded promising results.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 87. Qwen-Image Technical Report

- **Link:** [https://arxiv.org/abs/2508.02324v1](https://arxiv.org/abs/2508.02324v1)
- **Published:** 2025-08-04

"Qwen-Image Technical Report" (2025) is a modern system/report in the LLM/VLM-conditioned image generation line.

We present Qwen-Image, an image generation foundation model in the Qwen series that achieves significant advances in complex text rendering and precise image editing.

To address the challenges of complex text rendering, we design a comprehensive data pipeline that includes large-scale data collection, filtering, annotation, synthesis, and balancing.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 88. On the Feasibility of Poisoning Text-to-Image AI Models via Adversarial Mislabeling

- **Link:** [https://arxiv.org/abs/2506.21874v1](https://arxiv.org/abs/2506.21874v1)
- **Published:** 2025-06-27

"On the Feasibility of Poisoning Text-to-Image AI Models via Adversarial Mislabeling" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Today's text-to-image generative models are trained on millions of images sourced from the Internet, each paired with a detailed caption produced by Vision-Language Models (VLMs).

This part of the training pipeline is critical for supplying the models with large volumes of high-quality image-caption pairs during training.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 89. TIT-Score: Evaluating Long-Prompt Based Text-to-Image Alignment via Text-to-Image-to-Text Consistency

- **Link:** [https://arxiv.org/abs/2510.02987v1](https://arxiv.org/abs/2510.02987v1)
- **Published:** 2025-10-03

"TIT-Score: Evaluating Long-Prompt Based Text-to-Image Alignment via Text-to-Image-to-Text Consistency" (2025) studies prompt rewriting, optimization, or prompt-side control for image generators.

With the rapid advancement of large multimodal models (LMMs), recent text-to-image (T2I) models can generate high-quality images and demonstrate great alignment to short prompts.

However, they still struggle to effectively understand and follow long and detailed prompts, displaying inconsistent generation.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 90. AdaFV: Rethinking of Visual-Language alignment for VLM acceleration

- **Link:** [https://arxiv.org/abs/2501.09532v2](https://arxiv.org/abs/2501.09532v2)
- **Published:** 2025-01-16

"AdaFV: Rethinking of Visual-Language alignment for VLM acceleration" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

The success of VLMs often relies on the dynamic high-resolution schema that adaptively augments the input images to multiple crops, so that the details of the images can be retained.

However, such approaches result in a large number of redundant visual tokens, thus significantly reducing the efficiency of the VLMs.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 91. Multimodal Prompt Decoupling Attack on the Safety Filters in Text-to-Image Models

- **Link:** [https://arxiv.org/abs/2509.21360v1](https://arxiv.org/abs/2509.21360v1)
- **Published:** 2025-09-21

"Multimodal Prompt Decoupling Attack on the Safety Filters in Text-to-Image Models" (2025) studies prompt rewriting, optimization, or prompt-side control for image generators.

Text-to-image (T2I) models have been widely applied in generating high-fidelity images across various domains.

However, these models may also be abused to produce Not-Safe-for-Work (NSFW) content via jailbreak attacks.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 92. LLMs can see and hear without any training

- **Link:** [https://arxiv.org/abs/2501.18096v1](https://arxiv.org/abs/2501.18096v1)
- **Published:** 2025-01-30

"LLMs can see and hear without any training" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

We present MILS: Multimodal Iterative LLM Solver, a surprisingly simple, training-free approach, to imbue multimodal capabilities into your favorite LLM.

Leveraging their innate ability to perform multi-step reasoning, MILS prompts the LLM to generate candidate outputs, each of which are scored and fed back iteratively, eventually generating a solution to the task.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 93. Stitch: Training-Free Position Control in Multimodal Diffusion Transformers

- **Link:** [https://arxiv.org/abs/2509.26644v1](https://arxiv.org/abs/2509.26644v1)
- **Published:** 2025-09-30

"Stitch: Training-Free Position Control in Multimodal Diffusion Transformers" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Text-to-Image (T2I) generation models have advanced rapidly in recent years, but accurately capturing spatial relationships like "above" or "to the right of" poses a persistent challenge.

Earlier methods improved spatial relationship following with external position control.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 94. Hyper-Bagel: A Unified Acceleration Framework for Multimodal Understanding and Generation

- **Link:** [https://arxiv.org/abs/2509.18824v1](https://arxiv.org/abs/2509.18824v1)
- **Published:** 2025-09-23

"Hyper-Bagel: A Unified Acceleration Framework for Multimodal Understanding and Generation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Unified multimodal models have recently attracted considerable attention for their remarkable abilities in jointly understanding and generating diverse content.

However, as contexts integrate increasingly numerous interleaved multimodal tokens, the iterative processes of diffusion denoising and autoregressive decoding impose significant computational overhead.

Keep it as background on modern generation/evaluation; use only if its data or metrics inform caption-length decisions.


### 95. Lumina-OmniLV: A Unified Multimodal Framework for General Low-Level Vision

- **Link:** [https://arxiv.org/abs/2504.04903v2](https://arxiv.org/abs/2504.04903v2)
- **Published:** 2025-04-07

"Lumina-OmniLV: A Unified Multimodal Framework for General Low-Level Vision" (2025) is a modern system/report in the LLM/VLM-conditioned image generation line.

We present Lunima-OmniLV (abbreviated as OmniLV), a universal multimodal multi-task framework for low-level vision that addresses over 100 sub-tasks across four major categories: image restoration, image enhancement, weak-semantic dense prediction, and stylization.

OmniLV leverages both textual and visual prompts to offer flexible and user-friendly interactions.

Keep it as background on modern generation/evaluation; use only if its data or metrics inform caption-length decisions.


### 96. Low-hallucination Synthetic Captions for Large-Scale Vision-Language Model Pre-training

- **Link:** [https://arxiv.org/abs/2504.13123v2](https://arxiv.org/abs/2504.13123v2)
- **Published:** 2025-04-17

"Low-hallucination Synthetic Captions for Large-Scale Vision-Language Model Pre-training" (2025) focuses on captioning/recaptioning data that feeds text-to-image training.

In recent years, the field of vision-language model pre-training has experienced rapid advancements, driven primarily by the continuous enhancement of textual capabilities in large language models.

However, existing training paradigms for multimodal large language models heavily rely on high-quality image-text pairs.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 97. OneReward: Unified Mask-Guided Image Generation via Multi-Task Human Preference Learning

- **Link:** [https://arxiv.org/abs/2508.21066v1](https://arxiv.org/abs/2508.21066v1)
- **Published:** 2025-08-28

"OneReward: Unified Mask-Guided Image Generation via Multi-Task Human Preference Learning" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

In this paper, we introduce OneReward, a unified reinforcement learning framework that enhances the model's generative capabilities across multiple tasks under different evaluation criteria using only \textit{One Reward} model.

By employing a single vision-language model (VLM) as the generative reward model, which can distinguish the winner and loser for a given task and a given evaluation criterion, it can be effectively applied to multi-task generation models, particularly in contexts with varied data and diverse task objectives.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 98. Hallucination Behavior in Multimodal LLMs Across Agricultural Image Interpretation and Generation Tasks

- **Link:** [https://arxiv.org/abs/2605.27595v1](https://arxiv.org/abs/2605.27595v1)
- **Published:** 2026-05-26

"Hallucination Behavior in Multimodal LLMs Across Agricultural Image Interpretation and Generation Tasks" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Large Language Models (LLMs) are being rapidly adopted in agricultural imaging applications, ranging from crop interpretation to synthetic field image generation.

However, these models frequently exhibit hallucinations outputs that appear confident yet deviate from biological or environmental reality potentially leading to misinformed agronomic insights.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 99. ELLA: Equip Diffusion Models with LLM for Enhanced Semantic Alignment

- **Link:** [https://arxiv.org/abs/2403.05135v1](https://arxiv.org/abs/2403.05135v1)
- **Published:** 2024-03-08

"ELLA: Equip Diffusion Models with LLM for Enhanced Semantic Alignment" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Diffusion models have demonstrated remarkable performance in the domain of text-to-image generation.

However, most widely used models still employ CLIP as their text encoder, which constrains their ability to comprehend dense prompts, encompassing multiple objects, detailed attributes, complex relationships, long-text alignment, etc.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 100. Automated Prompt Generation for Creative and Counterfactual Text-to-image Synthesis

- **Link:** [https://arxiv.org/abs/2509.21375v1](https://arxiv.org/abs/2509.21375v1)
- **Published:** 2025-09-23

"Automated Prompt Generation for Creative and Counterfactual Text-to-image Synthesis" (2025) studies prompt rewriting, optimization, or prompt-side control for image generators.

Text-to-image generation has advanced rapidly with large-scale multimodal training, yet fine-grained controllability remains a critical challenge.

Counterfactual controllability, defined as the capacity to deliberately generate images that contradict common-sense patterns, remains a major challenge but plays a crucial role in enabling creativity and exploratory applications.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 101. EditID: Training-Free Editable ID Customization for Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2503.12526v1](https://arxiv.org/abs/2503.12526v1)
- **Published:** 2025-03-16

"EditID: Training-Free Editable ID Customization for Text-to-Image Generation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

We propose EditID, a training-free approach based on the DiT architecture, which achieves highly editable customized IDs for text to image generation.

Existing text-to-image models for customized IDs typically focus more on ID consistency while neglecting editability.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 102. Progressive Prompt Detailing for Improved Alignment in Text-to-Image Generative Models

- **Link:** [https://arxiv.org/abs/2503.17794v4](https://arxiv.org/abs/2503.17794v4)
- **Published:** 2025-03-22

"Progressive Prompt Detailing for Improved Alignment in Text-to-Image Generative Models" (2025) studies prompt rewriting, optimization, or prompt-side control for image generators.

Text-to-image generative models often struggle with long prompts detailing complex scenes, diverse objects with distinct visual characteristics and spatial relationships.

In this work, we propose SCoPE (Scheduled interpolation of Coarse-to-fine Prompt Embeddings), a training-free method to improve text-to-image alignment by progressively refining the input prompt in a coarse-to-fine-grained manner.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 103. EditIDv2: Editable ID Customization with Data-Lubricated ID Feature Integration for Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2509.05659v1](https://arxiv.org/abs/2509.05659v1)
- **Published:** 2025-09-06

"EditIDv2: Editable ID Customization with Data-Lubricated ID Feature Integration for Text-to-Image Generation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

We propose EditIDv2, a tuning-free solution specifically designed for high-complexity narrative scenes and long text inputs.

Existing character editing methods perform well under simple prompts, but often suffer from degraded editing capabilities, semantic understanding biases, and identity consistency breakdowns when faced with long text narratives containing multiple semantic layers, temporal logic, and complex contextual relationships.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 104. CAHS-Attack: CLIP-Aware Heuristic Search Attack Method for Stable Diffusion

- **Link:** [https://arxiv.org/abs/2511.21180v1](https://arxiv.org/abs/2511.21180v1)
- **Published:** 2025-11-26

"CAHS-Attack: CLIP-Aware Heuristic Search Attack Method for Stable Diffusion" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Diffusion models exhibit notable fragility when faced with adversarial prompts, and strengthening attack capabilities is crucial for uncovering such vulnerabilities and building more robust generative systems.

Existing works often rely on white-box access to model gradients or hand-crafted prompt engineering, which is infeasible in real-world deployments due to restricted access or poor attack effect.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 105. A Little More Like This: Text-to-Image Retrieval with Vision-Language Models Using Relevance Feedback

- **Link:** [https://arxiv.org/abs/2511.17255v1](https://arxiv.org/abs/2511.17255v1)
- **Published:** 2025-11-21

"A Little More Like This: Text-to-Image Retrieval with Vision-Language Models Using Relevance Feedback" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Large vision-language models (VLMs) enable intuitive visual search using natural language queries.

However, improving their performance often requires fine-tuning and scaling to larger model variants.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 106. Self-Rewarding Large Vision-Language Models for Optimizing Prompts in Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2505.16763v2](https://arxiv.org/abs/2505.16763v2)
- **Published:** 2025-05-22

"Self-Rewarding Large Vision-Language Models for Optimizing Prompts in Text-to-Image Generation" (2025) studies prompt rewriting, optimization, or prompt-side control for image generators.

Text-to-image models are powerful for producing high-quality images based on given text prompts, but crafting these prompts often requires specialized vocabulary.

To address this, existing methods train rewriting models with supervision from large amounts of manually annotated data and trained aesthetic assessment models.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 107. Dynamic Optimization and Safety Indicator Injection for Jailbreaking Text-to-Image Models with Multimodal Safety Filters

- **Link:** [https://arxiv.org/abs/2505.18979v2](https://arxiv.org/abs/2505.18979v2)
- **Published:** 2025-05-25

"Dynamic Optimization and Safety Indicator Injection for Jailbreaking Text-to-Image Models with Multimodal Safety Filters" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Text-to-image (T2I) models can generate not-safe-for-work (NSFW) content, motivating multi-stage safety pipelines with both text and image filters.

Newer LLM-based filters detect latent intent beyond keywords, making token-level perturbation attacks unreliable.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 108. MuLan: Multimodal-LLM Agent for Progressive and Interactive Multi-Object Diffusion

- **Link:** [https://arxiv.org/abs/2402.12741v2](https://arxiv.org/abs/2402.12741v2)
- **Published:** 2024-02-20

"MuLan: Multimodal-LLM Agent for Progressive and Interactive Multi-Object Diffusion" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Existing text-to-image models still struggle to generate images of multiple objects, especially in handling their spatial positions, relative sizes, overlapping, and attribute bindings.

To efficiently address these challenges, we develop a training-free Multimodal-LLM agent (MuLan), as a human painter, that can progressively generate multi-object with intricate planning and feedback control.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 109. Visual Autoregressive Modelling for Monocular Depth Estimation

- **Link:** [https://arxiv.org/abs/2512.22653v1](https://arxiv.org/abs/2512.22653v1)
- **Published:** 2025-12-27

"Visual Autoregressive Modelling for Monocular Depth Estimation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

We propose a monocular depth estimation method based on visual autoregressive (VAR) priors, offering an alternative to diffusion-based approaches.

Our method adapts a large-scale text-to-image VAR model and introduces a scale-wise conditional upsampling mechanism with classifier-free guidance.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 110. StrandDesigner: Towards Practical Strand Generation with Sketch Guidance

- **Link:** [https://arxiv.org/abs/2508.01650v1](https://arxiv.org/abs/2508.01650v1)
- **Published:** 2025-08-03

"StrandDesigner: Towards Practical Strand Generation with Sketch Guidance" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Realistic hair strand generation is crucial for applications like computer graphics and virtual reality.

While diffusion models can generate hairstyles from text or images, these inputs lack precision and user-friendliness.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 111. MMFace-DiT: A Dual-Stream Diffusion Transformer for High-Fidelity Multimodal Face Generation

- **Link:** [https://arxiv.org/abs/2603.29029v1](https://arxiv.org/abs/2603.29029v1)
- **Published:** 2026-03-30

"MMFace-DiT: A Dual-Stream Diffusion Transformer for High-Fidelity Multimodal Face Generation" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Recent multimodal face generation models address the spatial control limitations of text-to-image diffusion models by augmenting text-based conditioning with spatial priors such as segmentation masks, sketches, or edge maps.

This multimodal fusion enables controllable synthesis aligned with both high-level semantic intent and low-level structural layout.

Keep it as background on modern generation/evaluation; use only if its data or metrics inform caption-length decisions.


### 112. AccelAes: Accelerating Diffusion Transformers for Training-Free Aesthetic-Enhanced Image Generation

- **Link:** [https://arxiv.org/abs/2603.12575v2](https://arxiv.org/abs/2603.12575v2)
- **Published:** 2026-03-13

"AccelAes: Accelerating Diffusion Transformers for Training-Free Aesthetic-Enhanced Image Generation" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Diffusion Transformers (DiTs) are a dominant backbone for high-fidelity text-to-image generation due to strong scalability and alignment at high resolutions.

However, quadratic self-attention over dense spatial tokens leads to high inference latency and limits deployment.

Keep it as background on modern generation/evaluation; use only if its data or metrics inform caption-length decisions.


### 113. H-Adapter: Pose-Robust Hairstyle Transfer via Attention-Derived, Source-Aligned Hair Masks

- **Link:** [https://arxiv.org/abs/2606.25578v2](https://arxiv.org/abs/2606.25578v2)
- **Published:** 2026-06-24

"H-Adapter: Pose-Robust Hairstyle Transfer via Attention-Derived, Source-Aligned Hair Masks" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Hairstyle transfer has practical applications such as virtual try-on, yet remains challenging when the source and reference exhibit large head-pose discrepancies.

We propose H-Adapter, which improves pose robustness by training with a region-specific loss that disentangles hair and non-hair objectives and thereby induces spatially disentangled cross-attention, from which a source-aligned hair edit mask is derived to guide diffusion-based inpainting.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 114. Mural: Transferring LLM knowledge to image generation via Mixture-of-Transformers

- **Link:** [https://arxiv.org/abs/2606.29013v1](https://arxiv.org/abs/2606.29013v1)
- **Published:** 2026-06-27

"Mural: Transferring LLM knowledge to image generation via Mixture-of-Transformers" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Leveraging capabilities of large language models (LLMs) in text-to-image (T2I) synthesis is an important research direction.

In this work we investigate whether the knowledge of a frozen LLM can be effectively utilized in T2I generation when trained exclusively on standard text-image pairs.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 115. ERNIE-Image Technical Report

- **Link:** [https://arxiv.org/abs/2605.25347v1](https://arxiv.org/abs/2605.25347v1)
- **Published:** 2026-05-25

"ERNIE-Image Technical Report" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

We introduce ERNIE-Image, an open-source text-to-image generation model built upon an 8B single-stream DiT architecture.

ERNIE-Image aims to bridge the gap between current open-source models and leading closed-source systems through more effective mining of large-scale pre-training data and improved supervision quality throughout training.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 116. UniNDM: A Unified Noise-driven Detection and Mitigation Framework Against Sexual Content in Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2607.16828v1](https://arxiv.org/abs/2607.16828v1)
- **Published:** 2026-07-18

"UniNDM: A Unified Noise-driven Detection and Mitigation Framework Against Sexual Content in Text-to-Image Generation" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Despite the impressive generative capabilities of text-to-image diffusion models, they remain vulnerable to implicit sexual prompts, where subtle cues disguised as benign terms or adversarial tokens unexpectedly generate the inappropriate content due to model biases or latent correlations in training data.

Existing safety mechanisms face fundamental limitations: detection methods primarily identify explicit content and fail to capture implicit malicious intent, while mitigation approaches rely on static negative prompts inadequate for diverse implicit scenarios.

Keep it as background on modern generation/evaluation; use only if its data or metrics inform caption-length decisions.


### 117. What Concepts Lie Within? Detecting and Suppressing Risky Content in Diffusion Transformers

- **Link:** [https://arxiv.org/abs/2605.10180v1](https://arxiv.org/abs/2605.10180v1)
- **Published:** 2026-05-11

"What Concepts Lie Within? Detecting and Suppressing Risky Content in Diffusion Transformers" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

The rise of text-to-image (T2I) models has increasingly raised concerns regarding the generation of risky content, such as sexual, violent, and copyright-protected images, highlighting the need for effective safeguards within the models themselves.

Although existing methods have been proposed to eliminate risky concepts from T2I models, they are primarily developed for earlier U-Net architectures, leaving the state-of-the-art Diffusion-Transformer-based T2I models inadequately protected.

Keep it as background on modern generation/evaluation; use only if its data or metrics inform caption-length decisions.


### 118. Reflective Flow Sampling Enhancement

- **Link:** [https://arxiv.org/abs/2603.06165v2](https://arxiv.org/abs/2603.06165v2)
- **Published:** 2026-03-06

"Reflective Flow Sampling Enhancement" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

The growing demand for text-to-image generation has led to rapid advances in generative modeling.

Recently, text-to-image diffusion models trained with flow matching algorithms, such as FLUX, have achieved remarkable progress and emerged as strong alternatives to conventional diffusion models.

Keep it as background on modern generation/evaluation; use only if its data or metrics inform caption-length decisions.


### 119. D-OPSD: On-Policy Self-Distillation for Continuously Tuning Step-Distilled Diffusion Models

- **Link:** [https://arxiv.org/abs/2605.05204v3](https://arxiv.org/abs/2605.05204v3)
- **Published:** 2026-05-06

"D-OPSD: On-Policy Self-Distillation for Continuously Tuning Step-Distilled Diffusion Models" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

The landscape of high-performance image generation models is currently shifting from the inefficient multi-step ones to the efficient few-step counterparts (e.g, Z-Image-Turbo and FLUX.2-klein).

However, these models present significant challenges for direct continuous supervised fine-tuning.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 120. Qwen-Image-Bench: From Generation to Creation in Text-to-Image Evaluation

- **Link:** [https://arxiv.org/abs/2605.28091v2](https://arxiv.org/abs/2605.28091v2)
- **Published:** 2026-05-27

"Qwen-Image-Bench: From Generation to Creation in Text-to-Image Evaluation" (2026) introduces or expands evaluation for text-conditioned image generation, often under long or compositional prompts.

Text-to-Image generation has evolved from basic image synthesis into a frequently used core capability in professional creative workflows, where simple text-image alignment can no longer satisfy users' pressing demands for faithful real-world reconstruction and genuine creative expression.

Existing benchmarks, however, remain anchored in these foundational criteria and do not yet capture the nuanced capabilities that matter in authentic artistic practice, making it difficult to reliably distinguish state-of-the-art T2I models.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 121. LADR: Locality-Aware Dynamic Rescue for Efficient Text-to-Image Generation with Diffusion Large Language Models

- **Link:** [https://arxiv.org/abs/2603.13450v2](https://arxiv.org/abs/2603.13450v2)
- **Published:** 2026-03-13

"LADR: Locality-Aware Dynamic Rescue for Efficient Text-to-Image Generation with Diffusion Large Language Models" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Discrete Diffusion Language Models have emerged as a compelling paradigm for unified multimodal generation, yet their deployment is hindered by high inference latency arising from iterative decoding.

Existing acceleration strategies often require expensive re-training or fail to leverage the 2D spatial redundancy inherent in visual data.

Keep it as background on modern generation/evaluation; use only if its data or metrics inform caption-length decisions.


### 122. FAGER: Factually Grounded Evaluation and Refinement of Text-to-Image Models

- **Link:** [https://arxiv.org/abs/2605.19111v1](https://arxiv.org/abs/2605.19111v1)
- **Published:** 2026-05-18

"FAGER: Factually Grounded Evaluation and Refinement of Text-to-Image Models" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Existing text-to-image (T2I) evaluation metrics mainly assess whether generated images align with information explicitly stated in the prompt, but often fail to capture factual requirements that are implicit, externally grounded, or identity-defining.

As a result, they are not well suited for evaluating factual correctness in prompts involving scientific knowledge, historical facts, products, or culture-specific concepts.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 123. PRISM: Prompt Refinement via Image-grounded Self-rewarding Mechanism for Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2607.24353v1](https://arxiv.org/abs/2607.24353v1)
- **Published:** 2026-07-27

"PRISM: Prompt Refinement via Image-grounded Self-rewarding Mechanism for Text-to-Image Generation" (2026) studies prompt rewriting, optimization, or prompt-side control for image generators.

Text-to-image generation models can synthesize high-quality images from natural language descriptions, but their performance remains highly sensitive to prompt formulation.

Existing prompt optimization methods mainly rely on text-side rewriting, prompt expansion, or external reward signals, offering limited image-grounded diagnosis and weak support for learning reusable optimisation policies.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 124. FlowInOne:Unifying Multimodal Generation as Image-in, Image-out Flow Matching

- **Link:** [https://arxiv.org/abs/2604.06757v2](https://arxiv.org/abs/2604.06757v2)
- **Published:** 2026-04-08

"FlowInOne:Unifying Multimodal Generation as Image-in, Image-out Flow Matching" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Multimodal generation has long been dominated by text-driven pipelines where language dictates vision but cannot reason or create within it.

We challenge this paradigm by asking whether all modalities, including textual descriptions, spatial layouts, and editing instructions, can be unified into a single visual representation.

Keep it as background on modern generation/evaluation; use only if its data or metrics inform caption-length decisions.


### 125. PG-MAP: Joint MAP Optimization for Inference-Time Alignment of Diffusion and Flow-Matching Models

- **Link:** [https://arxiv.org/abs/2606.22958v1](https://arxiv.org/abs/2606.22958v1)
- **Published:** 2026-06-22

"PG-MAP: Joint MAP Optimization for Inference-Time Alignment of Diffusion and Flow-Matching Models" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Inference-time alignment of pretrained text-to-image models is typically performed along a single control axis, such as classifier-free guidance, attention editing, or reward-based latent perturbations.

This limitation prevents modeling joint dependencies between conditioning and latent variables and hinders transfer across generative transports.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 126. FreeText: Training-Free Text Rendering in Diffusion Transformers via Attention Localization and Spectral Glyph Injection

- **Link:** [https://arxiv.org/abs/2601.00535v1](https://arxiv.org/abs/2601.00535v1)
- **Published:** 2026-01-02

"FreeText: Training-Free Text Rendering in Diffusion Transformers via Attention Localization and Spectral Glyph Injection" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Large-scale text-to-image (T2I) diffusion models excel at open-domain synthesis but still struggle with precise text rendering, especially for multi-line layouts, dense typography, and long-tailed scripts such as Chinese.

Prior solutions typically require costly retraining or rigid external layout constraints, which can degrade aesthetics and limit flexibility.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 127. Unified Safe In-context Image Generation in Multimodal Diffusion Transformers via Restricting Unsafe Information Flows

- **Link:** [https://arxiv.org/abs/2606.06875v1](https://arxiv.org/abs/2606.06875v1)
- **Published:** 2026-06-05

"Unified Safe In-context Image Generation in Multimodal Diffusion Transformers via Restricting Unsafe Information Flows" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Diffusion transformers (DiTs) equipped with multimodal attention (MM-Attn) have become a dominant paradigm for image generation.

However, preventing the generation of harmful content remains a critical challenge, particularly in image-to-image (I2I) editing tasks.

Keep it as background on modern generation/evaluation; use only if its data or metrics inform caption-length decisions.


### 128. SANA-Streaming: Real-time Streaming Video Editing with Hybrid Diffusion Transformer

- **Link:** [https://arxiv.org/abs/2605.30409v1](https://arxiv.org/abs/2605.30409v1)
- **Published:** 2026-05-28

"SANA-Streaming: Real-time Streaming Video Editing with Hybrid Diffusion Transformer" (2026) is a modern system/report in the LLM/VLM-conditioned image generation line.

Real-time streaming video-to-video editing (V2V) is critical for interactive applications such as live broadcasting and gaming, yet it remains a formidable challenge due to the stringent requirements for temporal consistency and inference throughput.

In this paper, we present SANA-Streaming, a system-algorithm co-designed framework for high-resolution, real-time streaming video editing on consumer GPUs, with the following three core designs: (1) Hybrid Diffusion Transformer architecture introduces softmax attention in part of the blocks to improve local modeling capabilities while preserving...

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 129. Flash-BoN: Instant Drafts for Inference-Time Scaling in Diffusion Models

- **Link:** [https://arxiv.org/abs/2607.04461v1](https://arxiv.org/abs/2607.04461v1)
- **Published:** 2026-07-05

"Flash-BoN: Instant Drafts for Inference-Time Scaling in Diffusion Models" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Inference-time scaling for text-to-image generation has progressed from simple Best-of-$N$ (BoN) sampling to guided search methods that verify and steer candidate trajectories at intermediate denoising steps.

These approaches focus on when and how often to verify during denoising but largely treat the cost of generation itself as fixed.

Keep it as background on modern generation/evaluation; use only if its data or metrics inform caption-length decisions.


### 130. One Image is All You Need: Agentic One-Shot Image Generation via Text-Based World Models for Long-Tail Spatial Perception

- **Link:** [https://arxiv.org/abs/2606.20764v1](https://arxiv.org/abs/2606.20764v1)
- **Published:** 2026-06-18

"One Image is All You Need: Agentic One-Shot Image Generation via Text-Based World Models for Long-Tail Spatial Perception" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Reliable spatial decision automation, such as autonomous driving and maritime surveillance, critically depends on robust visual perception.

However, real-world spatiotemporal data exhibits severe heterogeneity, often manifesting as extreme long-tail distributions for safety-critical scenarios.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 131. An Empirical Study and Analysis of Text-to-Image Generation Using Large Language Model-Powered Textual Representation

- **Link:** [https://arxiv.org/abs/2405.12914v2](https://arxiv.org/abs/2405.12914v2)
- **Published:** 2024-05-21

"An Empirical Study and Analysis of Text-to-Image Generation Using Large Language Model-Powered Textual Representation" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

One critical prerequisite for faithful text-to-image generation is the accurate understanding of text inputs.

Existing methods leverage the text encoder of the CLIP model to represent input prompts.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 132. VisionFoundry: Teaching VLMs Visual Perception with Synthetic Images

- **Link:** [https://arxiv.org/abs/2604.09531v1](https://arxiv.org/abs/2604.09531v1)
- **Published:** 2026-04-10

"VisionFoundry: Teaching VLMs Visual Perception with Synthetic Images" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Vision-language models (VLMs) still struggle with visual perception tasks such as spatial understanding and viewpoint recognition.

One plausible contributing factor is that natural image datasets provide limited supervision for low-level visual skills.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 133. Visual Puns from Idioms: An Iterative LLM-T2IM-MLLM Framework

- **Link:** [https://arxiv.org/abs/2511.22943v1](https://arxiv.org/abs/2511.22943v1)
- **Published:** 2025-11-28

"Visual Puns from Idioms: An Iterative LLM-T2IM-MLLM Framework" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

We study idiom-based visual puns--images that align an idiom's literal and figurative meanings--and present an iterative framework that coordinates a large language model (LLM), a text-to-image model (T2IM), and a multimodal LLM (MLLM) for automatic generation and evaluation.

Given an idiom, the system iteratively (i) generates detailed visual prompts, (ii) synthesizes an image, (iii) infers the idiom from the image, and (iv) refines the prompt until recognition succeeds or a step limit is reached.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 134. Qwen-Image-Flash: Beyond Objective Design

- **Link:** [https://arxiv.org/abs/2606.03746v2](https://arxiv.org/abs/2606.03746v2)
- **Published:** 2026-06-02

"Qwen-Image-Flash: Beyond Objective Design" (2026) is a modern system/report in the LLM/VLM-conditioned image generation line.

Few-step distillation has become an effective strategy for accelerating advanced visual generative models, yet prior work has largely focused on distillation objectives.

In this work, we revisit few-step distillation from a complementary perspective, focusing on the training recipe that critically shapes student performance.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 135. MemoGen: Can Past Experience Improve Future Text-to-Image Generation?

- **Link:** [https://arxiv.org/abs/2606.03243v1](https://arxiv.org/abs/2606.03243v1)
- **Published:** 2026-06-02

"MemoGen: Can Past Experience Improve Future Text-to-Image Generation?" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Modern text-to-image models have achieved strong visual synthesis, yet remain unreliable when prompts require implicit visual constraints, relational reasoning, or external knowledge.

Existing retrieval-augmented and agentic generation methods mitigate this issue by acquiring external knowledge, references, or refined prompts for the current request, yet they typically treat each generation as an isolated episode and do not systematically preserve past successes or failures for future use.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 136. Qwen-Image-Agent: Bridging the Context Gap in Real-World Image Generation

- **Link:** [https://arxiv.org/abs/2606.26907v2](https://arxiv.org/abs/2606.26907v2)
- **Published:** 2026-06-25

"Qwen-Image-Agent: Bridging the Context Gap in Real-World Image Generation" (2026) is a modern system/report in the LLM/VLM-conditioned image generation line.

While text-to-image (T2I) models have achieved remarkable progress, they struggle with real-world requests that are often underspecified, implicit, or dependent on up-to-date knowledge.

We identify this challenge as the Context Gap: the mismatch between the user context and the sufficient generation context for T2I models.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 137. Benchmarking Multimodal Large Language Models for Missing Modality Completion in Product Catalogues

- **Link:** [https://arxiv.org/abs/2601.19750v2](https://arxiv.org/abs/2601.19750v2)
- **Published:** 2026-01-27

"Benchmarking Multimodal Large Language Models for Missing Modality Completion in Product Catalogues" (2026) introduces or expands evaluation for text-conditioned image generation, often under long or compositional prompts.

Missing-modality information on e-commerce platforms, such as absent product images or textual descriptions, often arises from annotation errors or incomplete metadata, impairing both product presentation and downstream applications such as recommendation systems.

Motivated by the multimodal generative capabilities of recent Multimodal Large Language Models (MLLMs), this work investigates a fundamental yet underexplored question: can MLLMs generate missing modalities for products in e-commerce scenarios?.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 138. Red-Teaming Text-to-Image Models via In-Context Experience Replay and Semantic-Preserving Prompt Rewriting

- **Link:** [https://arxiv.org/abs/2411.16769v3](https://arxiv.org/abs/2411.16769v3)
- **Published:** 2024-11-25

"Red-Teaming Text-to-Image Models via In-Context Experience Replay and Semantic-Preserving Prompt Rewriting" (2024) studies prompt rewriting, optimization, or prompt-side control for image generators.

Understanding the capabilities of text-to-image (T2I) models in harmful content generation is essential to safety and compliance.

However, human red-teaming is costly and inconsistent, driving the need for automatic tools that simulate realistic misuse attempts.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 139. Edify Image: High-Quality Image Generation with Pixel Space Laplacian Diffusion Models

- **Link:** [https://arxiv.org/abs/2411.07126v1](https://arxiv.org/abs/2411.07126v1)
- **Published:** 2024-11-11

"Edify Image: High-Quality Image Generation with Pixel Space Laplacian Diffusion Models" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

We introduce Edify Image, a family of diffusion models capable of generating photorealistic image content with pixel-perfect accuracy.

Edify Image utilizes cascaded pixel-space diffusion models trained using a novel Laplacian diffusion process, in which image signals at different frequency bands are attenuated at varying rates.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 140. Boogu-Image-0.1: Boosting Open Agentic Multimodal Generation via Understanding under a Minimal Budget

- **Link:** [https://arxiv.org/abs/2607.13125v2](https://arxiv.org/abs/2607.13125v2)
- **Published:** 2026-07-14

"Boogu-Image-0.1: Boosting Open Agentic Multimodal Generation via Understanding under a Minimal Budget" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

We introduce Boogu-Image-0.1, an open-source unified multimodal understanding and generation model family, comprising Base, Turbo, Edit, and Edit-Turbo variants.

It delivers competitive performance in high-quality text-to-image generation, fast inference, instruction-based editing, and bilingual (Chinese-English) text rendering.

Keep it as background on modern generation/evaluation; use only if its data or metrics inform caption-length decisions.


### 141. Spectral Image Tokenizer

- **Link:** [https://arxiv.org/abs/2412.09607v2](https://arxiv.org/abs/2412.09607v2)
- **Published:** 2024-12-12

"Spectral Image Tokenizer" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Image tokenizers map images to sequences of discrete tokens, and are a crucial component of autoregressive transformer-based image generation.

The tokens are typically associated with spatial locations in the input image, arranged in raster scan order, which is not ideal for autoregressive modeling.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 142. Scaling Diffusion Transformers Efficiently via $μ$P

- **Link:** [https://arxiv.org/abs/2505.15270v3](https://arxiv.org/abs/2505.15270v3)
- **Published:** 2025-05-21

"Scaling Diffusion Transformers Efficiently via $μ$P" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Diffusion Transformers have emerged as the foundation for vision generative models, but their scalability is limited by the high cost of hyperparameter (HP) tuning at large scales.

Recently, Maximal Update Parametrization ($μ$P) was proposed for vanilla Transformers, which enables stable HP transfer from small to large language models, and dramatically reduces tuning costs.

Keep it as background on modern generation/evaluation; use only if its data or metrics inform caption-length decisions.


### 143. FullFlow: Upgrading Text-to-Image Flow Matching Models for Bidirectional Vision--Language Generation

- **Link:** [https://arxiv.org/abs/2605.20316v1](https://arxiv.org/abs/2605.20316v1)
- **Published:** 2026-05-19

"FullFlow: Upgrading Text-to-Image Flow Matching Models for Bidirectional Vision--Language Generation" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Modern text-to-image diffusion models encode rich visual priors, but expose them only through one-way text-conditioned generation.

Existing unified vision--language models derived from them recover bidirectional capability through large-scale joint pretraining or substantial retraining of the text pathway, discarding the strong image prior the text-to-image backbone already encodes.

Keep it as background on modern generation/evaluation; use only if its data or metrics inform caption-length decisions.


### 144. Stable Velocity: A Variance Perspective on Flow Matching

- **Link:** [https://arxiv.org/abs/2602.05435v2](https://arxiv.org/abs/2602.05435v2)
- **Published:** 2026-02-05

"Stable Velocity: A Variance Perspective on Flow Matching" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

While flow matching is elegant, its reliance on single-sample conditional velocities leads to high-variance training targets that destabilize optimization and slow convergence.

By explicitly characterizing this variance, we identify 1) a high-variance regime near the prior, where optimization is challenging, and 2) a low-variance regime near the data distribution, where conditional and marginal velocities nearly coincide.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 145. Modular Energy Steering for Safe Text-to-Image Generation with Foundation Models

- **Link:** [https://arxiv.org/abs/2604.02265v1](https://arxiv.org/abs/2604.02265v1)
- **Published:** 2026-04-02

"Modular Energy Steering for Safe Text-to-Image Generation with Foundation Models" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Controlling the behavior of text-to-image generative models is critical for safe and practical deployment.

Existing safety approaches typically rely on model fine-tuning or curated datasets, which can degrade generation quality or limit scalability.

Keep it as background on modern generation/evaluation; use only if its data or metrics inform caption-length decisions.


### 146. SafeRoPE: Risk-specific Head-wise Embedding Rotation for Safe Generation in Rectified Flow Transformers

- **Link:** [https://arxiv.org/abs/2604.01826v1](https://arxiv.org/abs/2604.01826v1)
- **Published:** 2026-04-02

"SafeRoPE: Risk-specific Head-wise Embedding Rotation for Safe Generation in Rectified Flow Transformers" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Recent Text-to-Image (T2I) models based on rectified-flow transformers (e.g., SD3, FLUX) achieve high generative fidelity but remain vulnerable to unsafe semantics, especially when triggered by multi-token interactions.

Existing mitigation methods largely rely on fine-tuning or attention modulation for concept unlearning; however, their expensive computational overhead and design tailored to U-Net-based denoisers hinder direct adaptation to transformer-based diffusion models (e.g., MMDiT).

Keep it as background on modern generation/evaluation; use only if its data or metrics inform caption-length decisions.


### 147. MammothModa2: A Unified AR-Diffusion Framework for Multimodal Understanding and Generation

- **Link:** [https://arxiv.org/abs/2511.18262v1](https://arxiv.org/abs/2511.18262v1)
- **Published:** 2025-11-23

"MammothModa2: A Unified AR-Diffusion Framework for Multimodal Understanding and Generation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Unified multimodal models aim to integrate understanding and generation within a single framework, yet bridging the gap between discrete semantic reasoning and high-fidelity visual synthesis remains challenging.

We present MammothModa2 (Mammoth2), a unified autoregressive-diffusion (AR-Diffusion) framework designed to effectively couple autoregressive semantic planning with diffusion-based generation.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 148. Advances in GRPO for Generation Models: A Survey

- **Link:** [https://arxiv.org/abs/2603.06623v1](https://arxiv.org/abs/2603.06623v1)
- **Published:** 2026-02-21

"Advances in GRPO for Generation Models: A Survey" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Large-scale flow matching models have achieved strong performance across generative tasks such as text-to-image, video, 3D, and speech synthesis.

However, aligning their outputs with human preferences and task-specific objectives remains challenging.

Keep it as background on modern generation/evaluation; use only if its data or metrics inform caption-length decisions.


### 149. SANA-Video 2.0: Hybrid Linear Attention with Attention Residuals for Efficient Video Generation

- **Link:** [https://arxiv.org/abs/2607.21553v1](https://arxiv.org/abs/2607.21553v1)
- **Published:** 2026-07-23

"SANA-Video 2.0: Hybrid Linear Attention with Attention Residuals for Efficient Video Generation" (2026) is a modern system/report in the LLM/VLM-conditioned image generation line.

We introduce SANA-Video 2.0, a hybrid video diffusion transformer instantiated at 5B and 14B scales under a unified architecture.

Designed to generate high-quality video up to 720p on a single GPU, SANA-Video 2.0 matches full-softmax video DiTs in quality while retaining the favorable long-sequence scaling of linear attention.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 150. RubiCap: Rubric-Guided Reinforcement Learning for Dense Image Captioning

- **Link:** [https://arxiv.org/abs/2603.09160v1](https://arxiv.org/abs/2603.09160v1)
- **Published:** 2026-03-10

"RubiCap: Rubric-Guided Reinforcement Learning for Dense Image Captioning" (2026) focuses on captioning/recaptioning data that feeds text-to-image training.

Dense image captioning is critical for cross-modal alignment in vision-language pretraining and text-to-image generation, but scaling expert-quality annotations is prohibitively expensive.

While synthetic captioning via strong vision-language models (VLMs) is a practical alternative, supervised distillation often yields limited output diversity and weak generalization.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


---

## Fixed vs variable — final synthesis

- **Fixed long + PE** — current frontier default (Qwen-Image, FLUX.2, Seedream, i1, DALL·E-3 pattern).
- **Variable wide-band** — robust without relying on PE (HunyuanImage 3.0; How-to-Train randomization; RECAP mixes).
- **Fixed short** — obsolete as the only train mode for strong models.
- **~1000-token structured** — when controllability is the product goal and fusion cost is solved (FIBO).

For **Qwen-VLM / similar**: start at **`L≈512`**, train dense VLM captions (long-biased or 30–1000-word band), ship **PE ON** targeting train caption law with faithfulness rewards, validate on short and long benchmarks with an explicit length diagnostic.

---

## Why one length beats another — FAQ

**Universal optimum?** No — relative to deployment measure, capacity, and utility.

**Why long helps?** Higher mutual information about attributes/relations omitted by short alt-text.

**Why long hurts?** Covariate shift vs short users; attention dilution; captioner hallucination; extrapolation past train support.

**Fixed or variable?** Variable (or long+PE, which makes *user-facing* length variable) under heterogeneous traffic.

**Engineering only?** No — covariate shift + rate–distortion + constrained risk give a general language; closed-form `L*` still needs empirical channel estimates.

---

## Related files

- Earlier CLIP/T5-inclusive deep dive: `report.md`
- Structured JSON notes: `research/prompt-length/results/*.json`
