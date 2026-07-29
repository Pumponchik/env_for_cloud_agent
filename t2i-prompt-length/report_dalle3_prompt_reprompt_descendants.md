# Who cites "Improving Image Generation with Better Captions" and studies prompt/reprompt design?

**Seed:** Betker et al. (OpenAI), *Improving Image Generation with Better Captions* — the DALL·E 3 technical paper that popularized (a) training on **long detailed synthetic captions**, and (b) **prompt upsampling** at inference.

**Method:** retrieved all **1794** Semantic Scholar citations, scored each for relevance to prompt rewriting / caption length-density design / recaptioning practices, and filtered to the **top papers** that actually investigate **how to build prompts and reprompts** — not just mention DALL·E 3 as a baseline.

**Focus set:** 60 papers in three categories: prompt rewrite / PE (18), caption length & design (22), synthetic recaptioning (20).

---

## Key pattern: what these descendants answer

Betker et al. established the doctrine: "long descriptive synthetic captions + prompt upsampling at inference." The citing papers test, extend, or challenge this along **three axes**:

1. **Caption length/density/variability at training** — is longer always better? What happens to aesthetics, diversity, short-prompt behavior? How to mix or randomize?
2. **Prompt rewriting / enhancement at inference** — how to build the rewriter? What objective? What length? CoT? RL? Faithfulness? Does it transfer?
3. **Recaptioning methodology** — which VLM? What decode budget? Hallucination risk? Scale?

---

## Prompt rewriting / enhancement / PE (inference-side) (18 papers)

### 1. Improving Text-to-Image Generation with Input-Side Inference-Time Scaling

