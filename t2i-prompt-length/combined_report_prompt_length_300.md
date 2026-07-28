# Combined Report: Prompt Length, Variability, and Re-prompting for Modern Text-to-Image

*Combines the CLIP-to-modern deep dive (`report.md`) with the LLM/VLM literature review, expanded to **300 papers**. Focus: what to read, what the answers are, what problems remain, and where the field is going — especially for Qwen-VLM-class / similar stacks (not CLIP/T5 as design targets).*

*Catalog size: 300 · Length-focused subset: 122 · Generated: 2026-07-28*

---

## 0. The questions this report answers

1. **At what prompt/caption length should a modern T2I model be trained?**
2. **At what length should inference run?** Fixed or variable?
3. **If there is a re-prompt / PE / writer model, what length should its output have (train & infer)?** How to train that writer correctly?
4. **Should training length be variable?** What kind of variability? Or teach length-robustness natively without a separate rewriter?
5. **Why is one regime better than another** — engineering lore vs a more fundamental account?
6. **Where is the area going?**

---

## 1. What you should read (prioritized)

### Tier A — read these to get the answers

If you only read one shelf, read this. Each item directly constrains length, variability, or PE design for modern LLM/VLM-conditioned generators.

#### A1. i1: A Simple and Fully Open Recipe for Strong Text-to-Image Models

