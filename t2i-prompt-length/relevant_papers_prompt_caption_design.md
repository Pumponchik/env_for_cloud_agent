# Relevant Papers on Prompt & Caption Design for T2I

*64 papers. Each entry: Problem, Method, Result — 1–2 sentences per point.*

---

## 1. Improving Image Generation with Better Captions (DALL·E 3)

**Link:** [https://cdn.openai.com/papers/dall-e-3.pdf](https://cdn.openai.com/papers/dall-e-3.pdf)

**Problem:** Text-to-image models trained on noisy web alt-text fail to follow complex prompts faithfully, because captions are short, inaccurate, and lack detail.

**Method:** Train a dedicated image captioner to produce long, highly descriptive synthetic captions for all training images; at inference, use an LLM "prompt upsampler" to rewrite short user prompts into the detailed style the model was trained on.

**Result:** Dramatically improved prompt following compared to alt-text-trained baselines. Established the paradigm adopted by SD3, FLUX, Playground, and most subsequent frontier T2I systems.

---

## 2. How to Train Your Text-to-Image Model: Evaluating Design Choices for Synthetic Training Captions

**Link:** [https://www.semanticscholar.org/paper/31728f531ec52215f87f5d55446a34e9ca5488e0](https://www.semanticscholar.org/paper/31728f531ec52215f87f5d55446a34e9ca5488e0)

**Problem:** The "long dense captions are better" doctrine from DALL·E 3 is widely adopted but never rigorously ablated: nobody has isolated caption design choices in a controlled study.

**Method:** Fix architecture (SD v1.1), images (1M), and compute; vary only captions across hypotheses: VLM strength, caption length/density, temperature diversity, inter-epoch refresh, persona diversity, and gender-term bias. Evaluate with aesthetics, PickScore, LPIPS diversity, and bias metrics at four prompt-complexity levels.

**Result:** Long dense captions improve alignment but hurt aesthetics and short-prompt diversity. Randomizing caption length/density removes the trade-off and yields the best overall model. Caption term distributions directly shift output gender bias.

---

## 3. i1: A Simple and Fully Open Recipe for Strong Text-to-Image Models

**Link:** [https://arxiv.org/abs/2606.11289v1](https://arxiv.org/abs/2606.11289v1)
**Year:** 2026

**Problem:** Leading T2I models do not disclose training data or ablate design choices, making it impossible to attribute improvements to specific factors.

**Method:** Fully open recipe (i1): T5Gemma-2B encoder truncated to 256 tokens; controlled experiments on text encoders, caption strategies, and dataset mixing. Key ablation: train on 0–100% long captions, evaluate GenEval with original/repeated/rewritten prompts.

**Result:** Long-caption training scores 0.17 on short GenEval prompts, 0.49 with 12× repetition, 0.73 with LLM rewrite. Conclusion: train long and lengthen inference prompts to match, not train short to match users.

---

## 4. Improving Text-to-Image Generation with Input-Side Inference-Time Scaling

**Link:** [https://www.semanticscholar.org/paper/e40cbb9cf96ca92d7ad4cf83ab937612a85e1cfb](https://www.semanticscholar.org/paper/e40cbb9cf96ca92d7ad4cf83ab937612a85e1cfb)

**Problem:** T2I models underperform on short/underspecified prompts because user text is distributionally far from the dense training captions.

**Method:** Train an LLM prompt rewriter with iterative DPO (no SFT data needed); the rewriter expands user prompts to match the training caption distribution before generation.

**Result:** Rewriter transfers across T2I backbones without retraining. Closing the train/user text gap improves alignment, aesthetics, and quality across multiple models.

---

## 5. PromptEnhancer: A Simple Approach to Enhance Text-to-Image Models via Chain-of-Thought Prompt Rewriting

**Link:** [https://www.semanticscholar.org/paper/70a0f72b06327998b9274a5d7da6f89159b75d16](https://www.semanticscholar.org/paper/70a0f72b06327998b9274a5d7da6f89159b75d16)

**Problem:** Existing prompt enhancement methods either add generic stylistic details or optimize without understanding T2I failure modes like attribute leakage and spatial errors.

**Method:** PromptEnhancer: CoT prompt rewriting policy trained with RL against AlignEvaluator—a reward model scoring 24 T2I failure categories. Rewriting adds needed content, not empty verbosity.

**Result:** Consistently improves alignment metrics across multiple T2I backbones. Shows that content-focused rewriting (fixing failure modes) beats length-maximizing rewriting.

---

## 6. Seeing is Believing: Aligning Prompt Rewriting with Visual Anchors for Text-to-Image Generation

**Link:** [https://arxiv.org/abs/2606.08492v2](https://arxiv.org/abs/2606.08492v2)
**Year:** 2026

**Problem:** Text-only prompt rewriters hallucinate visually or physically impossible details (e.g., "water suspended mid-air") because they have no visual grounding.

**Method:** FaithRewriter generates an intermediate image from the original prompt, then uses it as a visual anchor when rewriting—ensuring expansions are faithful to what can actually be rendered.

**Result:** Reduces hallucinated details in expanded prompts and improves prompt-image faithfulness compared to text-only rewriters.

---

## 7. TIPO: Text to Image with Text Presampling for Prompt Optimization

**Link:** [https://arxiv.org/abs/2411.08127v6](https://arxiv.org/abs/2411.08127v6)
**Year:** 2024

**Problem:** User prompts differ from training captions in length, style, and content, causing a distribution gap that degrades generation quality.

**Method:** TIPO: "Text Presampling for Prompt Optimization"—expands prompts toward the training text distribution using a 30M-pair/40B-token caption corpus, deliberately expanding rather than fully rewriting.

**Result:** 62.8% human win rate over original prompts and up to 29.4% inference runtime improvement. Frames PE goal as matching μ_train, not maximizing verbosity.

---

## 8. A Picture is Worth a Thousand Words: Principled Recaptioning Improves Image Generation

**Link:** [https://www.semanticscholar.org/paper/10fce9e1718e968846c8429366c597380cce213d](https://www.semanticscholar.org/paper/10fce9e1718e968846c8429366c597380cce213d)

**Problem:** Web alt-text captions are noisy and unfaithful, degrading T2I training quality, but the right caption length and style for recaptioning is unknown.

**Method:** RECAP: fine-tune PaLI captioner with short vs long conditioning prefixes; compare training SD on RECAP-Short, RECAP-Long, 50/50 Mix, and original alt-text. Drop >77-token captions.

**Result:** Short wins FID; Long wins semantics; 50/50 Mix wins overall. First principled evidence for caption-length mixing under CLIP-77 limits.

---

## 9. What If We Recaption Billions of Web Images with LLaMA-3?

**Link:** [https://www.semanticscholar.org/paper/82bc594ddf77fe8e69e9b41dc32960d7f16b4b1d](https://www.semanticscholar.org/paper/82bc594ddf77fe8e69e9b41dc32960d7f16b4b1d)

**Problem:** Billion-scale web datasets use noisy short alt-text (~10 tokens average) that under-specifies images for T2I and representation learning.

**Method:** Recaption DataComp-1B with LLaVA-1.5-LLaMA3-8B using max_new_tokens=128, greedy decoding. Mean length jumps from 10.22 to 49.43 tokens with richer vocabulary.

**Result:** Improved downstream T2I and classification performance. Establishes the operating point for mid-scale offline VLM recaptioning (~128 decode budget → ~50 realized tokens).

---

## 10. Generating an Image From 1,000 Words: Enhancing Text-to-Image With Structured Captions

**Link:** [https://www.semanticscholar.org/paper/38fd53bac34ba902b8e7f1cf3f6552da5a3eaaaf](https://www.semanticscholar.org/paper/38fd53bac34ba902b8e7f1cf3f6552da5a3eaaaf)

**Problem:** Short free-form captions under-specify images and limit controllability; existing models cannot exploit long structured text efficiently.

**Method:** FIBO: train a T2I model on ~1000-token structured JSON-schema captions. DimFusion fuses intermediate LLM layers without growing token count (vs TokenFusion which doubles tokens).

**Result:** Long structured captions converge faster, improve FID, and unlock per-attribute control. DimFusion matches TokenFusion quality at ~1.6× less step time.

---

## 11. HunyuanImage 3.0 Technical Report

**Link:** [https://arxiv.org/abs/2509.23951v3](https://arxiv.org/abs/2509.23951v3)
**Year:** 2025

**Problem:** Existing T2I systems use either fixed short or fixed long captions, limiting robustness to diverse user prompt styles.

**Method:** HunyuanImage 3.0: Compositional Caption Synthesis samples and combines hierarchical caption fields to produce bilingual captions from ~30 to 1,000 words. Optional CoT think_recaption modes at inference.

**Result:** Achieves robust performance across short and long prompts without requiring a mandatory rewriter—the wide training band naturally covers both.

---

## 12. DetailMaster: Can Your Text-to-Image Model Handle Long Prompts?

**Link:** [https://www.semanticscholar.org/paper/7a94c25090610547ee3a9ba5ca6d1ce22e185acd](https://www.semanticscholar.org/paper/7a94c25090610547ee3a9ba5ca6d1ce22e185acd)

**Problem:** T2I benchmarks predominantly use short prompts; there is no rigorous evaluation of how models handle long, detail-rich professional prompts.

**Method:** DetailMaster: 4,116 prompts averaging 284.89 tokens with fine-grained metrics across character attributes, locations, scene attributes, and entity relationships.

**Result:** Even SOTA models achieve only ~50% on hard attribute tasks. Dense long training matters more than merely raising token capacity. Accuracy monotonically declines as prompt length grows.

---

## 13. RePrompt: Reasoning-Augmented Reprompting for Text-to-Image Generation via Reinforcement Learning

**Link:** [https://www.semanticscholar.org/paper/757a286592ffcc50735eb525edf32b9fbdd1309b](https://www.semanticscholar.org/paper/757a286592ffcc50735eb525edf32b9fbdd1309b)

**Problem:** Prompt enhancement for T2I is typically done with static templates or simple LLM paraphrasing, without reasoning about what the generator needs.

**Method:** RePrompt: reasoning-augmented reprompting trained via reinforcement learning, so the rewriter learns to reason about why the current prompt may fail.

**Result:** Improves alignment and image quality over static and template-based rewriting approaches.

---

## 14. Harnessing Caption Detailness for Data-Efficient Text-to-Image Generation

**Link:** [https://www.semanticscholar.org/paper/f00a1a44e2adb0d3dd735e5c35a8d382a1855ca7](https://www.semanticscholar.org/paper/f00a1a44e2adb0d3dd735e5c35a8d382a1855ca7)

**Problem:** Training T2I models on dense captions is expensive because generating high-quality synthetic captions for every image requires large VLMs at scale.

**Method:** Harnessing Caption Detailness: studies which images benefit most from detailed captions and allocates captioning effort accordingly (data-efficient).

**Result:** Achieves comparable or better T2I quality with fewer expensive dense captions by targeting detail where it matters.

---

## 15. Playground v3: Improving Text-to-Image Alignment with Deep-Fusion Large Language Models

**Link:** [https://www.semanticscholar.org/paper/b2e62ce609f3388f9a2fb709cb8f993fa4a8174f](https://www.semanticscholar.org/paper/b2e62ce609f3388f9a2fb709cb8f993fa4a8174f)

**Problem:** CLIP/T5 dual-tower conditioning limits how much language understanding reaches the generator; caption density and diversity also need attention.

**Method:** Playground v3: deep-fuse every layer of a Llama3-8B LLM into the DiT, replacing CLIP/T5 entirely. Train on synthetic captions with varying density and inter-epoch diversity.

**Result:** Strong text-image alignment and aesthetics; introduces CapsBench for evaluating caption quality. Motivates the "vary density + refresh captions" recipe.

---

## 16. PixArt-Σ: Weak-to-Strong Training of Diffusion Transformer for 4K Text-to-Image

**Link:** [https://arxiv.org/abs/2403.04692v2](https://arxiv.org/abs/2403.04692v2)
**Year:** 2024

**Problem:** The standard 77 text tokens from CLIP are insufficient for the dense captions needed for precise image generation at high resolution.

**Method:** PixArt-Σ: extend text encoder token length from PixArt-α's 120 to ~300 to accommodate denser captions, and train a 4K-resolution diffusion transformer.

**Result:** Improved text-image alignment and generation quality at high resolutions. Demonstrates that encoder token budget must scale with caption density.

---

## 17. PixArt-$α$: Fast Training of Diffusion Transformer for Photorealistic Text-to-Image Synthesis

**Link:** [https://arxiv.org/abs/2310.00426](https://arxiv.org/abs/2310.00426)
**Year:** 2023

**Problem:** Training a T2I diffusion transformer is extremely expensive; efficient training strategies and better caption data are needed.

**Method:** PixArt-α: fast DiT training with T5-XXL, using dense LLaVA captions. Explicitly raise token length from 77 to 120 because LLaVA captions are denser.

**Result:** Achieves competitive quality with much less compute than SD/DALL·E. Shows dense captions improve per-step learning efficiency.

---

## 18. Altogether: Image Captioning via Re-aligning Alt-text

**Link:** [https://arxiv.org/abs/2406.18583](https://arxiv.org/abs/2406.18583)

**Problem:** Synthetic captions are better than alt-text for T2I, but the optimal mixing ratio of synthetic vs original captions is unknown.

**Method:** Altogether: systematically vary the fraction of synthetic LLaVA captions mixed with original alt-text for both T2I and CLIP training.

**Result:** For T2I, ~100% synthetic is best (challenging DALL·E 3's 95/5 mix). For CLIP, only ~15% synthetic is optimal. Synthetic vs alt-text mixing must be tuned per task.

---

## 19. Lens: Rethinking Training Efficiency for Foundational Text-to-Image Models

**Link:** [https://www.semanticscholar.org/paper/f69e22f570f6a4584792ba1debabf3211cc6cbe7](https://www.semanticscholar.org/paper/f69e22f570f6a4584792ba1debabf3211cc6cbe7)

**Problem:** Training foundational T2I models requires enormous compute; it is unclear which data/caption strategies are most compute-efficient.

**Method:** Lens rethinks training efficiency for T2I by analyzing how caption quality, data composition, and training schedules interact.

**Result:** Identifies efficient configurations that reduce training cost while maintaining or improving generation quality.

---

## 20. PromptEcho: Annotation-Free Reward from Vision-Language Models for Text-to-Image Reinforcement Learning

**Link:** [https://arxiv.org/abs/2604.12652](https://arxiv.org/abs/2604.12652)
**Year:** 2026

**Problem:** Training PE/reward models for T2I typically requires expensive human annotations.

**Method:** PromptEcho: annotation-free reward extraction from VLMs for text-to-image reinforcement learning, using VLM scores as reward signal.

**Result:** Enables training prompt rewriters/generators with RL without needing human preference data.

---

## 21. DreamLIP: Language-Image Pre-training with Long Captions

**Link:** [https://www.semanticscholar.org/paper/0f284b2fdf001ced671ef87bea3435849c1e8059](https://www.semanticscholar.org/paper/0f284b2fdf001ced671ef87bea3435849c1e8059)

**Problem:** CLIP-style models are trained on short alt-text, limiting their understanding of detailed visual descriptions.

**Method:** DreamLIP: language-image pre-training with long, detailed synthetic captions to improve both CLIP-style representation and downstream T2I conditioning.

**Result:** Improved zero-shot and fine-tuned performance when language-image models see long dense captions during pre-training.

---

## 22. Low-hallucination Synthetic Captions for Large-Scale Vision-Language Model Pre-training

**Link:** [https://www.semanticscholar.org/paper/018700af04b19af74cc3745fd75ba3c47be3a299](https://www.semanticscholar.org/paper/018700af04b19af74cc3745fd75ba3c47be3a299)

**Problem:** Synthetic captions from VLMs can hallucinate objects or attributes not present in the image, poisoning training data.

**Method:** Low-hallucination synthetic captions: apply hallucination detection and filtering pipelines to VLM-generated captions before using them for VL pre-training.

**Result:** Cleaner captions improve downstream model reliability; highlights that caption length without faithfulness is harmful.

---

## 23. RICO: Improving Accuracy and Completeness in Image Recaptioning via Visual Reconstruction

**Link:** [https://www.semanticscholar.org/paper/7e10a5223adfd36121541ff64cb14addaef5475e](https://www.semanticscholar.org/paper/7e10a5223adfd36121541ff64cb14addaef5475e)

**Problem:** Existing recaptioning approaches prioritize either accuracy or completeness but rarely both, leaving captions that are faithful but incomplete or complete but hallucinated.

**Method:** RICO: use a visual reconstruction loop—generate an image from the caption and compare back to the original—to ensure captions are both accurate and complete.

**Result:** Improved recaptioning quality on multiple benchmarks; the reconstruction signal catches both omissions and hallucinations.

---

## 24. Building a Precise Video Language with Human-AI Oversight

**Link:** [https://www.semanticscholar.org/paper/84e9bfb2900a257aed59b6503cca04d9b1c5202d](https://www.semanticscholar.org/paper/84e9bfb2900a257aed59b6503cca04d9b1c5202d)

**Problem:** Video-language models (VLMs) learn to reason about the dynamic visual world through natural language.

**Method:** We introduce a suite of open datasets, benchmarks, and recipes for scalable oversight that enable precise video captioning.

**Result:** Data and code are available on our project page: https://linzhiqiu.github.io/papers/chai/

---

## 25. ShareGPT4Video: Improving Video Understanding and Generation with Better Captions

**Link:** [https://www.semanticscholar.org/paper/9583cadea300f67aaab0fdf7b6d1f774c3cd55e7](https://www.semanticscholar.org/paper/9583cadea300f67aaab0fdf7b6d1f774c3cd55e7)

**Problem:** We present the ShareGPT4Video series, aiming to facilitate the video understanding of large video-language models (LVLMs) and the video generation of text-to-video models (T2VMs) via dense and precise captions.

**Method:** The series comprises: 1) ShareGPT4Video, 40K GPT4V annotated dense captions of videos with various lengths and sources, developed through carefully designed data filtering and annotating strategy.

**Result:** Based on ShareGPT4Video, we further develop ShareCaptioner-Video, a superior captioner capable of efficiently generating high-quality captions for arbitrary videos...

---

## 26. VideoPainter: Any-length Video Inpainting and Editing with Plug-and-Play Context Control

**Link:** [https://www.semanticscholar.org/paper/38c29254113bbc6a98048fac368cb1914e2429c9](https://www.semanticscholar.org/paper/38c29254113bbc6a98048fac368cb1914e2429c9)

**Problem:** Video inpainting, crucial for the media industry, aims to restore corrupted content.

**Method:** However, current methods relying on limited pixel propagation or single-branch image inpainting architectures face challenges with generating fully masked objects, balancing background preservation with foreground generation, and maintaining ID consistency over long video.

**Result:** Extensive experiments demonstrate VideoPainter’s state-of-the-art performance in any-length video inpainting and editing across 8 key metrics, including video quality, mask region preservation, and textual coherence.

---

## 27. Efficient Scaling of Diffusion Transformers for Text-to-Image Generation

**Link:** [https://www.semanticscholar.org/paper/8d066b07fa15312338b6fba86149bc6e8526136d](https://www.semanticscholar.org/paper/8d066b07fa15312338b6fba86149bc6e8526136d)

**Problem:** We empirically study the scaling properties of various Diffusion Transformers (DiTs) for text-to-image generation by performing extensive and rigorous ablations, including training scaled DiTs ranging from 0.3B upto 8B parameters on datasets up to 600M images.

**Method:** We find that U-ViT, a pure self-attention based DiT model provides a simpler design and scales more effectively in comparison with cross-attention based DiT variants, which allows straightforward expansion for extra conditions and other modalities.

**Result:** On the data scaling side, we investigate how increasing dataset size and enhanced long caption improve the text-image alignment performance and the learning efficiency.

---

## 28. Moving Alphabet: A Controlled Study of Training Data for Text-to-Video Generation

**Link:** [https://www.semanticscholar.org/paper/f9934e0a4c2d2e76a7033255431e9a145df8779c](https://www.semanticscholar.org/paper/f9934e0a4c2d2e76a7033255431e9a145df8779c)

**Problem:** Text-to-video generation has advanced significantly over the past five years through scaling of model size, data, and compute.

**Method:** Unlike model architecture, training data is often underexplored.

**Result:** We believe these insights can inform the development of large-scale text-to-video models, and we advocate for greater attention to the science of pre-training data.

---

## 29. ETTA: Elucidating the Design Space of Text-to-Audio Models

**Link:** [https://www.semanticscholar.org/paper/2e1056e68951dedcfd492d5297840321b3b3daf0](https://www.semanticscholar.org/paper/2e1056e68951dedcfd492d5297840321b3b3daf0)

**Problem:** Recent years have seen significant progress in Text-To-Audio (TTA) synthesis, enabling users to enrich their creative workflows with synthetic audio generated from natural language prompts.

**Method:** Despite this progress, the effects of data, model architecture, training objective functions, and sampling strategies on target benchmarks are not well understood.

**Result:** Finally, we show ETTA's improved ability to generate creative audio following complex and imaginative captions -- a task that is more challenging than current benchmarks.

---

## 30. BACON: Improving Clarity of Image Captions via Bag-of-Concept Graphs

**Link:** [https://www.semanticscholar.org/paper/8cc04354e5b308e30206103ba3ea5f8c2b59c0b0](https://www.semanticscholar.org/paper/8cc04354e5b308e30206103ba3ea5f8c2b59c0b0)

**Problem:** Advancements in large Vision-Language Models have brought precise, accurate image captioning, vital for advancing multi-modal image understanding and processing.

**Method:** Yet these captions often carry lengthy, intertwined contexts that are difficult to parse and frequently overlook essential cues, posing a great barrier for models like GroundingDINO and SDXL, which lack the strong text encoding and syntax analysis needed to fully leverage dense captions.

**Result:** For example, BACON-style captions help GroundingDINO achieve 1.51× higher recall scores on open-vocabulary object detection tasks compared to leading methods.

---

## 31. Rethinking Music Captioning with Music Metadata LLMs

**Link:** [https://www.semanticscholar.org/paper/27bb0504e76395bf6ca8106929cc7b34f7c0ae06](https://www.semanticscholar.org/paper/27bb0504e76395bf6ca8106929cc7b34f7c0ae06)

**Problem:** Music captioning, or the task of generating a natural language description of music, is useful for both music understanding and controllable music generation.

**Method:** Training captioning models, however, typically requires high-quality music caption data which is scarce compared to metadata (e.g., genre, mood, etc.).

**Result:** Compared to a strong end-to-end baseline trained on LLM-generated captions derived from metadata, our method: (1) achieves comparable performance in less training time over end-to-end captioners, (2) offers flexibility to easily change stylization post-training, enabling output captions to be tailored to specific stylistic and quality requirements, and (3) can be prompted with audio and partial metadata to enable powerful metadata imputation or in-filling--a common task for organizing music data.

---

## 32. RAPO++: Cross-Stage Prompt Optimization for Text-to-Video Generation via Data Alignment and Test-Time Scaling

**Link:** [https://www.semanticscholar.org/paper/5d4f3bef456e9d038a4d569a5b8f76cbb0328a41](https://www.semanticscholar.org/paper/5d4f3bef456e9d038a4d569a5b8f76cbb0328a41)

**Problem:** Prompt design plays a crucial role in text-to-video (T2V) generation, yet user-provided prompts are often short, unstructured, and misaligned with training data, limiting the generative potential of diffusion-based T2V models.

**Method:** We present \textbf{RAPO++}, a cross-stage prompt optimization framework that unifies training-data--aligned refinement, test-time iterative scaling, and large language model (LLM) fine-tuning to substantially improve T2V generation without modifying the underlying generative backbone.

**Result:** The code is available at https://github.com/Vchitect/RAPO.

---

## 33. On the Scalability of Diffusion-based Text-to-Image Generation

**Link:** [https://www.semanticscholar.org/paper/a9489b4ad6f82db616f0b4a915dcfc0448e4c70e](https://www.semanticscholar.org/paper/a9489b4ad6f82db616f0b4a915dcfc0448e4c70e)

**Problem:** Scaling up model and data size has been quite successful for the evolution of LLMs.

**Method:** However, the scaling law for the diffusion based text-to-image (T2I) models is not fully explored.

**Result:** Finally, we provide scaling functions to predict the text-image alignment performance as functions of the scale of model size, compute and dataset size.

---

## 34. Mastering Text-to-Image Diffusion: Recaptioning, Planning, and Generating with Multimodal LLMs

**Link:** [https://www.semanticscholar.org/paper/140cfda71bfff852c3e205b7ad61854b78c76982](https://www.semanticscholar.org/paper/140cfda71bfff852c3e205b7ad61854b78c76982)

**Problem:** Diffusion models have exhibit exceptional performance in text-to-image generation and editing.

**Method:** However, existing methods often face challenges when handling complex text prompts that involve multiple objects with multiple attributes and relationships.

**Result:** Our code is available at: https://github.com/YangLing0818/RPG-DiffusionMaster

---

## 35. Semantic Browsing: Controllable Diversity for Image Generation

**Link:** [https://www.semanticscholar.org/paper/a370eda4515fb2ea120961196bd07e26205fd910](https://www.semanticscholar.org/paper/a370eda4515fb2ea120961196bd07e26205fd910)

**Problem:** Modern text-to-image models excel in visual fidelity and prompt adherence.

**Method:** However, this strict adherence comes at the cost of diversity: generated samples tend to collapse into a single visual interpretation.

**Result:** We demonstrate that our method produces diverse and navigable design spaces where every variation corresponds to a specific, user-understandable semantic decision.

---

## 36. Generate Any Scene: Scene Graph Driven Data Synthesis for Visual Generation Training

**Link:** [https://arxiv.org/abs/2412.08221](https://arxiv.org/abs/2412.08221)
**Year:** 2024

**Problem:** Recent advances in text-to-vision generation excel in visual fidelity but struggle with compositional generalization and semantic alignment.

**Method:** Existing datasets are noisy and weakly compositional, limiting models' understanding of complex scenes, while scalable solutions for dense, high-quality annotations remain a challenge.

**Result:** Finally, we apply these ideas to the downstream task of content moderation where we train models to identify challenging cases by learning from synthetic data.

---

## 37. View Selection for 3D Captioning via Diffusion Ranking

**Link:** [https://www.semanticscholar.org/paper/f4a3c29b3ed9442c848a6c6b226b142bcdef59b1](https://www.semanticscholar.org/paper/f4a3c29b3ed9442c848a6c6b226b142bcdef59b1)

**Problem:** Scalable annotation approaches are crucial for constructing extensive 3D-text datasets, facilitating a broader range of applications.

**Method:** However, existing methods sometimes lead to the generation of hallucinated captions, compromising caption quality.

**Result:** Additionally, we showcase the adaptability of DiffuRank by applying it to pre-trained text-to-image models for a Visual Question Answering task, where it outperforms the CLIP model.

---

## 38. Improving Explicit Spatial Relationships in Text-to-Image Generation through an Automatically Derived Dataset

**Link:** [https://www.semanticscholar.org/paper/8408419e8263fa08c8515948f14b58e64bfef609](https://www.semanticscholar.org/paper/8408419e8263fa08c8515948f14b58e64bfef609)

**Problem:** Existing work has observed that current text-to-image systems do not accurately reflect explicit spatial relations between objects such as 'left of' or 'below'.

**Method:** We hypothesize that this is because explicit spatial relations rarely appear in the image captions used to train these models.

**Result:** The dataset and the code will be publicly available.

---

## 39. APE: Agentic Prompt Enhancer for Image Generation and Editing

**Link:** [https://www.semanticscholar.org/paper/14333575850073eaa86bd09c2ffdd2d96c3536e4](https://www.semanticscholar.org/paper/14333575850073eaa86bd09c2ffdd2d96c3536e4)

**Problem:** Natural language has become a powerful interface for image generation and editing, yet text-guided visual systems remain highly sensitive to prompt formulation.

**Method:** Semantically similar requests can produce different outputs depending on wording, specificity, and how explicitly visual constraints are stated, motivating prompt enhancement as a trainable component rather than a peripheral user choice.

**Result:** Experiments on challenging image generation and editing benchmarks demonstrate that post-trained small prompt enhancers reliably outperform their base counterparts, narrowing the gap to closed-source prompt enhancers; in addition, MAPE proves particularly strong on complex compositional tasks within these benchmarks.

---

## 40. Factorized-Dreamer: Training A High-Quality Video Generator with Limited and Low-Quality Data

**Link:** [https://www.semanticscholar.org/paper/df85f8ba638ac00c374908179426b9feb8db488b](https://www.semanticscholar.org/paper/df85f8ba638ac00c374908179426b9feb8db488b)

**Problem:** Text-to-video (T2V) generation has gained significant attention due to its wide applications to video generation, editing, enhancement and translation, \etc.

**Method:** However, high-quality (HQ) video synthesis is extremely challenging because of the diverse and complex motions existed in real world.

**Result:** Our source codes are available at \url{https://github.com/yangxy/Factorized-Dreamer/}.

---

## 41. Precision or Recall? An Analysis of Image Captions for Training Text-to-Image Generation Model

**Link:** [https://www.semanticscholar.org/paper/ca1778e79ceaf1696181b49a19afd1834bd85914](https://www.semanticscholar.org/paper/ca1778e79ceaf1696181b49a19afd1834bd85914)

**Problem:** Despite advancements in text-to-image models, generating images that precisely align with textual descriptions remains challenging due to misalignment in training data.

**Method:** In this paper, we analyze the critical role of caption precision and recall in text-to-image model training.

**Result:** Models trained with these synthetic captions show similar behavior to those trained on human-annotated captions, underscores the potential for synthetic data in text-to-image training.

---

## 42. Revisit Large-Scale Image-Caption Data in Pre-training Multimodal Foundation Models

**Link:** [https://www.semanticscholar.org/paper/7497c8c863d46320b77e865c7a24bef9b0e9749f](https://www.semanticscholar.org/paper/7497c8c863d46320b77e865c7a24bef9b0e9749f)

**Problem:** Recent advancements in multimodal models highlight the value of rewritten captions for improving performance, yet key challenges remain.

**Method:** For example, while synthetic captions often provide superior quality and image-text alignment, it is not clear whether they can fully replace AltTexts: the role of synthetic captions and their interaction with original web-crawled AltTexts in pre-training is still not well understood.

**Result:** This comprehensive analysis provides valuable insights into optimizing captioning strategies, thereby advancing the pre-training of multimodal foundation models.

---

## 43. CommonCanvas: An Open Diffusion Model Trained with Creative-Commons Images

**Link:** [https://www.semanticscholar.org/paper/1b672e2ea961ef45a9f3322430ca5df9ff8ba165](https://www.semanticscholar.org/paper/1b672e2ea961ef45a9f3322430ca5df9ff8ba165)

**Problem:** We assemble a dataset of Creative-Commons-licensed (CC) images, which we use to train a set of open diffusion models that are qualitatively competitive with Stable Diffusion 2 (SD2).

**Method:** This task presents two challenges: (1) high-resolution CC images lack the captions necessary to train text-to-image generative models; (2) CC images are relatively scarce.

**Result:** We release our models, data, and code at https://github.com/mosaicml/diffusion/blob/main/assets/common-canvas.md

---

## 44. CRAFT: Continuous Reasoning and Agentic Feedback Tuning for Multimodal Text-to-Image Generation

**Link:** [https://www.semanticscholar.org/paper/b369583dc62cf4e16fae0e4e5c359b820a9fa021](https://www.semanticscholar.org/paper/b369583dc62cf4e16fae0e4e5c359b820a9fa021)

**Problem:** Recent work has shown that inference-time reasoning and reflection can improve text-to-image generation without retraining.

**Method:** However, existing approaches often rely on implicit, holistic critiques or unconstrained prompt rewrites, making their behavior difficult to interpret, control, or stop reliably.

**Result:** Our results suggest that explicitly structured, constraint-driven inference-time reasoning is a key ingredient for improving the reliability of multimodal generative models.

---

## 45. Improving Text Generation on Images with Synthetic Captions

**Link:** [https://www.semanticscholar.org/paper/bcf3a67b088aaea81323a496149abc4f39dd25a0](https://www.semanticscholar.org/paper/bcf3a67b088aaea81323a496149abc4f39dd25a0)

**Problem:** The recent emergence of latent diffusion models such as SDXL [1] and SD 1.5 [2] has shown significant capability in generating highly detailed and realistic images.

**Method:** Despite their remarkable ability to produce images, generating accurate text within images still remains a challenging task.

**Result:** Our experiments show that with the addition of random letters to our raw dataset, our model's performance improves in producing well-formed visual text.

---

## 46. KOALA: Empirical Lessons Toward Memory-Efficient and Fast Diffusion Models for Text-to-Image Synthesis

**Link:** [https://www.semanticscholar.org/paper/8b8d8cbbfaef256bddce273f5e541ef6e9ba3130](https://www.semanticscholar.org/paper/8b8d8cbbfaef256bddce273f5e541ef6e9ba3130)

**Problem:** As text-to-image (T2I) synthesis models increase in size, they demand higher inference costs due to the need for more expensive GPUs with larger memory, which makes it challenging to reproduce these models in addition to the restricted access to training datasets.

**Method:** Our study aims to reduce these inference costs and explores how far the generative capabilities of T2I models can be extended using only publicly available datasets and open-source models.

**Result:** We believe that our KOALA models will have a significant practical impact, serving as cost-effective alternatives to SDXL for academic researchers and general users in resource-constrained environments.

---

## 47. Segment and Caption Anything

**Link:** [https://www.semanticscholar.org/paper/339ec34efdccdf2bf43bb817ef7cab5058bfa2e7](https://www.semanticscholar.org/paper/339ec34efdccdf2bf43bb817ef7cab5058bfa2e7)

**Problem:** We propose a method to efficiently equip the Segment Anything Model (SAM) with the ability to generate regional captions.

**Method:** SAM presents strong generalizability to segment anything while is short for semantic understanding.

**Result:** The project page, along with the associated code, can be accessed via the following link.

---

## 48. LoTLIP: Improving Language-Image Pre-training for Long Text Understanding

**Link:** [https://www.semanticscholar.org/paper/9023e89eb0c1d060b8f3d9fcd048ca698cbd7bad](https://www.semanticscholar.org/paper/9023e89eb0c1d060b8f3d9fcd048ca698cbd7bad)

**Problem:** Understanding long text is of great demands in practice but beyond the reach of most language-image pre-training (LIP) models.

**Method:** In this work, we empirically confirm that the key reason causing such an issue is that the training images are usually paired with short captions, leaving certain tokens easily overshadowed by salient tokens.

**Result:** The project page is available at https://wuw2019.github.io/lot-lip.

---

## 49. Dual-Stage Value-Guided Inference with Margin-Based Reward Adjustment for Fast and Faithful VLM Captioning

**Link:** [https://www.semanticscholar.org/paper/d1666b3f89df3dfb906a0a1d276994580068ac70](https://www.semanticscholar.org/paper/d1666b3f89df3dfb906a0a1d276994580068ac70)

**Problem:** Despite significant advances in inference-time search for vision-language models (VLMs), existing approaches remain both computationally expensive and prone to unpenalized, low-confidence generations which often lead to persistent hallucinations.

**Method:** We introduce \textbf{Value-guided Inference with Margin-based Reward (ViMaR)}, a two-stage inference framework that improves both efficiency and output fidelity by combining a temporal-difference value model with a margin-aware reward adjustment.

**Result:** Furthermore, when ViMaR-generated captions are used for self-training, the underlying models achieve substantial gains across a broad suite of visual comprehension benchmarks, underscoring the potential of fast, accurate, and self-improving VLM pipelines.

---

## 50. Altogether: Image Captioning via Re-aligning Alt-text

**Link:** [https://www.semanticscholar.org/paper/4254ed35e15a99f6c7fbb634e42301e15212b696](https://www.semanticscholar.org/paper/4254ed35e15a99f6c7fbb634e42301e15212b696)

**Problem:** This paper focuses on creating synthetic data to improve the quality of image captions.

**Method:** Existing works typically have two shortcomings.

**Result:** Our results show our Altogether approach leads to richer image captions that also improve text-to-image generation and zero-shot image classification tasks.

---

## 51. DetCLIPv3: Towards Versatile Generative Open-Vocabulary Object Detection

**Link:** [https://www.semanticscholar.org/paper/9190dbc582c9871dc771fc87afd85ea4c2455fb9](https://www.semanticscholar.org/paper/9190dbc582c9871dc771fc87afd85ea4c2455fb9)

**Problem:** Existing open-vocabulary object detectors typically require a predefined set of categories from users, signifi-cantly confining their application scenarios.

**Method:** In this pa-per, we introduce DetCLIPv3, a high-performing detector that excels not only at both open-vocabulary object detection, but also generating hierarchical labels for detected objects.

**Result:** DetCLIPv3 also achieves a state-of-the-art 19.7 AP in dense captioning task on VG dataset, showcasing its strong generative capability.

---

## 52. Mimir: Improving Video Diffusion Models for Precise Text Understanding

**Link:** [https://www.semanticscholar.org/paper/9978e1c198aa9052005d181e7b62aee19ab18a3d](https://www.semanticscholar.org/paper/9978e1c198aa9052005d181e7b62aee19ab18a3d)

**Problem:** Text serves as the key control signal in video generation due to its narrative nature.

**Method:** To render text descriptions into video clips, current video diffusion models borrow features from text encoders yet struggle with limited text comprehension.

**Result:** Project page: https://lucaria-academy.github.io/Mimir/

---

## 53. MoTrans: Customized Motion Transfer with Text-driven Video Diffusion Models

**Link:** [https://www.semanticscholar.org/paper/cd851366e07d5dc5dc6920fc39835df46ab2cce0](https://www.semanticscholar.org/paper/cd851366e07d5dc5dc6920fc39835df46ab2cce0)

**Problem:** Existing pretrained text-to-video (T2V) models have demonstrated impressive abilities in generating realistic videos with basic motion or camera movement.

**Method:** However, these models exhibit significant limitations when generating intricate, human-centric motions.

**Result:** Experimental results demonstrate that our method effectively learns specific motion pattern from singular or multiple reference videos, performing favorably against existing methods in customized video generation.

---

## 54. Diffusion Probe: Generated Image Result Prediction Using CNN Probes

**Link:** [https://www.semanticscholar.org/paper/b879e05782c0165ea5a03000022bcbad23f2ccb4](https://www.semanticscholar.org/paper/b879e05782c0165ea5a03000022bcbad23f2ccb4)

**Problem:** Text-to-image (T2I) diffusion models lack an efficient mechanism for early quality assessment, leading to costly trial-and-error in multi-generation scenarios such as prompt iteration, agent-based generation, and flow-grpo.

**Method:** We reveal a strong correlation between early diffusion cross-attention distributions and final image quality.

**Result:** This reduces computational overhead while improving final output quality.Diffusion Probe is model-agnostic, efficient, and broadly applicable, offering a practical solution for improving T2I generation efficiency through early quality prediction.

---

## 55. Evolve to Inspire: Novelty Search for Diverse Image Generation

**Link:** [https://www.semanticscholar.org/paper/84c90e8d86bfcadb6d612d961d77f094b29a31b1](https://www.semanticscholar.org/paper/84c90e8d86bfcadb6d612d961d77f094b29a31b1)

**Problem:** Text-to-image diffusion models, while proficient at generating high-fidelity im- ages, often suffer from limited output diversity, hindering their application in exploratory and ideation tasks.

**Method:** Existing prompt optimization techniques typically target aesthetic fitness or are ill-suited to the creative visual domain.

**Result:** Ablation studies confirm the efficacy of emitters.

---

## 56. Reverse Prompt: Cracking the Recipe Inside Text-to-Image Generation

**Link:** [https://www.semanticscholar.org/paper/43cba35a8933d5f33fd5d0b3c4b15b366b732939](https://www.semanticscholar.org/paper/43cba35a8933d5f33fd5d0b3c4b15b366b732939)

**Problem:** Text-to-image generation has become increasingly popular, but achieving the desired images often requires extensive prompt engineering.

**Method:** In this paper, we explore how to decode textual prompts from reference images, a process we refer to as image reverse prompt engineering.

**Result:** More importantly, we can easily create novel images with diverse styles and content by directly editing these reverse prompts.

---

## 57. ReflectCAP: Detailed Image Captioning with Reflective Memory

**Link:** [https://www.semanticscholar.org/paper/68a13010d3915ff54dbdd86e7f5a423dfcceea42](https://www.semanticscholar.org/paper/68a13010d3915ff54dbdd86e7f5a423dfcceea42)

**Problem:** Detailed image captioning demands both factual grounding and fine-grained coverage, yet existing methods have struggled to achieve them simultaneously.

**Method:** We address this tension with Reflective Note-Guided Captioning (ReflectCAP), where a multi-agent pipeline analyzes what the target large vision-language model (LVLM) consistently hallucinates and what it systematically overlooks, distilling these patterns into reusable guidelines called Structured Reflection Notes.

**Result:** This makes high-quality detailed captioning viable under real-world cost and latency constraints.

---

## 58. GMAIL: Generative Modality Alignment for generated Image Learning

**Link:** [https://www.semanticscholar.org/paper/1f925d2a62f6e3276b591a1368fc091a4074437c](https://www.semanticscholar.org/paper/1f925d2a62f6e3276b591a1368fc091a4074437c)

**Problem:** Generative models have made it possible to synthesize highly realistic images, potentially providing an abundant data source for training machine learning models.

**Method:** Despite the advantages of these synthesizable data sources, the indiscriminate use of generated images as real images for training can even cause mode collapse due to modality discrepancies between real and synthetic domains.

**Result:** It also shows positive generated data scaling trends and notable enhancements in the captioning performance of the large multimodal model, LLaVA.

---

## 59. Value-Aligned Prompt Moderation via Zero-Shot Agentic Rewriting for Safe Image Generation

**Link:** [https://www.semanticscholar.org/paper/8256768881850042a773094d7977abd6f02c25f5](https://www.semanticscholar.org/paper/8256768881850042a773094d7977abd6f02c25f5)

**Problem:** Generative vision-language models like Stable Diffusion demonstrate remarkable capabilities in creative media synthesis, but they also pose substantial risks of producing unsafe, offensive, or culturally inappropriate content when prompted adversarially.

**Method:** Current defenses struggle to align outputs with human values without sacrificing generation quality or incurring high costs.

**Result:** These results highlight VALOR as a scalable and effective approach for deploying safe, aligned, and helpful image generation systems in open-world settings.

---

## 60. Personalizing Text-to-Image Generation to Individual Taste

**Link:** [https://arxiv.org/abs/2604.07427v1](https://arxiv.org/abs/2604.07427v1)
**Year:** 2026

**Problem:** Modern text-to-image (T2I) models generate high-fidelity visuals but remain indifferent to individual user preferences.

**Method:** While existing reward models optimize for "average" human appeal, they fail to capture the inherent subjectivity of aesthetic judgment.

**Result:** We release our dataset and model to facilitate standardized research in personalized T2I alignment and subjective visual quality assessment.

---

## 61. Endogenous Reprompting: Self-Evolving Cognitive Alignment for Unified Multimodal Models

**Link:** [https://www.semanticscholar.org/paper/8a5c529f9c45a61cef1f1883c0a9ff36a35eea04](https://www.semanticscholar.org/paper/8a5c529f9c45a61cef1f1883c0a9ff36a35eea04)

**Problem:** Unified Multimodal Models (UMMs) exhibit strong understanding, yet this capability often fails to effectively guide generation.

**Method:** We identify this as a Cognitive Gap: the model lacks the understanding of how to enhance its own generation process.

**Result:** Experiments show that SEER consistently outperforms state-of-the-art baselines in evaluation accuracy, reprompting efficiency, and generation quality, without sacrificing general multimodal capabilities.

---

## 62. AutoPrompt: Automated Red-Teaming of Text-to-Image Models via LLM-Driven Adversarial Prompts

**Link:** [https://www.semanticscholar.org/paper/5ef58b926d69915934afd9fc8f1c67f0c6d1f519](https://www.semanticscholar.org/paper/5ef58b926d69915934afd9fc8f1c67f0c6d1f519)

**Problem:** Despite rapid advancements in text-to-image (T2I) models, their safety mechanisms are vulnerable to adversarial prompts, which maliciously generate unsafe images.

**Method:** Current red-teaming methods for proactively assessing such vulnerabilities usually require white-box access to T2I models, and rely on inefficient per-prompt optimization, as well as inevitably generate semantically meaningless prompts easily blocked by filters.

**Result:** Warning: This paper contains model outputs that are offensive in nature.

---

## 63. The erasure of intensive livestock farming in text-to-image generative AI

**Link:** [https://www.semanticscholar.org/paper/dc6374f0563ed0c6d513d36ef3147d8206a173b2](https://www.semanticscholar.org/paper/dc6374f0563ed0c6d513d36ef3147d8206a173b2)

**Problem:** Generative AI (e.g., ChatGPT) is increasingly integrated into people's daily lives.

**Method:** While it is known that AI perpetuates biases against marginalized human groups, their impact on non-human animals remains understudied.

**Result:** While OpenAI introduced prompt revision to mitigate bias, in the case of farmed animal production systems, it paradoxically introduces a strong bias towards unrealistic farming practices.

---

## 64. Wolf: Dense Video Captioning with a World Summarization Framework

**Link:** [https://www.semanticscholar.org/paper/a469471c93fc6e99a5e71d8aaffdd0619df91d2f](https://www.semanticscholar.org/paper/a469471c93fc6e99a5e71d8aaffdd0619df91d2f)

**Problem:** We propose Wolf, a WOrLd summarization Framework for accurate video captioning.

**Method:** Wolf is an automated captioning framework that adopts a mixture-of-experts approach, leveraging complementary strengths of Vision Language Models (VLMs).

**Result:** Finally, we establish a benchmark for video captioning and introduce a leaderboard, aiming to accelerate advancements in video understanding, captioning, and data alignment.

---