- **Link:** [https://arxiv.org/abs/2510.12041](https://arxiv.org/abs/2510.12041)
- **Year:** 2025 · **Citations:** 4

Recent advances in text-to-image (T2I) generation have achieved impressive results, yet existing models often struggle with simple or underspecified prompts, leading to suboptimal image-text alignment, aesthetics, and quality.

We propose a prompt rewriting framework that leverages large language models (LLMs) to refine user inputs before feeding them into T2I backbones.

Our approach introduces a carefully designed reward system and an iterative direct preference optimization (DPO) training pipeline, enabling the rewriter to enhance prompts without requiring supervised fine-tuning data.

We evaluate our method across diverse T2I models and benchmarks.

**Why it matters for prompt/reprompt design:**
- Studies how to rewrite/enhance user prompts before generation.
- Uses RL/DPO to train the rewriter — relevant for PE training recipe.
- Shows rewriter transfers across T2I backbones.
- Documents aesthetics–alignment trade-off from caption choices.

### 2. PromptEnhancer: A Simple Approach to Enhance Text-to-Image Models via Chain-of-Thought Prompt Rewriting

- **Link:** [https://arxiv.org/abs/2509.04545](https://arxiv.org/abs/2509.04545)
- **Year:** 2025 · **Citations:** 32

Recent advancements in text-to-image (T2I) diffusion models have demonstrated remarkable capabilities in generating high-fidelity images.

However, these models often struggle to faithfully render complex user prompts, particularly in aspects like attribute binding, negation, and compositional relationships.

This leads to a significant mismatch between user intent and the generated output.

To address this challenge, we introduce PromptEnhancer, a novel and universal prompt rewriting framework that enhances any pretrained T2I model without requiring modifications to its weights.

**Why it matters for prompt/reprompt design:**
- Studies how to rewrite/enhance user prompts before generation.
- Uses RL/DPO to train the rewriter — relevant for PE training recipe.
- Uses chain-of-thought reasoning in the rewriting process.

### 3. RePrompt: Reasoning-Augmented Reprompting for Text-to-Image Generation via Reinforcement Learning

- **Link:** [https://arxiv.org/abs/2505.17540](https://arxiv.org/abs/2505.17540)
- **Year:** 2025 · **Citations:** 17

Despite recent progress in text-to-image (T2I) generation, existing models often struggle to faithfully capture user intentions from short and under-specified prompts.

While prior work has attempted to enhance prompts using large language models (LLMs), these methods frequently generate stylistic or unrealistic content due to insufficient grounding in visual semantics and real-world composition.

Inspired by recent advances in reasoning for language model, we propose RePrompt, a novel reprompting framework that introduces explicit reasoning into the prompt enhancement process via reinforcement learning.

Instead of relying on handcrafted rules or stylistic rewrites, our method trains a language model to generate structured, self-reflective prompts by optimizing for image-level outcomes.

**Why it matters for prompt/reprompt design:**
- Studies how to rewrite/enhance user prompts before generation.
- Uses RL/DPO to train the rewriter — relevant for PE training recipe.

### 4. RAPO++: Cross-Stage Prompt Optimization for Text-to-Video Generation via Data Alignment and Test-Time Scaling

- **Link:** [https://arxiv.org/abs/2510.20206](https://arxiv.org/abs/2510.20206)
- **Year:** 2025 · **Citations:** 6

Prompt design plays a crucial role in text-to-video (T2V) generation, yet user-provided prompts are often short, unstructured, and misaligned with training data, limiting the generative potential of diffusion-based T2V models.

We present \textbf{RAPO++}, a cross-stage prompt optimization framework that unifies training-data--aligned refinement, test-time iterative scaling, and large language model (LLM) fine-tuning to substantially improve T2V generation without modifying the underlying generative backbone.

In \textbf{Stage 1}, Retrieval-Augmented Prompt Optimization (RAPO) enriches user prompts with semantically relevant modifiers retrieved from a relation graph and refactors them to match training distributions, enhancing compositionality and multi-object fidelity.

\textbf{Stage 2} introduces Sample-Specific Prompt Optimization (SSPO), a closed-loop mechanism that iteratively refines prompts using multi-source feedback -- including semantic alignment, spatial fidelity, temporal coherence, and task-specific signals such as optical flow -- yielding progressively improved video g...

**Why it matters for prompt/reprompt design:**
- Studies how to rewrite/enhance user prompts before generation.
- Frames rewriting as distribution matching between train and user text.

### 5. BanditRewriter: Training-free Adaptive Prompt Optimization for Text-to-Image Generation

- **Link:** [https://www.semanticscholar.org/paper/acfc508e81309509e3095543761837d1f9c28da8](https://www.semanticscholar.org/paper/acfc508e81309509e3095543761837d1f9c28da8)
- **Year:** 2025 · **Citations:** 0

In the Text-to-Image (T2I) generation task, precisely constructed prompts are crucial for fully leveraging the generative model’s capabilities and obtaining preferable image outputs.

However, well-performed prompts are usually model-specific, requiring customization for each T2I model.

Existing prompt optimization methods typically rely on inefficient searches, heuristic algorithms, or model-specific training, which are computationally expensive and inflexible.

To address these challenges, BanditRewriter is proposed, which leverages large language model to adaptively optimize prompts for different T2I models.

**Why it matters for prompt/reprompt design:**
- Studies how to rewrite/enhance user prompts before generation.
- Uses RL/DPO to train the rewriter — relevant for PE training recipe.
- Documents aesthetics–alignment trade-off from caption choices.

### 6. APE: Agentic Prompt Enhancer for Image Generation and Editing

- **Link:** [https://arxiv.org/abs/2606.00204](https://arxiv.org/abs/2606.00204)
- **Year:** 2026 · **Citations:** 0

Natural language has become a powerful interface for image generation and editing, yet text-guided visual systems remain highly sensitive to prompt formulation.

Semantically similar requests can produce different outputs depending on wording, specificity, and how explicitly visual constraints are stated, motivating prompt enhancement as a trainable component rather than a peripheral user choice.

Existing strong enhancers often rely on large, proprietary LLMs such as ChatGPT or Gemini, adding cost, latency, and deployment dependence to the visual generation pipeline.

We propose Agentic Prompt Enhancer (APE), a lightweight framework that post-trains small language models (SLMs) as prompt-enhancement agents.

**Why it matters for prompt/reprompt design:**
- Studies how to rewrite/enhance user prompts before generation.
- Uses RL/DPO to train the rewriter — relevant for PE training recipe.

### 7. CRAFT: Continuous Reasoning and Agentic Feedback Tuning for Multimodal Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2512.20362](https://arxiv.org/abs/2512.20362)
- **Year:** 2025 · **Citations:** 2

Recent work has shown that inference-time reasoning and reflection can improve text-to-image generation without retraining.

However, existing approaches often rely on implicit, holistic critiques or unconstrained prompt rewrites, making their behavior difficult to interpret, control, or stop reliably.

In contrast, large language models have benefited from explicit, structured forms of **thinking** based on verification, targeted correction, and early stopping.

We introduce CRAFT (Continuous Reasoning and Agentic Feedback Tuning), a training-free and model-agnostic framework for multimodal image generation.

**Why it matters for prompt/reprompt design:**
- Studies how to rewrite/enhance user prompts before generation.

### 8. Cheap-Tune: A Low-Resource Framework for Text-to-Video Generation via Single-Video Fine-Tuning of Diffusion Models

- **Link:** [https://www.semanticscholar.org/paper/8e69d914df3633199a20c545e5bc366c71579bbb](https://www.semanticscholar.org/paper/8e69d914df3633199a20c545e5bc366c71579bbb)
- **Year:** 2025 · **Citations:** 0

Diffusion models have advanced text-to-image (T2I) generation significantly, inspiring efforts to adapt them for text-to-video (T2V) tasks.

However, existing T2V methods often require large-scale video-text datasets, limiting their practicality.

This paper introduces Cheap-Tune, a novel T2V training approach based on single-video fine-tuning, enabling efficient learning with minimal data.

Built on a pretrained T2I diffusion model, Cheap-Tune generates semantically consistent, temporally coherent videos through targeted fine-tuning.

**Why it matters for prompt/reprompt design:**
- Studies how to rewrite/enhance user prompts before generation.

### 9. Diffusion Probe: Generated Image Result Prediction Using CNN Probes

- **Link:** [https://arxiv.org/abs/2602.23783](https://arxiv.org/abs/2602.23783)
- **Year:** 2026 · **Citations:** 4

Text-to-image (T2I) diffusion models lack an efficient mechanism for early quality assessment, leading to costly trial-and-error in multi-generation scenarios such as prompt iteration, agent-based generation, and flow-grpo.

We reveal a strong correlation between early diffusion cross-attention distributions and final image quality.

Based on this finding, we introduce Diffusion Probe, a framework that leverages internal cross-attention maps as predictive signals.

We design a lightweight predictor that maps statistical properties of early-stage cross-attention extracted from initial denoising steps to the final image's overall quality.

**Why it matters for prompt/reprompt design:**
- Uses RL/DPO to train the rewriter — relevant for PE training recipe.

### 10. Evolve to Inspire: Novelty Search for Diverse Image Generation

- **Link:** [https://arxiv.org/abs/2511.00686](https://arxiv.org/abs/2511.00686)
- **Year:** 2025 · **Citations:** 0

Text-to-image diffusion models, while proficient at generating high-fidelity im- ages, often suffer from limited output diversity, hindering their application in exploratory and ideation tasks.

Existing prompt optimization techniques typically target aesthetic fitness or are ill-suited to the creative visual domain.

To address this shortcoming, we introduce WANDER, a novelty search-based approach to generating diverse sets of images from a single input prompt.

WANDER operates directly on natural language prompts, employing a Large Language Model (LLM) for semantic evolution of diverse sets of images, and using CLIP embeddings to quantify novelty.


### 11. Reverse Prompt: Cracking the Recipe Inside Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2503.19937](https://arxiv.org/abs/2503.19937)
- **Year:** 2025 · **Citations:** 2

Text-to-image generation has become increasingly popular, but achieving the desired images often requires extensive prompt engineering.

In this paper, we explore how to decode textual prompts from reference images, a process we refer to as image reverse prompt engineering.

This technique enables us to gain insights from reference images, understand the creative processes of great artists, and generate impressive new images.

To address this challenge, we propose a method known as automatic reverse prompt optimization (ARPO).


### 12. Value-Aligned Prompt Moderation via Zero-Shot Agentic Rewriting for Safe Image Generation

- **Link:** [https://arxiv.org/abs/2511.11693](https://arxiv.org/abs/2511.11693)
- **Year:** 2025 · **Citations:** 1

Generative vision-language models like Stable Diffusion demonstrate remarkable capabilities in creative media synthesis, but they also pose substantial risks of producing unsafe, offensive, or culturally inappropriate content when prompted adversarially.

Current defenses struggle to align outputs with human values without sacrificing generation quality or incurring high costs.

To address these challenges, we introduce VALOR (Value-Aligned LLM-Overseen Rewriter), a modular, zero-shot agentic framework for safer and more helpful text-to-image generation.

VALOR integrates layered prompt analysis with human-aligned value reasoning: a multi-level NSFW detector filters lexical and semantic risks; a cultural value alignment module identifies violations of social norms, legality, and representational ethics; and an intention disambiguator detects subtle or indirect unsafe...

**Why it matters for prompt/reprompt design:**
- Studies how to rewrite/enhance user prompts before generation.

### 13. Silencing controversial realities through prompt revision: The erasure of intensive livestock farming in text-to-image generative AI

- **Link:** [https://www.semanticscholar.org/paper/52e13aac02b3efa460447ab8ebb264961e2c465c](https://www.semanticscholar.org/paper/52e13aac02b3efa460447ab8ebb264961e2c465c)
- **Year:** 2026 · **Citations:** 0


### 14. Personalizing Text-to-Image Generation to Individual Taste

- **Link:** [https://arxiv.org/abs/2604.07427](https://arxiv.org/abs/2604.07427)
- **Year:** 2026 · **Citations:** 0

Modern text-to-image (T2I) models generate high-fidelity visuals but remain indifferent to individual user preferences.

While existing reward models optimize for"average"human appeal, they fail to capture the inherent subjectivity of aesthetic judgment.

In this work, we introduce a novel dataset and predictive framework, called PAMELA, designed to model personalized image evaluations.

Our dataset comprises 70,000 ratings across 5,000 diverse images generated by state-of-the-art models (Flux 2 and Nano Banana).

**Why it matters for prompt/reprompt design:**
- Uses RL/DPO to train the rewriter — relevant for PE training recipe.
- Frames rewriting as distribution matching between train and user text.

### 15. Endogenous Reprompting: Self-Evolving Cognitive Alignment for Unified Multimodal Models

- **Link:** [https://arxiv.org/abs/2601.20305](https://arxiv.org/abs/2601.20305)
- **Year:** 2026 · **Citations:** 4

Unified Multimodal Models (UMMs) exhibit strong understanding, yet this capability often fails to effectively guide generation.

We identify this as a Cognitive Gap: the model lacks the understanding of how to enhance its own generation process.

To bridge this gap, we propose Endogenous Reprompting, a mechanism that transforms the model's understanding from a passive encoding process into an explicit generative reasoning step by generating self-aligned descriptors during generation.

To achieve this, we introduce SEER (Self-Evolving Evaluator and Reprompter), a training framework that establishes a two-stage endogenous loop using only 300 samples from a compact proxy task, Visual Instruction Elaboration.

**Why it matters for prompt/reprompt design:**
- Studies how to rewrite/enhance user prompts before generation.
- Uses RL/DPO to train the rewriter — relevant for PE training recipe.

### 16. AutoPrompt: Automated Red-Teaming of Text-to-Image Models via LLM-Driven Adversarial Prompts

- **Link:** [https://arxiv.org/abs/2510.24034](https://arxiv.org/abs/2510.24034)
- **Year:** 2025 · **Citations:** 3

Despite rapid advancements in text-to-image (T2I) models, their safety mechanisms are vulnerable to adversarial prompts, which maliciously generate unsafe images.

Current red-teaming methods for proactively assessing such vulnerabilities usually require white-box access to T2I models, and rely on inefficient per-prompt optimization, as well as inevitably generate semantically meaningless prompts easily blocked by filters.

In this paper, we propose APT (AutoPrompT), a black-box framework that leverages large language models (LLMs) to automatically generate humanreadable adversarial suffixes for benign prompts.

We first introduce an alternating optimization-finetuning pipeline between adversarial suffix optimization and fine-tuning the LLM utilizing the optimized suffix.


### 17. The erasure of intensive livestock farming in text-to-image generative AI

- **Link:** [https://arxiv.org/abs/2502.19771](https://arxiv.org/abs/2502.19771)
- **Year:** 2025 · **Citations:** 3

Generative AI (e.g., ChatGPT) is increasingly integrated into people's daily lives.

While it is known that AI perpetuates biases against marginalized human groups, their impact on non-human animals remains understudied.

We found that ChatGPT's text-to-image model (DALL-E 3) introduces a strong bias toward romanticizing livestock farming as dairy cows on pasture and pigs rooting in mud.

This bias remained when we requested realistic depictions and was only mitigated when the automatic prompt revision was inhibited.


### 18. AP-Adapter: Improving Generalization of Automatic Prompts on Unseen Text-to-Image Diffusion Models

- **Link:** [https://www.semanticscholar.org/paper/576cd76439a75625ec7eb9f8aa0acffa88e60781](https://www.semanticscholar.org/paper/576cd76439a75625ec7eb9f8aa0acffa88e60781)
- **Year:** 2024 · **Citations:** 2

Recent advancements in Automatic Prompt Optimization (APO) for text-to-image generation have streamlined user input while ensuring high-quality image output.

However, most APO methods are trained assuming a fixed text-to-image model, which is impractical given the emergence of new models.

To address this, we propose a novel task, model-generalized automatic prompt optimization (MGAPO), which trains APO methods on a set of known models to enable generalization to unseen models during testing.

First, we experimentally confirm the suboptimal performance of existing APO methods on unseen models.

**Why it matters for prompt/reprompt design:**
- Studies how to rewrite/enhance user prompts before generation.

## Caption length, density, variability (training-side) (22 papers)

### 19. How to Train Your Text-to-Image Model: Evaluating Design Choices for Synthetic Training Captions

- **Link:** [https://arxiv.org/abs/2506.16679](https://arxiv.org/abs/2506.16679)
- **Year:** 2025 · **Citations:** 4

Training data is at the core of any successful text-to-image models.

The quality and descriptiveness of image text are crucial to a model's performance.

Given the noisiness and inconsistency in web-scraped datasets, recent works shifted towards synthetic training captions.

While this setup is generally believed to produce more capable models, current literature does not provide any insights into its design choices.

**Why it matters for prompt/reprompt design:**
- Studies how to rewrite/enhance user prompts before generation.
- Ablates caption length, density, or randomization at training.
- Investigates synthetic recaptioning pipeline and its parameters.
- Frames rewriting as distribution matching between train and user text.

### 20. Generating an Image From 1,000 Words: Enhancing Text-to-Image With Structured Captions

- **Link:** [https://arxiv.org/abs/2511.06876](https://arxiv.org/abs/2511.06876)
- **Year:** 2025 · **Citations:** 10

Text-to-image models have rapidly evolved from casual creative tools to professional-grade systems, achieving unprecedented levels of image quality and realism.

Yet, most models are trained to map short prompts into detailed images, creating a gap between sparse textual input and rich visual outputs.

This mismatch reduces controllability, as models often fill in missing details arbitrarily, biasing toward average user preferences and limiting precision for professional use.

We address this limitation by training the first open-source text-to-image model on long structured captions, where every training sample is annotated with the same set of fine-grained attributes.

**Why it matters for prompt/reprompt design:**
- Studies how to rewrite/enhance user prompts before generation.
- Ablates caption length, density, or randomization at training.

### 21. DreamLIP: Language-Image Pre-training with Long Captions

- **Link:** [https://arxiv.org/abs/2403.17007](https://arxiv.org/abs/2403.17007)
- **Year:** 2024 · **Citations:** 89

Language-image pre-training largely relies on how precisely and thoroughly a text describes its paired image.

In practice, however, the contents of an image can be so rich that well describing them requires lengthy captions (e.g., with 10 sentences), which are usually missing in existing datasets.

Consequently, there are currently no clear evidences on whether and how language-image pre-training could benefit from long captions.

To figure this out, we first re-caption 30M images with detailed descriptions using a pre-trained Multi-modality Large Language Model (MLLM), and then study the usage of the resulting captions under a contrastive learning framework.

**Why it matters for prompt/reprompt design:**
- Ablates caption length, density, or randomization at training.
- Investigates synthetic recaptioning pipeline and its parameters.

### 22. ShareGPT4Video: Improving Video Understanding and Generation with Better Captions

- **Link:** [https://arxiv.org/abs/2406.04325](https://arxiv.org/abs/2406.04325)
- **Year:** 2024 · **Citations:** 454

We present the ShareGPT4Video series, aiming to facilitate the video understanding of large video-language models (LVLMs) and the video generation of text-to-video models (T2VMs) via dense and precise captions.

The series comprises: 1) ShareGPT4Video, 40K GPT4V annotated dense captions of videos with various lengths and sources, developed through carefully designed data filtering and annotating strategy.

2) ShareCaptioner-Video, an efficient and capable captioning model for arbitrary videos, with 4.8M high-quality aesthetic videos annotated by it.

3) ShareGPT4Video-8B, a simple yet superb LVLM that reached SOTA performance on three advancing video benchmarks.

**Why it matters for prompt/reprompt design:**
- Ablates caption length, density, or randomization at training.
- Investigates synthetic recaptioning pipeline and its parameters.

### 23. Harnessing Caption Detailness for Data-Efficient Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2505.15172](https://arxiv.org/abs/2505.15172)
- **Year:** 2025 · **Citations:** 1

Training text-to-image (T2I) models with detailed captions can significantly improve their generation quality.

Existing methods often rely on simplistic metrics like caption length to represent the detailness of the caption in the T2I training set.

In this paper, we propose a new metric to estimate caption detailness based on two aspects: image coverage rate (ICR), which evaluates whether the caption covers all regions/objects in the image, and average object detailness (AOD), which quantifies the detailness of each object's description.

Through experiments on the COCO dataset using ShareGPT4V captions, we demonstrate that T2I models trained on high-ICR and -AOD captions achieve superior performance on DPG and other benchmarks.

**Why it matters for prompt/reprompt design:**
- Ablates caption length, density, or randomization at training.

### 24. VideoPainter: Any-length Video Inpainting and Editing with Plug-and-Play Context Control

- **Link:** [https://arxiv.org/abs/2503.05639](https://arxiv.org/abs/2503.05639)
- **Year:** 2025 · **Citations:** 78

Video inpainting, crucial for the media industry, aims to restore corrupted content.

However, current methods relying on limited pixel propagation or single-branch image inpainting architectures face challenges with generating fully masked objects, balancing background preservation with foreground generation, and maintaining ID consistency over long video.

To address these issues, we propose VideoPainter, an efficient dual-branch framework featuring a lightweight context encoder.

This plug-and-play encoder processes masked videos and injects background guidance into any pre-trained video diffusion transformer, generalizing across arbitrary mask types, enhancing background integration and foreground generation, and enabling user-customized control.

**Why it matters for prompt/reprompt design:**
- Studies how to rewrite/enhance user prompts before generation.
- Ablates caption length, density, or randomization at training.

### 25. Efficient Scaling of Diffusion Transformers for Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2412.12391](https://arxiv.org/abs/2412.12391)
- **Year:** 2024 · **Citations:** 4

We empirically study the scaling properties of various Diffusion Transformers (DiTs) for text-to-image generation by performing extensive and rigorous ablations, including training scaled DiTs ranging from 0.3B upto 8B parameters on datasets up to 600M images.

We find that U-ViT, a pure self-attention based DiT model provides a simpler design and scales more effectively in comparison with cross-attention based DiT variants, which allows straightforward expansion for extra conditions and other modalities.

We identify a 2.3B U-ViT model can get better performance than SDXL UNet and other DiT variants in controlled setting.

On the data scaling side, we investigate how increasing dataset size and enhanced long caption improve the text-image alignment performance and the learning efficiency.

**Why it matters for prompt/reprompt design:**
- Studies how to rewrite/enhance user prompts before generation.
- Ablates caption length, density, or randomization at training.

### 26. Lens: Rethinking Training Efficiency for Foundational Text-to-Image Models

- **Link:** [https://arxiv.org/abs/2605.21573](https://arxiv.org/abs/2605.21573)
- **Year:** 2026 · **Citations:** 1

We introduce Lens, a 3.8B-parameter T2I model that achieves performance competitive with, and in several cases surpassing, state-of-the-art models with more than 6B parameters across various benchmarks, while requiring significantly less training compute.

For example, Lens requires only about 19.3% of the training compute used by Z-Image.

The training efficiency of Lens stems from two key strategies beyond its compact model size.

First, we maximize data information density per training batch by (i) training on Lens-800M, a dataset of 800M densely captioned image-text pairs whose captions are generated by GPT-4.1 and contain approximately 109 words on average, providing richer semantic supervision than conventional short captions, and (ii) co...

**Why it matters for prompt/reprompt design:**
- Uses RL/DPO to train the rewriter — relevant for PE training recipe.

### 27. Moving Alphabet: A Controlled Study of Training Data for Text-to-Video Generation

- **Link:** [https://arxiv.org/abs/2607.18789](https://arxiv.org/abs/2607.18789)
- **Year:** 2026 · **Citations:** 0

Text-to-video generation has advanced significantly over the past five years through scaling of model size, data, and compute.

Unlike model architecture, training data is often underexplored.

Real-world data curation is complex and non-trivial, involving clip selection from raw videos and captioning to create video-text pairs for learning text-to-video mappings.

We study how data distribution and caption quality impact text-to-video models.


### 28. ETTA: Elucidating the Design Space of Text-to-Audio Models

- **Link:** [https://arxiv.org/abs/2412.19351](https://arxiv.org/abs/2412.19351)
- **Year:** 2024 · **Citations:** 20

Recent years have seen significant progress in Text-To-Audio (TTA) synthesis, enabling users to enrich their creative workflows with synthetic audio generated from natural language prompts.

Despite this progress, the effects of data, model architecture, training objective functions, and sampling strategies on target benchmarks are not well understood.

With the purpose of providing a holistic understanding of the design space of TTA models, we set up a large-scale empirical experiment focused on diffusion and flow matching models.

Our contributions include: 1) AF-Synthetic, a large dataset of high quality synthetic captions obtained from an audio understanding model; 2) a systematic comparison of different architectural, training, and inference design choices for TTA models; 3) an analysis of sampling methods and their Pareto curves with resp...

**Why it matters for prompt/reprompt design:**
- Investigates synthetic recaptioning pipeline and its parameters.

### 29. BACON: Improving Clarity of Image Captions via Bag-of-Concept Graphs

- **Link:** [https://arxiv.org/abs/2407.03314](https://arxiv.org/abs/2407.03314)
- **Year:** 2024 · **Citations:** 5

Advancements in large Vision-Language Models have brought precise, accurate image captioning, vital for advancing multi-modal image understanding and processing.

Yet these captions often carry lengthy, intertwined contexts that are difficult to parse and frequently overlook essential cues, posing a great barrier for models like GroundingDINO and SDXL, which lack the strong text encoding and syntax analysis needed to fully leverage dense captions.

To address this, we propose BACON, a prompting method that breaks down VLM-generated captions into disentangled, structured elements such as objects, relationships, styles, and themes.

This approach not only minimizes confusion from handling complex contexts but also allows for efficient transfer into a JSON dictionary, enabling models without linguistic processing capabilities to easily access key information.

**Why it matters for prompt/reprompt design:**
- Ablates caption length, density, or randomization at training.

### 30. On the Scalability of Diffusion-based Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2404.02883](https://arxiv.org/abs/2404.02883)
- **Year:** 2024 · **Citations:** 43

Scaling up model and data size has been quite successful for the evolution of LLMs.

However, the scaling law for the diffusion based text-to-image (T2I) models is not fully explored.

It is also unclear how to efficiently scale the model for better performance at reduced cost.

The different training settings and expensive training cost make a fair model comparison extremely difficult.


### 31. Semantic Browsing: Controllable Diversity for Image Generation

- **Link:** [https://arxiv.org/abs/2606.23679](https://arxiv.org/abs/2606.23679)
- **Year:** 2026 · **Citations:** 0

Modern text-to-image models excel in visual fidelity and prompt adherence.

However, this strict adherence comes at the cost of diversity: generated samples tend to collapse into a single visual interpretation.

Existing methods to improve diversity produce outputs driven by incidental variations rather than meaningful design choices.

This motivates a new variant of the diversity task where structure is enforced on the generated samples.


### 32. Generate Any Scene: Scene Graph Driven Data Synthesis for Visual Generation Training

- **Link:** [https://arxiv.org/abs/2412.08221](https://arxiv.org/abs/2412.08221)
- **Year:** 2024 · **Citations:** 3

Recent advances in text-to-vision generation excel in visual fidelity but struggle with compositional generalization and semantic alignment.

Existing datasets are noisy and weakly compositional, limiting models'understanding of complex scenes, while scalable solutions for dense, high-quality annotations remain a challenge.

We introduce Generate Any Scene, a data engine that systematically enumerates scene graphs representing the combinatorial array of possible visual scenes.

Generate Any Scene dynamically constructs scene graphs of varying complexity from a structured taxonomy of objects, attributes, and relations.

**Why it matters for prompt/reprompt design:**
- Studies how to rewrite/enhance user prompts before generation.
- Investigates synthetic recaptioning pipeline and its parameters.
- Uses RL/DPO to train the rewriter — relevant for PE training recipe.

### 33. KOALA: Empirical Lessons Toward Memory-Efficient and Fast Diffusion Models for Text-to-Image Synthesis

- **Link:** [https://arxiv.org/abs/2312.04005](https://arxiv.org/abs/2312.04005)
- **Year:** 2023 · **Citations:** 21

As text-to-image (T2I) synthesis models increase in size, they demand higher inference costs due to the need for more expensive GPUs with larger memory, which makes it challenging to reproduce these models in addition to the restricted access to training datasets.

Our study aims to reduce these inference costs and explores how far the generative capabilities of T2I models can be extended using only publicly available datasets and open-source models.

To this end, by using the de facto standard text-to-image model, Stable Diffusion XL (SDXL), we present three key practices in building an efficient T2I model: (1) Knowledge distillation: we explore how to effectively distill the generation capability of SDXL into an efficient U-Net and find that self-attention is t...

(2) Data: despite fewer samples, high-resolution images with rich captions are more crucial than a larger number of low-resolution images with short captions.


### 34. Segment and Caption Anything

- **Link:** [https://arxiv.org/abs/2312.00869](https://arxiv.org/abs/2312.00869)
- **Year:** 2023 · **Citations:** 38

We propose a method to efficiently equip the Segment Anything Model (SAM) with the ability to generate regional captions.

SAM presents strong generalizability to segment anything while is short for semantic understanding.

By introducing a lightweight query-based feature mixer, we align the region-specific features with the embedding space of language models for later caption generation.

As the number of trainable parameters is small (typically in the order of tens of millions), it costs less computation, less memory usage, and less communication bandwidth, resulting in both fast and scalable training.


### 35. LoTLIP: Improving Language-Image Pre-training for Long Text Understanding

- **Link:** [https://arxiv.org/abs/2410.05249](https://arxiv.org/abs/2410.05249)
- **Year:** 2024 · **Citations:** 33

Understanding long text is of great demands in practice but beyond the reach of most language-image pre-training (LIP) models.

In this work, we empirically confirm that the key reason causing such an issue is that the training images are usually paired with short captions, leaving certain tokens easily overshadowed by salient tokens.

Towards this problem, our initial attempt is to relabel the data with long captions, however, directly learning with which may lead to performance degradation in understanding short text (e.g., in the image classification task).

Then, after incorporating corner tokens to aggregate diverse textual information, we manage to help the model catch up to its original level of short text understanding yet greatly enhance its capability of long text understanding.

**Why it matters for prompt/reprompt design:**
- Studies how to rewrite/enhance user prompts before generation.
- Ablates caption length, density, or randomization at training.

### 36. DetailMaster: Can Your Text-to-Image Model Handle Long Prompts?

- **Link:** [https://arxiv.org/abs/2505.16915](https://arxiv.org/abs/2505.16915)
- **Year:** 2025 · **Citations:** 6

While recent Text-to-Image (T2I) models show impressive capabilities in synthesizing images from brief descriptions, they struggle with the long, detailed prompts required for professional applications.

We present DetailMaster, a comprehensive benchmark for evaluating T2I capabilities on long prompts with complex compositional requirements, accompanied by an automated data construction pipeline and an evaluation workflow.

Comprising expert-validated prompts averaging 284.89 tokens, our benchmark introduces four critical evaluation dimensions: Character Attributes, Structured Character Locations, Multi-Dimensional Scene Attributes, and Spatial/Interactive Relationships.

Evaluations on various general-purpose and long-prompt-optimized models reveal critical performance limitations, showing that weak encoders struggle to preserve syntactic dependencies within prompts and diffusion models suffer from attribute leakage under detail-intensive conditions.


### 37. DetCLIPv3: Towards Versatile Generative Open-Vocabulary Object Detection

- **Link:** [https://arxiv.org/abs/2404.09216](https://arxiv.org/abs/2404.09216)
- **Year:** 2024 · **Citations:** 70

Existing open-vocabulary object detectors typically require a predefined set of categories from users, signifi-cantly confining their application scenarios.

In this pa-per, we introduce DetCLIPv3, a high-performing detector that excels not only at both open-vocabulary object detection, but also generating hierarchical labels for detected objects.

DetCLIPv3 is characterized by three core designs: 1.

Versatile model architecture: we derive a robust open-set detection framework which is further empowered with generation ability via the integration of a caption head.

**Why it matters for prompt/reprompt design:**
- Studies how to rewrite/enhance user prompts before generation.
- Ablates caption length, density, or randomization at training.

### 38. Mimir: Improving Video Diffusion Models for Precise Text Understanding

- **Link:** [https://arxiv.org/abs/2412.03085](https://arxiv.org/abs/2412.03085)
- **Year:** 2024 · **Citations:** 19

Text serves as the key control signal in video generation due to its narrative nature.

To render text descriptions into video clips, current video diffusion models borrow features from text encoders yet struggle with limited text comprehension.

The recent success of large language models (LLMs) showcases the power of decoder-only transformers, which offers three clear benefits for text-to-video (T2V) generation, namely, precise text understanding resulting from the superior scalability, imagination beyond the input text enabled by next token prediction, an...

Nevertheless, the feature distribution gap emerging from the two different text modeling paradigms hinders the direct use of LLMs in established T2V models.

**Why it matters for prompt/reprompt design:**
- Frames rewriting as distribution matching between train and user text.

### 39. GMAIL: Generative Modality Alignment for generated Image Learning

- **Link:** [https://arxiv.org/abs/2602.15368](https://arxiv.org/abs/2602.15368)
- **Year:** 2026 · **Citations:** 2

Generative models have made it possible to synthesize highly realistic images, potentially providing an abundant data source for training machine learning models.

Despite the advantages of these synthesizable data sources, the indiscriminate use of generated images as real images for training can even cause mode collapse due to modality discrepancies between real and synthetic domains.

In this paper, we propose a novel framework for discriminative use of generated images, coined GMAIL, that explicitly treats generated images as a separate modality from real images.

Instead of indiscriminately replacing real images with generated ones in the pixel space, our approach bridges the two distinct modalities in the same latent space through a multi-modal learning approach.

**Why it matters for prompt/reprompt design:**
- Studies how to rewrite/enhance user prompts before generation.
- Ablates caption length, density, or randomization at training.

### 40. Playground v3: Improving Text-to-Image Alignment with Deep-Fusion Large Language Models

- **Link:** [https://arxiv.org/abs/2409.10695](https://arxiv.org/abs/2409.10695)
- **Year:** 2024 · **Citations:** 109

We introduce Playground v3 (PGv3), our latest text-to-image model that achieves state-of-the-art (SoTA) performance across multiple testing benchmarks, excels in graphic design abilities and introduces new capabilities.

Unlike traditional text-to-image generative models that rely on pre-trained language models like T5 or CLIP text encoders, our approach fully integrates Large Language Models (LLMs) with a novel structure that leverages text conditions exclusively from a decoder-only LLM.

Additionally, to enhance image captioning quality-we developed an in-house captioner, capable of generating captions with varying levels of detail, enriching the diversity of text structures.

We also introduce a new benchmark CapsBench to evaluate detailed image captioning performance.

**Why it matters for prompt/reprompt design:**
- Studies how to rewrite/enhance user prompts before generation.

## Synthetic recaptioning methodology (20 papers)

### 41. Building a Precise Video Language with Human-AI Oversight

- **Link:** [https://arxiv.org/abs/2604.21718](https://arxiv.org/abs/2604.21718)
- **Year:** 2026 · **Citations:** 1

Video-language models (VLMs) learn to reason about the dynamic visual world through natural language.

We introduce a suite of open datasets, benchmarks, and recipes for scalable oversight that enable precise video captioning.

First, we define a structured specification for describing subjects, scenes, motion, spatial, and camera dynamics, grounded by hundreds of carefully defined visual primitives developed with professional video creators such as filmmakers.

Next, to curate high-quality captions, we introduce CHAI (Critique-based Human-AI Oversight), a framework where trained experts critique and revise model-generated pre-captions into improved post-captions.

**Why it matters for prompt/reprompt design:**
- Investigates synthetic recaptioning pipeline and its parameters.
- Uses RL/DPO to train the rewriter — relevant for PE training recipe.

### 42. Rethinking Music Captioning with Music Metadata LLMs

- **Link:** [https://arxiv.org/abs/2602.03023](https://arxiv.org/abs/2602.03023)
- **Year:** 2026 · **Citations:** 2

Music captioning, or the task of generating a natural language description of music, is useful for both music understanding and controllable music generation.

Training captioning models, however, typically requires high-quality music caption data which is scarce compared to metadata (e.g., genre, mood, etc.).

As a result, it is common to use large language models (LLMs) to synthesize captions from metadata to generate training data for captioning models, though this process imposes a fixed stylization and entangles factual information with natural language style.

As a more direct approach, we propose metadata-based captioning.


### 43. RICO: Improving Accuracy and Completeness in Image Recaptioning via Visual Reconstruction

- **Link:** [https://arxiv.org/abs/2505.22613](https://arxiv.org/abs/2505.22613)
- **Year:** 2025 · **Citations:** 5

Image recaptioning is widely used to generate training datasets with enhanced quality for various multimodal tasks.

Existing recaptioning methods typically rely on powerful multimodal large language models (MLLMs) to enhance textual descriptions, but often suffer from inaccuracies due to hallucinations and incompleteness caused by missing fine-grained details.

To address these limitations, we propose RICO, a novel framework that refines captions through visual reconstruction.

Specifically, we leverage a text-to-image model to reconstruct a caption into a reference image, and prompt an MLLM to identify discrepancies between the original and reconstructed images to refine the caption.

**Why it matters for prompt/reprompt design:**
- Studies how to rewrite/enhance user prompts before generation.
- Investigates synthetic recaptioning pipeline and its parameters.
- Addresses faithfulness / hallucination risk of rewrites.
- Uses RL/DPO to train the rewriter — relevant for PE training recipe.

### 44. What If We Recaption Billions of Web Images with LLaMA-3?

- **Link:** [https://arxiv.org/abs/2406.08478](https://arxiv.org/abs/2406.08478)
- **Year:** 2024 · **Citations:** 81

Web-crawled image-text pairs are inherently noisy.

Prior studies demonstrate that semantically aligning and enriching textual descriptions of these pairs can significantly enhance model training across various vision-language tasks, particularly text-to-image generation.

However, large-scale investigations in this area remain predominantly closed-source.

Our paper aims to bridge this community effort, leveraging the powerful and \textit{open-sourced} LLaMA-3, a GPT-4 level LLM.

**Why it matters for prompt/reprompt design:**
- Studies how to rewrite/enhance user prompts before generation.
- Investigates synthetic recaptioning pipeline and its parameters.

### 45. Mastering Text-to-Image Diffusion: Recaptioning, Planning, and Generating with Multimodal LLMs

- **Link:** [https://arxiv.org/abs/2401.11708](https://arxiv.org/abs/2401.11708)
- **Year:** 2024 · **Citations:** 256

Diffusion models have exhibit exceptional performance in text-to-image generation and editing.

However, existing methods often face challenges when handling complex text prompts that involve multiple objects with multiple attributes and relationships.

In this paper, we propose a brand new training-free text-to-image generation/editing framework, namely Recaption, Plan and Generate (RPG), harnessing the powerful chain-of-thought reasoning ability of multimodal LLMs to enhance the compositionality of text-to-image diffusion models.

Our approach employs the MLLM as a global planner to decompose the process of generating complex images into multiple simpler generation tasks within subregions.

**Why it matters for prompt/reprompt design:**
- Studies how to rewrite/enhance user prompts before generation.
- Investigates synthetic recaptioning pipeline and its parameters.
- Uses chain-of-thought reasoning in the rewriting process.

### 46. A Picture is Worth a Thousand Words: Principled Recaptioning Improves Image Generation

- **Link:** [https://arxiv.org/abs/2310.16656](https://arxiv.org/abs/2310.16656)
- **Year:** 2023 · **Citations:** 40

Text-to-image diffusion models achieved a remarkable leap in capabilities over the last few years, enabling high-quality and diverse synthesis of images from a textual prompt.

However, even the most advanced models often struggle to precisely follow all of the directions in their prompts.

The vast majority of these models are trained on datasets consisting of (image, caption) pairs where the images often come from the web, and the captions are their HTML alternate text.

A notable example is the LAION dataset, used by Stable Diffusion and other models.

**Why it matters for prompt/reprompt design:**
- Investigates synthetic recaptioning pipeline and its parameters.

### 47. Low-hallucination Synthetic Captions for Large-Scale Vision-Language Model Pre-training

- **Link:** [https://arxiv.org/abs/2504.13123](https://arxiv.org/abs/2504.13123)
- **Year:** 2025 · **Citations:** 6

In recent years, the field of vision-language model pre-training has experienced rapid advancements, driven primarily by the continuous enhancement of textual capabilities in large language models.

However, existing training paradigms for multimodal large language models heavily rely on high-quality image-text pairs.

As models and data scales grow exponentially, the availability of such meticulously curated data has become increasingly scarce and saturated, thereby severely limiting further advancements in this domain.

This study investigates scalable caption generation techniques for vision-language model pre-training and demonstrates that large-scale low-hallucination synthetic captions can serve dual purposes: 1) acting as a viable alternative to real-world data for pre-training paradigms and 2) achieving superior performance e...

**Why it matters for prompt/reprompt design:**
- Studies how to rewrite/enhance user prompts before generation.
- Investigates synthetic recaptioning pipeline and its parameters.
- Addresses faithfulness / hallucination risk of rewrites.
- Uses RL/DPO to train the rewriter — relevant for PE training recipe.

### 48. View Selection for 3D Captioning via Diffusion Ranking

- **Link:** [https://arxiv.org/abs/2404.07984](https://arxiv.org/abs/2404.07984)
- **Year:** 2024 · **Citations:** 42

Scalable annotation approaches are crucial for constructing extensive 3D-text datasets, facilitating a broader range of applications.

However, existing methods sometimes lead to the generation of hallucinated captions, compromising caption quality.

This paper explores the issue of hallucination in 3D object captioning, with a focus on Cap3D method, which renders 3D objects into 2D views for captioning using pre-trained models.

We pinpoint a major challenge: certain rendered views of 3D objects are atypical, deviating from the training data of standard image captioning models and causing hallucinations.

**Why it matters for prompt/reprompt design:**
- Studies how to rewrite/enhance user prompts before generation.
- Addresses faithfulness / hallucination risk of rewrites.

### 49. Improving Explicit Spatial Relationships in Text-to-Image Generation through an Automatically Derived Dataset

- **Link:** [https://arxiv.org/abs/2403.00587](https://arxiv.org/abs/2403.00587)
- **Year:** 2024 · **Citations:** 3

Existing work has observed that current text-to-image systems do not accurately reflect explicit spatial relations between objects such as 'left of' or 'below'.

We hypothesize that this is because explicit spatial relations rarely appear in the image captions used to train these models.

We propose an automatic method that, given existing images, generates synthetic captions that contain 14 explicit spatial relations.

We introduce the Spatial Relation for Generation (SR4G) dataset, which contains 9.9 millions image-caption pairs for training, and more than 60 thousand captions for evaluation.

**Why it matters for prompt/reprompt design:**
- Investigates synthetic recaptioning pipeline and its parameters.

### 50. Factorized-Dreamer: Training A High-Quality Video Generator with Limited and Low-Quality Data

- **Link:** [https://arxiv.org/abs/2408.10119](https://arxiv.org/abs/2408.10119)
- **Year:** 2024 · **Citations:** 1

Text-to-video (T2V) generation has gained significant attention due to its wide applications to video generation, editing, enhancement and translation, \etc.

However, high-quality (HQ) video synthesis is extremely challenging because of the diverse and complex motions existed in real world.

Most existing works struggle to address this problem by collecting large-scale HQ videos, which are inaccessible to the community.

In this work, we show that publicly available limited and low-quality (LQ) data are sufficient to train a HQ video generator without recaptioning or finetuning.

**Why it matters for prompt/reprompt design:**
- Studies how to rewrite/enhance user prompts before generation.
- Investigates synthetic recaptioning pipeline and its parameters.

### 51. Precision or Recall? An Analysis of Image Captions for Training Text-to-Image Generation Model

- **Link:** [https://arxiv.org/abs/2411.05079](https://arxiv.org/abs/2411.05079)
- **Year:** 2024 · **Citations:** 0

Despite advancements in text-to-image models, generating images that precisely align with textual descriptions remains challenging due to misalignment in training data.

In this paper, we analyze the critical role of caption precision and recall in text-to-image model training.

Our analysis of human-annotated captions shows that both precision and recall are important for text-image alignment, but precision has a more significant impact.

Leveraging these insights, we utilize Large Vision Language Models to generate synthetic captions for training.

**Why it matters for prompt/reprompt design:**
- Investigates synthetic recaptioning pipeline and its parameters.

### 52. Revisit Large-Scale Image-Caption Data in Pre-training Multimodal Foundation Models

- **Link:** [https://arxiv.org/abs/2410.02740](https://arxiv.org/abs/2410.02740)
- **Year:** 2024 · **Citations:** 14

Recent advancements in multimodal models highlight the value of rewritten captions for improving performance, yet key challenges remain.

For example, while synthetic captions often provide superior quality and image-text alignment, it is not clear whether they can fully replace AltTexts: the role of synthetic captions and their interaction with original web-crawled AltTexts in pre-training is still not well understood.

Moreover, different multimodal foundation models may have unique preferences for specific caption formats, but efforts to identify the optimal captions for each model remain limited.

In this work, we propose a novel, controllable, and scalable captioning pipeline designed to generate diverse caption formats tailored to various multimodal models.

**Why it matters for prompt/reprompt design:**
- Investigates synthetic recaptioning pipeline and its parameters.

### 53. CommonCanvas: An Open Diffusion Model Trained with Creative-Commons Images

- **Link:** [https://arxiv.org/abs/2310.16825](https://arxiv.org/abs/2310.16825)
- **Year:** 2023 · **Citations:** 24

We assemble a dataset of Creative-Commons-licensed (CC) images, which we use to train a set of open diffusion models that are qualitatively competitive with Stable Diffusion 2 (SD2).

This task presents two challenges: (1) high-resolution CC images lack the captions necessary to train text-to-image generative models; (2) CC images are relatively scarce.

In turn, to address these challenges, we use an intuitive transfer learning technique to produce a set of high-quality synthetic captions paired with curated CC images.

We then develop a data- and compute-efficient training recipe that requires as little as 3% of the LAION-2B data needed to train existing SD2 models, but obtains comparable quality.

**Why it matters for prompt/reprompt design:**
- Investigates synthetic recaptioning pipeline and its parameters.

### 54. Improving Text Generation on Images with Synthetic Captions

- **Link:** [https://arxiv.org/abs/2406.00505](https://arxiv.org/abs/2406.00505)
- **Year:** 2024 · **Citations:** 4

The recent emergence of latent diffusion models such as SDXL [1] and SD 1.5 [2] has shown significant capability in generating highly detailed and realistic images.

Despite their remarkable ability to produce images, generating accurate text within images still remains a challenging task.

In this paper, we examine the validity of fine-tuning approaches in generating legible text within the image.

We propose a low-cost approach by leveraging SDXL without any time-consuming training on large-scale datasets.

**Why it matters for prompt/reprompt design:**
- Ablates caption length, density, or randomization at training.
- Investigates synthetic recaptioning pipeline and its parameters.

### 55. Dual-Stage Value-Guided Inference with Margin-Based Reward Adjustment for Fast and Faithful VLM Captioning

- **Link:** [https://arxiv.org/abs/2506.15649](https://arxiv.org/abs/2506.15649)
- **Year:** 2025 · **Citations:** 2

Despite significant advances in inference-time search for vision-language models (VLMs), existing approaches remain both computationally expensive and prone to unpenalized, low-confidence generations which often lead to persistent hallucinations.

We introduce \textbf{Value-guided Inference with Margin-based Reward (ViMaR)}, a two-stage inference framework that improves both efficiency and output fidelity by combining a temporal-difference value model with a margin-aware reward adjustment.

In the first stage, we perform a single pass to identify the highest-value caption among diverse candidates.

In the second stage, we selectively refine only those segments that were overlooked or exhibit weak visual grounding, thereby eliminating frequently rewarded evaluations.

**Why it matters for prompt/reprompt design:**
- Addresses faithfulness / hallucination risk of rewrites.
- Uses RL/DPO to train the rewriter — relevant for PE training recipe.

### 56. Altogether: Image Captioning via Re-aligning Alt-text

- **Link:** [https://arxiv.org/abs/2410.17251](https://arxiv.org/abs/2410.17251)
- **Year:** 2024 · **Citations:** 23

This paper focuses on creating synthetic data to improve the quality of image captions.

Existing works typically have two shortcomings.

First, they caption images from scratch, ignoring existing alt-text metadata, and second, lack transparency if the captioners’ training data (e.g.

In this paper, we study a principled approach Altogether based on the key idea to edit and re-align existing alt-texts associated with the images.


### 57. MoTrans: Customized Motion Transfer with Text-driven Video Diffusion Models

- **Link:** [https://arxiv.org/abs/2412.01343](https://arxiv.org/abs/2412.01343)
- **Year:** 2024 · **Citations:** 13

Existing pretrained text-to-video (T2V) models have demonstrated impressive abilities in generating realistic videos with basic motion or camera movement.

However, these models exhibit significant limitations when generating intricate, human-centric motions.

Current efforts primarily focus on fine-tuning models on a small set of videos containing a specific motion.

They often fail to effectively decouple motion and the appearance in the limited reference videos, thereby weakening the modeling capability of motion patterns.

**Why it matters for prompt/reprompt design:**
- Studies how to rewrite/enhance user prompts before generation.
- Investigates synthetic recaptioning pipeline and its parameters.

### 58. ReflectCAP: Detailed Image Captioning with Reflective Memory

- **Link:** [https://arxiv.org/abs/2604.12357](https://arxiv.org/abs/2604.12357)
- **Year:** 2026 · **Citations:** 1

Detailed image captioning demands both factual grounding and fine-grained coverage, yet existing methods have struggled to achieve them simultaneously.

We address this tension with Reflective Note-Guided Captioning (ReflectCAP), where a multi-agent pipeline analyzes what the target large vision-language model (LVLM) consistently hallucinates and what it systematically overlooks, distilling these patterns into reusable guidelines called Structured Reflection Notes.

At inference time, these notes steer the captioning model along both axes -- what to avoid and what to attend to -- yielding detailed captions that jointly improve factuality and coverage.

Applying this method to 8 LVLMs spanning the GPT-4.1 family, Qwen series, and InternVL variants, ReflectCAP reaches the Pareto frontier of the trade-off between factuality and coverage, and delivers substantial gains on CapArena-Auto, where generated captions are judged head-to-head against strong reference models.

**Why it matters for prompt/reprompt design:**
- Addresses faithfulness / hallucination risk of rewrites.

### 59. Wolf: Dense Video Captioning with a World Summarization Framework

- **Link:** [https://arxiv.org/abs/2407.18908](https://arxiv.org/abs/2407.18908)
- **Year:** 2024 · **Citations:** 6

We propose Wolf, a WOrLd summarization Framework for accurate video captioning.

Wolf is an automated captioning framework that adopts a mixture-of-experts approach, leveraging complementary strengths of Vision Language Models (VLMs).

By utilizing both image and video models, our framework captures different levels of information and summarizes them efficiently.

Our approach can be applied to enhance video understanding, auto-labeling, and captioning.

**Why it matters for prompt/reprompt design:**
- Studies how to rewrite/enhance user prompts before generation.

### 60. SpatialCLIP: Learning 3D-aware Image Representations from Spatially Discriminative Language

- **Link:** [https://www.semanticscholar.org/paper/34176c4820d3e8623574cbd2a97bdacdee2476d3](https://www.semanticscholar.org/paper/34176c4820d3e8623574cbd2a97bdacdee2476d3)
- **Year:** 2025 · **Citations:** 23

Contrastive Language-Image Pre-training (CLIP) learns robust visual models through language supervision, making it a crucial visual encoding technique for various applications.

However, CLIP struggles with comprehending spatial concepts in images, potentially restricting the spatial intelligence of CLIP-based AI systems.

In this work, we propose SpatialCLIP, an enhanced version of CLIP with better spatial understanding capabilities.

To capture the intricate 3D spatial relationships in images, we improve both "visual model" and "language supervision" of CLIP.

**Why it matters for prompt/reprompt design:**
- Studies how to rewrite/enhance user prompts before generation.
- Investigates synthetic recaptioning pipeline and its parameters.

---

## Summary: what this citation tree tells us about prompt/reprompt

1. **Betker's "long captions + upsample" sparked an entire sub-field** of prompt rewriting research (PromptEnhancer, TIPO, RePrompt, Input-Side Scaling, BanditRewriter, APE, FaithRewriter, RAPO++).
2. **The rewriting / PE line is converging** on: CoT reasoning, RL with fine-grained alignment rewards, optional visual anchors for faithfulness, and transferability across generators.
3. **The caption-design line** (Brack "How to Train", DreamLIP, FIBO, Lens, ETTA, Harnessing Caption Detailness) is nuancing the "longer is better" claim with trade-off analysis and randomization.
4. **The recaptioning line** (Recap-DataComp, RECAP, RICO, ShareGPT4Video, Low-hallucination Captions) focuses on VLM decode budgets, hallucination, and scale.
5. **The key open question** remains: how to jointly optimize train caption policy + inference PE policy, rather than tuning each in isolation.

---

## Practical reading order for someone building a reprompt system

1. **Betker et al. (DALL·E 3)** — the original doctrine
2. **Brack et al. (How to Train)** — why long-only hurts; randomize length
3. **PromptEnhancer** — CoT + AlignEvaluator RL for content-focused rewrite
4. **Input-Side Inference-Time Scaling** — iterative DPO rewriter; distribution matching; cross-backbone transfer
5. **RePrompt** — reasoning-augmented reprompting via RL
6. **FaithRewriter** — visual anchoring to prevent hallucination
7. **TIPO** — expand toward training distribution, not max verbosity
8. **i1** — length-alignment diagnostic (short→repeat→rewrite proves the distributional effect)
9. **RECAP / Recap-DataComp** — offline recaption budgets and length trade-offs
10. **Harnessing Caption Detailness** — data-efficient approach to caption density

---

## Machine-readable

- `citation_tree/dalle3_better_captions_cites_raw.json` — all 1794 S2 citations
- `citation_tree/dalle3_prompt_reprompt_descendants.json` — top 120 scored