- **Link:** [https://arxiv.org/abs/2606.11289v1](https://arxiv.org/abs/2606.11289v1)
- **Date:** 2026-06-09
- **Tags:** numeric token budget, benchmark/eval

i1 uses a modern encoder truncated to 256 tokens with long synthetic captions only.

Long-caption training scores 0.17 on short GenEval, 0.49 with 12× repetition, 0.73 with LLM rewrite.

Recommends train long and lengthen inference to match training, not train short to match users.

The length-alignment diagnostic remains the right experimental template for Qwen-VLM stacks.


#### A2. DetailMaster: Can Your Text-to-Image Model Handle Long Prompts?

- **Link:** [https://arxiv.org/abs/2505.16915v3](https://arxiv.org/abs/2505.16915v3)
- **Date:** 2025-05-22
- **Tags:** long/dense preferred, benchmark/eval

DetailMaster averages ~284.89 tokens with fine-grained attribute/relation metrics.

Dense long training matters more than merely raising token capacity; accuracy falls as length grows.

Even FLUX/SD3-class models plateau near ~50% on hard long-prompt attributes.

Use to stress-test professional long prompts, not only short GenEval-like sets.


#### A3. How to Train your Text-to-Image Model: Evaluating Design Choices for Synthetic Training Captions

- **Link:** [https://arxiv.org/abs/2506.16679v1](https://arxiv.org/abs/2506.16679v1)
- **Date:** 2025-06-20
- **Tags:** variable/mixed length, benchmark/eval

Fixed long synthetic captions trade aesthetics/diversity against alignment on SD-class models.

Randomizing caption length per image removes the trade-off and yields best overall PickScores.

Mixture/coverage principle transfers beyond CLIP budgets: cover length modes you will serve.

Main citation for variable train length when you may not ship a rewriter.


#### A4. HunyuanImage 3.0 Technical Report

- **Link:** [https://arxiv.org/abs/2509.23951v3](https://arxiv.org/abs/2509.23951v3)
- **Date:** 2025-09-28
- **Tags:** benchmark/eval

HunyuanImage 3.0 samples bilingual captions from about 30 to 1,000 words via Compositional Caption Synthesis.

Train length and pattern are deliberately variable across a wide band.

Inference can use CoT think_recaption/rewrite to map short users into that band.

Clearest published alternative to fixed-long-only training for LLM/VLM-era models.


#### A5. Qwen-Image-2.0 Technical Report

- **Link:** [https://arxiv.org/abs/2605.10730v1](https://arxiv.org/abs/2605.10730v1)
- **Date:** 2026-05-11
- **Tags:** LLM/VLM encoder, benchmark/eval

Qwen-Image-2.0 is a frontier open image system built on a Qwen-family VLM/LLM text pathway rather than CLIP or classic T5.

It documents large prompt budgets (hundreds to ~1.3k tokens by API/version) with hard truncation past the limit.

Prompt extension is first-class and default-on, so inference text is lengthened toward the training caption regime.

Primary reference for Qwen-VLM-class encoder max length, PE max_new_tokens, and default rewrite policy.


#### A6. Seedream 4.0: Toward Next-generation Multimodal Image Generation

- **Link:** [https://arxiv.org/abs/2509.20427v3](https://arxiv.org/abs/2509.20427v3)
- **Date:** 2025-09-24
- **Tags:** LLM/VLM encoder, benchmark/eval

Seedream 4.0 uses a VLM prompt enhancer with task routing and adaptive thinking budgets.

Rewrite length becomes conditional on task difficulty rather than a fixed expansion factor.

Shows modern stacks couple a strong multimodal language model to the generator and control how much text it emits.

Important for adaptive / native PE rather than static upsampling.


#### A7. PromptEnhancer: A Simple Approach to Enhance Text-to-Image Models via Chain-of-Thought Prompt Rewriting

- **Link:** [https://arxiv.org/abs/2509.04545v5](https://arxiv.org/abs/2509.04545v5)
- **Date:** 2025-09-04
- **Tags:** re-prompt/recaption, benchmark/eval

PromptEnhancer is a model-agnostic CoT rewriter trained with fine-grained RL against AlignEvaluator.

Rewriting should change content to fix T2I failures, not add stylistic verbosity.

PE length is a side-effect of needed content, not the optimization target.

Template for PE rewards when avoiding reward-hacked overlong prompts.


#### A8. Generating an Image From 1,000 Words: Enhancing Text-to-Image With Structured Captions

- **Link:** [https://arxiv.org/abs/2511.06876v1](https://arxiv.org/abs/2511.06876v1)
- **Date:** 2025-11-10
- **Tags:** long/dense preferred, LLM/VLM encoder, benchmark/eval

FIBO trains on long structured JSON-schema captions at ~thousand-token scale (mean ~1160).

DimFusion fuses intermediate LLM states without growing token count, controlling compute.

Long structured captions converge faster and improve controllability vs short captions.

Extreme fixed-long+structure pole for VLM/LLM-conditioned generators.


#### A9. Improving Text-to-Image Generation with Input-Side Inference-Time Scaling

- **Link:** [https://arxiv.org/abs/2510.12041v2](https://arxiv.org/abs/2510.12041v2)
- **Date:** 2025-10-14
- **Tags:** re-prompt/recaption, LLM/VLM encoder, benchmark/eval

Input-side inference-time scaling trains iterative rewriters (e.g. DPO) without backbone SFT.

Gains come from closing train/user text distribution gap; rewriters transfer across generators.

Rewrite length judged by distribution matching, not a universal token target.

Supports PE as a portable layer in front of Qwen-VLM generators.


#### A10. TIPO: Text to Image with Text Presampling for Prompt Optimization

- **Link:** [https://arxiv.org/abs/2411.08127v6](https://arxiv.org/abs/2411.08127v6)
- **Date:** 2024-11-12
- **Tags:** LLM/VLM encoder

TIPO expands user prompts toward the training caption distribution rather than unconstrained rewrite.

Reports human preference wins and runtime benefits from distribution matching.

Frames PE as transport into μ_train, not maximal verbosity.

Core conceptual paper for correct re-prompt objectives.


#### A11. Seeing is Believing: Aligning Prompt Rewriting with Visual Anchors for Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2606.08492v2](https://arxiv.org/abs/2606.08492v2)
- **Date:** 2026-06-07
- **Tags:** re-prompt/recaption, LLM/VLM encoder

FaithRewriter shows text-only rewriters can hallucinate visually impossible details.

Anchors rewriting with an intermediate image for visual faithfulness.

Extra PE tokens are harmful if they invent unsupported content.

Long-rewrite policies need faithfulness objectives, not only length targets.


#### A12. Playground v3: Improving Text-to-Image Alignment with Deep-Fusion Large Language Models

- **Link:** [https://arxiv.org/abs/2409.10695v2](https://arxiv.org/abs/2409.10695v2)
- **Date:** 2024-09-16
- **Tags:** LLM/VLM encoder, benchmark/eval

Playground v3 deep-fuses Llama3-8B into the DiT, replacing CLIP/T5 dual towers.

Text conditioning is native LLM hidden states across layers.

Ties generation quality to richness of the text channel (CapsBench).

Early clear break toward LLM-centric conditioning.


#### A13. SANA: Efficient High-Resolution Image Synthesis with Linear Diffusion Transformers

- **Link:** [https://arxiv.org/abs/2410.10679](https://arxiv.org/abs/2410.10679)
- **Date:** 2024-10-01
- **Tags:** numeric token budget, LLM/VLM encoder

SANA uses decoder-only Gemma as text encoder with linear-attention DiT.

Pipelines often set max_sequence_length ~300; instruction templates consume budget.

Shows chat/system wrappers shrink usable user length.

Relevant for templated Qwen/Gemma encoders.


#### A14. What If We Recaption Billions of Web Images with LLaMA-3?

- **Link:** [https://arxiv.org/abs/2406.08478v2](https://arxiv.org/abs/2406.08478v2)
- **Date:** 2024-06-12
- **Tags:** re-prompt/recaption, LLM/VLM encoder

Recap-DataComp-1B uses LLaVA-LLaMA3 with max_new_tokens=128, mean length ~49 vs ~10 alt-text.

Concrete operating point for offline VLM recaption at web scale.

Downstream models train on mid-length dense text instead of raw alt-text.

Lower-bound modern recaption recipe before 512–1000 token regimes.


#### A15. LongT2IBench: A Benchmark for Evaluating Long Text-to-Image Generation with Graph-structured Annotations

- **Link:** [https://arxiv.org/abs/2512.09271v1](https://arxiv.org/abs/2512.09271v1)
- **Date:** 2025-12-10
- **Tags:** long/dense preferred, LLM/VLM encoder, benchmark/eval

LongT2IBench evaluates long T2I with graph-structured annotations and balanced word-count bins.

Enables measuring generators/evaluators as length grows.

Pair with DetailMaster when validating length policies.

Shows the field is instrumenting length as a first-class axis.


#### A16. Long-Text-to-Image Generation via Compositional Prompt Decomposition

- **Link:** [https://arxiv.org/abs/2604.18258v1](https://arxiv.org/abs/2604.18258v1)
- **Date:** 2026-04-20
- **Tags:** long/dense preferred, benchmark/eval

Compositional prompt decomposition studies extreme long-text T2I.

Reports segment methods trained mostly under ~300 degrade up to ~30% above ~500 tokens.

Train support in length must cover deployment support.

Caution against claiming arbitrary long-context without training mass there.


#### A17. Wan: Open and Advanced Large-Scale Video Generative Models

- **Link:** [https://arxiv.org/abs/2503.20314](https://arxiv.org/abs/2503.20314)
- **Date:** 2025-01-01
- **Tags:** hand-curated

Wan states the principle plainly: dense captions in training, LLM rewriting at inference to match that distribution.

Default-on prompt extend is recommended in tooling.

Same PE-length logic as modern T2I, validated in video.

Cite for cross-modality train/infer text alignment.


#### A18. A Picture is Worth a Thousand Words: Principled Recaptioning Improves Image Generation

- **Link:** [https://arxiv.org/abs/2310.16656v1](https://arxiv.org/abs/2310.16656v1)
- **Date:** 2023-10-25
- **Tags:** long/dense preferred, re-prompt/recaption, benchmark/eval

RECAP shows Short captions win FID, Long win semantics, 50/50 Mix wins overall under CLIP-77.

Captions over 77 tokens were dropped (<1%).

Early principled evidence for length mixing inside a hard budget.

Still generalizes as a mixture-design lesson for any encoder limit.


### Tier B — supporting classics and bridges

Still worth reading: LM conditioning vs CLIP, encoder budgets, long-prompt bridges, and failure modes that survive after leaving CLIP/T5.

#### B1. Improving Long-Text Alignment for Text-to-Image Diffusion Models

- **Link:** [https://arxiv.org/abs/2410.11817v2](https://arxiv.org/abs/2410.11817v2)
- **Date:** 2024-10-15
- **Tags:** numeric token budget

LongAlign uses segment-level encoding and preference optimization for long prompts on CLIP-limited models.

Extends past 77 by split–encode–concatenate with careful special-token handling.

Later work shows weak extrapolation beyond the training length band.

Historical bridge from CLIP limits to long-prompt methods; principle still generalizes.


#### B2. Photorealistic Text-to-Image Diffusion Models with Deep Language Understanding

- **Link:** [https://arxiv.org/abs/2205.11487](https://arxiv.org/abs/2205.11487)
- **Date:** 2025-01-01
- **Tags:** long/dense preferred, re-prompt/recaption, LLM/VLM encoder

Imagen showed frozen large LM text encoders (T5-XXL) beat CLIP on challenging compositional prompts.

Motivated the shift from contrastive text towers to language-model conditioning.

Later Imagen APIs document concrete token limits (e.g. 480).

Historical root of “use a strong language model as the text pathway.”


#### B3. Scaling Rectified Flow Transformers for High-Resolution Image Synthesis

- **Link:** [https://arxiv.org/abs/2403.03206](https://arxiv.org/abs/2403.03206)
- **Date:** 2024-03-05
- **Tags:** supporting

"Scaling Rectified Flow Transformers for High-Resolution Image Synthesis" (2024) is a supporting paper for text-to-image conditioning, evaluation, or long-prompt methods.

Diffusion models create data from noise by inverting the forward paths of data towards noise and have emerged as a powerful generative modeling technique for high-dimensional, perceptual data such as images and videos.

Rectified flow is a recent generative model formulation that connects data and noise in a straight line.

Read as background/bridge evidence when designing length and PE policy for LLM/VLM-era generators.


#### B4. PixArt-$α$: Fast Training of Diffusion Transformer for Photorealistic Text-to-Image Synthesis

- **Link:** [https://arxiv.org/abs/2310.00426](https://arxiv.org/abs/2310.00426)
- **Date:** 2023-09-30
- **Tags:** supporting

"PixArt-$α$: Fast Training of Diffusion Transformer for Photorealistic Text-to-Image Synthesis" (2023) is a supporting paper for text-to-image conditioning, evaluation, or long-prompt methods.

The most advanced text-to-image (T2I) models require significant training costs (e.g., millions of GPU hours), seriously hindering the fundamental innovation for the AIGC community while increasing CO2 emissions.

This paper introduces PIXART-$α$, a Transformer-based T2I diffusion model whose image generation quality is competitive with state-of-the-art image generators (e.g., Imagen, SDXL, and even Midjourney), reaching near-commercial application standards.

Read as background/bridge evidence when designing length and PE policy for LLM/VLM-era generators.


#### B5. PixArt-Σ: Weak-to-Strong Training of Diffusion Transformer for 4K Text-to-Image

- **Link:** [https://arxiv.org/abs/2403.04692v2](https://arxiv.org/abs/2403.04692v2)
- **Date:** 2024-03-07
- **Tags:** —

"PixArt-Σ: Weak-to-Strong Training of Diffusion Transformer for 4K Text-to-Image Generation" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

In this paper, we introduce PixArt-Σ, a Diffusion Transformer model~(DiT) capable of directly generating images at 4K resolution.

PixArt-Σrepresents a significant advancement over its predecessor, PixArt-α, offering images of markedly higher fidelity and improved alignment with text prompts.

Keep it as background on modern generation/evaluation; use only if its data or metrics inform caption-length decisions.


#### B6. Draw ALL Your Imagine: A Holistic Benchmark and Agent Framework for Complex Instruction-based Image Generation

- **Link:** [https://arxiv.org/abs/2505.24787](https://arxiv.org/abs/2505.24787)
- **Date:** 2025-05-30
- **Tags:** supporting

"Draw ALL Your Imagine: A Holistic Benchmark and Agent Framework for Complex Instruction-based Image Generation" (2025) is a supporting paper for text-to-image conditioning, evaluation, or long-prompt methods.

Recent advancements in text-to-image (T2I) generation have enabled models to produce high-quality images from textual descriptions.

However, these models often struggle with complex instructions involving multiple objects, attributes, and spatial relationships.

Read as background/bridge evidence when designing length and PE policy for LLM/VLM-era generators.


#### B7. STRICT: Stress Test of Rendering Images Containing Text

- **Link:** [https://arxiv.org/abs/2505.18985](https://arxiv.org/abs/2505.18985)
- **Date:** 2025-05-25
- **Tags:** supporting

"STRICT: Stress Test of Rendering Images Containing Text" (2025) is a supporting paper for text-to-image conditioning, evaluation, or long-prompt methods.

While diffusion models have revolutionized text-to-image generation with their ability to synthesize realistic and diverse scenes, they continue to struggle to generate consistent and legible text within images.

This shortcoming is commonly attributed to the locality bias inherent in diffusion-based generation, which limits their ability to model long-range spatial dependencies.

Read as background/bridge evidence when designing length and PE policy for LLM/VLM-era generators.


#### B8. Reward Hacking in the Era of Large Models: Mechanisms, Emergent Misalignment, Challenges

- **Link:** [https://arxiv.org/abs/2604.13602](https://arxiv.org/abs/2604.13602)
- **Date:** 2026-04-15
- **Tags:** supporting

"Reward Hacking in the Era of Large Models: Mechanisms, Emergent Misalignment, Challenges" (2026) is a supporting paper for text-to-image conditioning, evaluation, or long-prompt methods.

Reinforcement Learning from Human Feedback (RLHF) and related alignment paradigms have become central to steering large language models (LLMs) and multimodal large language models (MLLMs) toward human-preferred behaviors.

However, these approaches introduce a systemic vulnerability: reward hacking, where models exploit imperfections in learned reward signals to maximize proxy objectives without fulfilling true task intent.

Read as background/bridge evidence when designing length and PE policy for LLM/VLM-era generators.


#### B9. SDXL: Improving Latent Diffusion Models for High-Resolution Image Synthesis

- **Link:** [https://arxiv.org/abs/2307.01952](https://arxiv.org/abs/2307.01952)
- **Date:** 2023-07-04
- **Tags:** supporting

"SDXL: Improving Latent Diffusion Models for High-Resolution Image Synthesis" (2023) is a supporting paper for text-to-image conditioning, evaluation, or long-prompt methods.

We present SDXL, a latent diffusion model for text-to-image synthesis.

Compared to previous versions of Stable Diffusion, SDXL leverages a three times larger UNet backbone: The increase of model parameters is mainly due to more attention blocks and a larger cross-attention context as SDXL uses a second text encoder.

Read as background/bridge evidence when designing length and PE policy for LLM/VLM-era generators.


#### B10. TULIP: Token-length Upgraded CLIP

- **Link:** [https://arxiv.org/abs/2410.10034v2](https://arxiv.org/abs/2410.10034v2)
- **Date:** 2024-10-13
- **Tags:** long/dense preferred, numeric token budget

"TULIP: Token-length Upgraded CLIP" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

We address the challenge of representing long captions in vision-language models, such as CLIP.

By design these models are limited by fixed, absolute positional encodings, restricting inputs to a maximum of 77 tokens and hindering performance on tasks requiring longer descriptions.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


#### B11. High-Resolution Image Synthesis with Latent Diffusion Models

- **Link:** [https://arxiv.org/abs/2112.10752](https://arxiv.org/abs/2112.10752)
- **Date:** 2021-12-20
- **Tags:** supporting

"High-Resolution Image Synthesis with Latent Diffusion Models" (2021) is a supporting paper for text-to-image conditioning, evaluation, or long-prompt methods.

By decomposing the image formation process into a sequential application of denoising autoencoders, diffusion models (DMs) achieve state-of-the-art synthesis results on image data and beyond.

Additionally, their formulation allows for a guiding mechanism to control the image generation process without retraining.

Read as background/bridge evidence when designing length and PE policy for LLM/VLM-era generators.


#### B12. Learning Transferable Visual Models From Natural Language Supervision

- **Link:** [https://arxiv.org/abs/2103.00020](https://arxiv.org/abs/2103.00020)
- **Date:** 2021-02-26
- **Tags:** supporting

"Learning Transferable Visual Models From Natural Language Supervision" (2021) is a supporting paper for text-to-image conditioning, evaluation, or long-prompt methods.

State-of-the-art computer vision systems are trained to predict a fixed set of predetermined object categories.

This restricted form of supervision limits their generality and usability since additional labeled data is needed to specify any other visual concept.

Read as background/bridge evidence when designing length and PE policy for LLM/VLM-era generators.


### Tier C — length-focused extended set

Remaining length/recaption/PE-relevant papers from the catalog (92 items). Skim; deep-read those matching your encoder/PE plan.

1. **PromptMoG: Enhancing Diversity in Long-Prompt Image Generation via Prompt Embedding Mixture-of-Gaussian Sampling** — [2511.20251](https://arxiv.org/abs/2511.20251v1) — 2025-11-25
   - "PromptMoG: Enhancing Diversity in Long-Prompt Image Generation via Prompt Embedding Mixture-of-Gaussian Sampling" (2025) studies prompt rewriting, optimization, or prompt-side control for image generators.

2. **Multi-Resolution Flow Matching: Training-Free Diffusion Acceleration via Staged Sampling** — [2607.01642](https://arxiv.org/abs/2607.01642v1) — 2026-07-02
   - "Multi-Resolution Flow Matching: Training-Free Diffusion Acceleration via Staged Sampling" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

3. **TeleStyle V2: Beyond Content-Preserving Style Transfer with Self-Distillation and Distribution-Matching-Distillation** — [2606.20709](https://arxiv.org/abs/2606.20709v1) — 2026-06-16
   - "TeleStyle V2: Beyond Content-Preserving Style Transfer with Self-Distillation and Distribution-Matching-Distillation" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

4. **Unify-Agent: A Unified Multimodal Agent for World-Grounded Image Synthesis** — [2603.29620](https://arxiv.org/abs/2603.29620v2) — 2026-03-31
   - "Unify-Agent: A Unified Multimodal Agent for World-Grounded Image Synthesis" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

5. **LumiGen: An LVLM-Enhanced Iterative Framework for Fine-Grained Text-to-Image Generation** — [2508.04732](https://arxiv.org/abs/2508.04732v1) — 2025-08-05
   - "LumiGen: An LVLM-Enhanced Iterative Framework for Fine-Grained Text-to-Image Generation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

6. **ERNIE-Image Technical Report** — [2605.25347](https://arxiv.org/abs/2605.25347v1) — 2026-05-25
   - "ERNIE-Image Technical Report" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

7. **PromptEcho: Annotation-Free Reward from Vision-Language Models for Text-to-Image Reinforcement Learning** — [2604.12652](https://arxiv.org/abs/2604.12652v2) — 2026-04-14
   - "PromptEcho: Annotation-Free Reward from Vision-Language Models for Text-to-Image Reinforcement Learning" (2026) studies prompt rewriting, optimization, or prompt-side control for image generators.

8. **ITIScore: An Image-to-Text-to-Image Rating Framework for the Image Captioning Ability of MLLMs** — [2604.03765](https://arxiv.org/abs/2604.03765v2) — 2026-04-04
   - "ITIScore: An Image-to-Text-to-Image Rating Framework for the Image Captioning Ability of MLLMs" (2026) focuses on captioning/recaptioning data that feeds text-to-image training.

9. **RePrompt: Reasoning-Augmented Reprompting for Text-to-Image Generation via Reinforcement Learning** — [2505.17540](https://arxiv.org/abs/2505.17540v1) — 2025-05-23
   - "RePrompt: Reasoning-Augmented Reprompting for Text-to-Image Generation via Reinforcement Learning" (2025) studies prompt rewriting, optimization, or prompt-side control for image generators.

10. **RICO: Improving Accuracy and Completeness in Image Recaptioning via Visual Reconstruction** — [2505.22613](https://arxiv.org/abs/2505.22613v1) — 2025-05-28
   - "RICO: Improving Accuracy and Completeness in Image Recaptioning via Visual Reconstruction" (2025) focuses on captioning/recaptioning data that feeds text-to-image training.

11. **UniGenBench++: A Unified Semantic Evaluation Benchmark for Text-to-Image Generation** — [2510.18701](https://arxiv.org/abs/2510.18701v2) — 2025-10-21
   - "UniGenBench++: A Unified Semantic Evaluation Benchmark for Text-to-Image Generation" (2025) introduces or expands evaluation for text-conditioned image generation, often under long or compositional prompts.

12. **APE: Agentic Prompt Enhancer for Image Generation and Editing** — [2606.00204](https://arxiv.org/abs/2606.00204v1) — 2026-05-29
   - "APE: Agentic Prompt Enhancer for Image Generation and Editing" (2026) studies prompt rewriting, optimization, or prompt-side control for generators.

13. **Omni-Dish: Photorealistic and Faithful Image Generation and Editing for Arbitrary Chinese Dishes** — [2504.09948](https://arxiv.org/abs/2504.09948v3) — 2025-04-14
   - "Omni-Dish: Photorealistic and Faithful Image Generation and Editing for Arbitrary Chinese Dishes" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

14. **Understanding-in-Generation: Reinforcing Generative Capability of Unified Model via Infusing Understanding into Generation** — [2509.18639](https://arxiv.org/abs/2509.18639v3) — 2025-09-23
   - "Understanding-in-Generation: Reinforcing Generative Capability of Unified Model via Infusing Understanding into Generation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

15. **Think-Then-Generate: Reasoning-Aware Text-to-Image Diffusion with LLM Encoders** — [2601.10332](https://arxiv.org/abs/2601.10332v1) — 2026-01-15
   - "Think-Then-Generate: Reasoning-Aware Text-to-Image Diffusion with LLM Encoders" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

16. **Reason2Attack: Jailbreaking Text-to-Image Models via LLM Reasoning** — [2503.17987](https://arxiv.org/abs/2503.17987v3) — 2025-03-23
   - "Reason2Attack: Jailbreaking Text-to-Image Models via LLM Reasoning" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

17. **Harnessing Caption Detailness for Data-Efficient Text-to-Image Generation** — [2505.15172](https://arxiv.org/abs/2505.15172v1) — 2025-05-21
   - "Harnessing Caption Detailness for Data-Efficient Text-to-Image Generation" (2025) focuses on captioning/recaptioning data that feeds text-to-image training.

18. **TIIF-Bench: How Does Your T2I Model Follow Your Instructions?** — [2506.02161](https://arxiv.org/abs/2506.02161v3) — 2025-06-02
   - "TIIF-Bench: How Does Your T2I Model Follow Your Instructions?" (2025) introduces or expands evaluation for text-conditioned image generation, often under long or compositional prompts.

19. **BlindSight: Harnessing Sparsity for Efficient Vision-Language Models** — [2507.09071](https://arxiv.org/abs/2507.09071v3) — 2025-07-11
   - "BlindSight: Harnessing Sparsity for Efficient Vision-Language Models" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

20. **Stable Score Distillation** — [2507.09168](https://arxiv.org/abs/2507.09168v1) — 2025-07-12
   - "Stable Score Distillation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

21. **ZIPP:Zero-shot Image Personalization from Personas** — [2606.08841](https://arxiv.org/abs/2606.08841v1) — 2026-06-07
   - "ZIPP:Zero-shot Image Personalization from Personas" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

22. **MMaDA: Multimodal Large Diffusion Language Models** — [2505.15809](https://arxiv.org/abs/2505.15809v2) — 2025-05-21
   - "MMaDA: Multimodal Large Diffusion Language Models" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

23. **Are Image-to-Video Models Good Zero-Shot Image Editors?** — [2511.19435](https://arxiv.org/abs/2511.19435v2) — 2025-11-24
   - "Are Image-to-Video Models Good Zero-Shot Image Editors?" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

24. **Identity-Preserving Text-to-Video Generation via Training-Free Prompt, Image, and Guidance Enhancement** — [2509.01362](https://arxiv.org/abs/2509.01362v1) — 2025-09-01
   - "Identity-Preserving Text-to-Video Generation via Training-Free Prompt, Image, and Guidance Enhancement" (2025) studies prompt rewriting, optimization, or prompt-side control for generators.

25. **Vision-Free Retrieval: Rethinking Multimodal Search with Textual Scene Descriptions** — [2509.19203](https://arxiv.org/abs/2509.19203v1) — 2025-09-23
   - "Vision-Free Retrieval: Rethinking Multimodal Search with Textual Scene Descriptions" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

26. **SPOT: Selective Prompt Projection via Total Variation for Inference-Only Safe Text-to-Image Generation** — [2602.00616](https://arxiv.org/abs/2602.00616v3) — 2026-01-31
   - "SPOT: Selective Prompt Projection via Total Variation for Inference-Only Safe Text-to-Image Generation" (2026) studies prompt rewriting, optimization, or prompt-side control for image generators.

27. **Efficient Scaling of Diffusion Transformers for Text-to-Image Generation** — [2412.12391](https://arxiv.org/abs/2412.12391v1) — 2024-12-16
   - "Efficient Scaling of Diffusion Transformers for Text-to-Image Generation" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

28. **PIPBench: A Profile-Inclusive Framework for Personalized Image Generation Evaluation** — [2607.06440](https://arxiv.org/abs/2607.06440v1) — 2026-07-07
   - "PIPBench: A Profile-Inclusive Framework for Personalized Image Generation Evaluation" (2026) evaluates text-conditioned image generation, often under long or compositional prompts.

29. **KG-FairDiff: Knowledge Graph-Guided Prompt Refinement for Demographically Fair Text-to-Image Generation** — [2606.01282](https://arxiv.org/abs/2606.01282v1) — 2026-05-31
   - "KG-FairDiff: Knowledge Graph-Guided Prompt Refinement for Demographically Fair Text-to-Image Generation" (2026) studies prompt rewriting, optimization, or prompt-side control for generators.

30. **CLIP Is Shortsighted: Paying Attention Beyond the First Sentence** — [2602.22419](https://arxiv.org/abs/2602.22419v2) — 2026-02-25
   - "CLIP Is Shortsighted: Paying Attention Beyond the First Sentence" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

31. **Unsafe2Safe: Controllable Image Anonymization for Downstream Utility** — [2603.28605](https://arxiv.org/abs/2603.28605v1) — 2026-03-30
   - "Unsafe2Safe: Controllable Image Anonymization for Downstream Utility" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

32. **Mastering Text-to-Image Diffusion: Recaptioning, Planning, and Generating with Multimodal LLMs** — [2401.11708](https://arxiv.org/abs/2401.11708v3) — 2024-01-22
   - "Mastering Text-to-Image Diffusion: Recaptioning, Planning, and Generating with Multimodal LLMs" (2024) focuses on captioning/recaptioning data that feeds text-to-image training.

33. **On Discrete Prompt Optimization for Diffusion Models** — [2407.01606](https://arxiv.org/abs/2407.01606v1) — 2024-06-27
   - "On Discrete Prompt Optimization for Diffusion Models" (2024) studies prompt rewriting, optimization, or prompt-side control for generators.

34. **PiD: Fast and High-Resolution Latent Decoding with Pixel Diffusion** — [2605.23902](https://arxiv.org/abs/2605.23902v1) — 2026-05-22
   - "PiD: Fast and High-Resolution Latent Decoding with Pixel Diffusion" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

35. **One Rewrite to Fix Them All? Type-Aware Repair Allocation for Text-to-Image Prompt Optimization** — [2607.18724](https://arxiv.org/abs/2607.18724v1) — 2026-07-21
   - "One Rewrite to Fix Them All? Type-Aware Repair Allocation for Text-to-Image Prompt Optimization" (2026) studies prompt rewriting, optimization, or prompt-side control for image generators.

36. **CineOrchestra: Unified Entity-Centric Conditioning for Cinematic Video Generation** — [2606.13768](https://arxiv.org/abs/2606.13768v2) — 2026-06-11
   - "CineOrchestra: Unified Entity-Centric Conditioning for Cinematic Video Generation" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

37. **OpenVTON-Bench: A Large-Scale High-Resolution Benchmark for Controllable Virtual Try-On Evaluation** — [2601.22725](https://arxiv.org/abs/2601.22725v4) — 2026-01-30
   - "OpenVTON-Bench: A Large-Scale High-Resolution Benchmark for Controllable Virtual Try-On Evaluation" (2026) evaluates text-conditioned image generation, often under long or compositional prompts.

38. **MoTrans: Customized Motion Transfer with Text-driven Video Diffusion Models** — [2412.01343](https://arxiv.org/abs/2412.01343v1) — 2024-12-02
   - "MoTrans: Customized Motion Transfer with Text-driven Video Diffusion Models" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

39. **Medical Video Generation for Disease Progression Simulation** — [2411.11943](https://arxiv.org/abs/2411.11943v1) — 2024-11-18
   - "Medical Video Generation for Disease Progression Simulation" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

40. **TIT-Score: Evaluating Long-Prompt Based Text-to-Image Alignment via Text-to-Image-to-Text Consistency** — [2510.02987](https://arxiv.org/abs/2510.02987v1) — 2025-10-03
   - "TIT-Score: Evaluating Long-Prompt Based Text-to-Image Alignment via Text-to-Image-to-Text Consistency" (2025) studies prompt rewriting, optimization, or prompt-side control for image generators.

41. **Prompting for products: Investigating design space exploration strategies for text-to-image generative models** — [2408.03946](https://arxiv.org/abs/2408.03946v1) — 2024-07-22
   - "Prompting for products: Investigating design space exploration strategies for text-to-image generative models" (2024) studies prompt rewriting, optimization, or prompt-side control for image generators.

42. **CRAFT: Continuous Reasoning and Agentic Feedback Tuning for Multimodal Text-to-Image Generation** — [2512.20362](https://arxiv.org/abs/2512.20362v2) — 2025-12-23
   - "CRAFT: Continuous Reasoning and Agentic Feedback Tuning for Multimodal Text-to-Image Generation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

43. **WorldGPT: A Sora-Inspired Video AI Agent as Rich World Models from Text and Image Inputs** — [2403.07944](https://arxiv.org/abs/2403.07944v1) — 2024-03-10
   - "WorldGPT: A Sora-Inspired Video AI Agent as Rich World Models from Text and Image Inputs" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

44. **LPNSR: Optimal Noise-Guided Diffusion Image Super-Resolution Via Learnable Noise Prediction** — [2603.21045](https://arxiv.org/abs/2603.21045v5) — 2026-03-22
   - "LPNSR: Optimal Noise-Guided Diffusion Image Super-Resolution Via Learnable Noise Prediction" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

45. **JoyAI-Image: Awaking Spatial Intelligence in Unified Multimodal Understanding and Generation** — [2605.04128](https://arxiv.org/abs/2605.04128v2) — 2026-05-05
   - "JoyAI-Image: Awaking Spatial Intelligence in Unified Multimodal Understanding and Generation" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

46. **sketch-plot: Progressive Editing for Text-to-Image Academic Figures** — [2606.09171](https://arxiv.org/abs/2606.09171v2) — 2026-06-08
   - "sketch-plot: Progressive Editing for Text-to-Image Academic Figures" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

47. **Multimodal Prompt Decoupling Attack on the Safety Filters in Text-to-Image Models** — [2509.21360](https://arxiv.org/abs/2509.21360v1) — 2025-09-21
   - "Multimodal Prompt Decoupling Attack on the Safety Filters in Text-to-Image Models" (2025) studies prompt rewriting, optimization, or prompt-side control for image generators.

48. **Automated Prompt Generation for Creative and Counterfactual Text-to-image Synthesis** — [2509.21375](https://arxiv.org/abs/2509.21375v1) — 2025-09-23
   - "Automated Prompt Generation for Creative and Counterfactual Text-to-image Synthesis" (2025) studies prompt rewriting, optimization, or prompt-side control for image generators.

49. **LSSGen: Leveraging Latent Space Scaling in Flow and Diffusion for Efficient Text to Image Generation** — [2507.16154](https://arxiv.org/abs/2507.16154v1) — 2025-07-22
   - "LSSGen: Leveraging Latent Space Scaling in Flow and Diffusion for Efficient Text to Image Generation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

50. **LLMs can see and hear without any training** — [2501.18096](https://arxiv.org/abs/2501.18096v1) — 2025-01-30
   - "LLMs can see and hear without any training" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

51. **Factorized-Dreamer: Training A High-Quality Video Generator with Limited and Low-Quality Data** — [2408.10119](https://arxiv.org/abs/2408.10119v1) — 2024-08-19
   - "Factorized-Dreamer: Training A High-Quality Video Generator with Limited and Low-Quality Data" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

52. **Decomposing Private Image Generation via Coarse-to-Fine Wavelet Modeling** — [2602.23262](https://arxiv.org/abs/2602.23262v1) — 2026-02-26
   - "Decomposing Private Image Generation via Coarse-to-Fine Wavelet Modeling" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

53. **Emotion-Director: Bridging Affective Shortcut in Emotion-Oriented Image Generation** — [2512.19479](https://arxiv.org/abs/2512.19479v1) — 2025-12-22
   - "Emotion-Director: Bridging Affective Shortcut in Emotion-Oriented Image Generation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

54. **StrandDesigner: Towards Practical Strand Generation with Sketch Guidance** — [2508.01650](https://arxiv.org/abs/2508.01650v1) — 2025-08-03
   - "StrandDesigner: Towards Practical Strand Generation with Sketch Guidance" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

55. **EditID: Training-Free Editable ID Customization for Text-to-Image Generation** — [2503.12526](https://arxiv.org/abs/2503.12526v1) — 2025-03-16
   - "EditID: Training-Free Editable ID Customization for Text-to-Image Generation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

56. **Progressive Prompt Detailing for Improved Alignment in Text-to-Image Generative Models** — [2503.17794](https://arxiv.org/abs/2503.17794v4) — 2025-03-22
   - "Progressive Prompt Detailing for Improved Alignment in Text-to-Image Generative Models" (2025) studies prompt rewriting, optimization, or prompt-side control for image generators.

57. **EditIDv2: Editable ID Customization with Data-Lubricated ID Feature Integration for Text-to-Image Generation** — [2509.05659](https://arxiv.org/abs/2509.05659v1) — 2025-09-06
   - "EditIDv2: Editable ID Customization with Data-Lubricated ID Feature Integration for Text-to-Image Generation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

58. **CAHS-Attack: CLIP-Aware Heuristic Search Attack Method for Stable Diffusion** — [2511.21180](https://arxiv.org/abs/2511.21180v1) — 2025-11-26
   - "CAHS-Attack: CLIP-Aware Heuristic Search Attack Method for Stable Diffusion" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

59. **Self-Rewarding Large Vision-Language Models for Optimizing Prompts in Text-to-Image Generation** — [2505.16763](https://arxiv.org/abs/2505.16763v2) — 2025-05-22
   - "Self-Rewarding Large Vision-Language Models for Optimizing Prompts in Text-to-Image Generation" (2025) studies prompt rewriting, optimization, or prompt-side control for image generators.

60. **Dynamic Optimization and Safety Indicator Injection for Jailbreaking Text-to-Image Models with Multimodal Safety Filters** — [2505.18979](https://arxiv.org/abs/2505.18979v2) — 2025-05-25
   - "Dynamic Optimization and Safety Indicator Injection for Jailbreaking Text-to-Image Models with Multimodal Safety Filters" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

61. **InterCoG: Towards Spatially Precise Image Editing with Interleaved Chain-of-Grounding Reasoning** — [2603.01586](https://arxiv.org/abs/2603.01586v3) — 2026-03-02
   - "InterCoG: Towards Spatially Precise Image Editing with Interleaved Chain-of-Grounding Reasoning" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

62. **NeuroPrompts: An Adaptive Framework to Optimize Prompts for Text-to-Image Generation** — [2311.12229](https://arxiv.org/abs/2311.12229v2) — 2023-11-20
   - "NeuroPrompts: An Adaptive Framework to Optimize Prompts for Text-to-Image Generation" (2023) studies prompt rewriting, optimization, or prompt-side control for generators.

63. **Make-An-Audio: Text-To-Audio Generation with Prompt-Enhanced Diffusion Models** — [2301.12661](https://arxiv.org/abs/2301.12661v1) — 2023-01-30
   - "Make-An-Audio: Text-To-Audio Generation with Prompt-Enhanced Diffusion Models" (2023) studies prompt rewriting, optimization, or prompt-side control for generators.

64. **Visual Autoregressive Modelling for Monocular Depth Estimation** — [2512.22653](https://arxiv.org/abs/2512.22653v1) — 2025-12-27
   - "Visual Autoregressive Modelling for Monocular Depth Estimation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

65. **APT: Improving Diffusion Models for High Resolution Image Generation with Adaptive Path Tracing** — [2507.21690](https://arxiv.org/abs/2507.21690v1) — 2025-07-29
   - "APT: Improving Diffusion Models for High Resolution Image Generation with Adaptive Path Tracing" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

66. **Latent Space Super-Resolution for Higher-Resolution Image Generation with Diffusion Models** — [2503.18446](https://arxiv.org/abs/2503.18446v2) — 2025-03-24
   - "Latent Space Super-Resolution for Higher-Resolution Image Generation with Diffusion Models" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

67. **A Reason-then-Describe Instruction Interpreter for Controllable Video Generation** — [2511.20563](https://arxiv.org/abs/2511.20563v1) — 2025-11-25
   - "A Reason-then-Describe Instruction Interpreter for Controllable Video Generation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

68. **Qwen-Image-Layered: Towards Inherent Editability via Layer Decomposition** — [2512.15603](https://arxiv.org/abs/2512.15603v1) — 2025-12-17
   - "Qwen-Image-Layered: Towards Inherent Editability via Layer Decomposition" (2025) is a modern system/report in the LLM/VLM-conditioned image generation line.

69. **FundusGAN: A Hierarchical Feature-Aware Generative Framework for High-Fidelity Fundus Image Generation** — [2503.17831](https://arxiv.org/abs/2503.17831v1) — 2025-03-22
   - "FundusGAN: A Hierarchical Feature-Aware Generative Framework for High-Fidelity Fundus Image Generation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

70. **Video-P2P: Video Editing with Cross-attention Control** — [2303.04761](https://arxiv.org/abs/2303.04761v1) — 2023-03-08
   - "Video-P2P: Video Editing with Cross-attention Control" (2023) contributes methods or analysis in contemporary text-to-image / multimodal generation.

71. **An Empirical Study and Analysis of Text-to-Image Generation Using Large Language Model-Powered Textual Representation** — [2405.12914](https://arxiv.org/abs/2405.12914v2) — 2024-05-21
   - "An Empirical Study and Analysis of Text-to-Image Generation Using Large Language Model-Powered Textual Representation" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

72. **Red-Teaming Text-to-Image Models via In-Context Experience Replay and Semantic-Preserving Prompt Rewriting** — [2411.16769](https://arxiv.org/abs/2411.16769v3) — 2024-11-25
   - "Red-Teaming Text-to-Image Models via In-Context Experience Replay and Semantic-Preserving Prompt Rewriting" (2024) studies prompt rewriting, optimization, or prompt-side control for image generators.

73. **Edify Image: High-Quality Image Generation with Pixel Space Laplacian Diffusion Models** — [2411.07126](https://arxiv.org/abs/2411.07126v1) — 2024-11-11
   - "Edify Image: High-Quality Image Generation with Pixel Space Laplacian Diffusion Models" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

74. **PG-MAP: Joint MAP Optimization for Inference-Time Alignment of Diffusion and Flow-Matching Models** — [2606.22958](https://arxiv.org/abs/2606.22958v1) — 2026-06-22
   - "PG-MAP: Joint MAP Optimization for Inference-Time Alignment of Diffusion and Flow-Matching Models" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

75. **Inf-DiT: Upsampling Any-Resolution Image with Memory-Efficient Diffusion Transformer** — [2405.04312](https://arxiv.org/abs/2405.04312v2) — 2024-05-07
   - "Inf-DiT: Upsampling Any-Resolution Image with Memory-Efficient Diffusion Transformer" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

76. **xGen-VideoSyn-1: High-fidelity Text-to-Video Synthesis with Compressed Representations** — [2408.12590](https://arxiv.org/abs/2408.12590v2) — 2024-08-22
   - "xGen-VideoSyn-1: High-fidelity Text-to-Video Synthesis with Compressed Representations" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

77. **Multistep Distillation of Diffusion Models via Moment Matching** — [2406.04103](https://arxiv.org/abs/2406.04103v1) — 2024-06-06
   - "Multistep Distillation of Diffusion Models via Moment Matching" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

78. **Spectral Image Tokenizer** — [2412.09607](https://arxiv.org/abs/2412.09607v2) — 2024-12-12
   - "Spectral Image Tokenizer" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

79. **Arc2Face: A Foundation Model for ID-Consistent Human Faces** — [2403.11641](https://arxiv.org/abs/2403.11641v2) — 2024-03-18
   - "Arc2Face: A Foundation Model for ID-Consistent Human Faces" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

80. **Generative Portrait Shadow Removal** — [2410.05525](https://arxiv.org/abs/2410.05525v1) — 2024-10-07
   - "Generative Portrait Shadow Removal" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

81. **A User-Friendly Framework for Generating Model-Preferred Prompts in Text-to-Image Synthesis** — [2402.12760](https://arxiv.org/abs/2402.12760v2) — 2024-02-20
   - "A User-Friendly Framework for Generating Model-Preferred Prompts in Text-to-Image Synthesis" (2024) studies prompt rewriting, optimization, or prompt-side control for generators.

82. **CapHDR2IR: Caption-Driven Transfer from Visible Light to Infrared Domain** — [2411.16327](https://arxiv.org/abs/2411.16327v1) — 2024-11-25
   - "CapHDR2IR: Caption-Driven Transfer from Visible Light to Infrared Domain" (2024) focuses on captioning/recaptioning data for text-to-image training.

83. **Latent Diffusion, Implicit Amplification: Efficient Continuous-Scale Super-Resolution for Remote Sensing Images** — [2410.22830](https://arxiv.org/abs/2410.22830v1) — 2024-10-30
   - "Latent Diffusion, Implicit Amplification: Efficient Continuous-Scale Super-Resolution for Remote Sensing Images" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

84. **RepLDM: Reprogramming Pretrained Latent Diffusion Models for High-Quality, High-Efficiency, High-Resolution Image Generation** — [2410.06055](https://arxiv.org/abs/2410.06055v2) — 2024-10-08
   - "RepLDM: Reprogramming Pretrained Latent Diffusion Models for High-Quality, High-Efficiency, High-Resolution Image Generation" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

85. **UltraPixel: Advancing Ultra-High-Resolution Image Synthesis to New Peaks** — [2407.02158](https://arxiv.org/abs/2407.02158v2) — 2024-07-02
   - "UltraPixel: Advancing Ultra-High-Resolution Image Synthesis to New Peaks" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

86. **DiM: Diffusion Mamba for Efficient High-Resolution Image Synthesis** — [2405.14224](https://arxiv.org/abs/2405.14224v2) — 2024-05-23
   - "DiM: Diffusion Mamba for Efficient High-Resolution Image Synthesis" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

87. **Arbitrary-Scale Image Generation and Upsampling using Latent Diffusion Model and Implicit Neural Decoder** — [2403.10255](https://arxiv.org/abs/2403.10255v1) — 2024-03-15
   - "Arbitrary-Scale Image Generation and Upsampling using Latent Diffusion Model and Implicit Neural Decoder" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

88. **RubiCap: Rubric-Guided Reinforcement Learning for Dense Image Captioning** — [2603.09160](https://arxiv.org/abs/2603.09160v1) — 2026-03-10
   - "RubiCap: Rubric-Guided Reinforcement Learning for Dense Image Captioning" (2026) focuses on captioning/recaptioning data that feeds text-to-image training.

89. **Synthetic Perception: Can Generated Images Unlock Latent Visual Prior for Text-Centric Reasoning?** — [2506.17623](https://arxiv.org/abs/2506.17623v2) — 2025-06-21
   - "Synthetic Perception: Can Generated Images Unlock Latent Visual Prior for Text-Centric Reasoning?" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

90. **HFI: A unified framework for training-free detection and implicit watermarking of latent diffusion model generated images** — [2412.20704](https://arxiv.org/abs/2412.20704v2) — 2024-12-30
   - "HFI: A unified framework for training-free detection and implicit watermarking of latent diffusion model generated images" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

91. **Beware of Aliases -- Signal Preservation is Crucial for Robust Image Restoration** — [2406.07435](https://arxiv.org/abs/2406.07435v2) — 2024-06-11
   - "Beware of Aliases -- Signal Preservation is Crucial for Robust Image Restoration" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

92. **Twins: Learn to Predict Unified Representations with Focal Loss** — [2607.22531](https://arxiv.org/abs/2607.22531v1) — 2026-07-24
   - "Twins: Learn to Predict Unified Representations with Focal Loss" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

---

## 2. Direct answers (combined from both studies)

### 2.1 Training prompt / caption length

| Stack class | What authors use / recommend | Fixed or variable? |
|-------------|------------------------------|--------------------|
| Historical CLIP (SD1/SDXL) | <= **77** tokens; alt-text often ~10-20 | Fixed cap; better as **short+long mix** or **random within 77** |
| Dense-caption CLIP fine-tunes (RECAP, How-to-Train) | Still <=77, denser text | **Variable/mix best** if no rewriter |
| PixArt-alpha to Sigma | **120 to ~300** as captions densify | Fixed raised with data density |
| Open modern recipe (i1) | Long captions, truncate **256** | **Fixed long** + infer rewrite |
| Qwen-Image / FLUX.2 / Seedream-class | Dense/long inside ~**512** (API sometimes 800-1300) | Long-biased; PE default-on |
| HunyuanImage 3.0 | **30-1000 words** sampled | **Variable by design** |
| FIBO structured | ~**1000 tokens** JSON schema | Fixed long structured |
| Imagen-class API | Strong LM encoder; Imagen 4 **480**-token limit | Product hard cap |

**Answer for a Qwen-VLM-like model:** train on **dense VLM captions** inside your encoder budget (start **`L ≈ 512`**). Prefer (i) **long-biased / long-only** if you ship PE, or (ii) **wide-band variable length** if you want robustness without PE. Do not train only on short alt-text.

### 2.2 Inference length

**Match the training caption distribution.**

- i1: GenEval **0.17** (short) -> **0.49** (repeat x12) -> **0.73** (LLM rewrite).
- TIPO / Wan / DALL-E-3: rewrite transports user prompts into the training caption law.
- DetailMaster (~285 tokens): strong models still degrade as length grows.
- LongAlign/PRISM: training under ~300 does not imply clean behavior above ~500.

**Answer:** after PE, inference text should land in the **same length band as training**. Short user prompts are a UI, not necessarily the raw conditioning string — unless wide-band training includes short.

### 2.3 Re-prompt / writer / PE output length

| Role | Length guidance | How to train the writer correctly |
|------|-----------------|-----------------------------------|
| Offline recaptioner | `max_new_tokens=128` -> mean ~**49** (Recap-DataComp); denser for 300-512; FIBO ~**1000** structured | Cap decode to encoder `L`; faithful VLM captioner; optional higher temperature for diversity |
| Online PE / rewriter | Target training caption law; often `max_new_tokens ≈ 512` | Optimize content fixes + distribution match, **not length**; alignment rewards (PromptEnhancer); faithfulness / visual anchors (FaithRewriter) |
| Adaptive PE | Variable budget by task (Seedream-style) | Route by difficulty; do not always emit max tokens |

**Answer:** PE length = whatever is needed to enter `mu_train` with faithful attribute-rich content. Practical setpoint: **`max_new_tokens ~ L` (about 512)**, default-on. Wrong objective: reward verbosity.

### 2.4 Variability

Three viable designs:

1. **Train-time mixture/randomization** (RECAP 50/50; How-to-Train; Hunyuan 30-1000 words).
2. **Fixed long train + infer PE** (i1, DALL-E-3, Qwen/FLUX.2).
3. **Structured long with field/schema sampling** (FIBO; Hunyuan compositional fields).

Correct variability covers **deployment support** after `g`. Incomplete: randomize without short+long, or PE that always maxes tokens.

### 2.5 Native training vs separate rewriter

| Approach | Pros | Cons | Examples |
|----------|------|------|----------|
| Separate PE default-on | Simple generator; portable; matches long train | Latency; hallucination; extra model | Qwen-Image, FLUX.2, Seedream, Wan |
| Native via variable train | No extra model; better short prompts | May lose peak long alignment | How-to-Train, Hunyuan wide-band |
| Native LLM/VLM encoder | Strong language prior | Still needs caption-law matching | Playground v3, SANA, i1 |
| Unified AR multimodal | Text budget trades with image tokens | New failure modes | Emu3 / Janus / BAGEL lineage |

**Answer:** field is not abandoning PE — it is making PE **native to the product**. Best systems do **both**: rich/variable train captions **and** faithfulness-aware PE.

---

## 3. Problems the literature keeps finding

1. Train-infer length shift (long-only makes short prompts OOD).
2. Capacity without dense data is weak (DetailMaster).
3. Length extrapolation failure beyond train band.
4. Detail overload / attribute leakage at extreme length.
5. Padding / EOT domination on very short pad-to-max prompts.
6. PE hallucination and verbosity reward hacking.
7. Benchmark confounding (short GenEval vs long DetailMaster/LongT2I).
8. Chat/system template overhead eating user budget.
9. Multilingual token inflation (e.g. CJK).
10. Compute wall for ~1000-token text without efficient fusion.

---

## 4. Fundamental framing

### Three objects

```
mu_train : training caption distribution
L        : encoder / context budget
g(.)     : inference map (identity | PE | schema fill | repeat)
c_infer = g(c_user),  x ~ p_theta(. | E(c_infer[:L]))
```

Best length is a property of `(mu_train, L, g)` under deployment, not of a single integer.

### Three mismatches

1. Capacity — truncate if `len(c) > L`.
2. Distributional length — law of `c_infer` vs `mu_train` (dominant empirical effect; i1 repetition diagnostic).
3. Semantic rate — same length, different task-relevant bits/token.

### Sketch

- Rate-distortion: useful info ~ `min(I(x; c_<=ell), C_model)`.
- Covariate shift: short-prompt collapse after long training.
- Mixture coverage: variable train = prior over length bins matching deployment.
- Objective: maximize deployment utility s.t. compute, faithfulness, and `support(Law(g(c)))` inside train support and `L`.

No universal closed-form `L*`. There is a well-posed ablation protocol: histograms, short/repeat/rewrite/long diagnostics, faithfulness of `g`, train-eval length delta on every score.

---

## 5. Open questions — what modern work already answers

| Open question | Status | Best current answer |
|---------------|--------|---------------------|
| Exact optimal token length? | No universal number | Cover p95 of train+PE; practice **256-512** (API 480-1300) |
| Fixed vs variable train? | Trade-off answered | Long+PE **or** wide-band variable; fixed short obsolete |
| How to vary correctly? | Partially answered | Random/mix/schema sampling over deployment band |
| PE output length? | Answered in principle | Match `mu_train`; ~`L` decode; content/faithfulness rewards |
| Train PE how? | Converging | SFT then RL/DPO/GRPO; optional visual anchors; transferable |
| Fully native without PE? | Possible, not dominant | Variable train helps; products still ship PE |
| Do LLM/VLM encoders remove the problem? | No — raise the ceiling | Still need matched `mu_train` + PE/variability |
| Extreme >500-1000? | Emerging | Train mass at that length + efficient fusion |
| Fair evaluation? | Improving fast | Length-binned benches; report length delta |

---

## 6. Full catalog (300 papers)

Title, link, four sentences each.

### 1. Photorealistic Text-to-Image Diffusion Models with Deep Language Understanding

- **Link:** [https://arxiv.org/abs/2205.11487](https://arxiv.org/abs/2205.11487)
- **Published:** 2025-01-01
- **Tags:** long/dense preferred, re-prompt/recaption, LLM/VLM encoder

Imagen showed frozen large LM text encoders (T5-XXL) beat CLIP on challenging compositional prompts.

Motivated the shift from contrastive text towers to language-model conditioning.

Later Imagen APIs document concrete token limits (e.g. 480).

Historical root of “use a strong language model as the text pathway.”


### 2. PromptEnhancer: A Simple Approach to Enhance Text-to-Image Models via Chain-of-Thought Prompt Rewriting

- **Link:** [https://arxiv.org/abs/2509.04545v5](https://arxiv.org/abs/2509.04545v5)
- **Published:** 2025-09-04
- **Tags:** re-prompt/recaption, benchmark/eval

PromptEnhancer is a model-agnostic CoT rewriter trained with fine-grained RL against AlignEvaluator.

Rewriting should change content to fix T2I failures, not add stylistic verbosity.

PE length is a side-effect of needed content, not the optimization target.

Template for PE rewards when avoiding reward-hacked overlong prompts.


### 3. LongT2IBench: A Benchmark for Evaluating Long Text-to-Image Generation with Graph-structured Annotations

- **Link:** [https://arxiv.org/abs/2512.09271v1](https://arxiv.org/abs/2512.09271v1)
- **Published:** 2025-12-10
- **Tags:** long/dense preferred, LLM/VLM encoder, benchmark/eval

LongT2IBench evaluates long T2I with graph-structured annotations and balanced word-count bins.

Enables measuring generators/evaluators as length grows.

Pair with DetailMaster when validating length policies.

Shows the field is instrumenting length as a first-class axis.


### 4. DetailMaster: Can Your Text-to-Image Model Handle Long Prompts?

- **Link:** [https://arxiv.org/abs/2505.16915v3](https://arxiv.org/abs/2505.16915v3)
- **Published:** 2025-05-22
- **Tags:** long/dense preferred, benchmark/eval

DetailMaster averages ~284.89 tokens with fine-grained attribute/relation metrics.

Dense long training matters more than merely raising token capacity; accuracy falls as length grows.

Even FLUX/SD3-class models plateau near ~50% on hard long-prompt attributes.

Use to stress-test professional long prompts, not only short GenEval-like sets.


### 5. Generating an Image From 1,000 Words: Enhancing Text-to-Image With Structured Captions

- **Link:** [https://arxiv.org/abs/2511.06876v1](https://arxiv.org/abs/2511.06876v1)
- **Published:** 2025-11-10
- **Tags:** long/dense preferred, LLM/VLM encoder, benchmark/eval

FIBO trains on long structured JSON-schema captions at ~thousand-token scale (mean ~1160).

DimFusion fuses intermediate LLM states without growing token count, controlling compute.

Long structured captions converge faster and improve controllability vs short captions.

Extreme fixed-long+structure pole for VLM/LLM-conditioned generators.


### 6. What If We Recaption Billions of Web Images with LLaMA-3?

- **Link:** [https://arxiv.org/abs/2406.08478v2](https://arxiv.org/abs/2406.08478v2)
- **Published:** 2024-06-12
- **Tags:** re-prompt/recaption, LLM/VLM encoder

Recap-DataComp-1B uses LLaVA-LLaMA3 with max_new_tokens=128, mean length ~49 vs ~10 alt-text.

Concrete operating point for offline VLM recaption at web scale.

Downstream models train on mid-length dense text instead of raw alt-text.

Lower-bound modern recaption recipe before 512–1000 token regimes.


### 7. Improving Text-to-Image Generation with Input-Side Inference-Time Scaling

- **Link:** [https://arxiv.org/abs/2510.12041v2](https://arxiv.org/abs/2510.12041v2)
- **Published:** 2025-10-14
- **Tags:** re-prompt/recaption, LLM/VLM encoder, benchmark/eval

Input-side inference-time scaling trains iterative rewriters (e.g. DPO) without backbone SFT.

Gains come from closing train/user text distribution gap; rewriters transfer across generators.

Rewrite length judged by distribution matching, not a universal token target.

Supports PE as a portable layer in front of Qwen-VLM generators.


### 8. Seeing is Believing: Aligning Prompt Rewriting with Visual Anchors for Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2606.08492v2](https://arxiv.org/abs/2606.08492v2)
- **Published:** 2026-06-07
- **Tags:** re-prompt/recaption, LLM/VLM encoder

FaithRewriter shows text-only rewriters can hallucinate visually impossible details.

Anchors rewriting with an intermediate image for visual faithfulness.

Extra PE tokens are harmful if they invent unsupported content.

Long-rewrite policies need faithfulness objectives, not only length targets.


### 9. Long-Text-to-Image Generation via Compositional Prompt Decomposition

- **Link:** [https://arxiv.org/abs/2604.18258v1](https://arxiv.org/abs/2604.18258v1)
- **Published:** 2026-04-20
- **Tags:** long/dense preferred, benchmark/eval

Compositional prompt decomposition studies extreme long-text T2I.

Reports segment methods trained mostly under ~300 degrade up to ~30% above ~500 tokens.

Train support in length must cover deployment support.

Caution against claiming arbitrary long-context without training mass there.


### 10. A Picture is Worth a Thousand Words: Principled Recaptioning Improves Image Generation

- **Link:** [https://arxiv.org/abs/2310.16656v1](https://arxiv.org/abs/2310.16656v1)
- **Published:** 2023-10-25
- **Tags:** long/dense preferred, re-prompt/recaption, benchmark/eval

RECAP shows Short captions win FID, Long win semantics, 50/50 Mix wins overall under CLIP-77.

Captions over 77 tokens were dropped (<1%).

Early principled evidence for length mixing inside a hard budget.

Still generalizes as a mixture-design lesson for any encoder limit.


### 11. Playground v3: Improving Text-to-Image Alignment with Deep-Fusion Large Language Models

- **Link:** [https://arxiv.org/abs/2409.10695v2](https://arxiv.org/abs/2409.10695v2)
- **Published:** 2024-09-16
- **Tags:** LLM/VLM encoder, benchmark/eval

Playground v3 deep-fuses Llama3-8B into the DiT, replacing CLIP/T5 dual towers.

Text conditioning is native LLM hidden states across layers.

Ties generation quality to richness of the text channel (CapsBench).

Early clear break toward LLM-centric conditioning.


### 12. Wan: Open and Advanced Large-Scale Video Generative Models

- **Link:** [https://arxiv.org/abs/2503.20314](https://arxiv.org/abs/2503.20314)
- **Published:** 2025-01-01
- **Tags:** hand-curated

Wan states the principle plainly: dense captions in training, LLM rewriting at inference to match that distribution.

Default-on prompt extend is recommended in tooling.

Same PE-length logic as modern T2I, validated in video.

Cite for cross-modality train/infer text alignment.


### 13. TULIP: Token-length Upgraded CLIP

- **Link:** [https://arxiv.org/abs/2410.10034v2](https://arxiv.org/abs/2410.10034v2)
- **Published:** 2024-10-13
- **Tags:** long/dense preferred, numeric token budget

"TULIP: Token-length Upgraded CLIP" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

We address the challenge of representing long captions in vision-language models, such as CLIP.

By design these models are limited by fixed, absolute positional encodings, restricting inputs to a maximum of 77 tokens and hindering performance on tasks requiring longer descriptions.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 14. Qwen-Image-2.0 Technical Report

- **Link:** [https://arxiv.org/abs/2605.10730v1](https://arxiv.org/abs/2605.10730v1)
- **Published:** 2026-05-11
- **Tags:** LLM/VLM encoder, benchmark/eval

Qwen-Image-2.0 is a frontier open image system built on a Qwen-family VLM/LLM text pathway rather than CLIP or classic T5.

It documents large prompt budgets (hundreds to ~1.3k tokens by API/version) with hard truncation past the limit.

Prompt extension is first-class and default-on, so inference text is lengthened toward the training caption regime.

Primary reference for Qwen-VLM-class encoder max length, PE max_new_tokens, and default rewrite policy.


### 15. Seedream 4.0: Toward Next-generation Multimodal Image Generation

- **Link:** [https://arxiv.org/abs/2509.20427v3](https://arxiv.org/abs/2509.20427v3)
- **Published:** 2025-09-24
- **Tags:** LLM/VLM encoder, benchmark/eval

Seedream 4.0 uses a VLM prompt enhancer with task routing and adaptive thinking budgets.

Rewrite length becomes conditional on task difficulty rather than a fixed expansion factor.

Shows modern stacks couple a strong multimodal language model to the generator and control how much text it emits.

Important for adaptive / native PE rather than static upsampling.


### 16. How to Train your Text-to-Image Model: Evaluating Design Choices for Synthetic Training Captions

- **Link:** [https://arxiv.org/abs/2506.16679v1](https://arxiv.org/abs/2506.16679v1)
- **Published:** 2025-06-20
- **Tags:** variable/mixed length, benchmark/eval

Fixed long synthetic captions trade aesthetics/diversity against alignment on SD-class models.

Randomizing caption length per image removes the trade-off and yields best overall PickScores.

Mixture/coverage principle transfers beyond CLIP budgets: cover length modes you will serve.

Main citation for variable train length when you may not ship a rewriter.


### 17. HunyuanImage 3.0 Technical Report

- **Link:** [https://arxiv.org/abs/2509.23951v3](https://arxiv.org/abs/2509.23951v3)
- **Published:** 2025-09-28
- **Tags:** benchmark/eval

HunyuanImage 3.0 samples bilingual captions from about 30 to 1,000 words via Compositional Caption Synthesis.

Train length and pattern are deliberately variable across a wide band.

Inference can use CoT think_recaption/rewrite to map short users into that band.

Clearest published alternative to fixed-long-only training for LLM/VLM-era models.


### 18. i1: A Simple and Fully Open Recipe for Strong Text-to-Image Models

- **Link:** [https://arxiv.org/abs/2606.11289v1](https://arxiv.org/abs/2606.11289v1)
- **Published:** 2026-06-09
- **Tags:** numeric token budget, benchmark/eval

i1 uses a modern encoder truncated to 256 tokens with long synthetic captions only.

Long-caption training scores 0.17 on short GenEval, 0.49 with 12× repetition, 0.73 with LLM rewrite.

Recommends train long and lengthen inference to match training, not train short to match users.

The length-alignment diagnostic remains the right experimental template for Qwen-VLM stacks.


### 19. Improving Long-Text Alignment for Text-to-Image Diffusion Models

- **Link:** [https://arxiv.org/abs/2410.11817v2](https://arxiv.org/abs/2410.11817v2)
- **Published:** 2024-10-15
- **Tags:** numeric token budget

LongAlign uses segment-level encoding and preference optimization for long prompts on CLIP-limited models.

Extends past 77 by split–encode–concatenate with careful special-token handling.

Later work shows weak extrapolation beyond the training length band.

Historical bridge from CLIP limits to long-prompt methods; principle still generalizes.


### 20. TIPO: Text to Image with Text Presampling for Prompt Optimization

- **Link:** [https://arxiv.org/abs/2411.08127v6](https://arxiv.org/abs/2411.08127v6)
- **Published:** 2024-11-12
- **Tags:** LLM/VLM encoder

TIPO expands user prompts toward the training caption distribution rather than unconstrained rewrite.

Reports human preference wins and runtime benefits from distribution matching.

Frames PE as transport into μ_train, not maximal verbosity.

Core conceptual paper for correct re-prompt objectives.


### 21. PixArt-Σ: Weak-to-Strong Training of Diffusion Transformer for 4K Text-to-Image

- **Link:** [https://arxiv.org/abs/2403.04692v2](https://arxiv.org/abs/2403.04692v2)
- **Published:** 2024-03-07

"PixArt-Σ: Weak-to-Strong Training of Diffusion Transformer for 4K Text-to-Image Generation" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

In this paper, we introduce PixArt-Σ, a Diffusion Transformer model~(DiT) capable of directly generating images at 4K resolution.

PixArt-Σrepresents a significant advancement over its predecessor, PixArt-α, offering images of markedly higher fidelity and improved alignment with text prompts.

Keep it as background on modern generation/evaluation; use only if its data or metrics inform caption-length decisions.


### 22. SANA: Efficient High-Resolution Image Synthesis with Linear Diffusion Transformers

- **Link:** [https://arxiv.org/abs/2410.10679](https://arxiv.org/abs/2410.10679)
- **Published:** 2024-10-01
- **Tags:** numeric token budget, LLM/VLM encoder

SANA uses decoder-only Gemma as text encoder with linear-attention DiT.

Pipelines often set max_sequence_length ~300; instruction templates consume budget.

Shows chat/system wrappers shrink usable user length.

Relevant for templated Qwen/Gemma encoders.


### 23. Scaling Rectified Flow Transformers for High-Resolution Image Synthesis

- **Link:** [https://arxiv.org/abs/2403.03206](https://arxiv.org/abs/2403.03206)
- **Published:** 2024-03-05
- **Tags:** supporting

"Scaling Rectified Flow Transformers for High-Resolution Image Synthesis" (2024) is a supporting paper for text-to-image conditioning, evaluation, or long-prompt methods.

Diffusion models create data from noise by inverting the forward paths of data towards noise and have emerged as a powerful generative modeling technique for high-dimensional, perceptual data such as images and videos.

Rectified flow is a recent generative model formulation that connects data and noise in a straight line.

Read as background/bridge evidence when designing length and PE policy for LLM/VLM-era generators.


### 24. PixArt-$α$: Fast Training of Diffusion Transformer for Photorealistic Text-to-Image Synthesis

- **Link:** [https://arxiv.org/abs/2310.00426](https://arxiv.org/abs/2310.00426)
- **Published:** 2023-09-30
- **Tags:** supporting

"PixArt-$α$: Fast Training of Diffusion Transformer for Photorealistic Text-to-Image Synthesis" (2023) is a supporting paper for text-to-image conditioning, evaluation, or long-prompt methods.

The most advanced text-to-image (T2I) models require significant training costs (e.g., millions of GPU hours), seriously hindering the fundamental innovation for the AIGC community while increasing CO2 emissions.

This paper introduces PIXART-$α$, a Transformer-based T2I diffusion model whose image generation quality is competitive with state-of-the-art image generators (e.g., Imagen, SDXL, and even Midjourney), reaching near-commercial application standards.

Read as background/bridge evidence when designing length and PE policy for LLM/VLM-era generators.


### 25. Draw ALL Your Imagine: A Holistic Benchmark and Agent Framework for Complex Instruction-based Image Generation

- **Link:** [https://arxiv.org/abs/2505.24787](https://arxiv.org/abs/2505.24787)
- **Published:** 2025-05-30
- **Tags:** supporting

"Draw ALL Your Imagine: A Holistic Benchmark and Agent Framework for Complex Instruction-based Image Generation" (2025) is a supporting paper for text-to-image conditioning, evaluation, or long-prompt methods.

Recent advancements in text-to-image (T2I) generation have enabled models to produce high-quality images from textual descriptions.

However, these models often struggle with complex instructions involving multiple objects, attributes, and spatial relationships.

Read as background/bridge evidence when designing length and PE policy for LLM/VLM-era generators.


### 26. STRICT: Stress Test of Rendering Images Containing Text

- **Link:** [https://arxiv.org/abs/2505.18985](https://arxiv.org/abs/2505.18985)
- **Published:** 2025-05-25
- **Tags:** supporting

"STRICT: Stress Test of Rendering Images Containing Text" (2025) is a supporting paper for text-to-image conditioning, evaluation, or long-prompt methods.

While diffusion models have revolutionized text-to-image generation with their ability to synthesize realistic and diverse scenes, they continue to struggle to generate consistent and legible text within images.

This shortcoming is commonly attributed to the locality bias inherent in diffusion-based generation, which limits their ability to model long-range spatial dependencies.

Read as background/bridge evidence when designing length and PE policy for LLM/VLM-era generators.


### 27. Reward Hacking in the Era of Large Models: Mechanisms, Emergent Misalignment, Challenges

- **Link:** [https://arxiv.org/abs/2604.13602](https://arxiv.org/abs/2604.13602)
- **Published:** 2026-04-15
- **Tags:** supporting

"Reward Hacking in the Era of Large Models: Mechanisms, Emergent Misalignment, Challenges" (2026) is a supporting paper for text-to-image conditioning, evaluation, or long-prompt methods.

Reinforcement Learning from Human Feedback (RLHF) and related alignment paradigms have become central to steering large language models (LLMs) and multimodal large language models (MLLMs) toward human-preferred behaviors.

However, these approaches introduce a systemic vulnerability: reward hacking, where models exploit imperfections in learned reward signals to maximize proxy objectives without fulfilling true task intent.

Read as background/bridge evidence when designing length and PE policy for LLM/VLM-era generators.


### 28. SDXL: Improving Latent Diffusion Models for High-Resolution Image Synthesis

- **Link:** [https://arxiv.org/abs/2307.01952](https://arxiv.org/abs/2307.01952)
- **Published:** 2023-07-04
- **Tags:** supporting

"SDXL: Improving Latent Diffusion Models for High-Resolution Image Synthesis" (2023) is a supporting paper for text-to-image conditioning, evaluation, or long-prompt methods.

We present SDXL, a latent diffusion model for text-to-image synthesis.

Compared to previous versions of Stable Diffusion, SDXL leverages a three times larger UNet backbone: The increase of model parameters is mainly due to more attention blocks and a larger cross-attention context as SDXL uses a second text encoder.

Read as background/bridge evidence when designing length and PE policy for LLM/VLM-era generators.


### 29. High-Resolution Image Synthesis with Latent Diffusion Models

- **Link:** [https://arxiv.org/abs/2112.10752](https://arxiv.org/abs/2112.10752)
- **Published:** 2021-12-20
- **Tags:** supporting

"High-Resolution Image Synthesis with Latent Diffusion Models" (2021) is a supporting paper for text-to-image conditioning, evaluation, or long-prompt methods.

By decomposing the image formation process into a sequential application of denoising autoencoders, diffusion models (DMs) achieve state-of-the-art synthesis results on image data and beyond.

Additionally, their formulation allows for a guiding mechanism to control the image generation process without retraining.

Read as background/bridge evidence when designing length and PE policy for LLM/VLM-era generators.


### 30. Learning Transferable Visual Models From Natural Language Supervision

- **Link:** [https://arxiv.org/abs/2103.00020](https://arxiv.org/abs/2103.00020)
- **Published:** 2021-02-26
- **Tags:** supporting

"Learning Transferable Visual Models From Natural Language Supervision" (2021) is a supporting paper for text-to-image conditioning, evaluation, or long-prompt methods.

State-of-the-art computer vision systems are trained to predict a fixed set of predetermined object categories.

This restricted form of supervision limits their generality and usability since additional labeled data is needed to specify any other visual concept.

Read as background/bridge evidence when designing length and PE policy for LLM/VLM-era generators.


### 31. PromptMoG: Enhancing Diversity in Long-Prompt Image Generation via Prompt Embedding Mixture-of-Gaussian Sampling

- **Link:** [https://arxiv.org/abs/2511.20251v1](https://arxiv.org/abs/2511.20251v1)
- **Published:** 2025-11-25
- **Tags:** long/dense preferred, LLM/VLM encoder, benchmark/eval

"PromptMoG: Enhancing Diversity in Long-Prompt Image Generation via Prompt Embedding Mixture-of-Gaussian Sampling" (2025) studies prompt rewriting, optimization, or prompt-side control for image generators.

Recent advances in text-to-image (T2I) generation have achieved remarkable visual outcomes through large-scale rectified flow models.

However, how these models behave under long prompts remains underexplored.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 32. Beyond the Prompt: Gender Bias in Text-to-Image Models, with a Case Study on Hospital Professions

- **Link:** [https://arxiv.org/abs/2510.00045v1](https://arxiv.org/abs/2510.00045v1)
- **Published:** 2025-09-27
- **Tags:** LLM/VLM encoder

"Beyond the Prompt: Gender Bias in Text-to-Image Models, with a Case Study on Hospital Professions" (2025) studies prompt rewriting, optimization, or prompt-side control for generators.

Text-to-image (TTI) models are increasingly used in professional, educational, and creative contexts, yet their outputs often embed and amplify social biases.

This paper investigates gender representation in six state-of-the-art open-weight models: HunyuanImage 2.1, HiDream-I1-dev, Qwen-Image, FLUX.1-dev, Stable-Diffusion 3.5 Large, and Stable-Diffusion-XL.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 33. Multi-Resolution Flow Matching: Training-Free Diffusion Acceleration via Staged Sampling

- **Link:** [https://arxiv.org/abs/2607.01642v1](https://arxiv.org/abs/2607.01642v1)
- **Published:** 2026-07-02
- **Tags:** re-prompt/recaption, LLM/VLM encoder

"Multi-Resolution Flow Matching: Training-Free Diffusion Acceleration via Staged Sampling" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Hardware-agnostic strategies for accelerating text-to-image diffusion, such as timestep distillation and feature caching, can reduce inference time without custom kernels or system-level optimization.

Among them, multi-resolution generation strategies have recently received broad attention, attaining more than 5x speedup without any training.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 34. TeleStyle V2: Beyond Content-Preserving Style Transfer with Self-Distillation and Distribution-Matching-Distillation

- **Link:** [https://arxiv.org/abs/2606.20709v1](https://arxiv.org/abs/2606.20709v1)
- **Published:** 2026-06-16
- **Tags:** re-prompt/recaption, LLM/VLM encoder, benchmark/eval

"TeleStyle V2: Beyond Content-Preserving Style Transfer with Self-Distillation and Distribution-Matching-Distillation" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Given a content reference and a style reference, content-preserving style transfer requires the model to generate stylized outputs with content and style consistency.

We introduced TeleStyle V1 to tackle this problem.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 35. TexTailor: Inference-Time Textual Guidance Tailoring for Multimodal Diffusion Transformers

- **Link:** [https://arxiv.org/abs/2601.02211v2](https://arxiv.org/abs/2601.02211v2)
- **Published:** 2026-01-05
- **Tags:** LLM/VLM encoder

"TexTailor: Inference-Time Textual Guidance Tailoring for Multimodal Diffusion Transformers" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Recent breakthroughs of transformer-based diffusion models, particularly with Multimodal Diffusion Transformers (MMDiT) driven models like FLUX and Qwen Image, have facilitated thrilling experiences in visual generation.

However, these models rely only on the interactions between textual conditions and visual features to produce semantically aligned images.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 36. Unify-Agent: A Unified Multimodal Agent for World-Grounded Image Synthesis

- **Link:** [https://arxiv.org/abs/2603.29620v2](https://arxiv.org/abs/2603.29620v2)
- **Published:** 2026-03-31
- **Tags:** re-prompt/recaption, benchmark/eval

"Unify-Agent: A Unified Multimodal Agent for World-Grounded Image Synthesis" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Unified multimodal models provide a natural and promising architecture for understanding diverse and complex real-world knowledge while generating high-quality images.

However, they still rely primarily on frozen parametric knowledge, which makes them struggle with real-world image generation involving long-tail and knowledge-intensive concepts.

For length policy: note its train/infer token regime, fixed vs mixed length, and any re-prompt design.


### 37. LumiGen: An LVLM-Enhanced Iterative Framework for Fine-Grained Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2508.04732v1](https://arxiv.org/abs/2508.04732v1)
- **Published:** 2025-08-05
- **Tags:** re-prompt/recaption, LLM/VLM encoder, benchmark/eval

"LumiGen: An LVLM-Enhanced Iterative Framework for Fine-Grained Text-to-Image Generation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Text-to-Image (T2I) generation has made significant advancements with diffusion models, yet challenges persist in handling complex instructions, ensuring fine-grained content control, and maintaining deep semantic consistency.

Existing T2I models often struggle with tasks like accurate text rendering, precise pose generation, or intricate compositional coherence.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 38. Meta-TTRL: A Metacognitive Framework for Self-Improving Test-Time Reinforcement Learning in Unified Multimodal Models

- **Link:** [https://arxiv.org/abs/2603.15724v1](https://arxiv.org/abs/2603.15724v1)
- **Published:** 2026-03-16
- **Tags:** LLM/VLM encoder, benchmark/eval

"Meta-TTRL: A Metacognitive Framework for Self-Improving Test-Time Reinforcement Learning in Unified Multimodal Models" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Existing test-time scaling (TTS) methods for unified multimodal models (UMMs) in text-to-image (T2I) generation primarily rely on search or sampling strategies that produce only instance-level improvements, limiting the ability to learn from prior inferences and accumulate knowledge across similar prompts.

To overcome these limitations, we propose Meta-TTRL, a metacognitive test-time reinforcement learning framework.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 39. ERNIE-Image Technical Report

- **Link:** [https://arxiv.org/abs/2605.25347v1](https://arxiv.org/abs/2605.25347v1)
- **Published:** 2026-05-25
- **Tags:** re-prompt/recaption, benchmark/eval

"ERNIE-Image Technical Report" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

We introduce ERNIE-Image, an open-source text-to-image generation model built upon an 8B single-stream DiT architecture.

ERNIE-Image aims to bridge the gap between current open-source models and leading closed-source systems through more effective mining of large-scale pre-training data and improved supervision quality throughout training.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 40. Stitch: Training-Free Position Control in Multimodal Diffusion Transformers

- **Link:** [https://arxiv.org/abs/2509.26644v1](https://arxiv.org/abs/2509.26644v1)
- **Published:** 2025-09-30
- **Tags:** LLM/VLM encoder, benchmark/eval

"Stitch: Training-Free Position Control in Multimodal Diffusion Transformers" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Text-to-Image (T2I) generation models have advanced rapidly in recent years, but accurately capturing spatial relationships like "above" or "to the right of" poses a persistent challenge.

Earlier methods improved spatial relationship following with external position control.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 41. Lumina-mGPT 2.0: Stand-Alone AutoRegressive Image Modeling

- **Link:** [https://arxiv.org/abs/2507.17801v1](https://arxiv.org/abs/2507.17801v1)
- **Published:** 2025-07-23
- **Tags:** LLM/VLM encoder, benchmark/eval

"Lumina-mGPT 2.0: Stand-Alone AutoRegressive Image Modeling" (2025) is a modern system/report in the LLM/VLM-conditioned image generation line.

We present Lumina-mGPT 2.0, a stand-alone, decoder-only autoregressive model that revisits and revitalizes the autoregressive paradigm for high-quality image generation and beyond.

Unlike existing approaches that rely on pretrained components or hybrid architectures, Lumina-mGPT 2.0 is trained entirely from scratch, enabling unrestricted architectural design and licensing freedom.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 42. PromptEcho: Annotation-Free Reward from Vision-Language Models for Text-to-Image Reinforcement Learning

- **Link:** [https://arxiv.org/abs/2604.12652v2](https://arxiv.org/abs/2604.12652v2)
- **Published:** 2026-04-14
- **Tags:** long/dense preferred, numeric token budget, LLM/VLM encoder, benchmark/eval

"PromptEcho: Annotation-Free Reward from Vision-Language Models for Text-to-Image Reinforcement Learning" (2026) studies prompt rewriting, optimization, or prompt-side control for image generators.

Reinforcement learning (RL) can improve the prompt following capability of text-to-image (T2I) models, yet obtaining high-quality reward signals remains challenging: CLIP Score is too coarse-grained, while VLM-based reward models (e.g., RewardDance) require costly human-annotated preference data and additional fine-tuning.

We propose PromptEcho, a reward construction method that requires \emph{no} annotation and \emph{no} reward model training.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 43. ITIScore: An Image-to-Text-to-Image Rating Framework for the Image Captioning Ability of MLLMs

- **Link:** [https://arxiv.org/abs/2604.03765v2](https://arxiv.org/abs/2604.03765v2)
- **Published:** 2026-04-04
- **Tags:** long/dense preferred, LLM/VLM encoder, benchmark/eval

"ITIScore: An Image-to-Text-to-Image Rating Framework for the Image Captioning Ability of MLLMs" (2026) focuses on captioning/recaptioning data that feeds text-to-image training.

Recent advances in multimodal large language models (MLLMs) have greatly improved image understanding and captioning capabilities.

However, existing image captioning benchmarks typically suffer from limited diversity in caption length, the absence of recent advanced MLLMs, and insufficient human annotations, which potentially introduces bias and limits the ability to comprehensively assess the performance of modern MLLMs.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 44. TextAlign: Preference Alignment for Text Rendering with Hierarchical Rewards

- **Link:** [https://arxiv.org/abs/2605.19320v2](https://arxiv.org/abs/2605.19320v2)
- **Published:** 2026-05-19
- **Tags:** LLM/VLM encoder

"TextAlign: Preference Alignment for Text Rendering with Hierarchical Rewards" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Faithful text rendering remains a persistent weakness of large text-to-image generative models, as it requires both semantic instruction following and fine-grained glyph-level structure.

Prior methods often improve this ability through architecture-specific modules or encoder modifications, which complicate deployment across foundation models.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 45. FreeText: Training-Free Text Rendering in Diffusion Transformers via Attention Localization and Spectral Glyph Injection

- **Link:** [https://arxiv.org/abs/2601.00535v1](https://arxiv.org/abs/2601.00535v1)
- **Published:** 2026-01-02
- **Tags:** LLM/VLM encoder, benchmark/eval

"FreeText: Training-Free Text Rendering in Diffusion Transformers via Attention Localization and Spectral Glyph Injection" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Large-scale text-to-image (T2I) diffusion models excel at open-domain synthesis but still struggle with precise text rendering, especially for multi-line layouts, dense typography, and long-tailed scripts such as Chinese.

Prior solutions typically require costly retraining or rigid external layout constraints, which can degrade aesthetics and limit flexibility.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 46. A Decomposable Probe for Few-Step Diffusion Models: Prompt, Latent, and Score Selectivity across Backbone Families and Distillation Paradigms

- **Link:** [https://arxiv.org/abs/2607.03256v1](https://arxiv.org/abs/2607.03256v1)
- **Published:** 2026-07-03
- **Tags:** benchmark/eval

"A Decomposable Probe for Few-Step Diffusion Models: Prompt, Latent, and Score Selectivity across Backbone Families and Distillation Paradigms" (2026) studies prompt rewriting, optimization, or prompt-side control for generators.

Few-step distilled diffusion students cut text-to-image inference from ~50 to 1-8 network evaluations, but the quality gap is usually summarised by a single FID/CLIP scalar that cannot say which axis of the conditioning response changed, nor whether a behaviour comes from the architecture, the distillation objective, or simply from bei...

We replace the scalar with a decomposable probe that injects controlled perturbations along three layers (prompt encoder, denoiser input, denoiser output) under three modes (mean, variance, scale) and six strengths, reporting a bootstrap-median Bures W2^2 selectivity ratio on Inception features.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 47. Enhancing Diffusion-Based Quantitatively Controllable Image Generation via Matrix-Form EDM and Adaptive Vicinal Training

- **Link:** [https://arxiv.org/abs/2602.02114v1](https://arxiv.org/abs/2602.02114v1)
- **Published:** 2026-02-02
- **Tags:** numeric token budget, LLM/VLM encoder, benchmark/eval

"Enhancing Diffusion-Based Quantitatively Controllable Image Generation via Matrix-Form EDM and Adaptive Vicinal Training" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Continuous Conditional Diffusion Model (CCDM) is a diffusion-based framework designed to generate high-quality images conditioned on continuous regression labels.

Although CCDM has demonstrated clear advantages over prior approaches across a range of datasets, it still exhibits notable limitations and has recently been surpassed by a GAN-based method, namely CcGAN-AVAR.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 48. DeepGen 1.0: A Lightweight Unified Multimodal Model for Advancing Image Generation and Editing

- **Link:** [https://arxiv.org/abs/2602.12205v2](https://arxiv.org/abs/2602.12205v2)
- **Published:** 2026-02-12
- **Tags:** LLM/VLM encoder, benchmark/eval

"DeepGen 1.0: A Lightweight Unified Multimodal Model for Advancing Image Generation and Editing" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Current unified multimodal models for image generation and editing typically rely on massive parameter scales (e.g., >10B), entailing prohibitive training costs and deployment footprints.

In this work, we present DeepGen 1.0, a lightweight 5B unified model that achieves comprehensive capabilities competitive with or surpassing much larger counterparts.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 49. RePrompt: Reasoning-Augmented Reprompting for Text-to-Image Generation via Reinforcement Learning

- **Link:** [https://arxiv.org/abs/2505.17540v1](https://arxiv.org/abs/2505.17540v1)
- **Published:** 2025-05-23
- **Tags:** re-prompt/recaption, LLM/VLM encoder

"RePrompt: Reasoning-Augmented Reprompting for Text-to-Image Generation via Reinforcement Learning" (2025) studies prompt rewriting, optimization, or prompt-side control for image generators.

Despite recent progress in text-to-image (T2I) generation, existing models often struggle to faithfully capture user intentions from short and under-specified prompts.

While prior work has attempted to enhance prompts using large language models (LLMs), these methods frequently generate stylistic or unrealistic content due to insufficient grounding in visual semantics and real-world composition.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 50. RICO: Improving Accuracy and Completeness in Image Recaptioning via Visual Reconstruction

- **Link:** [https://arxiv.org/abs/2505.22613v1](https://arxiv.org/abs/2505.22613v1)
- **Published:** 2025-05-28
- **Tags:** re-prompt/recaption, LLM/VLM encoder

"RICO: Improving Accuracy and Completeness in Image Recaptioning via Visual Reconstruction" (2025) focuses on captioning/recaptioning data that feeds text-to-image training.

Image recaptioning is widely used to generate training datasets with enhanced quality for various multimodal tasks.

Existing recaptioning methods typically rely on powerful multimodal large language models (MLLMs) to enhance textual descriptions, but often suffer from inaccuracies due to hallucinations and incompleteness caused by missing fine-grained details.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 51. UniGenBench++: A Unified Semantic Evaluation Benchmark for Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2510.18701v2](https://arxiv.org/abs/2510.18701v2)
- **Published:** 2025-10-21
- **Tags:** variable/mixed length, LLM/VLM encoder, benchmark/eval

"UniGenBench++: A Unified Semantic Evaluation Benchmark for Text-to-Image Generation" (2025) introduces or expands evaluation for text-conditioned image generation, often under long or compositional prompts.

Recent progress in text-to-image (T2I) generation underscores the importance of reliable benchmarks in evaluating how accurately generated images reflect the semantics of their textual prompt.

However, (1) existing benchmarks lack the diversity of prompt scenarios and multilingual support, both essential for real-world applicability; (2) they offer only coarse evaluations across primary dimensions, covering a narrow range of sub-dimensions, and fall short in fine-grained sub-dimension assessment.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 52. Guiding Diffusion Models with Semantically Degraded Conditions

- **Link:** [https://arxiv.org/abs/2603.10780v1](https://arxiv.org/abs/2603.10780v1)
- **Published:** 2026-03-11
- **Tags:** LLM/VLM encoder

"Guiding Diffusion Models with Semantically Degraded Conditions" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Classifier-Free Guidance (CFG) is a cornerstone of modern text-to-image models, yet its reliance on a semantically vacuous null prompt ($\varnothing$) generates a guidance signal prone to geometric entanglement.

This is a key factor limiting its precision, leading to well-documented failures in complex compositional tasks.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 53. CFG-Ctrl: Control-Based Classifier-Free Diffusion Guidance

- **Link:** [https://arxiv.org/abs/2603.03281v2](https://arxiv.org/abs/2603.03281v2)
- **Published:** 2026-03-03
- **Tags:** LLM/VLM encoder

"CFG-Ctrl: Control-Based Classifier-Free Diffusion Guidance" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Classifier-Free Guidance (CFG) has emerged as a central approach for enhancing semantic alignment in flow-based diffusion models.

In this paper, we explore a unified framework called CFG-Ctrl, which reinterprets CFG as a control applied to the first-order continuous-time generative flow, using the conditional-unconditional discrepancy as an error signal to adjust the velocity field.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 54. APE: Agentic Prompt Enhancer for Image Generation and Editing

- **Link:** [https://arxiv.org/abs/2606.00204v1](https://arxiv.org/abs/2606.00204v1)
- **Published:** 2026-05-29
- **Tags:** re-prompt/recaption, LLM/VLM encoder, benchmark/eval

"APE: Agentic Prompt Enhancer for Image Generation and Editing" (2026) studies prompt rewriting, optimization, or prompt-side control for generators.

Natural language has become a powerful interface for image generation and editing, yet text-guided visual systems remain highly sensitive to prompt formulation.

Semantically similar requests can produce different outputs depending on wording, specificity, and how explicitly visual constraints are stated, motivating prompt enhancement as a trainable component rather than a peripheral user choice.

For length policy: note its train/infer token regime, fixed vs mixed length, and any re-prompt design.


### 55. Omni-Dish: Photorealistic and Faithful Image Generation and Editing for Arbitrary Chinese Dishes

- **Link:** [https://arxiv.org/abs/2504.09948v3](https://arxiv.org/abs/2504.09948v3)
- **Published:** 2025-04-14
- **Tags:** re-prompt/recaption

"Omni-Dish: Photorealistic and Faithful Image Generation and Editing for Arbitrary Chinese Dishes" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Dish images play a crucial role in the digital era, with the demand for culturally distinctive dish images continuously increasing due to the digitization of the food industry and e-commerce.

In general cases, existing text-to-image generation models excel in producing high-quality images; however, they struggle to capture diverse characteristics and faithful details of specific domains, particularly Chinese dishes.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 56. Understanding-in-Generation: Reinforcing Generative Capability of Unified Model via Infusing Understanding into Generation

- **Link:** [https://arxiv.org/abs/2509.18639v3](https://arxiv.org/abs/2509.18639v3)
- **Published:** 2025-09-23
- **Tags:** long/dense preferred, benchmark/eval

"Understanding-in-Generation: Reinforcing Generative Capability of Unified Model via Infusing Understanding into Generation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Recent works have made notable advancements in enhancing unified models for text-to-image generation through the Chain-of-Thought (CoT).

However, these reasoning methods separate the processes of understanding and generation, which limits their ability to guide the reasoning of unified models in addressing the deficiencies of their generative capabilities.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 57. FullFlow: Upgrading Text-to-Image Flow Matching Models for Bidirectional Vision--Language Generation

- **Link:** [https://arxiv.org/abs/2605.20316v1](https://arxiv.org/abs/2605.20316v1)
- **Published:** 2026-05-19

"FullFlow: Upgrading Text-to-Image Flow Matching Models for Bidirectional Vision--Language Generation" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Modern text-to-image diffusion models encode rich visual priors, but expose them only through one-way text-conditioned generation.

Existing unified vision--language models derived from them recover bidirectional capability through large-scale joint pretraining or substantial retraining of the text pathway, discarding the strong image prior the text-to-image backbone already encodes.

Keep it as background on modern generation/evaluation; use only if its data or metrics inform caption-length decisions.


### 58. Stable Velocity: A Variance Perspective on Flow Matching

- **Link:** [https://arxiv.org/abs/2602.05435v2](https://arxiv.org/abs/2602.05435v2)
- **Published:** 2026-02-05
- **Tags:** numeric token budget, LLM/VLM encoder

"Stable Velocity: A Variance Perspective on Flow Matching" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

While flow matching is elegant, its reliance on single-sample conditional velocities leads to high-variance training targets that destabilize optimization and slow convergence.

By explicitly characterizing this variance, we identify 1) a high-variance regime near the prior, where optimization is challenging, and 2) a low-variance regime near the data distribution, where conditional and marginal velocities nearly coincide.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 59. Obliviate: Erasing Concepts from Autoregressive Image Generation Models

- **Link:** [https://arxiv.org/abs/2606.28643v1](https://arxiv.org/abs/2606.28643v1)
- **Published:** 2026-06-26
- **Tags:** benchmark/eval

"Obliviate: Erasing Concepts from Autoregressive Image Generation Models" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

The widespread adoption of generative AI models has intensified concerns about misuse, including the creation of unsafe or disturbing imagery.

To mitigate such issues, several concept erasure approaches have been proposed to remove harmful content from multimodal generative models.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 60. Think-Then-Generate: Reasoning-Aware Text-to-Image Diffusion with LLM Encoders

- **Link:** [https://arxiv.org/abs/2601.10332v1](https://arxiv.org/abs/2601.10332v1)
- **Published:** 2026-01-15
- **Tags:** re-prompt/recaption, LLM/VLM encoder, benchmark/eval

"Think-Then-Generate: Reasoning-Aware Text-to-Image Diffusion with LLM Encoders" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Recent progress in text-to-image (T2I) diffusion models (DMs) has enabled high-quality visual synthesis from diverse textual prompts.

Yet, most existing T2I DMs, even those equipped with large language model (LLM)-based text encoders, remain text-pixel mappers -- they employ LLMs merely as text encoders, without leveraging their inherent reasoning capabilities to infer what should be visually depicted given the textual prompt.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 61. Reason2Attack: Jailbreaking Text-to-Image Models via LLM Reasoning

- **Link:** [https://arxiv.org/abs/2503.17987v3](https://arxiv.org/abs/2503.17987v3)
- **Published:** 2025-03-23
- **Tags:** LLM/VLM encoder

"Reason2Attack: Jailbreaking Text-to-Image Models via LLM Reasoning" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Text-to-Image(T2I) models typically deploy safety filters to prevent the generation of sensitive images.

Unfortunately, recent jailbreaking attack methods manually design instructions for the LLM to generate adversarial prompts, which effectively bypass safety filters while producing sensitive images, exposing safety vulnerabilities of T2I models.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 62. Harnessing Caption Detailness for Data-Efficient Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2505.15172v1](https://arxiv.org/abs/2505.15172v1)
- **Published:** 2025-05-21
- **Tags:** long/dense preferred, benchmark/eval

"Harnessing Caption Detailness for Data-Efficient Text-to-Image Generation" (2025) focuses on captioning/recaptioning data that feeds text-to-image training.

Training text-to-image (T2I) models with detailed captions can significantly improve their generation quality.

Existing methods often rely on simplistic metrics like caption length to represent the detailness of the caption in the T2I training set.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 63. TIIF-Bench: How Does Your T2I Model Follow Your Instructions?

- **Link:** [https://arxiv.org/abs/2506.02161v3](https://arxiv.org/abs/2506.02161v3)
- **Published:** 2025-06-02
- **Tags:** LLM/VLM encoder, benchmark/eval

"TIIF-Bench: How Does Your T2I Model Follow Your Instructions?" (2025) introduces or expands evaluation for text-conditioned image generation, often under long or compositional prompts.

The rapid advancements of Text-to-Image (T2I) models have ushered in a new phase of AI-generated content, marked by their growing ability to interpret and follow user instructions.

However, existing T2I model evaluation benchmarks fall short in limited prompt diversity and complexity, as well as coarse evaluation metrics, making it difficult to evaluate the fine-grained alignment performance between textual instructions and generated images.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 64. BlindSight: Harnessing Sparsity for Efficient Vision-Language Models

- **Link:** [https://arxiv.org/abs/2507.09071v3](https://arxiv.org/abs/2507.09071v3)
- **Published:** 2025-07-11
- **Tags:** numeric token budget, LLM/VLM encoder, benchmark/eval

"BlindSight: Harnessing Sparsity for Efficient Vision-Language Models" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Large vision-language models (VLMs) enable joint processing of text and images.

However, incorporating vision data significantly increases the prompt length, resulting in a longer time to first token (TTFT).

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 65. Score Distillation of Flow Matching Models

- **Link:** [https://arxiv.org/abs/2509.25127v2](https://arxiv.org/abs/2509.25127v2)
- **Published:** 2025-09-29

"Score Distillation of Flow Matching Models" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Diffusion models achieve high-quality image generation but are limited by slow iterative sampling.

Distillation methods alleviate this by enabling one- or few-step generation.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 66. SafeRoPE: Risk-specific Head-wise Embedding Rotation for Safe Generation in Rectified Flow Transformers

- **Link:** [https://arxiv.org/abs/2604.01826v1](https://arxiv.org/abs/2604.01826v1)
- **Published:** 2026-04-02

"SafeRoPE: Risk-specific Head-wise Embedding Rotation for Safe Generation in Rectified Flow Transformers" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Recent Text-to-Image (T2I) models based on rectified-flow transformers (e.g., SD3, FLUX) achieve high generative fidelity but remain vulnerable to unsafe semantics, especially when triggered by multi-token interactions.

Existing mitigation methods largely rely on fine-tuning or attention modulation for concept unlearning; however, their expensive computational overhead and design tailored to U-Net-based denoisers hinder direct adaptation to transformer-based diffusion models (e.g., MMDiT).

Keep it as background on modern generation/evaluation; use only if its data or metrics inform caption-length decisions.


### 67. Seedream 2.0: A Native Chinese-English Bilingual Image Generation Foundation Model

- **Link:** [https://arxiv.org/abs/2503.07703v1](https://arxiv.org/abs/2503.07703v1)
- **Published:** 2025-03-10

"Seedream 2.0: A Native Chinese-English Bilingual Image Generation Foundation Model" (2025) is a modern system/report in the LLM/VLM-conditioned image generation line.

Rapid advancement of diffusion models has catalyzed remarkable progress in the field of image generation.

However, prevalent models such as Flux, SD3.5 and Midjourney, still grapple with issues like model bias, limited text rendering capabilities, and insufficient understanding of Chinese cultural nuances.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 68. Stable Score Distillation

- **Link:** [https://arxiv.org/abs/2507.09168v1](https://arxiv.org/abs/2507.09168v1)
- **Published:** 2025-07-12
- **Tags:** re-prompt/recaption

"Stable Score Distillation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Text-guided image and 3D editing have advanced with diffusion-based models, yet methods like Delta Denoising Score often struggle with stability, spatial control, and editing strength.

These limitations stem from reliance on complex auxiliary structures, which introduce conflicting optimization signals and restrict precise, localized edits.

For length policy: note its train/infer token regime, fixed vs mixed length, and any re-prompt design.


### 69. ZIPP:Zero-shot Image Personalization from Personas

- **Link:** [https://arxiv.org/abs/2606.08841v1](https://arxiv.org/abs/2606.08841v1)
- **Published:** 2026-06-07
- **Tags:** re-prompt/recaption, LLM/VLM encoder, benchmark/eval

"ZIPP:Zero-shot Image Personalization from Personas" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Text-to-image diffusion models are increasingly deployed in open-ended creative contexts, yet their outputs remain impersonal, optimized for aggregate aesthetics rather than individual taste.

Human preferences are pluralistic: one user favoring muted, nostalgic portraits may prefer vibrant street photography, while another gravitates toward dreamy film aesthetics.

For length policy: note its train/infer token regime, fixed vs mixed length, and any re-prompt design.


### 70. MMaDA: Multimodal Large Diffusion Language Models

- **Link:** [https://arxiv.org/abs/2505.15809v2](https://arxiv.org/abs/2505.15809v2)
- **Published:** 2025-05-21
- **Tags:** variable/mixed length, LLM/VLM encoder

"MMaDA: Multimodal Large Diffusion Language Models" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

We introduce MMaDA, a novel class of multimodal diffusion foundation models designed to achieve superior performance across diverse domains such as textual reasoning, multimodal understanding, and text-to-image generation.

The approach is distinguished by three key innovations: (i) MMaDA adopts a unified diffusion architecture with a shared probabilistic formulation and a modality-agnostic design, eliminating the need for modality-specific components.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 71. Are Image-to-Video Models Good Zero-Shot Image Editors?

- **Link:** [https://arxiv.org/abs/2511.19435v2](https://arxiv.org/abs/2511.19435v2)
- **Published:** 2025-11-24
- **Tags:** re-prompt/recaption, benchmark/eval

"Are Image-to-Video Models Good Zero-Shot Image Editors?" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Large-scale video diffusion models show strong world simulation and temporal reasoning abilities, but their use as zero-shot image editors remains underexplored.

We introduce IF-Edit, a tuning-free framework that repurposes pretrained image-to-video diffusion models for instruction-driven image editing.

For length policy: note its train/infer token regime, fixed vs mixed length, and any re-prompt design.


### 72. Identity-Preserving Text-to-Video Generation via Training-Free Prompt, Image, and Guidance Enhancement

- **Link:** [https://arxiv.org/abs/2509.01362v1](https://arxiv.org/abs/2509.01362v1)
- **Published:** 2025-09-01
- **Tags:** re-prompt/recaption, benchmark/eval

"Identity-Preserving Text-to-Video Generation via Training-Free Prompt, Image, and Guidance Enhancement" (2025) studies prompt rewriting, optimization, or prompt-side control for generators.

Identity-preserving text-to-video (IPT2V) generation creates videos faithful to both a reference subject image and a text prompt.

While fine-tuning large pretrained video diffusion models on ID-matched data achieves state-of-the-art results on IPT2V, data scarcity and high tuning costs hinder broader improvement.

For length policy: note its train/infer token regime, fixed vs mixed length, and any re-prompt design.


### 73. Vision-Free Retrieval: Rethinking Multimodal Search with Textual Scene Descriptions

- **Link:** [https://arxiv.org/abs/2509.19203v1](https://arxiv.org/abs/2509.19203v1)
- **Published:** 2025-09-23
- **Tags:** long/dense preferred, LLM/VLM encoder, benchmark/eval

"Vision-Free Retrieval: Rethinking Multimodal Search with Textual Scene Descriptions" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Contrastively-trained Vision-Language Models (VLMs), such as CLIP, have become the standard approach for learning discriminative vision-language representations.

However, these models often exhibit shallow language understanding, manifesting bag-of-words behaviour.

For length policy: note its train/infer token regime, fixed vs mixed length, and any re-prompt design.


### 74. SPOT: Selective Prompt Projection via Total Variation for Inference-Only Safe Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2602.00616v3](https://arxiv.org/abs/2602.00616v3)
- **Published:** 2026-01-31
- **Tags:** re-prompt/recaption, LLM/VLM encoder, benchmark/eval

"SPOT: Selective Prompt Projection via Total Variation for Inference-Only Safe Text-to-Image Generation" (2026) studies prompt rewriting, optimization, or prompt-side control for image generators.

Text-to-Image (T2I) diffusion models enable high quality open ended synthesis, but practical use requires suppressing unsafe generations while preserving behavior on benign prompts.

We study this tension relative to the frozen generator, using its prompt conditioned distribution as the preservation reference.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 75. Exploring Multimodal Diffusion Transformers for Enhanced Prompt-based Image Editing

- **Link:** [https://arxiv.org/abs/2508.07519v1](https://arxiv.org/abs/2508.07519v1)
- **Published:** 2025-08-11

"Exploring Multimodal Diffusion Transformers for Enhanced Prompt-based Image Editing" (2025) studies prompt rewriting, optimization, or prompt-side control for generators.

Transformer-based diffusion models have recently superseded traditional U-Net architectures, with multimodal diffusion transformers (MM-DiT) emerging as the dominant approach in state-of-the-art models like Stable Diffusion 3 and Flux.1.

Previous approaches have relied on unidirectional cross-attention mechanisms, with information flowing from text embeddings to image latents.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 76. CFG-Zero*: Improved Classifier-Free Guidance for Flow Matching Models

- **Link:** [https://arxiv.org/abs/2503.18886v2](https://arxiv.org/abs/2503.18886v2)
- **Published:** 2025-03-24

"CFG-Zero*: Improved Classifier-Free Guidance for Flow Matching Models" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Classifier-Free Guidance (CFG) is a widely adopted technique in diffusion/flow models to improve image fidelity and controllability.

In this work, we first analytically study the effect of CFG on flow matching models trained on Gaussian mixtures where the ground-truth flow can be derived.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 77. Efficient Scaling of Diffusion Transformers for Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2412.12391v1](https://arxiv.org/abs/2412.12391v1)
- **Published:** 2024-12-16
- **Tags:** long/dense preferred

"Efficient Scaling of Diffusion Transformers for Text-to-Image Generation" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

We empirically study the scaling properties of various Diffusion Transformers (DiTs) for text-to-image generation by performing extensive and rigorous ablations, including training scaled DiTs ranging from 0.3B upto 8B parameters on datasets up to 600M images.

We find that U-ViT, a pure self-attention based DiT model provides a simpler design and scales more effectively in comparison with cross-attention based DiT variants, which allows straightforward expansion for extra conditions and other modalities.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 78. Learning Sampling Parameters for Diffusion Models

- **Link:** [https://arxiv.org/abs/2607.23488v1](https://arxiv.org/abs/2607.23488v1)
- **Published:** 2026-07-26
- **Tags:** LLM/VLM encoder, benchmark/eval

"Learning Sampling Parameters for Diffusion Models" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Text-to-image diffusion models expose many inference-time sampling parameters, including prompts, negative prompts, classifier-free guidance scales, and noise schedules.

These parameters are typically manually chosen once and then held fixed across prompts and denoising timesteps, even though different prompts and stages of generation can benefit from different parameter values.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 79. PIPBench: A Profile-Inclusive Framework for Personalized Image Generation Evaluation

- **Link:** [https://arxiv.org/abs/2607.06440v1](https://arxiv.org/abs/2607.06440v1)
- **Published:** 2026-07-07
- **Tags:** benchmark/eval

"PIPBench: A Profile-Inclusive Framework for Personalized Image Generation Evaluation" (2026) evaluates text-conditioned image generation, often under long or compositional prompts.

Recent text-to-image models such as DALLE-3 excel at following diverse prompts yet remain blind to individual aesthetic preferences.

We study personalized image generation, where models must align outputs with a user's implicit visual preferences based on a few historically preferred images and a short prompt.

For length policy: note its train/infer token regime, fixed vs mixed length, and any re-prompt design.


### 80. KG-FairDiff: Knowledge Graph-Guided Prompt Refinement for Demographically Fair Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2606.01282v1](https://arxiv.org/abs/2606.01282v1)
- **Published:** 2026-05-31
- **Tags:** re-prompt/recaption, LLM/VLM encoder, benchmark/eval

"KG-FairDiff: Knowledge Graph-Guided Prompt Refinement for Demographically Fair Text-to-Image Generation" (2026) studies prompt rewriting, optimization, or prompt-side control for generators.

Text-to-Image (TTI) systems are now everyday infrastructure for journalism, education, advertising, and public communication, and the demographic and cultural stereotypes they inherit from training data (rendering women, people of colour, older adults, and non-Western cultures as under-represented or caricatured) become a population-le...

Existing mitigations either require costly retraining, infeasible for the closed-source backbones that dominate consumer products, or rely on fixed demographic templates that ignore cultural context.

For length policy: note its train/infer token regime, fixed vs mixed length, and any re-prompt design.


### 81. CLIP Is Shortsighted: Paying Attention Beyond the First Sentence

- **Link:** [https://arxiv.org/abs/2602.22419v2](https://arxiv.org/abs/2602.22419v2)
- **Published:** 2026-02-25
- **Tags:** long/dense preferred, LLM/VLM encoder

"CLIP Is Shortsighted: Paying Attention Beyond the First Sentence" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

CLIP models learn transferable multi-modal features via image-text contrastive learning on internet-scale data.

They are widely used in zero-shot classification, multi-modal retrieval, text-to-image diffusion, and as image encoders in large vision-language models.

For length policy: note its train/infer token regime, fixed vs mixed length, and any re-prompt design.


### 82. Unsafe2Safe: Controllable Image Anonymization for Downstream Utility

- **Link:** [https://arxiv.org/abs/2603.28605v1](https://arxiv.org/abs/2603.28605v1)
- **Published:** 2026-03-30
- **Tags:** re-prompt/recaption, benchmark/eval

"Unsafe2Safe: Controllable Image Anonymization for Downstream Utility" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Large-scale image datasets frequently contain identifiable or sensitive content, raising privacy risks when training models that may memorize and leak such information.

We present Unsafe2Safe, a fully automated pipeline that detects privacy-prone images and rewrites only their sensitive regions using multimodally guided diffusion editing.

For length policy: note its train/infer token regime, fixed vs mixed length, and any re-prompt design.


### 83. Mastering Text-to-Image Diffusion: Recaptioning, Planning, and Generating with Multimodal LLMs

- **Link:** [https://arxiv.org/abs/2401.11708v3](https://arxiv.org/abs/2401.11708v3)
- **Published:** 2024-01-22
- **Tags:** re-prompt/recaption, LLM/VLM encoder

"Mastering Text-to-Image Diffusion: Recaptioning, Planning, and Generating with Multimodal LLMs" (2024) focuses on captioning/recaptioning data that feeds text-to-image training.

Diffusion models have exhibit exceptional performance in text-to-image generation and editing.

However, existing methods often face challenges when handling complex text prompts that involve multiple objects with multiple attributes and relationships.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 84. RealGen: Photorealistic Text-to-Image Generation via Detector-Guided Rewards

- **Link:** [https://arxiv.org/abs/2512.00473v1](https://arxiv.org/abs/2512.00473v1)
- **Published:** 2025-11-29
- **Tags:** LLM/VLM encoder, benchmark/eval

"RealGen: Photorealistic Text-to-Image Generation via Detector-Guided Rewards" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

With the continuous advancement of image generation technology, advanced models such as GPT-Image-1 and Qwen-Image have achieved remarkable text-to-image consistency and world knowledge However, these models still fall short in photorealistic image generation.

Even on simple T2I tasks, they tend to produce " fake" images with distinct AI artifacts, often characterized by "overly smooth skin" and "oily facial sheens".

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 85. On Discrete Prompt Optimization for Diffusion Models

- **Link:** [https://arxiv.org/abs/2407.01606v1](https://arxiv.org/abs/2407.01606v1)
- **Published:** 2024-06-27
- **Tags:** re-prompt/recaption, benchmark/eval

"On Discrete Prompt Optimization for Diffusion Models" (2024) studies prompt rewriting, optimization, or prompt-side control for generators.

This paper introduces the first gradient-based framework for prompt optimization in text-to-image diffusion models.

We formulate prompt engineering as a discrete optimization problem over the language space.

For length policy: note its train/infer token regime, fixed vs mixed length, and any re-prompt design.


### 86. PiD: Fast and High-Resolution Latent Decoding with Pixel Diffusion

- **Link:** [https://arxiv.org/abs/2605.23902v1](https://arxiv.org/abs/2605.23902v1)
- **Published:** 2026-05-22
- **Tags:** re-prompt/recaption, numeric token budget

"PiD: Fast and High-Resolution Latent Decoding with Pixel Diffusion" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Most practical high-resolution text-to-image systems, including latent diffusion and autoregressive models, perform generation in a compact latent space, and a decoder maps the generated latents back to pixels.

Yet the latent-to-pixel decoder is reconstruction-oriented, optimized to invert the encoder rather than synthesize more details, and becomes increasingly costly at megapixel scale.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 87. Robust and Generalizable Safety Steering for Text-to-Image Diffusion Transformers

- **Link:** [https://arxiv.org/abs/2605.30049v1](https://arxiv.org/abs/2605.30049v1)
- **Published:** 2026-05-28

"Robust and Generalizable Safety Steering for Text-to-Image Diffusion Transformers" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Diffusion Transformers have become a powerful backbone for text-to-image generation, but their layered and cross-modal generation process makes safety control fundamentally different from prompt-level filtering or output-level detection.

Harmful semantics may be weakly expressed in text representations, progressively bound to visual latents, and finally entangled with rendering dynamics.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 88. Prompt Reinjection: Alleviating Prompt Forgetting in Multimodal Diffusion Transformers

- **Link:** [https://arxiv.org/abs/2602.06886v4](https://arxiv.org/abs/2602.06886v4)
- **Published:** 2026-02-06

"Prompt Reinjection: Alleviating Prompt Forgetting in Multimodal Diffusion Transformers" (2026) studies prompt rewriting, optimization, or prompt-side control for generators.

Multimodal Diffusion Transformers (MMDiTs) for text-to-image generation maintain separate text and image branches, with bidirectional information flow between text tokens and visual latents throughout denoising.

In this setting, we observe a prompt forgetting phenomenon: the semantics of the prompt representation in the text branch is progressively forgotten as depth increases.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 89. UltraFlux: Data-Model Co-Design for High-quality Native 4K Text-to-Image Generation across Diverse Aspect Ratios

- **Link:** [https://arxiv.org/abs/2511.18050v1](https://arxiv.org/abs/2511.18050v1)
- **Published:** 2025-11-22
- **Tags:** LLM/VLM encoder, benchmark/eval

"UltraFlux: Data-Model Co-Design for High-quality Native 4K Text-to-Image Generation across Diverse Aspect Ratios" (2025) is a modern system/report in the LLM/VLM-conditioned image generation line.

Diffusion transformers have recently delivered strong text-to-image generation around 1K resolution, but we show that extending them to native 4K across diverse aspect ratios exposes a tightly coupled failure mode spanning positional encoding, VAE compression, and optimization.

Tackling any of these factors in isolation leaves substantial quality on the table.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 90. SANA: Efficient High-Resolution Image Synthesis with Linear Diffusion Transformers

- **Link:** [https://arxiv.org/abs/2410.10629v3](https://arxiv.org/abs/2410.10629v3)
- **Published:** 2024-10-14
- **Tags:** LLM/VLM encoder

"SANA: Efficient High-Resolution Image Synthesis with Linear Diffusion Transformers" (2024) is a modern system/report in the LLM/VLM-conditioned image generation line.

We introduce Sana, a text-to-image framework that can efficiently generate images up to 4096$\times$4096 resolution.

Sana can synthesize high-resolution, high-quality images with strong text-image alignment at a remarkably fast speed, deployable on laptop GPU.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 91. One Rewrite to Fix Them All? Type-Aware Repair Allocation for Text-to-Image Prompt Optimization

- **Link:** [https://arxiv.org/abs/2607.18724v1](https://arxiv.org/abs/2607.18724v1)
- **Published:** 2026-07-21
- **Tags:** re-prompt/recaption, benchmark/eval

"One Rewrite to Fix Them All? Type-Aware Repair Allocation for Text-to-Image Prompt Optimization" (2026) studies prompt rewriting, optimization, or prompt-side control for image generators.

Text-to-image (T2I) generators often fail to follow their prompts faithfully, producing wrong counts, swapped attributes, ambiguous relations, and illegible text.

Prompt optimization repairs such failures by rewriting the user prompt, requiring no generator retraining, and has yielded promising results.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 92. Arena-T2I Hard: Benchmarking and Improving Faithfulness with Dependency-Aware Checklist

- **Link:** [https://arxiv.org/abs/2606.31711v1](https://arxiv.org/abs/2606.31711v1)
- **Published:** 2026-06-30
- **Tags:** LLM/VLM encoder, benchmark/eval

"Arena-T2I Hard: Benchmarking and Improving Faithfulness with Dependency-Aware Checklist" (2026) evaluates text-conditioned image generation, often under long or compositional prompts.

Faithfulness -- how precisely a generated image aligns with its prompt -- is increasingly central to the real-world utility of text-to-image (T2I) models.

Existing faithfulness benchmarks, however, rely on simple atomic instructions, on which top-tier systems already achieve near-perfect scores.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 93. BAFIS: Dataset + Framework to assess occupational Bias and Human Preference in modern Text-to-image Models

- **Link:** [https://arxiv.org/abs/2606.20241v1](https://arxiv.org/abs/2606.20241v1)
- **Published:** 2026-06-18
- **Tags:** benchmark/eval

"BAFIS: Dataset + Framework to assess occupational Bias and Human Preference in modern Text-to-image Models" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Generative artificial intelligence has the potential to improve productivity and transform the production of creative content.

However, existing research indicates that image generation models are significantly influenced by biases.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 94. Imagine Before You Draw: Visual Prompt Engineering for Image Generation

- **Link:** [https://arxiv.org/abs/2606.04457v1](https://arxiv.org/abs/2606.04457v1)
- **Published:** 2026-06-03

"Imagine Before You Draw: Visual Prompt Engineering for Image Generation" (2026) studies prompt rewriting, optimization, or prompt-side control for generators.

Incorporating visual semantic representations as an intermediate step before image generation can reduce the modeling difficulty between text and images, thereby improving generation quality.

Recent works such as X-Omni and BLIP3o-Next have explored this direction, but they typically use a two-stage external pipeline: a separate autoregressive model first generates semantic tokens, which are then fed as conditioning to an independent diffusion decoder.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 95. Beyond Text Prompts: Visual-to-Visual Generation as A Unified Paradigm

- **Link:** [https://arxiv.org/abs/2605.12271v2](https://arxiv.org/abs/2605.12271v2)
- **Published:** 2026-05-12
- **Tags:** LLM/VLM encoder, benchmark/eval

"Beyond Text Prompts: Visual-to-Visual Generation as A Unified Paradigm" (2026) studies prompt rewriting, optimization, or prompt-side control for generators.

Humans often specify and create through visual artifacts: typography sheets, sketches, reference images, and annotated scenes.

Yet modern visual generators still ask users to serialize this intent into text, a bottleneck that compresses signals like spatial structure, exact appearance, and glyph shape.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 96. Let Triggers Control: Frequency-Aware Dropout for Effective Token Control

- **Link:** [https://arxiv.org/abs/2603.27199v1](https://arxiv.org/abs/2603.27199v1)
- **Published:** 2026-03-28
- **Tags:** LLM/VLM encoder

"Let Triggers Control: Frequency-Aware Dropout for Effective Token Control" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Text-to-image models such as Stable Diffusion have achieved unprecedented levels of high-fidelity visual synthesis.

As these models advance, personalization of generative models -- commonly facilitated through Low-Rank Adaptation (LoRA) with a dedicated trigger token -- has become a significant area of research.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 97. EruDiff: Refactoring Knowledge in Diffusion Models for Advanced Text-to-Image Synthesis

- **Link:** [https://arxiv.org/abs/2603.20828v1](https://arxiv.org/abs/2603.20828v1)
- **Published:** 2026-03-21
- **Tags:** LLM/VLM encoder, benchmark/eval

"EruDiff: Refactoring Knowledge in Diffusion Models for Advanced Text-to-Image Synthesis" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Text-to-image diffusion models have achieved remarkable fidelity in synthesizing images from explicit text prompts, yet exhibit a critical deficiency in processing implicit prompts that require deep-level world knowledge, ranging from natural sciences to cultural commonsense, resulting in counter-factual synthesis.

This paper traces the root of this limitation to a fundamental dislocation of the underlying knowledge structures, manifesting as a chaotic organization of implicit prompts compared to their explicit counterparts.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 98. CineOrchestra: Unified Entity-Centric Conditioning for Cinematic Video Generation

- **Link:** [https://arxiv.org/abs/2606.13768v2](https://arxiv.org/abs/2606.13768v2)
- **Published:** 2026-06-11
- **Tags:** long/dense preferred, benchmark/eval

"CineOrchestra: Unified Entity-Centric Conditioning for Cinematic Video Generation" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Cinematic video depicts multiple subjects acting or interacting at specific moments, captured with deliberate camera movement, and stitched together by shot transitions.

Together, these elements demand a level of fine-grained control beyond current text-to-video models.

For length policy: note its train/infer token regime, fixed vs mixed length, and any re-prompt design.


### 99. OpenVTON-Bench: A Large-Scale High-Resolution Benchmark for Controllable Virtual Try-On Evaluation

- **Link:** [https://arxiv.org/abs/2601.22725v4](https://arxiv.org/abs/2601.22725v4)
- **Published:** 2026-01-30
- **Tags:** long/dense preferred, LLM/VLM encoder, benchmark/eval

"OpenVTON-Bench: A Large-Scale High-Resolution Benchmark for Controllable Virtual Try-On Evaluation" (2026) evaluates text-conditioned image generation, often under long or compositional prompts.

Recent advances in diffusion models have significantly elevated the visual fidelity of Virtual Try-On (VTON) systems, yet reliable evaluation remains a persistent bottleneck.

Traditional metrics struggle to quantify fine-grained texture details and semantic consistency, while existing datasets fail to meet commercial standards in scale and diversity.

For length policy: note its train/infer token regime, fixed vs mixed length, and any re-prompt design.


### 100. MoTrans: Customized Motion Transfer with Text-driven Video Diffusion Models

- **Link:** [https://arxiv.org/abs/2412.01343v1](https://arxiv.org/abs/2412.01343v1)
- **Published:** 2024-12-02
- **Tags:** re-prompt/recaption, LLM/VLM encoder

"MoTrans: Customized Motion Transfer with Text-driven Video Diffusion Models" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Existing pretrained text-to-video (T2V) models have demonstrated impressive abilities in generating realistic videos with basic motion or camera movement.

However, these models exhibit significant limitations when generating intricate, human-centric motions.

For length policy: note its train/infer token regime, fixed vs mixed length, and any re-prompt design.


### 101. Medical Video Generation for Disease Progression Simulation

- **Link:** [https://arxiv.org/abs/2411.11943v1](https://arxiv.org/abs/2411.11943v1)
- **Published:** 2024-11-18
- **Tags:** re-prompt/recaption, LLM/VLM encoder

"Medical Video Generation for Disease Progression Simulation" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Modeling disease progression is crucial for improving the quality and efficacy of clinical diagnosis and prognosis, but it is often hindered by a lack of longitudinal medical image monitoring for individual patients.

To address this challenge, we propose the first Medical Video Generation (MVG) framework that enables controlled manipulation of disease-related image and video features, allowing precise, realistic, and personalized simulations of disease progression.

For length policy: note its train/infer token regime, fixed vs mixed length, and any re-prompt design.


### 102. TIT-Score: Evaluating Long-Prompt Based Text-to-Image Alignment via Text-to-Image-to-Text Consistency

- **Link:** [https://arxiv.org/abs/2510.02987v1](https://arxiv.org/abs/2510.02987v1)
- **Published:** 2025-10-03
- **Tags:** LLM/VLM encoder, benchmark/eval

"TIT-Score: Evaluating Long-Prompt Based Text-to-Image Alignment via Text-to-Image-to-Text Consistency" (2025) studies prompt rewriting, optimization, or prompt-side control for image generators.

With the rapid advancement of large multimodal models (LMMs), recent text-to-image (T2I) models can generate high-quality images and demonstrate great alignment to short prompts.

However, they still struggle to effectively understand and follow long and detailed prompts, displaying inconsistent generation.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 103. Prompting for products: Investigating design space exploration strategies for text-to-image generative models

- **Link:** [https://arxiv.org/abs/2408.03946v1](https://arxiv.org/abs/2408.03946v1)
- **Published:** 2024-07-22

"Prompting for products: Investigating design space exploration strategies for text-to-image generative models" (2024) studies prompt rewriting, optimization, or prompt-side control for image generators.

Text-to-image models are enabling efficient design space exploration, rapidly generating images from text prompts.

However, many generative AI tools are imperfect for product design applications as they are not built for the goals and requirements of product design.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 104. CRAFT: Continuous Reasoning and Agentic Feedback Tuning for Multimodal Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2512.20362v2](https://arxiv.org/abs/2512.20362v2)
- **Published:** 2025-12-23
- **Tags:** re-prompt/recaption, benchmark/eval

"CRAFT: Continuous Reasoning and Agentic Feedback Tuning for Multimodal Text-to-Image Generation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Recent work has shown that inference-time reasoning and reflection can improve text-to-image generation without retraining.

However, existing approaches often rely on implicit, holistic critiques or unconstrained prompt rewrites, making their behavior difficult to interpret, control, or stop reliably.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 105. WorldGPT: A Sora-Inspired Video AI Agent as Rich World Models from Text and Image Inputs

- **Link:** [https://arxiv.org/abs/2403.07944v1](https://arxiv.org/abs/2403.07944v1)
- **Published:** 2024-03-10
- **Tags:** re-prompt/recaption

"WorldGPT: A Sora-Inspired Video AI Agent as Rich World Models from Text and Image Inputs" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Several text-to-video diffusion models have demonstrated commendable capabilities in synthesizing high-quality video content.

However, it remains a formidable challenge pertaining to maintaining temporal consistency and ensuring action smoothness throughout the generated sequences.

For length policy: note its train/infer token regime, fixed vs mixed length, and any re-prompt design.


### 106. LPNSR: Optimal Noise-Guided Diffusion Image Super-Resolution Via Learnable Noise Prediction

- **Link:** [https://arxiv.org/abs/2603.21045v5](https://arxiv.org/abs/2603.21045v5)
- **Published:** 2026-03-22
- **Tags:** re-prompt/recaption

"LPNSR: Optimal Noise-Guided Diffusion Image Super-Resolution Via Learnable Noise Prediction" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Diffusion-based image super-resolution (SR) aims to reconstruct high-resolution (HR) images from low-resolution (LR) observations.

However, the inherent randomness injected during the reverse diffusion process causes the performance of diffusion-based SR models to vary significantly across different sampling runs, particularly when the sampling trajectory is compressed into a limited number of steps.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 107. Amber-Image: Efficient Compression of Large-Scale Diffusion Transformers

- **Link:** [https://arxiv.org/abs/2602.17047v1](https://arxiv.org/abs/2602.17047v1)
- **Published:** 2026-02-19
- **Tags:** LLM/VLM encoder, benchmark/eval

"Amber-Image: Efficient Compression of Large-Scale Diffusion Transformers" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Diffusion Transformer (DiT) architectures have significantly advanced Text-to-Image (T2I) generation but suffer from prohibitive computational costs and deployment barriers.

To address these challenges, we propose an efficient compression framework that transforms the 60-layer dual-stream MMDiT-based Qwen-Image into lightweight models without training from scratch.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 108. JoyAI-Image: Awaking Spatial Intelligence in Unified Multimodal Understanding and Generation

- **Link:** [https://arxiv.org/abs/2605.04128v2](https://arxiv.org/abs/2605.04128v2)
- **Published:** 2026-05-05
- **Tags:** LLM/VLM encoder, benchmark/eval

"JoyAI-Image: Awaking Spatial Intelligence in Unified Multimodal Understanding and Generation" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

We present JoyAI-Image, a unified multimodal foundation model for visual understanding, text-to-image generation, and instruction-guided image editing.

JoyAI-Image couples a spatially enhanced Multimodal Large Language Model (MLLM) with a Multimodal Diffusion Transformer (MMDiT), allowing perception and generation to interact through a shared multimodal interface.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 109. HiDream-O1-Image: A Natively Unified Image Generative Foundation Model with Pixel-level Unified Transformer

- **Link:** [https://arxiv.org/abs/2605.11061v1](https://arxiv.org/abs/2605.11061v1)
- **Published:** 2026-05-11
- **Tags:** LLM/VLM encoder, benchmark/eval

"HiDream-O1-Image: A Natively Unified Image Generative Foundation Model with Pixel-level Unified Transformer" (2026) is a modern system/report in the LLM/VLM-conditioned image generation line.

The evolution of visual generative models has long been constrained by fragmented architectures relying on disjoint text encoders and external VAEs.

In this report, we present HiDream-O1-Image, a natively unified generative foundation model via pixel-space Diffusion Transformer, that pioneers a paradigm shift from modular architectures to an end-to-end in-context visual generation engine.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 110. FlowCodec: One-Step Flow Prior for Generative Image Compression

- **Link:** [https://arxiv.org/abs/2606.21030v1](https://arxiv.org/abs/2606.21030v1)
- **Published:** 2026-06-19
- **Tags:** numeric token budget, LLM/VLM encoder

"FlowCodec: One-Step Flow Prior for Generative Image Compression" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Diffusion-based image compression methods, leveraging powerful generative priors, have demonstrated remarkable perceptual quality at ultra-low bitrates.

However, adapting modern generative models to image compression often relies on carefully engineered conditioning or auxiliary branches, together with substantial retraining, and these costs grow as the models scale.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 111. sketch-plot: Progressive Editing for Text-to-Image Academic Figures

- **Link:** [https://arxiv.org/abs/2606.09171v2](https://arxiv.org/abs/2606.09171v2)
- **Published:** 2026-06-08

"sketch-plot: Progressive Editing for Text-to-Image Academic Figures" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Text to image (T2I) models such as gpt-image-2 can now generate publication grade academic figures from a short prompt, but the output is a flat raster: a user who wants to change one arrow, one label, or one icon has to regenerate the whole image, which also disturbs the parts they wanted to keep.

We present sketch-plot, an interactive system that closes this controllability gap with a three layer progressive editing pipeline: a generated PNG, an addressable puzzle of editable pieces, and a per piece SVG.

For length policy: note its train/infer token regime, fixed vs mixed length, and any re-prompt design.


### 112. ArcFlow: Unleashing 2-Step Text-to-Image Generation via High-Precision Non-Linear Flow Distillation

- **Link:** [https://arxiv.org/abs/2602.09014v1](https://arxiv.org/abs/2602.09014v1)
- **Published:** 2026-02-09
- **Tags:** LLM/VLM encoder, benchmark/eval

"ArcFlow: Unleashing 2-Step Text-to-Image Generation via High-Precision Non-Linear Flow Distillation" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Diffusion models have achieved remarkable generation quality, but they suffer from significant inference cost due to their reliance on multiple sequential denoising steps, motivating recent efforts to distill this inference process into a few-step regime.

However, existing distillation methods typically approximate the teacher trajectory by using linear shortcuts, which makes it difficult to match its constantly changing tangent directions as velocities evolve across timesteps, thereby leading to quality degradation.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 113. M3: High-fidelity Text-to-Image Generation via Multi-Modal, Multi-Agent and Multi-Round Visual Reasoning

- **Link:** [https://arxiv.org/abs/2602.06166v1](https://arxiv.org/abs/2602.06166v1)
- **Published:** 2026-02-05
- **Tags:** LLM/VLM encoder, benchmark/eval

"M3: High-fidelity Text-to-Image Generation via Multi-Modal, Multi-Agent and Multi-Round Visual Reasoning" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Generative models have achieved impressive fidelity in text-to-image synthesis, yet struggle with complex compositional prompts involving multiple constraints.

We introduce \textbf{M3 (Multi-Modal, Multi-Agent, Multi-Round)}, a training-free framework that systematically resolves these failures through iterative inference-time refinement.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 114. Embedding Arithmetic: A Lightweight, Tuning-Free Framework for Post-hoc Bias Mitigation in Text-to-Image Models

- **Link:** [https://arxiv.org/abs/2604.18167v1](https://arxiv.org/abs/2604.18167v1)
- **Published:** 2026-04-20
- **Tags:** benchmark/eval

"Embedding Arithmetic: A Lightweight, Tuning-Free Framework for Post-hoc Bias Mitigation in Text-to-Image Models" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Modern text-to-image (T2I) models amplify harmful societal biases, challenging their ethical deployment.

We introduce an inference-time method that reliably mitigates social bias while keeping prompt semantics and visual context (background, layout, and style) intact.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 115. Multimodal Prompt Decoupling Attack on the Safety Filters in Text-to-Image Models

- **Link:** [https://arxiv.org/abs/2509.21360v1](https://arxiv.org/abs/2509.21360v1)
- **Published:** 2025-09-21
- **Tags:** re-prompt/recaption, LLM/VLM encoder

"Multimodal Prompt Decoupling Attack on the Safety Filters in Text-to-Image Models" (2025) studies prompt rewriting, optimization, or prompt-side control for image generators.

Text-to-image (T2I) models have been widely applied in generating high-fidelity images across various domains.

However, these models may also be abused to produce Not-Safe-for-Work (NSFW) content via jailbreak attacks.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 116. Automated Prompt Generation for Creative and Counterfactual Text-to-image Synthesis

- **Link:** [https://arxiv.org/abs/2509.21375v1](https://arxiv.org/abs/2509.21375v1)
- **Published:** 2025-09-23
- **Tags:** re-prompt/recaption, benchmark/eval

"Automated Prompt Generation for Creative and Counterfactual Text-to-image Synthesis" (2025) studies prompt rewriting, optimization, or prompt-side control for image generators.

Text-to-image generation has advanced rapidly with large-scale multimodal training, yet fine-grained controllability remains a critical challenge.

Counterfactual controllability, defined as the capacity to deliberately generate images that contradict common-sense patterns, remains a major challenge but plays a crucial role in enabling creativity and exploratory applications.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 117. LSSGen: Leveraging Latent Space Scaling in Flow and Diffusion for Efficient Text to Image Generation

- **Link:** [https://arxiv.org/abs/2507.16154v1](https://arxiv.org/abs/2507.16154v1)
- **Published:** 2025-07-22
- **Tags:** re-prompt/recaption, benchmark/eval

"LSSGen: Leveraging Latent Space Scaling in Flow and Diffusion for Efficient Text to Image Generation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Flow matching and diffusion models have shown impressive results in text-to-image generation, producing photorealistic images through an iterative denoising process.

A common strategy to speed up synthesis is to perform early denoising at lower resolutions.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 118. LLMs can see and hear without any training

- **Link:** [https://arxiv.org/abs/2501.18096v1](https://arxiv.org/abs/2501.18096v1)
- **Published:** 2025-01-30
- **Tags:** re-prompt/recaption, LLM/VLM encoder

"LLMs can see and hear without any training" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

We present MILS: Multimodal Iterative LLM Solver, a surprisingly simple, training-free approach, to imbue multimodal capabilities into your favorite LLM.

Leveraging their innate ability to perform multi-step reasoning, MILS prompts the LLM to generate candidate outputs, each of which are scored and fed back iteratively, eventually generating a solution to the task.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 119. Factorized-Dreamer: Training A High-Quality Video Generator with Limited and Low-Quality Data

- **Link:** [https://arxiv.org/abs/2408.10119v1](https://arxiv.org/abs/2408.10119v1)
- **Published:** 2024-08-19
- **Tags:** long/dense preferred, re-prompt/recaption

"Factorized-Dreamer: Training A High-Quality Video Generator with Limited and Low-Quality Data" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Text-to-video (T2V) generation has gained significant attention due to its wide applications to video generation, editing, enhancement and translation, \etc.

However, high-quality (HQ) video synthesis is extremely challenging because of the diverse and complex motions existed in real world.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 120. Exploring the Design Space of Reward Backpropagation for Flow Matching

- **Link:** [https://arxiv.org/abs/2606.11075v1](https://arxiv.org/abs/2606.11075v1)
- **Published:** 2026-06-09

"Exploring the Design Space of Reward Backpropagation for Flow Matching" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Aligning text-to-image flow matching models with human preferences via direct reward backpropagation is sample-efficient but hampered by two well-known pathologies: activations cannot be stored across the full sampling trajectory at modern model scale, and chained Jacobian products across steps inflate the reward gradient as it travels...

Connector-based methods, such as LeapAlign, address these issues by replacing the full backward trajectory with a short pinned path, highlighting a useful decoupling between sampling and optimization.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 121. Diagnosing and Correcting Concept Omission in Multimodal Diffusion Transformers

- **Link:** [https://arxiv.org/abs/2605.14270v2](https://arxiv.org/abs/2605.14270v2)
- **Published:** 2026-05-14

"Diagnosing and Correcting Concept Omission in Multimodal Diffusion Transformers" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Multimodal Diffusion Transformers (MM-DiTs) have achieved remarkable progress in text-to-image generation, yet they frequently suffer from concept omission, where specified objects or attributes fail to emerge in the generated image.

By performing linear probing on text tokens, we demonstrate that text embeddings can distinguish a characteristic `omission signal' representing the absence of target concepts.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 122. Compressing Image Style Training into a Single Model Forward

- **Link:** [https://arxiv.org/abs/2606.13809v1](https://arxiv.org/abs/2606.13809v1)
- **Published:** 2026-06-11

"Compressing Image Style Training into a Single Model Forward" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Diffusion-based style transfer must balance inference efficiency with stylization fidelity.

Adapter-based methods are efficient, but they inject style as an external condition and can either weaken reference-specific appearance or copy reference semantics into the generated image.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 123. LESA: Learnable Stage-Aware Predictors for Diffusion Model Acceleration

- **Link:** [https://arxiv.org/abs/2602.20497v3](https://arxiv.org/abs/2602.20497v3)
- **Published:** 2026-02-24
- **Tags:** LLM/VLM encoder

"LESA: Learnable Stage-Aware Predictors for Diffusion Model Acceleration" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Diffusion models have achieved remarkable success in image and video generation tasks.

However, the high computational demands of Diffusion Transformers (DiTs) pose a significant challenge to their practical deployment.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 124. Decomposing Private Image Generation via Coarse-to-Fine Wavelet Modeling

- **Link:** [https://arxiv.org/abs/2602.23262v1](https://arxiv.org/abs/2602.23262v1)
- **Published:** 2026-02-26
- **Tags:** re-prompt/recaption

"Decomposing Private Image Generation via Coarse-to-Fine Wavelet Modeling" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Generative models trained on sensitive image datasets risk memorizing and reproducing individual training examples, making strong privacy guarantees essential.

While differential privacy (DP) provides a principled framework for such guarantees, standard DP finetuning (e.g., with DP-SGD) often results in severe degradation of image quality, particularly in high-frequency textures, due to the indiscriminate addition of noise across all model parameters.

For length policy: note its train/infer token regime, fixed vs mixed length, and any re-prompt design.


### 125. Emotion-Director: Bridging Affective Shortcut in Emotion-Oriented Image Generation

- **Link:** [https://arxiv.org/abs/2512.19479v1](https://arxiv.org/abs/2512.19479v1)
- **Published:** 2025-12-22
- **Tags:** re-prompt/recaption

"Emotion-Director: Bridging Affective Shortcut in Emotion-Oriented Image Generation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Image generation based on diffusion models has demonstrated impressive capability, motivating exploration into diverse and specialized applications.

Owing to the importance of emotion in advertising, emotion-oriented image generation has attracted increasing attention.

For length policy: note its train/infer token regime, fixed vs mixed length, and any re-prompt design.


### 126. Ask, Solve, Generate: Self-Evolving Unified Multimodal Understanding and Generation via Self-Consistency Rewards

- **Link:** [https://arxiv.org/abs/2606.27376v1](https://arxiv.org/abs/2606.27376v1)
- **Published:** 2026-06-25
- **Tags:** benchmark/eval

"Ask, Solve, Generate: Self-Evolving Unified Multimodal Understanding and Generation via Self-Consistency Rewards" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Most unified large multimodal models (LMMs) that support both visual understanding and image generation still rely on curated post-training supervision, such as human annotations, preference labels, or external reward models.

We ask whether a unified LMM can improve both abilities autonomously using only unlabeled images.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 127. Latent Action Control for Reasoning-Guided Unified Image Generation

- **Link:** [https://arxiv.org/abs/2605.16961v1](https://arxiv.org/abs/2605.16961v1)
- **Published:** 2026-05-16

"Latent Action Control for Reasoning-Guided Unified Image Generation" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Unified multimodal models can encode visual understanding and image generation within a shared backbone, yet understanding does not automatically translate into control: models may infer objects, relations, or knowledge cues but fail to instantiate them in the generated image.

We propose Latent Action Control (LAC), which makes reasoning actionable by representing it as hidden continuous actions inside a unified generator.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 128. Accelerating Rectified Flow Models via Trajectory-Aware Caching

- **Link:** [https://arxiv.org/abs/2605.16789v1](https://arxiv.org/abs/2605.16789v1)
- **Published:** 2026-05-16
- **Tags:** benchmark/eval

"Accelerating Rectified Flow Models via Trajectory-Aware Caching" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Diffusion and rectified flow (RF) models generate high-fidelity images and videos, but their iterative velocity-field evaluations are computationally expensive.

Existing caching methods accelerate sampling by skipping timesteps, yet their coarse approximations introduce accumulated errors over long skip intervals and degrade quality under aggressive acceleration.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 129. Correlation-Weighted Multi-Reward Optimization for Compositional Generation

- **Link:** [https://arxiv.org/abs/2603.18528v2](https://arxiv.org/abs/2603.18528v2)
- **Published:** 2026-03-19
- **Tags:** benchmark/eval

"Correlation-Weighted Multi-Reward Optimization for Compositional Generation" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Text-to-image models produce images that align well with natural language prompts, but compositional generation has long been a central challenge.

Models often struggle to satisfy multiple concepts within a single prompt, frequently omitting some concepts and resulting in partial success.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 130. StrandDesigner: Towards Practical Strand Generation with Sketch Guidance

- **Link:** [https://arxiv.org/abs/2508.01650v1](https://arxiv.org/abs/2508.01650v1)
- **Published:** 2025-08-03
- **Tags:** re-prompt/recaption, benchmark/eval

"StrandDesigner: Towards Practical Strand Generation with Sketch Guidance" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Realistic hair strand generation is crucial for applications like computer graphics and virtual reality.

While diffusion models can generate hairstyles from text or images, these inputs lack precision and user-friendliness.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 131. EditID: Training-Free Editable ID Customization for Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2503.12526v1](https://arxiv.org/abs/2503.12526v1)
- **Published:** 2025-03-16
- **Tags:** long/dense preferred, benchmark/eval

"EditID: Training-Free Editable ID Customization for Text-to-Image Generation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

We propose EditID, a training-free approach based on the DiT architecture, which achieves highly editable customized IDs for text to image generation.

Existing text-to-image models for customized IDs typically focus more on ID consistency while neglecting editability.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 132. Progressive Prompt Detailing for Improved Alignment in Text-to-Image Generative Models

- **Link:** [https://arxiv.org/abs/2503.17794v4](https://arxiv.org/abs/2503.17794v4)
- **Published:** 2025-03-22
- **Tags:** long/dense preferred

"Progressive Prompt Detailing for Improved Alignment in Text-to-Image Generative Models" (2025) studies prompt rewriting, optimization, or prompt-side control for image generators.

Text-to-image generative models often struggle with long prompts detailing complex scenes, diverse objects with distinct visual characteristics and spatial relationships.

In this work, we propose SCoPE (Scheduled interpolation of Coarse-to-fine Prompt Embeddings), a training-free method to improve text-to-image alignment by progressively refining the input prompt in a coarse-to-fine-grained manner.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 133. EditIDv2: Editable ID Customization with Data-Lubricated ID Feature Integration for Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2509.05659v1](https://arxiv.org/abs/2509.05659v1)
- **Published:** 2025-09-06
- **Tags:** long/dense preferred, benchmark/eval

"EditIDv2: Editable ID Customization with Data-Lubricated ID Feature Integration for Text-to-Image Generation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

We propose EditIDv2, a tuning-free solution specifically designed for high-complexity narrative scenes and long text inputs.

Existing character editing methods perform well under simple prompts, but often suffer from degraded editing capabilities, semantic understanding biases, and identity consistency breakdowns when faced with long text narratives containing multiple semantic layers, temporal logic, and complex contextual relationships.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 134. CAHS-Attack: CLIP-Aware Heuristic Search Attack Method for Stable Diffusion

- **Link:** [https://arxiv.org/abs/2511.21180v1](https://arxiv.org/abs/2511.21180v1)
- **Published:** 2025-11-26
- **Tags:** long/dense preferred

"CAHS-Attack: CLIP-Aware Heuristic Search Attack Method for Stable Diffusion" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Diffusion models exhibit notable fragility when faced with adversarial prompts, and strengthening attack capabilities is crucial for uncovering such vulnerabilities and building more robust generative systems.

Existing works often rely on white-box access to model gradients or hand-crafted prompt engineering, which is infeasible in real-world deployments due to restricted access or poor attack effect.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 135. Self-Rewarding Large Vision-Language Models for Optimizing Prompts in Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2505.16763v2](https://arxiv.org/abs/2505.16763v2)
- **Published:** 2025-05-22
- **Tags:** re-prompt/recaption, LLM/VLM encoder

"Self-Rewarding Large Vision-Language Models for Optimizing Prompts in Text-to-Image Generation" (2025) studies prompt rewriting, optimization, or prompt-side control for image generators.

Text-to-image models are powerful for producing high-quality images based on given text prompts, but crafting these prompts often requires specialized vocabulary.

To address this, existing methods train rewriting models with supervision from large amounts of manually annotated data and trained aesthetic assessment models.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 136. Dynamic Optimization and Safety Indicator Injection for Jailbreaking Text-to-Image Models with Multimodal Safety Filters

- **Link:** [https://arxiv.org/abs/2505.18979v2](https://arxiv.org/abs/2505.18979v2)
- **Published:** 2025-05-25
- **Tags:** re-prompt/recaption, LLM/VLM encoder, benchmark/eval

"Dynamic Optimization and Safety Indicator Injection for Jailbreaking Text-to-Image Models with Multimodal Safety Filters" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Text-to-image (T2I) models can generate not-safe-for-work (NSFW) content, motivating multi-stage safety pipelines with both text and image filters.

Newer LLM-based filters detect latent intent beyond keywords, making token-level perturbation attacks unreliable.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 137. M*: A Modular, Extensible, Serving System for Multimodal Models

- **Link:** [https://arxiv.org/abs/2606.12688v2](https://arxiv.org/abs/2606.12688v2)
- **Published:** 2026-06-10
- **Tags:** LLM/VLM encoder

"M*: A Modular, Extensible, Serving System for Multimodal Models" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

We are entering a new era of composite model architectures that integrate diverse components such as vision encoders, language backbones, diffusion and flow heads, audio codecs, action generators, and world-model predictors.

Such architectures underpin a broad class of multimodal models, including unified multimodal models, omni models, speech-language models, vision-language-action policies, and world models.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 138. MapReduce LoRA: Advancing the Pareto Front in Multi-Preference Optimization for Generative Models

- **Link:** [https://arxiv.org/abs/2511.20629v5](https://arxiv.org/abs/2511.20629v5)
- **Published:** 2025-11-25
- **Tags:** LLM/VLM encoder

"MapReduce LoRA: Advancing the Pareto Front in Multi-Preference Optimization for Generative Models" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Reinforcement learning from human feedback (RLHF) with reward models has advanced alignment of generative models to human aesthetic and perceptual preferences.

However, jointly optimizing multiple rewards often incurs an alignment tax, improving one dimension while degrading others.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 139. InterleaveThinker: Reinforcing Agentic Interleaved Generation

- **Link:** [https://arxiv.org/abs/2606.13679v2](https://arxiv.org/abs/2606.13679v2)
- **Published:** 2026-06-11
- **Tags:** benchmark/eval

"InterleaveThinker: Reinforcing Agentic Interleaved Generation" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Recent image generators have demonstrated impressive photorealism and instruction-following capabilities in single-image generation and editing.

However, constrained by their architectures, they cannot achieve interleaved generation (text-image sequence), which has crucial applications in visual narratives, guidance, and embodied manipulation.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 140. Do Understanding and Generation Fight? A Diagnostic Study of DPO for Unified Multimodal Models

- **Link:** [https://arxiv.org/abs/2603.17044v2](https://arxiv.org/abs/2603.17044v2)
- **Published:** 2026-03-17

"Do Understanding and Generation Fight? A Diagnostic Study of DPO for Unified Multimodal Models" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Unified multimodal models share a language model backbone for both understanding and generating images.

Can DPO align both capabilities simultaneously?.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 141. InterCoG: Towards Spatially Precise Image Editing with Interleaved Chain-of-Grounding Reasoning

- **Link:** [https://arxiv.org/abs/2603.01586v3](https://arxiv.org/abs/2603.01586v3)
- **Published:** 2026-03-02
- **Tags:** re-prompt/recaption, benchmark/eval

"InterCoG: Towards Spatially Precise Image Editing with Interleaved Chain-of-Grounding Reasoning" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Emerging unified editing models have demonstrated strong capabilities in general object editing tasks.

However, it remains a significant challenge to perform fine-grained editing in complex multi-entity scenes, particularly those where targets are not visually salient and require spatial reasoning.

For length policy: note its train/infer token regime, fixed vs mixed length, and any re-prompt design.


### 142. UniWeTok: An Unified Binary Tokenizer with Codebook Size $\mathit{2^{128}}$ for Unified Multimodal Large Language Model

- **Link:** [https://arxiv.org/abs/2602.14178v3](https://arxiv.org/abs/2602.14178v3)
- **Published:** 2026-02-15
- **Tags:** numeric token budget, LLM/VLM encoder

"UniWeTok: An Unified Binary Tokenizer with Codebook Size $\mathit{2^{128}}$ for Unified Multimodal Large Language Model" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Unified Multimodal Large Language Models (MLLMs) require a visual representation that simultaneously supports high-fidelity reconstruction, complex semantic extraction, and generative suitability.

However, existing visual tokenizers typically struggle to satisfy these conflicting objectives within a single framework.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 143. FineGRAIN: Evaluating Failure Modes of Text-to-Image Models with Vision Language Model Judges

- **Link:** [https://arxiv.org/abs/2512.02161v1](https://arxiv.org/abs/2512.02161v1)
- **Published:** 2025-12-01
- **Tags:** LLM/VLM encoder, benchmark/eval

"FineGRAIN: Evaluating Failure Modes of Text-to-Image Models with Vision Language Model Judges" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Text-to-image (T2I) models are capable of generating visually impressive images, yet they often fail to accurately capture specific attributes in user prompts, such as the correct number of objects with the specified colors.

The diversity of such errors underscores the need for a hierarchical evaluation framework that can compare prompt adherence abilities of different image generation models.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 144. NeuroPrompts: An Adaptive Framework to Optimize Prompts for Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2311.12229v2](https://arxiv.org/abs/2311.12229v2)
- **Published:** 2023-11-20
- **Tags:** re-prompt/recaption

"NeuroPrompts: An Adaptive Framework to Optimize Prompts for Text-to-Image Generation" (2023) studies prompt rewriting, optimization, or prompt-side control for generators.

Despite impressive recent advances in text-to-image diffusion models, obtaining high-quality images often requires prompt engineering by humans who have developed expertise in using them.

In this work, we present NeuroPrompts, an adaptive framework that automatically enhances a user's prompt to improve the quality of generations produced by text-to-image models.

For length policy: note its train/infer token regime, fixed vs mixed length, and any re-prompt design.


### 145. Make-An-Audio: Text-To-Audio Generation with Prompt-Enhanced Diffusion Models

- **Link:** [https://arxiv.org/abs/2301.12661v1](https://arxiv.org/abs/2301.12661v1)
- **Published:** 2023-01-30
- **Tags:** re-prompt/recaption, benchmark/eval

"Make-An-Audio: Text-To-Audio Generation with Prompt-Enhanced Diffusion Models" (2023) studies prompt rewriting, optimization, or prompt-side control for generators.

Large-scale multimodal generative modeling has created milestones in text-to-image and text-to-video generation.

Its application to audio still lags behind for two main reasons: the lack of large-scale datasets with high-quality text-audio pairs, and the complexity of modeling long continuous audio data.

For length policy: note its train/infer token regime, fixed vs mixed length, and any re-prompt design.


### 146. Visual Autoregressive Modelling for Monocular Depth Estimation

- **Link:** [https://arxiv.org/abs/2512.22653v1](https://arxiv.org/abs/2512.22653v1)
- **Published:** 2025-12-27
- **Tags:** re-prompt/recaption, benchmark/eval

"Visual Autoregressive Modelling for Monocular Depth Estimation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

We propose a monocular depth estimation method based on visual autoregressive (VAR) priors, offering an alternative to diffusion-based approaches.

Our method adapts a large-scale text-to-image VAR model and introduces a scale-wise conditional upsampling mechanism with classifier-free guidance.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 147. FOCUS: Optimal Control for Multi-Entity World Modeling in Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2510.02315v2](https://arxiv.org/abs/2510.02315v2)
- **Published:** 2025-10-02

"FOCUS: Optimal Control for Multi-Entity World Modeling in Text-to-Image Generation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Text-to-image (T2I) models excel on single-entity prompts but struggle with multi-entity scenes, often exhibiting attribute leakage, identity entanglement, and subject omissions.

We present a principled theoretical framework that steers sampling toward multi-subject fidelity by casting flow matching (FM) as stochastic optimal control (SOC), yielding a single hyperparameter controlled trade-off between fidelity and object-centric state separation / binding consistency.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 148. Rethinking Cross-Modal Interaction in Multimodal Diffusion Transformers

- **Link:** [https://arxiv.org/abs/2506.07986v3](https://arxiv.org/abs/2506.07986v3)
- **Published:** 2025-06-09
- **Tags:** benchmark/eval

"Rethinking Cross-Modal Interaction in Multimodal Diffusion Transformers" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Multimodal Diffusion Transformers (MM-DiTs) have achieved remarkable progress in text-driven visual generation.

However, even state-of-the-art MM-DiT models like FLUX struggle with achieving precise alignment between text prompts and generated content.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 149. Multimodal Representation Alignment for Image Generation: Text-Image Interleaved Control Is Easier Than You Think

- **Link:** [https://arxiv.org/abs/2502.20172v1](https://arxiv.org/abs/2502.20172v1)
- **Published:** 2025-02-27
- **Tags:** LLM/VLM encoder, benchmark/eval

"Multimodal Representation Alignment for Image Generation: Text-Image Interleaved Control Is Easier Than You Think" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

The field of advanced text-to-image generation is witnessing the emergence of unified frameworks that integrate powerful text encoders, such as CLIP and T5, with Diffusion Transformer backbones.

Although there have been efforts to control output images with additional conditions, like canny and depth map, a comprehensive framework for arbitrary text-image interleaved control is still lacking.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 150. OneReward: Unified Mask-Guided Image Generation via Multi-Task Human Preference Learning

- **Link:** [https://arxiv.org/abs/2508.21066v1](https://arxiv.org/abs/2508.21066v1)
- **Published:** 2025-08-28
- **Tags:** LLM/VLM encoder, benchmark/eval

"OneReward: Unified Mask-Guided Image Generation via Multi-Task Human Preference Learning" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

In this paper, we introduce OneReward, a unified reinforcement learning framework that enhances the model's generative capabilities across multiple tasks under different evaluation criteria using only \textit{One Reward} model.

By employing a single vision-language model (VLM) as the generative reward model, which can distinguish the winner and loser for a given task and a given evaluation criterion, it can be effectively applied to multi-task generation models, particularly in contexts with varied data and diverse task objectives.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 151. Self-Adversarial One Step Generation via Condition Shifting

- **Link:** [https://arxiv.org/abs/2604.12322v1](https://arxiv.org/abs/2604.12322v1)
- **Published:** 2026-04-14
- **Tags:** LLM/VLM encoder

"Self-Adversarial One Step Generation via Condition Shifting" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

The push for efficient text to image synthesis has moved the field toward one step sampling, yet existing methods still face a three way tradeoff among fidelity, inference speed, and training efficiency.

Approaches that rely on external discriminators can sharpen one step performance, but they often introduce training instability, high GPU memory overhead, and slow convergence, which complicates scaling and parameter efficient tuning.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 152. TwinFlow: Realizing One-step Generation on Large Models with Self-adversarial Flows

- **Link:** [https://arxiv.org/abs/2512.05150v2](https://arxiv.org/abs/2512.05150v2)
- **Published:** 2025-12-03
- **Tags:** LLM/VLM encoder, benchmark/eval

"TwinFlow: Realizing One-step Generation on Large Models with Self-adversarial Flows" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Recent advances in large multi-modal generative models have demonstrated impressive capabilities in multi-modal generation, including image and video generation.

These models are typically built upon multi-step frameworks like diffusion and flow matching, which inherently limits their inference efficiency (requiring 40-100 Number of Function Evaluations (NFEs)).

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 153. SliderEdit: Continuous Image Editing with Fine-Grained Instruction Control

- **Link:** [https://arxiv.org/abs/2511.09715v1](https://arxiv.org/abs/2511.09715v1)
- **Published:** 2025-11-12
- **Tags:** LLM/VLM encoder

"SliderEdit: Continuous Image Editing with Fine-Grained Instruction Control" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Instruction-based image editing models have recently achieved impressive performance, enabling complex edits to an input image from a multi-instruction prompt.

However, these models apply each instruction in the prompt with a fixed strength, limiting the user's ability to precisely and continuously control the intensity of individual edits.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 154. APT: Improving Diffusion Models for High Resolution Image Generation with Adaptive Path Tracing

- **Link:** [https://arxiv.org/abs/2507.21690v1](https://arxiv.org/abs/2507.21690v1)
- **Published:** 2025-07-29
- **Tags:** re-prompt/recaption

"APT: Improving Diffusion Models for High Resolution Image Generation with Adaptive Path Tracing" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Latent Diffusion Models (LDMs) are generally trained at fixed resolutions, limiting their capability when scaling up to high-resolution images.

While training-based approaches address this limitation by training on high-resolution datasets, they require large amounts of data and considerable computational resources, making them less practical.

For length policy: note its train/infer token regime, fixed vs mixed length, and any re-prompt design.


### 155. Latent Space Super-Resolution for Higher-Resolution Image Generation with Diffusion Models

- **Link:** [https://arxiv.org/abs/2503.18446v2](https://arxiv.org/abs/2503.18446v2)
- **Published:** 2025-03-24
- **Tags:** re-prompt/recaption

"Latent Space Super-Resolution for Higher-Resolution Image Generation with Diffusion Models" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

In this paper, we propose LSRNA, a novel framework for higher-resolution (exceeding 1K) image generation using diffusion models by leveraging super-resolution directly in the latent space.

Existing diffusion models struggle with scaling beyond their training resolutions, often leading to structural distortions or content repetition.

For length policy: note its train/infer token regime, fixed vs mixed length, and any re-prompt design.


### 156. A Reason-then-Describe Instruction Interpreter for Controllable Video Generation

- **Link:** [https://arxiv.org/abs/2511.20563v1](https://arxiv.org/abs/2511.20563v1)
- **Published:** 2025-11-25
- **Tags:** long/dense preferred

"A Reason-then-Describe Instruction Interpreter for Controllable Video Generation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Diffusion Transformers have significantly improved video fidelity and temporal coherence, however, practical controllability remains limited.

Concise, ambiguous, and compositionally complex user inputs contrast with the detailed prompts used in training, yielding an intent-output mismatch.

For length policy: note its train/infer token regime, fixed vs mixed length, and any re-prompt design.


### 157. Second-Order Multi-Level Variance Correction for Modality Competition in Multimodal Models

- **Link:** [https://arxiv.org/abs/2605.16165v1](https://arxiv.org/abs/2605.16165v1)
- **Published:** 2026-05-15

"Second-Order Multi-Level Variance Correction for Modality Competition in Multimodal Models" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Autoregressive next-token training offers a unified formulation for image generation and text understanding, but it also creates strong modality competition that destabilizes optimization and limits large-batch scaling.

We show that first-order optimizers such as AdamW are vulnerable to cross-modality gradient heterogeneity, while second-order preconditioning, particularly SOAP, provides a more stable basis for multimodal alignment.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 158. Beyond Language Modeling: An Exploration of Multimodal Pretraining

- **Link:** [https://arxiv.org/abs/2603.03276v1](https://arxiv.org/abs/2603.03276v1)
- **Published:** 2026-03-03

"Beyond Language Modeling: An Exploration of Multimodal Pretraining" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

The visual world offers a critical axis for advancing foundation models beyond language.

Despite growing interest in this direction, the design space for native multimodal models remains opaque.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 159. Qwen-Image Technical Report

- **Link:** [https://arxiv.org/abs/2508.02324v1](https://arxiv.org/abs/2508.02324v1)
- **Published:** 2025-08-04
- **Tags:** LLM/VLM encoder, benchmark/eval

"Qwen-Image Technical Report" (2025) is a modern system/report in the LLM/VLM-conditioned image generation line.

We present Qwen-Image, an image generation foundation model in the Qwen series that achieves significant advances in complex text rendering and precise image editing.

To address the challenges of complex text rendering, we design a comprehensive data pipeline that includes large-scale data collection, filtering, annotation, synthesis, and balancing.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 160. Towards Evaluating Robustness of Prompt Adherence in Text to Image Models

- **Link:** [https://arxiv.org/abs/2507.08039v1](https://arxiv.org/abs/2507.08039v1)
- **Published:** 2025-07-09
- **Tags:** LLM/VLM encoder, benchmark/eval

"Towards Evaluating Robustness of Prompt Adherence in Text to Image Models" (2025) studies prompt rewriting, optimization, or prompt-side control for generators.

The advancements in the domain of LLMs in recent years have surprised many, showcasing their remarkable capabilities and diverse applications.

Their potential applications in various real-world scenarios have led to significant research on their reliability and effectiveness.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 161. FreeFlux: Understanding and Exploiting Layer-Specific Roles in RoPE-Based MMDiT for Versatile Image Editing

- **Link:** [https://arxiv.org/abs/2503.16153v1](https://arxiv.org/abs/2503.16153v1)
- **Published:** 2025-03-20
- **Tags:** benchmark/eval

"FreeFlux: Understanding and Exploiting Layer-Specific Roles in RoPE-Based MMDiT for Versatile Image Editing" (2025) is a modern system/report in the LLM/VLM-conditioned image generation line.

The integration of Rotary Position Embedding (RoPE) in Multimodal Diffusion Transformer (MMDiT) has significantly enhanced text-to-image generation quality.

However, the fundamental reliance of self-attention layers on positional embedding versus query-key similarity during generation remains an intriguing question.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 162. CTA-Flux: Integrating Chinese Cultural Semantics into High-Quality English Text-to-Image Communities

- **Link:** [https://arxiv.org/abs/2508.14405v1](https://arxiv.org/abs/2508.14405v1)
- **Published:** 2025-08-20
- **Tags:** benchmark/eval

"CTA-Flux: Integrating Chinese Cultural Semantics into High-Quality English Text-to-Image Communities" (2025) is a modern system/report in the LLM/VLM-conditioned image generation line.

We proposed the Chinese Text Adapter-Flux (CTA-Flux).

An adaptation method fits the Chinese text inputs to Flux, a powerful text-to-image (TTI) generative model initially trained on the English corpus.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 163. Qwen-Image-Layered: Towards Inherent Editability via Layer Decomposition

- **Link:** [https://arxiv.org/abs/2512.15603v1](https://arxiv.org/abs/2512.15603v1)
- **Published:** 2025-12-17
- **Tags:** LLM/VLM encoder

"Qwen-Image-Layered: Towards Inherent Editability via Layer Decomposition" (2025) is a modern system/report in the LLM/VLM-conditioned image generation line.

Recent visual generative models often struggle with consistency during image editing due to the entangled nature of raster images, where all visual content is fused into a single canvas.

In contrast, professional design tools employ layered representations, allowing isolated edits while preserving consistency.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 164. Hyper-Bagel: A Unified Acceleration Framework for Multimodal Understanding and Generation

- **Link:** [https://arxiv.org/abs/2509.18824v1](https://arxiv.org/abs/2509.18824v1)
- **Published:** 2025-09-23

"Hyper-Bagel: A Unified Acceleration Framework for Multimodal Understanding and Generation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Unified multimodal models have recently attracted considerable attention for their remarkable abilities in jointly understanding and generating diverse content.

However, as contexts integrate increasingly numerous interleaved multimodal tokens, the iterative processes of diffusion denoising and autoregressive decoding impose significant computational overhead.

Keep it as background on modern generation/evaluation; use only if its data or metrics inform caption-length decisions.


### 165. SANA-Sprint: One-Step Diffusion with Continuous-Time Consistency Distillation

- **Link:** [https://arxiv.org/abs/2503.09641v4](https://arxiv.org/abs/2503.09641v4)
- **Published:** 2025-03-12

"SANA-Sprint: One-Step Diffusion with Continuous-Time Consistency Distillation" (2025) is a modern system/report in the LLM/VLM-conditioned image generation line.

This paper presents SANA-Sprint, an efficient diffusion model for ultra-fast text-to-image (T2I) generation.

SANA-Sprint is built on a pre-trained foundation model and augmented with hybrid distillation, dramatically reducing inference steps from 20 to 1-4.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 166. LaDe: Unified Multi-Layered Graphic Media Generation and Decomposition

- **Link:** [https://arxiv.org/abs/2603.17965v1](https://arxiv.org/abs/2603.17965v1)
- **Published:** 2026-03-18
- **Tags:** LLM/VLM encoder, benchmark/eval

"LaDe: Unified Multi-Layered Graphic Media Generation and Decomposition" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Media design layer generation enables the creation of fully editable, layered design documents such as posters, flyers, and logos using only natural language prompts.

Existing methods either restrict outputs to a fixed number of layers or require each layer to contain only spatially continuous regions, causing the layer count to scale linearly with design complexity.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 167. Ovis-Image Technical Report

- **Link:** [https://arxiv.org/abs/2511.22982v1](https://arxiv.org/abs/2511.22982v1)
- **Published:** 2025-11-28
- **Tags:** LLM/VLM encoder

"Ovis-Image Technical Report" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

We introduce $\textbf{Ovis-Image}$, a 7B text-to-image model specifically optimized for high-quality text rendering, designed to operate efficiently under stringent computational constraints.

Built upon our previous Ovis-U1 framework, Ovis-Image integrates a diffusion-based visual decoder with the stronger Ovis 2.5 multimodal backbone, leveraging a text-centric training pipeline that combines large-scale pre-training with carefully tailored post-training refinements.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 168. MindOmni: Unleashing Reasoning Generation in Vision Language Models with RGPO

- **Link:** [https://arxiv.org/abs/2505.13031v2](https://arxiv.org/abs/2505.13031v2)
- **Published:** 2025-05-19
- **Tags:** LLM/VLM encoder, benchmark/eval

"MindOmni: Unleashing Reasoning Generation in Vision Language Models with RGPO" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Recent text-to-image systems face limitations in handling multimodal inputs and complex reasoning tasks.

We introduce MindOmni, a unified multimodal large language model that addresses these challenges by incorporating reasoning generation through reinforcement learning.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 169. FundusGAN: A Hierarchical Feature-Aware Generative Framework for High-Fidelity Fundus Image Generation

- **Link:** [https://arxiv.org/abs/2503.17831v1](https://arxiv.org/abs/2503.17831v1)
- **Published:** 2025-03-22
- **Tags:** re-prompt/recaption, benchmark/eval

"FundusGAN: A Hierarchical Feature-Aware Generative Framework for High-Fidelity Fundus Image Generation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Recent advancements in ophthalmology foundation models such as RetFound have demonstrated remarkable diagnostic capabilities but require massive datasets for effective pre-training, creating significant barriers for development and deployment.

To address this critical challenge, we propose FundusGAN, a novel hierarchical feature-aware generative framework specifically designed for high-fidelity fundus image synthesis.

For length policy: note its train/infer token regime, fixed vs mixed length, and any re-prompt design.


### 170. Video-P2P: Video Editing with Cross-attention Control

- **Link:** [https://arxiv.org/abs/2303.04761v1](https://arxiv.org/abs/2303.04761v1)
- **Published:** 2023-03-08
- **Tags:** re-prompt/recaption

"Video-P2P: Video Editing with Cross-attention Control" (2023) contributes methods or analysis in contemporary text-to-image / multimodal generation.

This paper presents Video-P2P, a novel framework for real-world video editing with cross-attention control.

While attention control has proven effective for image editing with pre-trained image generation models, there are currently no large-scale video generation models publicly available.

For length policy: note its train/infer token regime, fixed vs mixed length, and any re-prompt design.


### 171. Rethinking UMM Visual Generation: Masked Modeling for Efficient Image-Only Pre-training

- **Link:** [https://arxiv.org/abs/2603.16139v1](https://arxiv.org/abs/2603.16139v1)
- **Published:** 2026-03-17

"Rethinking UMM Visual Generation: Masked Modeling for Efficient Image-Only Pre-training" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Unified Multimodal Models (UMMs) are often constrained by the pre-training of their $\textbf{visual generation components}$, which typically relies on inefficient paradigms and scarce, high-quality text-image paired data.

In this paper, we systematically analyze pre-training recipes for $\textbf{UMM visual generation}$ and identify these two issues as the major bottlenecks.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 172. Exploring the Role of Large Language Models in Prompt Encoding for Diffusion Models

- **Link:** [https://arxiv.org/abs/2406.11831v3](https://arxiv.org/abs/2406.11831v3)
- **Published:** 2024-06-17
- **Tags:** LLM/VLM encoder

"Exploring the Role of Large Language Models in Prompt Encoding for Diffusion Models" (2024) studies prompt rewriting, optimization, or prompt-side control for generators.

Large language models (LLMs) based on decoder-only transformers have demonstrated superior text understanding capabilities compared to CLIP and T5-series models.

However, the paradigm for utilizing current advanced LLMs in text-to-image diffusion models remains to be explored.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 173. Training-free Regional Prompting for Diffusion Transformers

- **Link:** [https://arxiv.org/abs/2411.02395v1](https://arxiv.org/abs/2411.02395v1)
- **Published:** 2024-11-04
- **Tags:** LLM/VLM encoder

"Training-free Regional Prompting for Diffusion Transformers" (2024) studies prompt rewriting, optimization, or prompt-side control for generators.

Diffusion models have demonstrated excellent capabilities in text-to-image generation.

Their semantic understanding (i.e., prompt following) ability has also been greatly improved with large language models (e.g., T5, Llama).

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 174. LGCC: Enhancing Flow Matching Based Text-Guided Image Editing with Local Gaussian Coupling and Context Consistency

- **Link:** [https://arxiv.org/abs/2511.01894v1](https://arxiv.org/abs/2511.01894v1)
- **Published:** 2025-10-29
- **Tags:** LLM/VLM encoder

"LGCC: Enhancing Flow Matching Based Text-Guided Image Editing with Local Gaussian Coupling and Context Consistency" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Recent advancements have demonstrated the great potential of flow matching-based Multimodal Large Language Models (MLLMs) in image editing.

However, state-of-the-art works like BAGEL face limitations, including detail degradation, content inconsistency, and inefficiency due to their reliance on random noise initialization.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 175. Lumina-OmniLV: A Unified Multimodal Framework for General Low-Level Vision

- **Link:** [https://arxiv.org/abs/2504.04903v2](https://arxiv.org/abs/2504.04903v2)
- **Published:** 2025-04-07

"Lumina-OmniLV: A Unified Multimodal Framework for General Low-Level Vision" (2025) is a modern system/report in the LLM/VLM-conditioned image generation line.

We present Lunima-OmniLV (abbreviated as OmniLV), a universal multimodal multi-task framework for low-level vision that addresses over 100 sub-tasks across four major categories: image restoration, image enhancement, weak-semantic dense prediction, and stylization.

OmniLV leverages both textual and visual prompts to offer flexible and user-friendly interactions.

Keep it as background on modern generation/evaluation; use only if its data or metrics inform caption-length decisions.


### 176. Qwen-Image-2.0-RL Technical Report

- **Link:** [https://arxiv.org/abs/2606.27608v1](https://arxiv.org/abs/2606.27608v1)
- **Published:** 2026-06-25
- **Tags:** LLM/VLM encoder, benchmark/eval

"Qwen-Image-2.0-RL Technical Report" (2026) is a modern system/report in the LLM/VLM-conditioned image generation line.

We present Qwen-Image-2.0-RL, a post-training pipeline that applies reinforcement learning from human feedback (RLHF) and on-policy distillation (OPD) to improve both the visual quality and instruction-following capability of the Qwen-Image-2.0 diffusion model.

To provide reliable reward signals, we construct task-specific composite reward models by fine-tuning vision-language models with a pointwise scoring paradigm and chain-of-thought reasoning.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 177. Flow-OPD: On-Policy Distillation for Flow Matching Models

- **Link:** [https://arxiv.org/abs/2605.08063v5](https://arxiv.org/abs/2605.08063v5)
- **Published:** 2026-05-08

"Flow-OPD: On-Policy Distillation for Flow Matching Models" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Existing Flow Matching (FM) text-to-image models suffer from two critical bottlenecks under multi-task alignment: the reward sparsity induced by scalar-valued rewards, and the gradient interference arising from jointly optimizing heterogeneous objectives, which together give rise to a 'seesaw effect' of competing metrics and pervasive ...

Inspired by the success of On-Policy Distillation (OPD) in the large language model community, we propose Flow-OPD, the first unified post-training framework that integrates on-policy distillation into Flow Matching models.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 178. DiT-Reward: Generative Representations for Text-to-Image Reward Modeling

- **Link:** [https://arxiv.org/abs/2606.23626v1](https://arxiv.org/abs/2606.23626v1)
- **Published:** 2026-06-22
- **Tags:** numeric token budget, benchmark/eval

"DiT-Reward: Generative Representations for Text-to-Image Reward Modeling" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Can representations learned for image generation also support the evaluation of generated images?.

We study text-to-image reward prediction as a downstream task of generative representation learning.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 179. ImagenWorld: Stress-Testing Image Generation Models with Explainable Human Evaluation on Open-ended Real-World Tasks

- **Link:** [https://arxiv.org/abs/2603.27862v1](https://arxiv.org/abs/2603.27862v1)
- **Published:** 2026-03-29
- **Tags:** LLM/VLM encoder, benchmark/eval

"ImagenWorld: Stress-Testing Image Generation Models with Explainable Human Evaluation on Open-ended Real-World Tasks" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Advances in diffusion, autoregressive, and hybrid models have enabled high-quality image synthesis for tasks such as text-to-image, editing, and reference-guided composition.

Yet, existing benchmarks remain limited, either focus on isolated tasks, cover only narrow domains, or provide opaque scores without explaining failure modes.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 180. An Empirical Study and Analysis of Text-to-Image Generation Using Large Language Model-Powered Textual Representation

- **Link:** [https://arxiv.org/abs/2405.12914v2](https://arxiv.org/abs/2405.12914v2)
- **Published:** 2024-05-21
- **Tags:** numeric token budget, LLM/VLM encoder

"An Empirical Study and Analysis of Text-to-Image Generation Using Large Language Model-Powered Textual Representation" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

One critical prerequisite for faithful text-to-image generation is the accurate understanding of text inputs.

Existing methods leverage the text encoder of the CLIP model to represent input prompts.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 181. Qwen-Image-Bench: From Generation to Creation in Text-to-Image Evaluation

- **Link:** [https://arxiv.org/abs/2605.28091v2](https://arxiv.org/abs/2605.28091v2)
- **Published:** 2026-05-27
- **Tags:** LLM/VLM encoder, benchmark/eval

"Qwen-Image-Bench: From Generation to Creation in Text-to-Image Evaluation" (2026) introduces or expands evaluation for text-conditioned image generation, often under long or compositional prompts.

Text-to-Image generation has evolved from basic image synthesis into a frequently used core capability in professional creative workflows, where simple text-image alignment can no longer satisfy users' pressing demands for faithful real-world reconstruction and genuine creative expression.

Existing benchmarks, however, remain anchored in these foundational criteria and do not yet capture the nuanced capabilities that matter in authentic artistic practice, making it difficult to reliably distinguish state-of-the-art T2I models.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 182. Red-Teaming Text-to-Image Models via In-Context Experience Replay and Semantic-Preserving Prompt Rewriting

- **Link:** [https://arxiv.org/abs/2411.16769v3](https://arxiv.org/abs/2411.16769v3)
- **Published:** 2024-11-25
- **Tags:** re-prompt/recaption, LLM/VLM encoder, benchmark/eval

"Red-Teaming Text-to-Image Models via In-Context Experience Replay and Semantic-Preserving Prompt Rewriting" (2024) studies prompt rewriting, optimization, or prompt-side control for image generators.

Understanding the capabilities of text-to-image (T2I) models in harmful content generation is essential to safety and compliance.

However, human red-teaming is costly and inconsistent, driving the need for automatic tools that simulate realistic misuse attempts.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 183. Edify Image: High-Quality Image Generation with Pixel Space Laplacian Diffusion Models

- **Link:** [https://arxiv.org/abs/2411.07126v1](https://arxiv.org/abs/2411.07126v1)
- **Published:** 2024-11-11
- **Tags:** re-prompt/recaption

"Edify Image: High-Quality Image Generation with Pixel Space Laplacian Diffusion Models" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

We introduce Edify Image, a family of diffusion models capable of generating photorealistic image content with pixel-perfect accuracy.

Edify Image utilizes cascaded pixel-space diffusion models trained using a novel Laplacian diffusion process, in which image signals at different frequency bands are attenuated at varying rates.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 184. FairFlow: Demystifying and Mitigating Stereotype Bias in Text-to-Image Diffusion Transformers

- **Link:** [https://arxiv.org/abs/2607.03180v1](https://arxiv.org/abs/2607.03180v1)
- **Published:** 2026-07-03
- **Tags:** benchmark/eval

"FairFlow: Demystifying and Mitigating Stereotype Bias in Text-to-Image Diffusion Transformers" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Multimodal diffusion transformers (MM-DiTs) have emerged as the prevalent backbone for modern text-to-image generation systems.

However, they exhibit critical alignment vulnerabilities, systematically manifesting severe stereotype biases even under benign prompts.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 185. Linear-DPO: Linear Direct Preference Optimization for Diffusion and Flow-Matching Generative Models

- **Link:** [https://arxiv.org/abs/2605.21123v1](https://arxiv.org/abs/2605.21123v1)
- **Published:** 2026-05-20
- **Tags:** LLM/VLM encoder

"Linear-DPO: Linear Direct Preference Optimization for Diffusion and Flow-Matching Generative Models" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Direct Preference Optimization (DPO) is successful for alignment in LLMs but still faces challenges in text-to-image generation.

Existing studies are confined to denoising diffusion models while overlooking flow-matching, and suffer from an objective mismatch when applying discrete NLP-based DPO to regression-based generative tasks.\ In this paper, we derive a generalized DPO objective that covers both diffusion and flow-matching via a unified reverse-time SDE f...

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 186. PG-MAP: Joint MAP Optimization for Inference-Time Alignment of Diffusion and Flow-Matching Models

- **Link:** [https://arxiv.org/abs/2606.22958v1](https://arxiv.org/abs/2606.22958v1)
- **Published:** 2026-06-22
- **Tags:** benchmark/eval

"PG-MAP: Joint MAP Optimization for Inference-Time Alignment of Diffusion and Flow-Matching Models" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Inference-time alignment of pretrained text-to-image models is typically performed along a single control axis, such as classifier-free guidance, attention editing, or reward-based latent perturbations.

This limitation prevents modeling joint dependencies between conditioning and latent variables and hinders transfer across generative transports.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 187. UniNDM: A Unified Noise-driven Detection and Mitigation Framework Against Sexual Content in Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2607.16828v1](https://arxiv.org/abs/2607.16828v1)
- **Published:** 2026-07-18

"UniNDM: A Unified Noise-driven Detection and Mitigation Framework Against Sexual Content in Text-to-Image Generation" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Despite the impressive generative capabilities of text-to-image diffusion models, they remain vulnerable to implicit sexual prompts, where subtle cues disguised as benign terms or adversarial tokens unexpectedly generate the inappropriate content due to model biases or latent correlations in training data.

Existing safety mechanisms face fundamental limitations: detection methods primarily identify explicit content and fail to capture implicit malicious intent, while mitigation approaches rely on static negative prompts inadequate for diverse implicit scenarios.

Keep it as background on modern generation/evaluation; use only if its data or metrics inform caption-length decisions.


### 188. AccelAes: Accelerating Diffusion Transformers for Training-Free Aesthetic-Enhanced Image Generation

- **Link:** [https://arxiv.org/abs/2603.12575v2](https://arxiv.org/abs/2603.12575v2)
- **Published:** 2026-03-13
- **Tags:** benchmark/eval

"AccelAes: Accelerating Diffusion Transformers for Training-Free Aesthetic-Enhanced Image Generation" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Diffusion Transformers (DiTs) are a dominant backbone for high-fidelity text-to-image generation due to strong scalability and alignment at high resolutions.

However, quadratic self-attention over dense spatial tokens leads to high inference latency and limits deployment.

Keep it as background on modern generation/evaluation; use only if its data or metrics inform caption-length decisions.


### 189. Reflective Flow Sampling Enhancement

- **Link:** [https://arxiv.org/abs/2603.06165v2](https://arxiv.org/abs/2603.06165v2)
- **Published:** 2026-03-06
- **Tags:** benchmark/eval

"Reflective Flow Sampling Enhancement" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

The growing demand for text-to-image generation has led to rapid advances in generative modeling.

Recently, text-to-image diffusion models trained with flow matching algorithms, such as FLUX, have achieved remarkable progress and emerged as strong alternatives to conventional diffusion models.

Keep it as background on modern generation/evaluation; use only if its data or metrics inform caption-length decisions.


### 190. D-OPSD: On-Policy Self-Distillation for Continuously Tuning Step-Distilled Diffusion Models

- **Link:** [https://arxiv.org/abs/2605.05204v3](https://arxiv.org/abs/2605.05204v3)
- **Published:** 2026-05-06
- **Tags:** LLM/VLM encoder

"D-OPSD: On-Policy Self-Distillation for Continuously Tuning Step-Distilled Diffusion Models" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

The landscape of high-performance image generation models is currently shifting from the inefficient multi-step ones to the efficient few-step counterparts (e.g, Z-Image-Turbo and FLUX.2-klein).

However, these models present significant challenges for direct continuous supervised fine-tuning.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 191. Read It Back: Pretrained MLLMs Are Zero-Shot Reward Models for Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2607.11886v1](https://arxiv.org/abs/2607.11886v1)
- **Published:** 2026-07-13
- **Tags:** LLM/VLM encoder, benchmark/eval

"Read It Back: Pretrained MLLMs Are Zero-Shot Reward Models for Text-to-Image Generation" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

In this paper, we propose SpectraReward, a training-free reward function that turns pretrained MLLMs into off-the-shelf reward models for image-generation reinforcement learning.

Instead of asking the MLLM to judge a generated image or answer decomposed verification questions, SpectraReward measures how well the original prompt can be recovered from the generated image through a single image-conditioned, teacher-forced forward pass.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 192. STAR: SpatioTemporal Adaptive Reward Allocation for Text-to-Image RL Post-Training

- **Link:** [https://arxiv.org/abs/2606.17979v2](https://arxiv.org/abs/2606.17979v2)
- **Published:** 2026-06-16
- **Tags:** benchmark/eval

"STAR: SpatioTemporal Adaptive Reward Allocation for Text-to-Image RL Post-Training" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Existing RL post-training methods for text-to-image generation usually convert the final-image reward into a single scalar advantage and apply it with the same strength to the entire generative trajectory.

However, text-to-image generation naturally has temporal and spatial structure: different denoising steps are responsible for different generation stages, and the content that truly determines text alignment often appears only in part of the image.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 193. Emotion-Aware Image Generation from Korean Diary Text via LLM-based Prompt Translation and LoRA Fine-Tuning

- **Link:** [https://arxiv.org/abs/2606.05816v2](https://arxiv.org/abs/2606.05816v2)
- **Published:** 2026-06-04
- **Tags:** LLM/VLM encoder, benchmark/eval

"Emotion-Aware Image Generation from Korean Diary Text via LLM-based Prompt Translation and LoRA Fine-Tuning" (2026) studies prompt rewriting, optimization, or prompt-side control for generators.

T2I models cannot effectively capture sentiment from various types of text, including diaries, as they primarily focus on visual object-related patterns rather than contextual emotional understanding.

This paper proposes an emotion-aware text-to-image pipeline that generates children's hand drawing style images from short Korean diary entries.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 194. Inf-DiT: Upsampling Any-Resolution Image with Memory-Efficient Diffusion Transformer

- **Link:** [https://arxiv.org/abs/2405.04312v2](https://arxiv.org/abs/2405.04312v2)
- **Published:** 2024-05-07
- **Tags:** re-prompt/recaption, benchmark/eval

"Inf-DiT: Upsampling Any-Resolution Image with Memory-Efficient Diffusion Transformer" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Diffusion models have shown remarkable performance in image generation in recent years.

However, due to a quadratic increase in memory during generating ultra-high-resolution images (e.g.

For length policy: note its train/infer token regime, fixed vs mixed length, and any re-prompt design.


### 195. xGen-VideoSyn-1: High-fidelity Text-to-Video Synthesis with Compressed Representations

- **Link:** [https://arxiv.org/abs/2408.12590v2](https://arxiv.org/abs/2408.12590v2)
- **Published:** 2024-08-22
- **Tags:** long/dense preferred, LLM/VLM encoder

"xGen-VideoSyn-1: High-fidelity Text-to-Video Synthesis with Compressed Representations" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

We present xGen-VideoSyn-1, a text-to-video (T2V) generation model capable of producing realistic scenes from textual descriptions.

Building on recent advancements, such as OpenAI's Sora, we explore the latent diffusion model (LDM) architecture and introduce a video variational autoencoder (VidVAE).

For length policy: note its train/infer token regime, fixed vs mixed length, and any re-prompt design.


### 196. Vision-Language Binding in In-Context Image Generation

- **Link:** [https://arxiv.org/abs/2605.24624v1](https://arxiv.org/abs/2605.24624v1)
- **Published:** 2026-05-23

"Vision-Language Binding in In-Context Image Generation" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

In-context image generation models such as FLUX.2 take a text prompt and an optional reference image as visual conditioning for the output.

Internally, all three inputs -- text, reference image, and the noise tokens -- are concatenated and processed through a single attention stream, where all tokens can attend to one another.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 197. AlphaGRPO: Unlocking Self-Reflective Multimodal Generation in UMMs via Decompositional Verifiable Reward

- **Link:** [https://arxiv.org/abs/2605.12495v1](https://arxiv.org/abs/2605.12495v1)
- **Published:** 2026-05-12
- **Tags:** LLM/VLM encoder, benchmark/eval

"AlphaGRPO: Unlocking Self-Reflective Multimodal Generation in UMMs via Decompositional Verifiable Reward" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

In this paper, we propose AlphaGRPO, a novel framework that applies Group Relative Policy Optimization (GRPO) to AR-Diffusion Unified Multimodal Models (UMMs) to enhance multimodal generation capabilities without an additional cold-start stage.

Our approach unlocks the model's intrinsic potential to perform advanced reasoning tasks: Reasoning Text-to-Image Generation, where the model actively infers implicit user intents, and Self-Reflective Refinement, where it autonomously diagnoses and corrects misalignments in generated outputs.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 198. Pseudo-Unification: Entropy Probing Reveals Divergent Information Patterns in Unified Multimodal Models

- **Link:** [https://arxiv.org/abs/2604.10949v1](https://arxiv.org/abs/2604.10949v1)
- **Published:** 2026-04-13
- **Tags:** LLM/VLM encoder

"Pseudo-Unification: Entropy Probing Reveals Divergent Information Patterns in Unified Multimodal Models" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Unified multimodal models (UMMs) were designed to combine the reasoning ability of large language models (LLMs) with the generation capability of vision models.

In practice, however, this synergy remains elusive: UMMs fail to transfer LLM-like reasoning to image synthesis and exhibit divergent response behaviors.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 199. Cheers: Decoupling Patch Details from Semantic Representations Enables Unified Multimodal Comprehension and Generation

- **Link:** [https://arxiv.org/abs/2603.12793v1](https://arxiv.org/abs/2603.12793v1)
- **Published:** 2026-03-13
- **Tags:** LLM/VLM encoder, benchmark/eval

"Cheers: Decoupling Patch Details from Semantic Representations Enables Unified Multimodal Comprehension and Generation" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

A recent cutting-edge topic in multimodal modeling is to unify visual comprehension and generation within a single model.

However, the two tasks demand mismatched decoding regimes and visual representations, making it non-trivial to jointly optimize within a shared feature space.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 200. SpatialReward: Verifiable Spatial Reward Modeling for Fine-Grained Spatial Consistency in Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2603.22228v1](https://arxiv.org/abs/2603.22228v1)
- **Published:** 2026-03-23
- **Tags:** benchmark/eval

"SpatialReward: Verifiable Spatial Reward Modeling for Fine-Grained Spatial Consistency in Text-to-Image Generation" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Recent advances in text-to-image (T2I) generation via reinforcement learning (RL) have benefited from reward models that assess semantic alignment and visual quality.

However, most existing reward models pay limited attention to fine-grained spatial relationships, often producing images that appear plausible overall yet contain inaccuracies in object positioning.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 201. Qwen-Image-Agent: Bridging the Context Gap in Real-World Image Generation

- **Link:** [https://arxiv.org/abs/2606.26907v2](https://arxiv.org/abs/2606.26907v2)
- **Published:** 2026-06-25
- **Tags:** LLM/VLM encoder, benchmark/eval

"Qwen-Image-Agent: Bridging the Context Gap in Real-World Image Generation" (2026) is a modern system/report in the LLM/VLM-conditioned image generation line.

While text-to-image (T2I) models have achieved remarkable progress, they struggle with real-world requests that are often underspecified, implicit, or dependent on up-to-date knowledge.

We identify this challenge as the Context Gap: the mismatch between the user context and the sufficient generation context for T2I models.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 202. LADR: Locality-Aware Dynamic Rescue for Efficient Text-to-Image Generation with Diffusion Large Language Models

- **Link:** [https://arxiv.org/abs/2603.13450v2](https://arxiv.org/abs/2603.13450v2)
- **Published:** 2026-03-13
- **Tags:** benchmark/eval

"LADR: Locality-Aware Dynamic Rescue for Efficient Text-to-Image Generation with Diffusion Large Language Models" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Discrete Diffusion Language Models have emerged as a compelling paradigm for unified multimodal generation, yet their deployment is hindered by high inference latency arising from iterative decoding.

Existing acceleration strategies often require expensive re-training or fail to leverage the 2D spatial redundancy inherent in visual data.

Keep it as background on modern generation/evaluation; use only if its data or metrics inform caption-length decisions.


### 203. Agentic Retoucher for Text-To-Image Generation

- **Link:** [https://arxiv.org/abs/2601.02046v3](https://arxiv.org/abs/2601.02046v3)
- **Published:** 2026-01-05
- **Tags:** LLM/VLM encoder, benchmark/eval

"Agentic Retoucher for Text-To-Image Generation" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Text-to-image (T2I) diffusion models such as SDXL and FLUX have achieved impressive photorealism, yet small-scale distortions remain pervasive in limbs, face, text and so on.

Existing refinement approaches either perform costly iterative re-generation or rely on vision-language models (VLMs) with weak spatial grounding, leading to semantic drift and unreliable local edits.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 204. Multistep Distillation of Diffusion Models via Moment Matching

- **Link:** [https://arxiv.org/abs/2406.04103v1](https://arxiv.org/abs/2406.04103v1)
- **Published:** 2024-06-06
- **Tags:** re-prompt/recaption

"Multistep Distillation of Diffusion Models via Moment Matching" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

We present a new method for making diffusion models faster to sample.

The method distills many-step diffusion models into few-step models by matching conditional expectations of the clean data given noisy data along the sampling trajectory.

For length policy: note its train/infer token regime, fixed vs mixed length, and any re-prompt design.


### 205. PromptRL: Prompt Matters in RL for Flow-Based Image Generation

- **Link:** [https://arxiv.org/abs/2602.01382v1](https://arxiv.org/abs/2602.01382v1)
- **Published:** 2026-02-01
- **Tags:** benchmark/eval

"PromptRL: Prompt Matters in RL for Flow-Based Image Generation" (2026) studies prompt rewriting, optimization, or prompt-side control for generators.

Flow matching models (FMs) have revolutionized text-to-image (T2I) generation, with reinforcement learning (RL) serving as a critical post-training strategy for alignment with reward objectives.

In this research, we show that current RL pipelines for FMs suffer from two underappreciated yet important limitations: sample inefficiency due to insufficient generation diversity, and pronounced prompt overfitting, where models memorize specific training formulations and exhibit dramatic performance collapse when evaluated on semanti...

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 206. Spectral Image Tokenizer

- **Link:** [https://arxiv.org/abs/2412.09607v2](https://arxiv.org/abs/2412.09607v2)
- **Published:** 2024-12-12
- **Tags:** re-prompt/recaption, benchmark/eval

"Spectral Image Tokenizer" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Image tokenizers map images to sequences of discrete tokens, and are a crucial component of autoregressive transformer-based image generation.

The tokens are typically associated with spatial locations in the input image, arranged in raster scan order, which is not ideal for autoregressive modeling.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 207. Arc2Face: A Foundation Model for ID-Consistent Human Faces

- **Link:** [https://arxiv.org/abs/2403.11641v2](https://arxiv.org/abs/2403.11641v2)
- **Published:** 2024-03-18
- **Tags:** re-prompt/recaption

"Arc2Face: A Foundation Model for ID-Consistent Human Faces" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

This paper presents Arc2Face, an identity-conditioned face foundation model, which, given the ArcFace embedding of a person, can generate diverse photo-realistic images with an unparalleled degree of face similarity than existing models.

Despite previous attempts to decode face recognition features into detailed images, we find that common high-resolution datasets (e.g.

For length policy: note its train/infer token regime, fixed vs mixed length, and any re-prompt design.


### 208. Generative Portrait Shadow Removal

- **Link:** [https://arxiv.org/abs/2410.05525v1](https://arxiv.org/abs/2410.05525v1)
- **Published:** 2024-10-07
- **Tags:** re-prompt/recaption

"Generative Portrait Shadow Removal" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

We introduce a high-fidelity portrait shadow removal model that can effectively enhance the image of a portrait by predicting its appearance under disturbing shadows and highlights.

Portrait shadow removal is a highly ill-posed problem where multiple plausible solutions can be found based on a single image.

For length policy: note its train/infer token regime, fixed vs mixed length, and any re-prompt design.


### 209. Tuning Real-World Image Restoration at Inference: A Test-Time Scaling Paradigm for Flow Matching Models

- **Link:** [https://arxiv.org/abs/2603.22027v1](https://arxiv.org/abs/2603.22027v1)
- **Published:** 2026-03-23
- **Tags:** benchmark/eval

"Tuning Real-World Image Restoration at Inference: A Test-Time Scaling Paradigm for Flow Matching Models" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Although diffusion-based real-world image restoration (Real-IR) has achieved remarkable progress, efficiently leveraging ultra-large-scale pre-trained text-to-image (T2I) models and fully exploiting their potential remain significant challenges.

To address this issue, we propose ResFlow-Tuner, an image restoration framework based on the state-of-the-art flow matching model, FLUX.1-dev, which integrates unified multi-modal fusion (UMMF) with test-time scaling (TTS) to achieve unprecedented restoration performance.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 210. TrioPose: Native Triple-Stream Diffusion Transformers for Pose-Guided Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2606.07053v1](https://arxiv.org/abs/2606.07053v1)
- **Published:** 2026-06-05
- **Tags:** benchmark/eval

"TrioPose: Native Triple-Stream Diffusion Transformers for Pose-Guided Text-to-Image Generation" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Pose-guided text-to-image generation often suffers from limb distortions and feature crosstalk in complex multi-person scenarios.

While existing UNet-based adapters struggle with long-range spatial dependencies, emerging Multimodal Diffusion Transformers (MM-DiTs) offer superior global modeling.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 211. Advances in GRPO for Generation Models: A Survey

- **Link:** [https://arxiv.org/abs/2603.06623v1](https://arxiv.org/abs/2603.06623v1)
- **Published:** 2026-02-21

"Advances in GRPO for Generation Models: A Survey" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Large-scale flow matching models have achieved strong performance across generative tasks such as text-to-image, video, 3D, and speech synthesis.

However, aligning their outputs with human preferences and task-specific objectives remains challenging.

Keep it as background on modern generation/evaluation; use only if its data or metrics inform caption-length decisions.


### 212. Qwen-Image-VAE-2.0 Technical Report

- **Link:** [https://arxiv.org/abs/2605.13565v1](https://arxiv.org/abs/2605.13565v1)
- **Published:** 2026-05-13
- **Tags:** LLM/VLM encoder, benchmark/eval

"Qwen-Image-VAE-2.0 Technical Report" (2026) is a modern system/report in the LLM/VLM-conditioned image generation line.

We present Qwen-Image-VAE-2.0, a suite of high-compression Variational Autoencoders (VAEs) that achieve significant advances in both reconstruction fidelity and diffusability.

To address the reconstruction bottlenecks of high compression, we adopt an improved architecture featuring Global Skip Connections (GSC) and expanded latent channels.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 213. A User-Friendly Framework for Generating Model-Preferred Prompts in Text-to-Image Synthesis

- **Link:** [https://arxiv.org/abs/2402.12760v2](https://arxiv.org/abs/2402.12760v2)
- **Published:** 2024-02-20
- **Tags:** re-prompt/recaption

"A User-Friendly Framework for Generating Model-Preferred Prompts in Text-to-Image Synthesis" (2024) studies prompt rewriting, optimization, or prompt-side control for generators.

Well-designed prompts have demonstrated the potential to guide text-to-image models in generating amazing images.

Although existing prompt engineering methods can provide high-level guidance, it is challenging for novice users to achieve the desired results by manually entering prompts due to a discrepancy between novice-user-input prompts and the model-preferred prompts.

For length policy: note its train/infer token regime, fixed vs mixed length, and any re-prompt design.


### 214. CapHDR2IR: Caption-Driven Transfer from Visible Light to Infrared Domain

- **Link:** [https://arxiv.org/abs/2411.16327v1](https://arxiv.org/abs/2411.16327v1)
- **Published:** 2024-11-25
- **Tags:** long/dense preferred

"CapHDR2IR: Caption-Driven Transfer from Visible Light to Infrared Domain" (2024) focuses on captioning/recaptioning data for text-to-image training.

Infrared (IR) imaging offers advantages in several fields due to its unique ability of capturing content in extreme light conditions.

However, the demanding hardware requirements of high-resolution IR sensors limit its widespread application.

For length policy: note its train/infer token regime, fixed vs mixed length, and any re-prompt design.


### 215. UniGen-AR: Unifying Visual Generation with Auto-Regressive Modeling

- **Link:** [https://arxiv.org/abs/2607.24157v1](https://arxiv.org/abs/2607.24157v1)
- **Published:** 2026-07-27
- **Tags:** LLM/VLM encoder

"UniGen-AR: Unifying Visual Generation with Auto-Regressive Modeling" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Modern computer vision pipelines remain fragmented, with tasks such as text-to-image generation, editing, restoration, and classical perception handled by separate models.

We study Unified Visual Generation (UVG), where a single model produces diverse image-valued outputs through a unified multimodal interface.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 216. Multi-Axis Max@K Reinforcement Learning for Representative Diversity in Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2607.14962v1](https://arxiv.org/abs/2607.14962v1)
- **Published:** 2026-07-16
- **Tags:** benchmark/eval

"Multi-Axis Max@K Reinforcement Learning for Representative Diversity in Text-to-Image Generation" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Text-to-image (T2I) models can synthesize realistic, prompt-aligned images, yet samples generated for the same prompt often cover only a small subset of visually distinct modes.

This limits the diversity of images, and for person-centric prompts, can reflect or amplify demographic skew.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 217. LILAC: Layer-Wise Independent LoRAs and Cascaded Conditioning for Multi-Concept Customization of Diffusion Models

- **Link:** [https://arxiv.org/abs/2607.04801v1](https://arxiv.org/abs/2607.04801v1)
- **Published:** 2026-07-06
- **Tags:** LLM/VLM encoder

"LILAC: Layer-Wise Independent LoRAs and Cascaded Conditioning for Multi-Concept Customization of Diffusion Models" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Personalizing text-to-image diffusion models to render several specific subjects in a coherent image remains challenging: the model must preserve each subject's identity while keeping the scene spatially and visually coherent.

Methods that fuse independently trained concept adapters in a shared weight space (via federated averaging, gradient fusion, or orthogonality constraints) suffer from identity confusion and style bleeding and require joint retraining.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 218. EquiSteer: Cross-Attention Steering Towards a Fairer Text-Guided Image Generation

- **Link:** [https://arxiv.org/abs/2607.01147v1](https://arxiv.org/abs/2607.01147v1)
- **Published:** 2026-07-01

"EquiSteer: Cross-Attention Steering Towards a Fairer Text-Guided Image Generation" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Text-to-image diffusion models power everyday creative tasks, but they still reproduce the demographic biases in their training data.

On common prompts such as ``a photo of a nurse,'' ``a photo of a CEO'', they skew their outputs toward one gender, driven by the statistics of training data rather than anything in the text.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 219. SciIR: A Large-scale Training Dataset and Benchmark for Scientific Image Reasoning Generation

- **Link:** [https://arxiv.org/abs/2606.30124v1](https://arxiv.org/abs/2606.30124v1)
- **Published:** 2026-06-29
- **Tags:** LLM/VLM encoder, benchmark/eval

"SciIR: A Large-scale Training Dataset and Benchmark for Scientific Image Reasoning Generation" (2026) evaluates text-conditioned image generation, often under long or compositional prompts.

While Text-to-Image (T2I) models have shown remarkable success in generating photorealistic visual content, they still struggle with the rigorous semantic alignment and logical reasoning required for scientific imagery.

Inspired by Peirce's Semiotic Triad, we introduce Scientific Image Reasoning (SciIR), a comprehensive resource for training and evaluation of scientific image generation.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 220. JuZhou 1.0 Technical Report: The First Edge-Native Text-to-Image Foundation Model Trained Entirely on China-Developed AI Accelerators

- **Link:** [https://arxiv.org/abs/2606.28421v2](https://arxiv.org/abs/2606.28421v2)
- **Published:** 2026-06-25

"JuZhou 1.0 Technical Report: The First Edge-Native Text-to-Image Foundation Model Trained Entirely on China-Developed AI Accelerators" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Text-to-image (T2I) diffusion models typically require substantial computational resources and cloud infrastructure, posing significant challenges for edge deployment in terms of latency, cost, and user privacy.

We present JuZhou 1.0, an ultra-lightweight T2I foundation model designed for fully offline, on-device execution.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 221. SeFi-Image: A Text-to-Image Foundation Model with Semantic-First Diffusion

- **Link:** [https://arxiv.org/abs/2606.22568v4](https://arxiv.org/abs/2606.22568v4)
- **Published:** 2026-06-21
- **Tags:** LLM/VLM encoder, benchmark/eval

"SeFi-Image: A Text-to-Image Foundation Model with Semantic-First Diffusion" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Training image generation foundation models consumes substantial resources.

Previous methods have attempted to leverage semantic guidance to accelerate the training process, yet their experiments were only conducted on simple datasets such as ImageNet, at low resolutions, and with small-scale models.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 222. DifFRACT: Diffusion Feature Reconstruction and Attribution for Circuit Tracing

- **Link:** [https://arxiv.org/abs/2606.15796v1](https://arxiv.org/abs/2606.15796v1)
- **Published:** 2026-06-14

"DifFRACT: Diffusion Feature Reconstruction and Attribution for Circuit Tracing" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Mechanistic interpretability seeks to explain neural network behavior by decomposing model computations into interpretable features and circuits.

While transcoder-based circuit tracing has recently enabled detailed causal analyses of large language models, multimodal diffusion transformers for image generation remain comparatively opaque.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 223. HPSv3++: Scaling Reward Models Across the Full Spectrum of Diffusion Model Capabilities

- **Link:** [https://arxiv.org/abs/2606.14657v1](https://arxiv.org/abs/2606.14657v1)
- **Published:** 2026-06-12
- **Tags:** LLM/VLM encoder

"HPSv3++: Scaling Reward Models Across the Full Spectrum of Diffusion Model Capabilities" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Reward models guide text-to-image (T2I) systems toward outputs aligned with human preferences.

However, typical reward models such as HPSv3 are trained on pre-annotated data from earlier T2I models, without accounting for quality discriminative shifts arising from evolving model capabilities and reinforcement learning (RL) iterations, limiting their broader applicability.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 224. Trust Your Critic: Robust Reward Modeling and Reinforcement Learning for Faithful Image Editing and Generation

- **Link:** [https://arxiv.org/abs/2603.12247v1](https://arxiv.org/abs/2603.12247v1)
- **Published:** 2026-03-12
- **Tags:** LLM/VLM encoder, benchmark/eval

"Trust Your Critic: Robust Reward Modeling and Reinforcement Learning for Faithful Image Editing and Generation" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Reinforcement learning (RL) has emerged as a promising paradigm for enhancing image editing and text-to-image (T2I) generation.

However, current reward models, which act as critics during RL, often suffer from hallucinations and assign noisy scores, inherently misguiding the optimization process.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 225. SIDiffAgent: Self-Improving Diffusion Agent

- **Link:** [https://arxiv.org/abs/2602.02051v1](https://arxiv.org/abs/2602.02051v1)
- **Published:** 2026-02-02
- **Tags:** LLM/VLM encoder

"SIDiffAgent: Self-Improving Diffusion Agent" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Text-to-image diffusion models have revolutionized generative AI, enabling high-quality and photorealistic image synthesis.

However, their practical deployment remains hindered by several limitations: sensitivity to prompt phrasing, ambiguity in semantic interpretation (e.g., ``mouse" as animal vs.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 226. Mind-Brush: Integrating Agentic Cognitive Search and Reasoning into Image Generation

- **Link:** [https://arxiv.org/abs/2602.01756v1](https://arxiv.org/abs/2602.01756v1)
- **Published:** 2026-02-02
- **Tags:** LLM/VLM encoder, benchmark/eval

"Mind-Brush: Integrating Agentic Cognitive Search and Reasoning into Image Generation" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

While text-to-image generation has achieved unprecedented fidelity, the vast majority of existing models function fundamentally as static text-to-pixel decoders.

Consequently, they often fail to grasp implicit user intentions.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 227. Latent Diffusion, Implicit Amplification: Efficient Continuous-Scale Super-Resolution for Remote Sensing Images

- **Link:** [https://arxiv.org/abs/2410.22830v1](https://arxiv.org/abs/2410.22830v1)
- **Published:** 2024-10-30
- **Tags:** re-prompt/recaption

"Latent Diffusion, Implicit Amplification: Efficient Continuous-Scale Super-Resolution for Remote Sensing Images" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Recent advancements in diffusion models have significantly improved performance in super-resolution (SR) tasks.

However, previous research often overlooks the fundamental differences between SR and general image generation.

For length policy: note its train/infer token regime, fixed vs mixed length, and any re-prompt design.


### 228. RepLDM: Reprogramming Pretrained Latent Diffusion Models for High-Quality, High-Efficiency, High-Resolution Image Generation

- **Link:** [https://arxiv.org/abs/2410.06055v2](https://arxiv.org/abs/2410.06055v2)
- **Published:** 2024-10-08
- **Tags:** re-prompt/recaption

"RepLDM: Reprogramming Pretrained Latent Diffusion Models for High-Quality, High-Efficiency, High-Resolution Image Generation" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

While latent diffusion models (LDMs), such as Stable Diffusion, are designed for high-resolution (HR) image generation, they often struggle with significant structural distortions when generating images at resolutions higher than their training one.

Instead of relying on extensive retraining, a more resource-efficient approach is to reprogram the pretrained model for HR image generation; however, existing methods often result in poor image quality and long inference time.

For length policy: note its train/infer token regime, fixed vs mixed length, and any re-prompt design.


### 229. UltraPixel: Advancing Ultra-High-Resolution Image Synthesis to New Peaks

- **Link:** [https://arxiv.org/abs/2407.02158v2](https://arxiv.org/abs/2407.02158v2)
- **Published:** 2024-07-02
- **Tags:** re-prompt/recaption

"UltraPixel: Advancing Ultra-High-Resolution Image Synthesis to New Peaks" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Ultra-high-resolution image generation poses great challenges, such as increased semantic planning complexity and detail synthesis difficulties, alongside substantial training resource demands.

We present UltraPixel, a novel architecture utilizing cascade diffusion models to generate high-quality images at multiple resolutions (\textit{e.g.}, 1K to 6K) within a single model, while maintaining computational efficiency.

For length policy: note its train/infer token regime, fixed vs mixed length, and any re-prompt design.


### 230. DiM: Diffusion Mamba for Efficient High-Resolution Image Synthesis

- **Link:** [https://arxiv.org/abs/2405.14224v2](https://arxiv.org/abs/2405.14224v2)
- **Published:** 2024-05-23
- **Tags:** re-prompt/recaption, numeric token budget

"DiM: Diffusion Mamba for Efficient High-Resolution Image Synthesis" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Diffusion models have achieved great success in image generation, with the backbone evolving from U-Net to Vision Transformers.

However, the computational cost of Transformers is quadratic to the number of tokens, leading to significant challenges when dealing with high-resolution images.

For length policy: note its train/infer token regime, fixed vs mixed length, and any re-prompt design.


### 231. Arbitrary-Scale Image Generation and Upsampling using Latent Diffusion Model and Implicit Neural Decoder

- **Link:** [https://arxiv.org/abs/2403.10255v1](https://arxiv.org/abs/2403.10255v1)
- **Published:** 2024-03-15
- **Tags:** re-prompt/recaption, benchmark/eval

"Arbitrary-Scale Image Generation and Upsampling using Latent Diffusion Model and Implicit Neural Decoder" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Super-resolution (SR) and image generation are important tasks in computer vision and are widely adopted in real-world applications.

Most existing methods, however, generate images only at fixed-scale magnification and suffer from over-smoothing and artifacts.

For length policy: note its train/infer token regime, fixed vs mixed length, and any re-prompt design.


### 232. Omni-Flow: A Unified Workflow Orchestration and Distributed KV Cache Sharing Framework for Multimodal Inference

- **Link:** [https://arxiv.org/abs/2606.31093v1](https://arxiv.org/abs/2606.31093v1)
- **Published:** 2026-06-30
- **Tags:** LLM/VLM encoder

"Omni-Flow: A Unified Workflow Orchestration and Distributed KV Cache Sharing Framework for Multimodal Inference" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

As large language model (LLM) inference evolves from text-only to multimodal paradigms, inference systems face three challenges: (1) flexible orchestration of multimodal workflows, where heterogeneous computing units exhibit complex dependencies and concurrent control; (2) efficient transmission of massive intermediate data across proc...

Existing solutions deploy LLMs and diffusion models independently, lacking a system-level abstraction for multimodal pipelines; this scatters orchestration logic, tightly couples transmission paths to specific models, and incurs high cost to integrate new models.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 233. ProductWebGen: Benchmarking Multimodal Product Webpage Generation

- **Link:** [https://arxiv.org/abs/2606.01022v1](https://arxiv.org/abs/2606.01022v1)
- **Published:** 2026-05-31
- **Tags:** LLM/VLM encoder, benchmark/eval

"ProductWebGen: Benchmarking Multimodal Product Webpage Generation" (2026) evaluates text-conditioned image generation, often under long or compositional prompts.

Crafting a product display webpage from a source product image, along with layout and visual content instructions, holds significant practical value for domains such as marketing, advertising, and E-commerce.

Intuitively, this task demands strict visual consistency across product displays and high-fidelity instruction following to jointly generate renderable HTML code.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 234. MICON-Bench: Benchmarking and Enhancing Multi-Image Context Image Generation in Unified Multimodal Models

- **Link:** [https://arxiv.org/abs/2602.19497v1](https://arxiv.org/abs/2602.19497v1)
- **Published:** 2026-02-23
- **Tags:** LLM/VLM encoder, benchmark/eval

"MICON-Bench: Benchmarking and Enhancing Multi-Image Context Image Generation in Unified Multimodal Models" (2026) evaluates text-conditioned image generation, often under long or compositional prompts.

Recent advancements in Unified Multimodal Models (UMMs) have enabled remarkable image understanding and generation capabilities.

However, while models like Gemini-2.5-Flash-Image show emerging abilities to reason over multiple related images, existing benchmarks rarely address the challenges of multi-image context generation, focusing mainly on text-to-image or single-image editing tasks.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 235. Orthogonal Negative Guidance in Attention Feature Space for Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2605.29390v1](https://arxiv.org/abs/2605.29390v1)
- **Published:** 2026-05-28
- **Tags:** benchmark/eval

"Orthogonal Negative Guidance in Attention Feature Space for Text-to-Image Generation" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Text-to-image (T2I) models have become increasingly capable of generating high-quality images.

Yet, enforcing the explicit absence of a specified object or attribute remains a fundamentally challenging problem.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 236. A Safety Report on GPT-5.2, Gemini 3 Pro, Qwen3-VL, Grok 4.1 Fast, Nano Banana Pro, and Seedream 4.5

- **Link:** [https://arxiv.org/abs/2601.10527v2](https://arxiv.org/abs/2601.10527v2)
- **Published:** 2026-01-15
- **Tags:** LLM/VLM encoder, benchmark/eval

"A Safety Report on GPT-5.2, Gemini 3 Pro, Qwen3-VL, Grok 4.1 Fast, Nano Banana Pro, and Seedream 4.5" (2026) is a modern system/report in the LLM/VLM-conditioned image generation line.

The rapid evolution of Large Language Models (LLMs) and Multimodal Large Language Models (MLLMs) has driven major gains in reasoning, perception, and generation across language and vision, yet whether these advances translate into comparable improvements in safety remains unclear, partly due to fragmented evaluations that focus on isol...

In this report, we present an integrated safety evaluation of six frontier models--GPT-5.2, Gemini 3 Pro, Qwen3-VL, Grok 4.1 Fast, Nano Banana Pro, and Seedream 4.5--assessing each across language, vision-language, and image generation using a unified protocol that combines benchmark, adversarial, multilingual, and compliance evaluations.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 237. Leveraging Verifier-Based Reinforcement Learning in Image Editing

- **Link:** [https://arxiv.org/abs/2604.27505v2](https://arxiv.org/abs/2604.27505v2)
- **Published:** 2026-04-30
- **Tags:** LLM/VLM encoder, benchmark/eval

"Leveraging Verifier-Based Reinforcement Learning in Image Editing" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

While Reinforcement Learning from Human Feedback (RLHF) has become a pivotal paradigm for text-to-image generation, its application to image editing remains largely unexplored.

A key bottleneck is the lack of a robust general reward model for all editing tasks.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 238. OSPO: Object-Centric Self-Improving Preference Optimization for Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2506.02015v3](https://arxiv.org/abs/2506.02015v3)
- **Published:** 2025-05-28
- **Tags:** LLM/VLM encoder, benchmark/eval

"OSPO: Object-Centric Self-Improving Preference Optimization for Text-to-Image Generation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Recent advances in Multimodal Large Language Models (MLLMs) have enabled unified multimodal understanding and generation.

However, they still struggle with fine-grained text-image alignment, often failing to faithfully depict objects with correct attributes such as color, shape, and spatial relations.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 239. Visual Puns from Idioms: An Iterative LLM-T2IM-MLLM Framework

- **Link:** [https://arxiv.org/abs/2511.22943v1](https://arxiv.org/abs/2511.22943v1)
- **Published:** 2025-11-28
- **Tags:** LLM/VLM encoder, benchmark/eval

"Visual Puns from Idioms: An Iterative LLM-T2IM-MLLM Framework" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

We study idiom-based visual puns--images that align an idiom's literal and figurative meanings--and present an iterative framework that coordinates a large language model (LLM), a text-to-image model (T2IM), and a multimodal LLM (MLLM) for automatic generation and evaluation.

Given an idiom, the system iteratively (i) generates detailed visual prompts, (ii) synthesizes an image, (iii) infers the idiom from the image, and (iv) refines the prompt until recognition succeeds or a step limit is reached.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 240. Qwen-Image-Flash: Beyond Objective Design

- **Link:** [https://arxiv.org/abs/2606.03746v2](https://arxiv.org/abs/2606.03746v2)
- **Published:** 2026-06-02
- **Tags:** LLM/VLM encoder

"Qwen-Image-Flash: Beyond Objective Design" (2026) is a modern system/report in the LLM/VLM-conditioned image generation line.

Few-step distillation has become an effective strategy for accelerating advanced visual generative models, yet prior work has largely focused on distillation objectives.

In this work, we revisit few-step distillation from a complementary perspective, focusing on the training recipe that critically shapes student performance.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 241. MemoGen: Can Past Experience Improve Future Text-to-Image Generation?

- **Link:** [https://arxiv.org/abs/2606.03243v1](https://arxiv.org/abs/2606.03243v1)
- **Published:** 2026-06-02
- **Tags:** LLM/VLM encoder, benchmark/eval

"MemoGen: Can Past Experience Improve Future Text-to-Image Generation?" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Modern text-to-image models have achieved strong visual synthesis, yet remain unreliable when prompts require implicit visual constraints, relational reasoning, or external knowledge.

Existing retrieval-augmented and agentic generation methods mitigate this issue by acquiring external knowledge, references, or refined prompts for the current request, yet they typically treat each generation as an isolated episode and do not systematically preserve past successes or failures for future use.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 242. GeoDiv: Framework For Measuring Geographical Diversity In Text-To-Image Models

- **Link:** [https://arxiv.org/abs/2602.22120v1](https://arxiv.org/abs/2602.22120v1)
- **Published:** 2026-02-25
- **Tags:** benchmark/eval

"GeoDiv: Framework For Measuring Geographical Diversity In Text-To-Image Models" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Text-to-image (T2I) models are rapidly gaining popularity, yet their outputs often lack geographical diversity, reinforce stereotypes, and misrepresent regions.

Given their broad reach, it is critical to rigorously evaluate how these models portray the world.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 243. ELDiff: When Evidential Learning Meets Text-to-Image Diffusion

- **Link:** [https://arxiv.org/abs/2606.20924v1](https://arxiv.org/abs/2606.20924v1)
- **Published:** 2026-06-18
- **Tags:** LLM/VLM encoder

"ELDiff: When Evidential Learning Meets Text-to-Image Diffusion" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

In multi-object text-to-image (T2I) diffusion, ensuring semantic consistency between textual prompts and generated visual content is crucial for image synthesis.

However, such consistency constraint is often underemphasized in the denoising process of diffusion models.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 244. Boogu-Image-0.1: Boosting Open Agentic Multimodal Generation via Understanding under a Minimal Budget

- **Link:** [https://arxiv.org/abs/2607.13125v2](https://arxiv.org/abs/2607.13125v2)
- **Published:** 2026-07-14
- **Tags:** benchmark/eval

"Boogu-Image-0.1: Boosting Open Agentic Multimodal Generation via Understanding under a Minimal Budget" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

We introduce Boogu-Image-0.1, an open-source unified multimodal understanding and generation model family, comprising Base, Turbo, Edit, and Edit-Turbo variants.

It delivers competitive performance in high-quality text-to-image generation, fast inference, instruction-based editing, and bilingual (Chinese-English) text rendering.

Keep it as background on modern generation/evaluation; use only if its data or metrics inform caption-length decisions.


### 245. UniFusion: Vision-Language Model as Unified Encoder in Image Generation

- **Link:** [https://arxiv.org/abs/2510.12789v1](https://arxiv.org/abs/2510.12789v1)
- **Published:** 2025-10-14
- **Tags:** LLM/VLM encoder

"UniFusion: Vision-Language Model as Unified Encoder in Image Generation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Although recent advances in visual generation have been remarkable, most existing architectures still depend on distinct encoders for images and text.

This separation constrains diffusion models' ability to perform cross-modal reasoning and knowledge transfer.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 246. Reflect-DiT: Inference-Time Scaling for Text-to-Image Diffusion Transformers via In-Context Reflection

- **Link:** [https://arxiv.org/abs/2503.12271v1](https://arxiv.org/abs/2503.12271v1)
- **Published:** 2025-03-15
- **Tags:** benchmark/eval

"Reflect-DiT: Inference-Time Scaling for Text-to-Image Diffusion Transformers via In-Context Reflection" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

The predominant approach to advancing text-to-image generation has been training-time scaling, where larger models are trained on more data using greater computational resources.

While effective, this approach is computationally expensive, leading to growing interest in inference-time scaling to improve performance.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 247. NanoFLUX: Distillation-Driven Compression of Large Text-to-Image Generation Models for Mobile Devices

- **Link:** [https://arxiv.org/abs/2602.06879v1](https://arxiv.org/abs/2602.06879v1)
- **Published:** 2026-02-06
- **Tags:** numeric token budget

"NanoFLUX: Distillation-Driven Compression of Large Text-to-Image Generation Models for Mobile Devices" (2026) is a modern system/report in the LLM/VLM-conditioned image generation line.

While large-scale text-to-image diffusion models continue to improve in visual quality, their increasing scale has widened the gap between state-of-the-art models and on-device solutions.

To address this gap, we introduce NanoFLUX, a 2.4B text-to-image flow-matching model distilled from 17B FLUX.1-Schnell using a progressive compression pipeline designed to preserve generation quality.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 248. NanoControl: A Lightweight Framework for Precise and Efficient Control in Diffusion Transformer

- **Link:** [https://arxiv.org/abs/2508.10424v1](https://arxiv.org/abs/2508.10424v1)
- **Published:** 2025-08-14
- **Tags:** benchmark/eval

"NanoControl: A Lightweight Framework for Precise and Efficient Control in Diffusion Transformer" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Diffusion Transformers (DiTs) have demonstrated exceptional capabilities in text-to-image synthesis.

However, in the domain of controllable text-to-image generation using DiTs, most existing methods still rely on the ControlNet paradigm originally designed for UNet-based diffusion models.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 249. Differential Vector Erasure: Unified Training-Free Concept Erasure for Flow Matching Models

- **Link:** [https://arxiv.org/abs/2602.01089v1](https://arxiv.org/abs/2602.01089v1)
- **Published:** 2026-02-01

"Differential Vector Erasure: Unified Training-Free Concept Erasure for Flow Matching Models" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Text-to-image diffusion models have demonstrated remarkable capabilities in generating high-quality images, yet their tendency to reproduce undesirable concepts, such as NSFW content, copyrighted styles, or specific objects, poses growing concerns for safe and controllable deployment.

While existing concept erasure approaches primarily focus on DDPM-based diffusion models and rely on costly fine-tuning, the recent emergence of flow matching models introduces a fundamentally different generative paradigm for which prior methods are not directly applicable.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 250. Z-Erase: Enabling Concept Erasure in Single-Stream Diffusion Transformers

- **Link:** [https://arxiv.org/abs/2603.25074v2](https://arxiv.org/abs/2603.25074v2)
- **Published:** 2026-03-26

"Z-Erase: Enabling Concept Erasure in Single-Stream Diffusion Transformers" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Concept erasure serves as a vital safety mechanism for removing unwanted concepts from text-to-image (T2I) models.

While extensively studied in U-Net and dual-stream architectures (e.g., Flux), this task remains under-explored in the recent emerging paradigm of single-stream diffusion transformers (e.g., Z-Image).

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 251. DIAMOND: Directed Inference for Artifact Mitigation in Flow Matching Models

- **Link:** [https://arxiv.org/abs/2602.00883v1](https://arxiv.org/abs/2602.00883v1)
- **Published:** 2026-01-31

"DIAMOND: Directed Inference for Artifact Mitigation in Flow Matching Models" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Despite impressive results from recent text-to-image models like FLUX, visual and anatomical artifacts remain a significant hurdle for practical and professional use.

Existing methods for artifact reduction, typically work in a post-hoc manner, consequently failing to intervene effectively during the core image formation process.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 252. SuperFlow: Training Flow Matching Models with RL on the Fly

- **Link:** [https://arxiv.org/abs/2512.17951v3](https://arxiv.org/abs/2512.17951v3)
- **Published:** 2025-12-17

"SuperFlow: Training Flow Matching Models with RL on the Fly" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Recent progress in flow-based generative models and reinforcement learning (RL) has improved text-image alignment and visual quality.

However, current RL training for flow models still has two main problems: (i) GRPO-style fixed per-prompt group sizes ignore variation in sampling importance across prompts, which leads to inefficient sampling and slower training; and (ii) trajectory-level advantages are reused as per-step estimates, which biases credit assignment alon...

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 253. Visual Stereotypes of Autism Spectrum in Janus-Pro-7B, DALL-E, Stable Diffusion, SDXL, FLUX, and Midjourney

- **Link:** [https://arxiv.org/abs/2407.16292v3](https://arxiv.org/abs/2407.16292v3)
- **Published:** 2024-07-23

"Visual Stereotypes of Autism Spectrum in Janus-Pro-7B, DALL-E, Stable Diffusion, SDXL, FLUX, and Midjourney" (2024) is a modern system/report in the LLM/VLM-conditioned image generation line.

Avoiding systemic discrimination of neurodiverse individuals is an ongoing challenge in training AI models, which often propagate negative stereotypes.

This study examined whether six text-to-image models (Janus-Pro-7B VL2 vs.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 254. SANA-Streaming: Real-time Streaming Video Editing with Hybrid Diffusion Transformer

- **Link:** [https://arxiv.org/abs/2605.30409v1](https://arxiv.org/abs/2605.30409v1)
- **Published:** 2026-05-28
- **Tags:** numeric token budget

"SANA-Streaming: Real-time Streaming Video Editing with Hybrid Diffusion Transformer" (2026) is a modern system/report in the LLM/VLM-conditioned image generation line.

Real-time streaming video-to-video editing (V2V) is critical for interactive applications such as live broadcasting and gaming, yet it remains a formidable challenge due to the stringent requirements for temporal consistency and inference throughput.

In this paper, we present SANA-Streaming, a system-algorithm co-designed framework for high-resolution, real-time streaming video editing on consumer GPUs, with the following three core designs: (1) Hybrid Diffusion Transformer architecture introduces softmax attention in part of the blocks to improve local modeling capabilities while preserving...

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 255. Lumina-mGPT: Illuminate Flexible Photorealistic Text-to-Image Generation with Multimodal Generative Pretraining

- **Link:** [https://arxiv.org/abs/2408.02657v3](https://arxiv.org/abs/2408.02657v3)
- **Published:** 2024-08-05
- **Tags:** LLM/VLM encoder

"Lumina-mGPT: Illuminate Flexible Photorealistic Text-to-Image Generation with Multimodal Generative Pretraining" (2024) is a modern system/report in the LLM/VLM-conditioned image generation line.

We present Lumina-mGPT, a family of multimodal autoregressive models capable of various vision and language tasks, particularly excelling in generating flexible photorealistic images from text descriptions.

By initializing from multimodal Generative PreTraining (mGPT), we demonstrate that decoder-only Autoregressive (AR) model can achieve image generation performance comparable to modern diffusion models with high efficiency through Flexible Progressive Supervised Fine-tuning (FP-SFT).

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 256. RubiCap: Rubric-Guided Reinforcement Learning for Dense Image Captioning

- **Link:** [https://arxiv.org/abs/2603.09160v1](https://arxiv.org/abs/2603.09160v1)
- **Published:** 2026-03-10
- **Tags:** LLM/VLM encoder, benchmark/eval

"RubiCap: Rubric-Guided Reinforcement Learning for Dense Image Captioning" (2026) focuses on captioning/recaptioning data that feeds text-to-image training.

Dense image captioning is critical for cross-modal alignment in vision-language pretraining and text-to-image generation, but scaling expert-quality annotations is prohibitively expensive.

While synthetic captioning via strong vision-language models (VLMs) is a practical alternative, supervised distillation often yields limited output diversity and weak generalization.

For our length question: extract its train/infer token policy, whether length is fixed or mixed, and any stated reason those choices work.


### 257. Personalizing Text-to-Image Generation to Individual Taste

- **Link:** [https://arxiv.org/abs/2604.07427v1](https://arxiv.org/abs/2604.07427v1)
- **Published:** 2026-04-08
- **Tags:** benchmark/eval

"Personalizing Text-to-Image Generation to Individual Taste" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Modern text-to-image (T2I) models generate high-fidelity visuals but remain indifferent to individual user preferences.

While existing reward models optimize for "average" human appeal, they fail to capture the inherent subjectivity of aesthetic judgment.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 258. Evolve to Inspire: Novelty Search for Diverse Image Generation

- **Link:** [https://arxiv.org/abs/2511.00686v1](https://arxiv.org/abs/2511.00686v1)
- **Published:** 2025-11-01
- **Tags:** LLM/VLM encoder, benchmark/eval

"Evolve to Inspire: Novelty Search for Diverse Image Generation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Text-to-image diffusion models, while proficient at generating high-fidelity images, often suffer from limited output diversity, hindering their application in exploratory and ideation tasks.

Existing prompt optimization techniques typically target aesthetic fitness or are ill-suited to the creative visual domain.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 259. Agentic Flow Steering and Parallel Rollout Search for Spatially Grounded Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2603.18627v1](https://arxiv.org/abs/2603.18627v1)
- **Published:** 2026-03-19
- **Tags:** LLM/VLM encoder, benchmark/eval

"Agentic Flow Steering and Parallel Rollout Search for Spatially Grounded Text-to-Image Generation" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Precise Text-to-Image (T2I) generation has achieved great success but is hindered by the limited relational reasoning of static text encoders and the error accumulation in open-loop sampling.

Without real-time feedback, initial semantic ambiguities during the Ordinary Differential Equation trajectory inevitably escalate into stochastic deviations from spatial constraints.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 260. STARFlow2: Bridging Language Models and Normalizing Flows for Unified Multimodal Generation

- **Link:** [https://arxiv.org/abs/2605.08029v1](https://arxiv.org/abs/2605.08029v1)
- **Published:** 2026-05-08
- **Tags:** LLM/VLM encoder, benchmark/eval

"STARFlow2: Bridging Language Models and Normalizing Flows for Unified Multimodal Generation" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Deep generative models have advanced rapidly across text and vision, motivating unified multimodal systems that can understand, reason over, and generate interleaved text-image sequences.

Most existing approaches combine autoregressive language modeling with diffusion-based image generators, inheriting a structural mismatch between causal text generation and iterative visual denoising.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 261. Safe Autoregressive Image Generation with Iterative Self-Improving Codebooks

- **Link:** [https://arxiv.org/abs/2606.27147v1](https://arxiv.org/abs/2606.27147v1)
- **Published:** 2026-06-25

"Safe Autoregressive Image Generation with Iterative Self-Improving Codebooks" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Unlike diffusion-based models that operate in continuous latent spaces, autoregressive unified multimodal models produce images by sequentially predicting discretized visual tokens.

These tokens are derived from a codebook that maps embeddings to quantized visual patterns.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 262. Redirecting the Flow: Image Customization through Attention Distribution Shift

- **Link:** [https://arxiv.org/abs/2606.16866v1](https://arxiv.org/abs/2606.16866v1)
- **Published:** 2026-06-15
- **Tags:** benchmark/eval

"Redirecting the Flow: Image Customization through Attention Distribution Shift" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Subject-driven image customization aims to generate images that not only follow textual instructions but also preserve the identity of a given reference subject.

Existing approaches, including test-time fine-tuning, encoder-based methods, and token competition in shared attention spaces, suffer from limited efficiency, misalignment between extracted reference features and the generative process, and interference from irrelevant information.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 263. Efficient Reinforcement for Visual-Textual Thinking with Discrete Diffusion Model

- **Link:** [https://arxiv.org/abs/2606.14792v1](https://arxiv.org/abs/2606.14792v1)
- **Published:** 2026-06-11

"Efficient Reinforcement for Visual-Textual Thinking with Discrete Diffusion Model" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

RL-based post-training has been widely adopted to enable interleaved visual and textual reasoning in unified multimodal models capable of both text and image generation.

However, most existing approaches are built upon autoregressive (AR) unified models, which require full image regeneration during visual reasoning.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 264. Bridging Modal Isolation in Interleaved Thinking: Supervising Modality Transitions via Stepwise Reinforcement

- **Link:** [https://arxiv.org/abs/2606.12886v2](https://arxiv.org/abs/2606.12886v2)
- **Published:** 2026-06-11
- **Tags:** benchmark/eval

"Bridging Modal Isolation in Interleaved Thinking: Supervising Modality Transitions via Stepwise Reinforcement" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Interleaved thinking, where a unified multimodal model alternates between textual reasoning and visual generation, has shown promise on spatial and physical tasks.

However, in complex long-chain scenarios, we identify a fundamental failure mode: generated images diverge from the textual context while subsequent text ignores the visual evidence, causing the two modalities to alternate without genuinely informing each other.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 265. Edit-R2: Context-Aware Reinforcement Learning for Multi-Turn Image Editing

- **Link:** [https://arxiv.org/abs/2606.05950v2](https://arxiv.org/abs/2606.05950v2)
- **Published:** 2026-06-04
- **Tags:** benchmark/eval

"Edit-R2: Context-Aware Reinforcement Learning for Multi-Turn Image Editing" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Text-guided image editing has advanced rapidly with diffusion models and unified multimodal foundation models.

However, most existing methods remain confined to single-turn settings, overlooking the more realistic scenario of multi-turn in-context editing, where users iteratively refine an image through a sequence of instructions.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 266. Are we really tilting? The mechanics of reward guidance in flow and diffusion models

- **Link:** [https://arxiv.org/abs/2606.02884v1](https://arxiv.org/abs/2606.02884v1)
- **Published:** 2026-06-01

"Are we really tilting? The mechanics of reward guidance in flow and diffusion models" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Reward guidance algorithms steer a learned generative process toward the reward-tilted measure at inference time.

While empirically powerful, these methods are prone to reward hacking: the guided model over-optimizes the reward at the cost of fidelity to the learned distribution.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 267. EDGE-Shield: Efficient Denoising-staGE Shield for Violative Content Filtering via Scalable Reference-Based Matching

- **Link:** [https://arxiv.org/abs/2604.06063v2](https://arxiv.org/abs/2604.06063v2)
- **Published:** 2026-04-04
- **Tags:** LLM/VLM encoder

"EDGE-Shield: Efficient Denoising-staGE Shield for Violative Content Filtering via Scalable Reference-Based Matching" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

The advent of Text-to-Image generative models poses significant risks of copyright violation and deepfake generation.

Since the rapid proliferation of new copyrighted works and private individuals constantly emerges, reference-based training-free content filters are essential for providing up-to-date protection without the constraints of a fixed knowledge cutoff.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 268. DermaFlux: Synthetic Skin Lesion Generation with Rectified Flows for Enhanced Image Classification

- **Link:** [https://arxiv.org/abs/2603.16392v1](https://arxiv.org/abs/2603.16392v1)
- **Published:** 2026-03-17
- **Tags:** LLM/VLM encoder

"DermaFlux: Synthetic Skin Lesion Generation with Rectified Flows for Enhanced Image Classification" (2026) is a modern system/report in the LLM/VLM-conditioned image generation line.

Despite recent advances in deep generative modeling, skin lesion classification systems remain constrained by the limited availability of large, diverse, and well-annotated clinical datasets, resulting in class imbalance between benign and malignant lesions and consequently reduced generalization performance.

We introduce DermaFlux, a rectified flow-based text-to-image generative framework that synthesizes clinically grounded skin lesion images from natural language descriptions of dermatological attributes.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 269. EditHF-1M: A Million-Scale Rich Human Preference Feedback for Image Editing

- **Link:** [https://arxiv.org/abs/2603.14916v1](https://arxiv.org/abs/2603.14916v1)
- **Published:** 2026-03-16
- **Tags:** LLM/VLM encoder, benchmark/eval

"EditHF-1M: A Million-Scale Rich Human Preference Feedback for Image Editing" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Recent text-guided image editing (TIE) models have achieved remarkable progress, while many edited images still suffer from issues such as artifacts, unexpected editings, unaesthetic contents.

Although some benchmarks and methods have been proposed for evaluating edited images, scalable evaluation models are still lacking, which limits the development of human feedback reward models for image editing.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 270. TextPecker: Rewarding Structural Anomaly Quantification for Enhancing Visual Text Rendering

- **Link:** [https://arxiv.org/abs/2602.20903v3](https://arxiv.org/abs/2602.20903v3)
- **Published:** 2026-02-24
- **Tags:** LLM/VLM encoder, benchmark/eval

"TextPecker: Rewarding Structural Anomaly Quantification for Enhancing Visual Text Rendering" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Visual Text Rendering (VTR) remains a critical challenge in text-to-image generation, where even advanced models frequently produce text with structural anomalies such as distortion, blurriness, and misalignment.

However, we find that leading MLLMs and specialist OCR models largely fail to perceive these structural anomalies, creating a critical bottleneck for both VTR evaluation and RL-based optimization.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 271. Synthetic Perception: Can Generated Images Unlock Latent Visual Prior for Text-Centric Reasoning?

- **Link:** [https://arxiv.org/abs/2506.17623v2](https://arxiv.org/abs/2506.17623v2)
- **Published:** 2025-06-21
- **Tags:** LLM/VLM encoder, benchmark/eval

"Synthetic Perception: Can Generated Images Unlock Latent Visual Prior for Text-Centric Reasoning?" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

A significant ``modality gap" exists between the abundance of text-only data and the increasing power of multimodal models.

This work systematically investigates whether images generated on-the-fly by Text-to-Image (T2I) models can serve as a mechanism to unlock latent visual priors for text-centric reasoning.

For length policy: note its train/infer token regime, fixed vs mixed length, and any re-prompt design.


### 272. Decoder-Only LLMs are Better Controllers for Diffusion Models

- **Link:** [https://arxiv.org/abs/2502.04412v1](https://arxiv.org/abs/2502.04412v1)
- **Published:** 2025-02-06
- **Tags:** LLM/VLM encoder, benchmark/eval

"Decoder-Only LLMs are Better Controllers for Diffusion Models" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Groundbreaking advancements in text-to-image generation have recently been achieved with the emergence of diffusion models.

These models exhibit a remarkable ability to generate highly artistic and intricately detailed images based on textual prompts.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 273. HFI: A unified framework for training-free detection and implicit watermarking of latent diffusion model generated images

- **Link:** [https://arxiv.org/abs/2412.20704v2](https://arxiv.org/abs/2412.20704v2)
- **Published:** 2024-12-30
- **Tags:** re-prompt/recaption

"HFI: A unified framework for training-free detection and implicit watermarking of latent diffusion model generated images" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Dramatic advances in the quality of the latent diffusion models (LDMs) also led to the malicious use of AI-generated images.

While current AI-generated image detection methods assume the availability of real/AI-generated images for training, this is practically limited given the vast expressibility of LDMs.

For length policy: note its train/infer token regime, fixed vs mixed length, and any re-prompt design.


### 274. Beware of Aliases -- Signal Preservation is Crucial for Robust Image Restoration

- **Link:** [https://arxiv.org/abs/2406.07435v2](https://arxiv.org/abs/2406.07435v2)
- **Published:** 2024-06-11
- **Tags:** re-prompt/recaption

"Beware of Aliases -- Signal Preservation is Crucial for Robust Image Restoration" (2024) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Image restoration networks are usually comprised of an encoder and a decoder, responsible for aggregating image content from noisy, distorted data and to restore clean, undistorted images, respectively.

Data aggregation as well as high-resolution image generation both usually come at the risk of involving aliases, i.e.~standard architectures put their ability to reconstruct the model input in jeopardy to reach high PSNR values on validation data.

For length policy: note its train/infer token regime, fixed vs mixed length, and any re-prompt design.


### 275. Twins: Learn to Predict Unified Representations with Focal Loss

- **Link:** [https://arxiv.org/abs/2607.22531v1](https://arxiv.org/abs/2607.22531v1)
- **Published:** 2026-07-24
- **Tags:** numeric token budget, benchmark/eval

"Twins: Learn to Predict Unified Representations with Focal Loss" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Unified multimodal models seek a shared visual token space that supports both multimodal understanding and image generation.

Discrete methods unify the interface via a shared codebook, whereas continuous pipelines often rely on two disparate representations -- semantic features (e.g., ViT) for understanding and low-level latents (e.g., VAE) for synthesis -- resulting in mismatched latent spaces.

For length policy: note its train/infer token regime, fixed vs mixed length, and any re-prompt design.


### 276. Think, Plan, Paint: Layout-Aware Reasoning for Controllable Image Generation in Unified Models

- **Link:** [https://arxiv.org/abs/2607.16409v1](https://arxiv.org/abs/2607.16409v1)
- **Published:** 2026-07-17
- **Tags:** LLM/VLM encoder, benchmark/eval

"Think, Plan, Paint: Layout-Aware Reasoning for Controllable Image Generation in Unified Models" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Unified Multimodal Large Language Models (MLLMs) offer a promising paradigm for unifying visual understanding and generation, yet they still struggle to follow complex spatial instructions and logical constraints in controllable image generation.

To address this gap, we present ATLAS, a unified framework that equips MLLMs with a human-like "Think, Plan, and Paint" paradigm.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 277. UniDDT: Unifying Multimodal Understanding and Generation with Decoupled Diffusion Transformer

- **Link:** [https://arxiv.org/abs/2606.16255v1](https://arxiv.org/abs/2606.16255v1)
- **Published:** 2026-06-15
- **Tags:** LLM/VLM encoder, benchmark/eval

"UniDDT: Unifying Multimodal Understanding and Generation with Decoupled Diffusion Transformer" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Unified Multimodal Models (UMMs) have emerged as a critical direction for general-purpose multimodal intelligence, integrating understanding and generation into a single framework.

However, existing UMMs face prominent challenges: (1) the inherent learning conflicts between visual understanding and generation tasks, leading to suboptimal modeling in both tasks; (2) different understanding and generation visual spaces impeding scalability; (3) over-reliance on task-specific data that neglects the duality of text-i...

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 278. Do Text Edits Generalize to Visual Generation? Benchmarking Cross-Modal Knowledge Editing in UMMs

- **Link:** [https://arxiv.org/abs/2606.00477v1](https://arxiv.org/abs/2606.00477v1)
- **Published:** 2026-05-30
- **Tags:** benchmark/eval

"Do Text Edits Generalize to Visual Generation? Benchmarking Cross-Modal Knowledge Editing in UMMs" (2026) evaluates text-conditioned image generation, often under long or compositional prompts.

Unified multimodal models (UMMs) have emerged as a promising paradigm for general-purpose multimodal intelligence.

As they are deployed in real-world applications, effectively updating internal knowledge becomes critical.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 279. Benchmarking and Evolving Reason-Reflect-Rectify for Reflective Visual Generation

- **Link:** [https://arxiv.org/abs/2605.19639v1](https://arxiv.org/abs/2605.19639v1)
- **Published:** 2026-05-19
- **Tags:** LLM/VLM encoder, benchmark/eval

"Benchmarking and Evolving Reason-Reflect-Rectify for Reflective Visual Generation" (2026) evaluates text-conditioned image generation, often under long or compositional prompts.

Text-to-Image (T2I) models and Unified Multimodal Models (UMMs) have achieved remarkable progress in visual generation.

However, their reliance on a single-pass generation paradigm limits their ability to handle complex prompts requiring iterative refinement.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 280. Exploring Spatial Intelligence from a Generative Perspective

- **Link:** [https://arxiv.org/abs/2604.20570v1](https://arxiv.org/abs/2604.20570v1)
- **Published:** 2026-04-22
- **Tags:** benchmark/eval

"Exploring Spatial Intelligence from a Generative Perspective" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Spatial intelligence is essential for multimodal large language models, yet current benchmarks largely assess it only from an understanding perspective.

We ask whether modern generative or unified multimodal models also possess generative spatial intelligence (GSI), the ability to respect and manipulate 3D spatial constraints during image generation, and whether such capability can be measured or improved.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 281. Think in Strokes, Not Pixels: Process-Driven Image Generation via Interleaved Reasoning

- **Link:** [https://arxiv.org/abs/2604.04746v3](https://arxiv.org/abs/2604.04746v3)
- **Published:** 2026-04-06
- **Tags:** benchmark/eval

"Think in Strokes, Not Pixels: Process-Driven Image Generation via Interleaved Reasoning" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Humans paint images incrementally: they plan a global layout, sketch a coarse draft, inspect, and refine details, and most importantly, each step is grounded in the evolving visual states.

However, can unified multimodal models trained on text-image interleaved datasets also imagine the chain of intermediate states?.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 282. Unsafe by Reciprocity: How Generation-Understanding Coupling Undermines Safety in Unified Multimodal Models

- **Link:** [https://arxiv.org/abs/2603.27332v1](https://arxiv.org/abs/2603.27332v1)
- **Published:** 2026-03-28
- **Tags:** LLM/VLM encoder, benchmark/eval

"Unsafe by Reciprocity: How Generation-Understanding Coupling Undermines Safety in Unified Multimodal Models" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Recent advances in Large Language Models (LLMs) and Text-to-Image (T2I) models have led to the emergence of Unified Multimodal Models (UMMs), where multimodal understanding and image generation are tightly integrated within a shared architecture.

Prior studies suggest that such reciprocity enhances cross-functionality performance through shared representations and joint optimization.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 283. Dress-ED: Instruction-Guided Editing for Virtual Try-On and Try-Off

- **Link:** [https://arxiv.org/abs/2603.22607v4](https://arxiv.org/abs/2603.22607v4)
- **Published:** 2026-03-23
- **Tags:** LLM/VLM encoder, benchmark/eval

"Dress-ED: Instruction-Guided Editing for Virtual Try-On and Try-Off" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Recent advances in Virtual Try-On (VTON) and Virtual Try-Off (VTOFF) have greatly improved photo-realistic fashion synthesis and garment reconstruction.

However, existing datasets remain static, lacking instruction-driven editing for controllable and interactive fashion generation.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 284. Towards Unified Multimodal Interleaved Generation via Group Relative Policy Optimization

- **Link:** [https://arxiv.org/abs/2603.09538v1](https://arxiv.org/abs/2603.09538v1)
- **Published:** 2026-03-10

"Towards Unified Multimodal Interleaved Generation via Group Relative Policy Optimization" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Unified vision-language models have made significant progress in multimodal understanding and generation, yet they largely fall short in producing multimodal interleaved outputs, which is a crucial capability for tasks like visual storytelling and step-by-step visual reasoning.

In this work, we propose a reinforcement learning-based post-training strategy to unlock this capability in existing unified models, without relying on large-scale multimodal interleaved datasets.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 285. CoCo: Code as CoT for Text-to-Image Preview and Rare Concept Generation

- **Link:** [https://arxiv.org/abs/2603.08652v1](https://arxiv.org/abs/2603.08652v1)
- **Published:** 2026-03-09
- **Tags:** benchmark/eval

"CoCo: Code as CoT for Text-to-Image Preview and Rare Concept Generation" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Recent advancements in Unified Multimodal Models (UMMs) have significantly advanced text-to-image (T2I) generation, particularly through the integration of Chain-of-Thought (CoT) reasoning.

However, existing CoT-based T2I methods largely rely on abstract natural-language planning, which lacks the precision required for complex spatial layouts, structured visual elements, and dense textual content.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 286. Omni-Diffusion: Unified Multimodal Understanding and Generation with Masked Discrete Diffusion

- **Link:** [https://arxiv.org/abs/2603.06577v2](https://arxiv.org/abs/2603.06577v2)
- **Published:** 2026-03-06
- **Tags:** LLM/VLM encoder, benchmark/eval

"Omni-Diffusion: Unified Multimodal Understanding and Generation with Masked Discrete Diffusion" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

While recent multimodal large language models (MLLMs) have made impressive strides, they predominantly employ a conventional autoregressive architecture as their backbone, leaving significant room to explore effective and efficient alternatives in architectural design.

Concurrently, recent studies have successfully applied discrete diffusion models to various domains, such as visual understanding and image generation, revealing their considerable potential as a promising backbone for multimodal systems.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 287. SkyReels-V4: Multi-modal Video-Audio Generation, Inpainting and Editing model

- **Link:** [https://arxiv.org/abs/2602.21818v3](https://arxiv.org/abs/2602.21818v3)
- **Published:** 2026-02-25
- **Tags:** LLM/VLM encoder

"SkyReels-V4: Multi-modal Video-Audio Generation, Inpainting and Editing model" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

SkyReels V4 is a unified multi modal video foundation model for joint video audio generation, inpainting, and editing.

The model adopts a dual stream Multimodal Diffusion Transformer (MMDiT) architecture, where one branch synthesizes video and the other generates temporally aligned audio, while sharing a powerful text encoder based on the Multimodal Large Language Models (MLLM).

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 288. From Reasoning to Pixels: Benchmarking the Alignment Gap in Unified Multimodal Models

- **Link:** [https://arxiv.org/abs/2602.08336v2](https://arxiv.org/abs/2602.08336v2)
- **Published:** 2026-02-09
- **Tags:** benchmark/eval

"From Reasoning to Pixels: Benchmarking the Alignment Gap in Unified Multimodal Models" (2026) evaluates text-conditioned image generation, often under long or compositional prompts.

Unified multimodal models (UMMs) aim to integrate multimodal understanding and generation within a unified architecture, yet it remains unclear to what extent their representations are truly aligned across modalities.

To investigate this question, we use reasoning-guided image generation as a diagnostic task, where models produce textual reasoning first and then generate images.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 289. The Silent Brush: Evaluating Artistic Style Leakage in AI Art Generation

- **Link:** [https://arxiv.org/abs/2605.17500v1](https://arxiv.org/abs/2605.17500v1)
- **Published:** 2026-05-17
- **Tags:** benchmark/eval

"The Silent Brush: Evaluating Artistic Style Leakage in AI Art Generation" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Generative text-to-image models are typically trained on large-scale web-scraped datasets that include diverse visual content such as copyrighted and stylistically distinctive artworks, raising concerns about ownership, attribution, and the unintended reuse of protected visual expressions.

A key issue is that models can learn stylistic patterns from this data and reproduce them in generated outputs without any explicit reference in the prompt.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 290. Shape of Thought: Progressive Object Assembly via Visual Chain-of-Thought

- **Link:** [https://arxiv.org/abs/2601.21081v2](https://arxiv.org/abs/2601.21081v2)
- **Published:** 2026-01-28
- **Tags:** benchmark/eval

"Shape of Thought: Progressive Object Assembly via Visual Chain-of-Thought" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Multimodal models for text-to-image generation have achieved strong visual fidelity, yet they remain brittle under compositional structural constraints, notably generative numeracy, attribute binding, and part-level relations.

To address these challenges, we propose Shape-of-Thought (SoT), a visual CoT framework for process-supervised progressive shape assembly in the rendered 2D domain, without external engines at inference time.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 291. Forgetting is Competition: Rethinking Unlearning as Representation Interference in Diffusion Models

- **Link:** [https://arxiv.org/abs/2603.00975v2](https://arxiv.org/abs/2603.00975v2)
- **Published:** 2026-03-01

"Forgetting is Competition: Rethinking Unlearning as Representation Interference in Diffusion Models" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Deployed text-to-image diffusion models increasingly require post-hoc concept unlearning for copyright claims, artist opt-outs, safety updates, and protected-content mitigation without full retraining.

A central challenge is erase-retain imbalance, aggressive updates suppress targets but damage shared capabilities, while conservative or anchor-based updates preserve quality yet leave concepts recoverable through related, compositional, paraphrased, or adversarial prompts.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 292. Adaptive Divergence Regularized Policy Optimization for Fine-tuning Generative Models

- **Link:** [https://arxiv.org/abs/2510.18053v1](https://arxiv.org/abs/2510.18053v1)
- **Published:** 2025-10-20
- **Tags:** LLM/VLM encoder

"Adaptive Divergence Regularized Policy Optimization for Fine-tuning Generative Models" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Balancing exploration and exploitation during reinforcement learning fine-tuning of generative models presents a critical challenge, as existing approaches rely on fixed divergence regularization that creates an inherent dilemma: strong regularization preserves model capabilities but limits reward optimization, while weak regularizatio...

We introduce Adaptive Divergence Regularized Policy Optimization (ADRPO), which automatically adjusts regularization strength based on advantage estimates-reducing regularization for high-value samples while applying stronger regularization to poor samples, enabling policies to navigate between exploration and aggressive exploitation a...

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 293. Semantic Chameleon: Corpus-Dependent Poisoning Attacks and Defenses in RAG Systems

- **Link:** [https://arxiv.org/abs/2603.18034v1](https://arxiv.org/abs/2603.18034v1)
- **Published:** 2026-03-10
- **Tags:** LLM/VLM encoder, benchmark/eval

"Semantic Chameleon: Corpus-Dependent Poisoning Attacks and Defenses in RAG Systems" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Retrieval-Augmented Generation (RAG) systems extend large language models (LLMs) with external knowledge sources but introduce new attack surfaces through the retrieval pipeline.

In particular, adversaries can poison retrieval corpora so that malicious documents are preferentially retrieved at inference time, enabling targeted manipulation of model outputs.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 294. DETONATE: A Benchmark for Text-to-Image Alignment and Kernelized Direct Preference Optimization

- **Link:** [https://arxiv.org/abs/2506.14903v1](https://arxiv.org/abs/2506.14903v1)
- **Published:** 2025-06-17
- **Tags:** LLM/VLM encoder, benchmark/eval

"DETONATE: A Benchmark for Text-to-Image Alignment and Kernelized Direct Preference Optimization" (2025) evaluates text-conditioned image generation, often under long or compositional prompts.

Alignment is crucial for text-to-image (T2I) models to ensure that generated images faithfully capture user intent while maintaining safety and fairness.

Direct Preference Optimization (DPO), prominent in large language models (LLMs), is extending its influence to T2I systems.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 295. A Comprehensive Study of Decoder-Only LLMs for Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2506.08210v1](https://arxiv.org/abs/2506.08210v1)
- **Published:** 2025-06-09
- **Tags:** LLM/VLM encoder, benchmark/eval

"A Comprehensive Study of Decoder-Only LLMs for Text-to-Image Generation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Both text-to-image generation and large language models (LLMs) have made significant advancements.

However, many text-to-image models still employ the somewhat outdated T5 and CLIP as their text encoders.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 296. DeCoT: Decomposing Complex Instructions for Enhanced Text-to-Image Generation with Large Language Models

- **Link:** [https://arxiv.org/abs/2508.12396v1](https://arxiv.org/abs/2508.12396v1)
- **Published:** 2025-08-17
- **Tags:** LLM/VLM encoder, benchmark/eval

"DeCoT: Decomposing Complex Instructions for Enhanced Text-to-Image Generation with Large Language Models" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Despite remarkable advancements, current Text-to-Image (T2I) models struggle with complex, long-form textual instructions, frequently failing to accurately render intricate details, spatial relationships, or specific constraints.

This limitation is highlighted by benchmarks such as LongBench-T2I, which reveal deficiencies in handling composition, specific text, and fine textures.

For post-CLIP/T5 stacks: evidence about LLM/VLM conditioning budgets and caption recipes.


### 297. Discovering Divergent Representations between Text-to-Image Models

- **Link:** [https://arxiv.org/abs/2509.08940v1](https://arxiv.org/abs/2509.08940v1)
- **Published:** 2025-09-10
- **Tags:** LLM/VLM encoder, benchmark/eval

"Discovering Divergent Representations between Text-to-Image Models" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

In this paper, we investigate when and how visual representations learned by two different generative models diverge.

Given two text-to-image models, our goal is to discover visual attributes that appear in images generated by one model but not the other, along with the types of prompts that trigger these attribute differences.

For a post-CLIP/T5 stack: treat it as evidence about LLM/VLM conditioning budgets and caption recipes that replace older encoders.


### 298. Scaling Text-to-Image Diffusion Transformers with Representation Autoencoders

- **Link:** [https://arxiv.org/abs/2601.16208v1](https://arxiv.org/abs/2601.16208v1)
- **Published:** 2026-01-22
- **Tags:** numeric token budget

"Scaling Text-to-Image Diffusion Transformers with Representation Autoencoders" (2026) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Representation Autoencoders (RAEs) have shown distinct advantages in diffusion modeling on ImageNet by training in high-dimensional semantic latent spaces.

In this work, we investigate whether this framework can scale to large-scale, freeform text-to-image (T2I) generation.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


### 299. Scaling Diffusion Transformers Efficiently via $μ$P

- **Link:** [https://arxiv.org/abs/2505.15270v3](https://arxiv.org/abs/2505.15270v3)
- **Published:** 2025-05-21

"Scaling Diffusion Transformers Efficiently via $μ$P" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Diffusion Transformers have emerged as the foundation for vision generative models, but their scalability is limited by the high cost of hyperparameter (HP) tuning at large scales.

Recently, Maximal Update Parametrization ($μ$P) was proposed for vanilla Transformers, which enables stable HP transfer from small to large language models, and dramatically reduces tuning costs.

Keep it as background on modern generation/evaluation; use only if its data or metrics inform caption-length decisions.


### 300. DyDiT++: Diffusion Transformers with Timestep and Spatial Dynamics for Efficient Visual Generation

- **Link:** [https://arxiv.org/abs/2504.06803v4](https://arxiv.org/abs/2504.06803v4)
- **Published:** 2025-04-09

"DyDiT++: Diffusion Transformers with Timestep and Spatial Dynamics for Efficient Visual Generation" (2025) contributes methods or analysis in contemporary text-to-image / multimodal generation.

Diffusion Transformer (DiT), an emerging diffusion model for visual generation, has demonstrated superior performance but suffers from substantial computational costs.

Our investigations reveal that these costs primarily stem from the static inference paradigm, which inevitably introduces redundant computation in certain diffusion timesteps and spatial regions.

Background on modern generation/evaluation; use if its data or metrics inform caption-length decisions.


---

## 7. Where the area is going (outlook)

The center of gravity has already left CLIP-77 and classic frozen-T5-only designs. Text conditioning is becoming **an LLM/VLM pathway** (Qwen, Gemma, Llama, Mistral, unified AR multimodal models) with a practical context cluster around **hundreds of tokens (about 256-512, product caps to roughly 1k+)**, while **prompt enhancement is being absorbed into the stack** as a default-on, sometimes adaptive, module whose job is distribution matching—not decorative verbosity. In parallel, data policy is shifting from short web alt-text to **VLM synthetic captions**, with the serious designs either **randomizing/mixing length over a wide band** or **training long and rewriting users into that band**. Evaluation is finally treating length as a first-class axis (DetailMaster, LongT2IBench), which will punish papers that only look strong on short prompts. The winning conceptual picture is no longer "pick L*"; it is **jointly choose `(mu_train, L, g)`** under faithfulness and compute constraints, and prove the choice with length diagnostics.

Looking forward, progress likely comes from making this joint policy **more native and less bolted-on**: faithfulness-aware PE with visual anchors or world-knowledge constraints; **adaptive token budgets** (spend tokens only when the task needs them, as in Seedream-style routing); **structured or slot-based captions** that vary semantically without drowning the model in prose; efficient long-text fusion so ~1k-token conditioning is affordable; and unified multimodal models that negotiate text vs image tokens in one sequence. The hard limitations of the current method are clear: PE can hallucinate and reward-hack length; variable training without covering deployment modes still fails; long context without training mass at that length does not extrapolate; and utility is still benchmark-dependent. A more native next step is a generator trained end-to-end for **heterogeneous conditioning length**—multi-caption per image, on-policy PE distillation into the backbone, and evaluation reported as curves over length—not a single headline score. That is the direction that turns today's engineering recipes into a stable, general solution.

---

## Related files

- First deep dive: `report.md`, `results/*.json`
- Prior modern review (~150): `literature_review_modern_prompt_length.md`
- This combined report: `combined_report_prompt_length_300.md`
- Catalogs: `corpus/catalog_300.json`, `corpus/core_length_300.json`
