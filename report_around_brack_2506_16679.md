# Digging Around Brack et al. 2025: Synthetic Training Caption Design

**Seed paper:** [How to Train your Text-to-Image Model: Evaluating Design Choices for Synthetic Training Captions](https://arxiv.org/abs/2506.16679) (arXiv:2506.16679)

**Authors:** Manuel Brack, Sudeep Katakol, Felix Friedrich, Patrick Schramowski, Hareesh Ravi, Kristian Kersting, Ajinkya Kale (Adobe Applied Research / hessian.AI / TU Darmstadt / DFKI)

*This report maps the citation neighborhood of the seed, then expands to ~100 similar empirical / caption-design papers. Goal: find work with a **similar scientific approach** (controlled hypotheses & ablations on training captions), not only model tech reports.*

---

## Why this paper is special

Most modern T2I releases say they use “synthetic captions” and move on. Brack et al. instead run a **continual-pretraining ablation lab**:

- Fix architecture (SD), images (1M LAION-Aesthetics subset), order, and compute; **vary only captions**.
- State hypotheses (**H1** long dense is better; **H2** diversity matters; **H3** caption gender terms drive bias).
- Test VLM strength, length/density, temperature diversity, inter-epoch caption refresh, persona prompting, and occupation-gender bias.
- Evaluate with aesthetics, PickScore, LPIPS diversity, and bias metrics across **four prompt-complexity levels**.

**Main results that matter for length/variability:**

1. Stronger VLM captions → better text following.
2. Long dense captions are **not unequivocally better**: they help alignment but hurt aesthetics and short-prompt diversity (short prompts become OOD).
3. **Randomizing caption length/density** removes the aesthetics–alignment trade-off and preserves diversity.
4. Caption term distributions shift output bias (e.g., gender).

That is why it sits above most tech reports for our question.

---

## Citation tree

### Descendants (papers citing the seed)

The paper is recent (June 2025). Indexed forward citations are still sparse. Semantic Scholar currently returns **4 citing works**; OpenAlex lists the work but still shows **0 cited_by** (index lag).

### D1. No Safe Dose: How Training Data Drives Unsafe Image Generation

- **Link:** [https://arxiv.org/abs/2605.28137](https://arxiv.org/abs/2605.28137)
- **Year:** 2026 · **arXiv:** 2605.28137 · **S2 cites:** 0

Text-to-image models trained on large-scale data often inevitably ingest unsafe content. While some people observe input-output amplifications, it remains unclear whether and how training data composition directly drives model output safety or by other factors. We shed light on this question by isolating this variable: we train the same text-to-image model on datasets that differ \emph{only} in their fraction of unsafe images (0\% to 9.6\%), across several dataset scales (100K to 8M). Then we generate images with the resulting models, and evaluate them with four independent safety classifiers. Output unsafety rises monotonically from 16.6\% at 0\% contamination to 25.5\% at 5\%. A factorial

*Relevance:* uses / extends the idea that **training text distribution** shapes model behavior (safety angle rather than length).

### D2. Jano: Adaptive Diffusion Generation with Early-stage Convergence Awareness

- **Link:** [https://arxiv.org/abs/2603.00519](https://arxiv.org/abs/2603.00519)
- **Year:** 2026 · **arXiv:** 2603.00519 · **S2 cites:** 1

Diffusion models have achieved remarkable success in generative AI, yet their computational efficiency remains a significant challenge, particularly for Diffusion Transformers (DiTs) requiring intensive full-attention computation. While existing acceleration approaches focus on content-agnostic uniform optimization strategies, we observe that different regions in generated content exhibit heterogeneous convergence patterns during the denoising process. We present Jano, a training-free framework that leverages this insight for efficient region-aware generation. Jano introduces an early-stage complexity recognition algorithm that accurately identifies regional convergence requirements within i

*Relevance:* early forward citation; not a full methodological sequel.

### D3. Asymmetric Idiosyncrasies in Multimodal Models

- **Link:** [https://arxiv.org/abs/2602.22734](https://arxiv.org/abs/2602.22734)
- **Year:** 2026 · **arXiv:** 2602.22734 · **S2 cites:** 1

In this work, we study idiosyncrasies in the caption models and their downstream impact on text-to-image models. We design a systematic analysis: given either a generated caption or the corresponding image, we train neural networks to predict the originating caption model. Our results show that text classification yields very high accuracy (99.70\%), indicating that captioning models embed distinctive stylistic signatures. In contrast, these signatures largely disappear in the generated images, with classification accuracy dropping to at most 50\% even for the state-of-the-art Flux model. To better understand this cross-modal discrepancy, we further analyze the data and find that the generat

*Relevance:* multimodal idiosyncrasy analysis citing caption-training findings as background.

### D4. UniFusion: Vision-Language Model as Unified Encoder in Image Generation

- **Link:** [https://arxiv.org/abs/2510.12789](https://arxiv.org/abs/2510.12789)
- **Year:** 2025 · **arXiv:** 2510.12789 · **S2 cites:** 6

Although recent advances in visual generation have been remarkable, most existing architectures still depend on distinct encoders for images and text. This separation constrains diffusion models'ability to perform cross-modal reasoning and knowledge transfer. Prior attempts to bridge this gap often use the last layer information from VLM, employ multiple visual encoders, or train large unified models jointly for text and image generation, which demands substantial computational resources and large-scale data, limiting its accessibility.We present UniFusion, a diffusion-based generative model conditioned on a frozen large vision-language model (VLM) that serves as a unified multimodal encoder

*Relevance:* modern encoder/captioning stack paper that cites the seed in the synthetic-caption training discussion.

**Bottom line on continuations:** there is **no clear dedicated sequel** yet that repeats Brack’s caption-design lab at larger scale. Same-author follow-ups exist in **bias/fairness/editing** (Safe Latent Diffusion, LEDITS++, multilingual T2I gender stereotypes), but not a second “caption design choices” paper. The research line is young; the true sequels are currently **sibling empirical papers** (below), not children.

### Same-author neighborhood (Manuel Brack)

- (2025) ActivationReasoning: Logical Reasoning in Latent Activation Spaces — cites≈0
- (2025) CHRONOBERG: Capturing Language Evolution and Temporal Awareness in Foundation Models — cites≈0
- (2025) Judging Quality Across Languages: A Multilingual Approach to Pretraining Data Filtering with Language Models — cites≈0
- (2025) The Cake that is Intelligence and Who Gets to Bake it: An AI Analogy and its Implications for Participation — cites≈3
- (2025) Multilingual Text-to-Image Generation Magnifies Gender Stereotypes — cites≈4
- (2025) Judging Quality Across Languages: A Multilingual Approach to Pretraining Data Filtering with Language Models — cites≈1
- (2024) Auditing and instructing text-to-image generation models on fairness — cites≈40
- (2024) LEDITS++: Limitless Image Editing Using Text-to-Image Models — cites≈67
- (2023) Safe Latent Diffusion: Mitigating Inappropriate Degeneration in Diffusion Models — cites≈167
- (2023) Mitigating Inappropriateness in Image Generation: Can there be Value in Reflecting the World's Ugliness? — cites≈5
- (2022) Safe Latent Diffusion: Mitigating Inappropriate Degeneration in Diffusion Models — cites≈8
- (2022) ILLUME: Rationalizing Vision-Language Models through Human Interactions — cites≈0

These are thematically adjacent (safety, fairness, editing), useful if you care about Brack H3 (bias), but they are **not** caption-length ablations.

### Ancestors (what the seed stands on)

Semantic Scholar reports **51 references**; the HTML bibliography has **41** entries. Below: the ones that matter for caption design, grouped by role.

#### Key claim being tested

- **Improving Image Generation with Better Captions** (None) — [https://www.semanticscholar.org/paper/cfee1826dd4743eab44c6e27a0cc5970effa4d80](https://www.semanticscholar.org/paper/cfee1826dd4743eab44c6e27a0cc5970effa4d80) · cites≈1794
  - Brack H1 is a direct stress-test of this claim (“long descriptive synthetic captions are better”).


#### Direct method ancestors

- **Playground v3: Improving Text-to-Image Alignment with Deep-Fusion Large Language Models** (2024) — [https://arxiv.org/abs/2409.10695](https://arxiv.org/abs/2409.10695) · cites≈109
  - Motivates H2: varying density / inter-epoch caption diversity.

- **CommonCanvas: An Open Diffusion Model Trained with Creative-Commons Images** (2023) — [https://arxiv.org/abs/2310.16825](https://arxiv.org/abs/2310.16825) · cites≈24


#### Data / captioning ancestors

- **Hierarchical Text-Conditional Image Generation with CLIP Latents** (2022) — [https://arxiv.org/abs/2204.06125](https://arxiv.org/abs/2204.06125) · cites≈9235

- **BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models** (2023) — [https://arxiv.org/abs/2301.12597](https://arxiv.org/abs/2301.12597) · cites≈8733

- **LAION-5B: An open large-scale dataset for training next generation image-text models** (2022) — [https://arxiv.org/abs/2210.08402](https://arxiv.org/abs/2210.08402) · cites≈5410

- **CLIPScore: A Reference-free Evaluation Metric for Image Captioning** (2021) — [https://arxiv.org/abs/2104.08718](https://arxiv.org/abs/2104.08718) · cites≈3028

- **LAION-400M: Open Dataset of CLIP-Filtered 400 Million Image-Text Pairs** (2021) — [https://arxiv.org/abs/2111.02114](https://arxiv.org/abs/2111.02114) · cites≈1890

- **DataComp: In search of the next generation of multimodal datasets** (2023) — [https://arxiv.org/abs/2304.14108](https://arxiv.org/abs/2304.14108) · cites≈738

- **The Bias Amplification Paradox in Text-to-Image Generation** (2023) — [https://arxiv.org/abs/2308.00755](https://arxiv.org/abs/2308.00755) · cites≈92

- **On the Scalability of Diffusion-based Text-to-Image Generation** (2024) — [https://arxiv.org/abs/2404.02883](https://arxiv.org/abs/2404.02883) · cites≈43

- **Training on long, dense captions results in better prompt following of the downstream text-to-image model** (None) · cites≈None

- **Randomizing training caption length does not adversely affect text alignment while providing the beneﬁts out-lined in Sec. 4.2** (None) · cites≈None


#### Model / training ancestors

- **High-Resolution Image Synthesis with Latent Diffusion Models** (2021) — [https://arxiv.org/abs/2112.10752](https://arxiv.org/abs/2112.10752) · cites≈26396

- **The Unreasonable Effectiveness of Deep Features as a Perceptual Metric** (2018) — [https://arxiv.org/abs/1801.03924](https://arxiv.org/abs/1801.03924) · cites≈18892

- **Photorealistic Text-to-Image Diffusion Models with Deep Language Understanding** (2022) — [https://arxiv.org/abs/2205.11487](https://arxiv.org/abs/2205.11487) · cites≈8661

- **Sigmoid Loss for Language Image Pre-Training** (2023) — [https://arxiv.org/abs/2303.15343](https://arxiv.org/abs/2303.15343) · cites≈3477

- **Scaling Autoregressive Models for Content-Rich Text-to-Image Generation** (2022) — [https://arxiv.org/abs/2206.10789](https://arxiv.org/abs/2206.10789) · cites≈1542

- **Safe Latent Diffusion: Mitigating Inappropriate Degeneration in Diffusion Models** (2022) — [https://arxiv.org/abs/2211.05105](https://arxiv.org/abs/2211.05105) · cites≈593

- **Fast High-Resolution Image Synthesis with Latent Adversarial Diffusion Distillation** (2024) — [https://arxiv.org/abs/2403.12015](https://arxiv.org/abs/2403.12015) · cites≈300

- **GenAI-Bench: Evaluating and Improving Compositional Text-to-Visual Generation** (2024) — [https://arxiv.org/abs/2406.13743](https://arxiv.org/abs/2406.13743) · cites≈120

- **Evaluating and Improving Compositional Text-to-Visual Generation** (2024) — [https://www.semanticscholar.org/paper/befc322dd67db943e66fff57553056fe78009dff](https://www.semanticscholar.org/paper/befc322dd67db943e66fff57553056fe78009dff) · cites≈63


#### Evaluation ancestors

- **Classifier-Free Diffusion Guidance** (2022) — [https://arxiv.org/abs/2207.12598](https://arxiv.org/abs/2207.12598) · cites≈6806

- **Scaling Rectified Flow Transformers for High-Resolution Image Synthesis** (2024) — [https://arxiv.org/abs/2403.03206](https://arxiv.org/abs/2403.03206) · cites≈4406

- **Semantics derived automatically from language corpora contain human-like biases** (2016) — [https://arxiv.org/abs/1608.07187](https://arxiv.org/abs/1608.07187) · cites≈3201

- **Pick-a-Pic: An Open Dataset of User Preferences for Text-to-Image Generation** (2023) — [https://arxiv.org/abs/2305.01569](https://arxiv.org/abs/2305.01569) · cites≈1070

- **FairFace: Face Attribute Dataset for Balanced Race, Gender, and Age for Bias Measurement and Mitigation** (2021) — [https://www.semanticscholar.org/paper/1c301a8a2dc281d43fa34cc7a7eee64a8acd711f](https://www.semanticscholar.org/paper/1c301a8a2dc281d43fa34cc7a7eee64a8acd711f) · cites≈788

- **On Aliased Resizing and Surprising Subtleties in GAN Evaluation** (2022) — [https://www.semanticscholar.org/paper/c539f6ab5818bde96f61298856cb0c38f6268369](https://www.semanticscholar.org/paper/c539f6ab5818bde96f61298856cb0c38f6268369) · cites≈548

- **Easily Accessible Text-to-Image Generation Amplifies Demographic Stereotypes at Large Scale** (2022) — [https://arxiv.org/abs/2211.03759](https://arxiv.org/abs/2211.03759) · cites≈535

- **Auditing and instructing text-to-image generation models on fairness** (2024) — [https://www.semanticscholar.org/paper/f240825e618621eff36510d916b23f6c06af680d](https://www.semanticscholar.org/paper/f240825e618621eff36510d916b23f6c06af680d) · cites≈44

- **Multilingual Text-to-Image Generation Magnifies Gender Stereotypes and Prompt Engineering May Not Help You** (2024) — [https://arxiv.org/abs/2401.16092](https://arxiv.org/abs/2401.16092) · cites≈21


#### Other references

- **Decoupled Weight Decay Regularization** (2017) — [https://www.semanticscholar.org/paper/d07284a6811f1b2745d91bdb06b040b57f226882](https://www.semanticscholar.org/paper/d07284a6811f1b2745d91bdb06b040b57f226882) · cites≈36845

- **GANs Trained by a Two Time-Scale Update Rule Converge to a Local Nash Equilibrium** (2017) — [https://www.semanticscholar.org/paper/231af7dc01a166cac3b5b01ca05778238f796e41](https://www.semanticscholar.org/paper/231af7dc01a166cac3b5b01ca05778238f796e41) · cites≈19080

- **Contributors** (1966) — [https://www.semanticscholar.org/paper/4aa95dc3682d664b333a868ce350d1567abc47cd](https://www.semanticscholar.org/paper/4aa95dc3682d664b333a868ce350d1567abc47cd) · cites≈2495

- **How far are we to GPT-4V? Closing the gap to commercial multimodal models with open-source suites** (2024) — [https://arxiv.org/abs/2404.16821](https://arxiv.org/abs/2404.16821) · cites≈1239

- **SGLang: Efficient Execution of Structured Language Model Programs** (2023) — [https://arxiv.org/abs/2312.07104](https://arxiv.org/abs/2312.07104) · cites≈1121

- **eDiff-I: Text-to-Image Diffusion Models with an Ensemble of Expert Denoisers** (2022) — [https://arxiv.org/abs/2211.01324](https://arxiv.org/abs/2211.01324) · cites≈1091

- **LLaVA-NeXT-Interleave: Tackling Multi-image, Video, and 3D in Large Multimodal Models** (2024) — [https://arxiv.org/abs/2407.07895](https://arxiv.org/abs/2407.07895) · cites≈623

- **Evaluating Large Language Models in Generating Synthetic HCI Research Data: a Case Study** (2023) — [https://www.semanticscholar.org/paper/0ffd57884d7957f6b5634b9fa24843dc3759668f](https://www.semanticscholar.org/paper/0ffd57884d7957f6b5634b9fa24843dc3759668f) · cites≈331

- **Scaling Rectiﬁed Flow Transformers for High-Resolution Image Synthesis** (None) — [https://www.semanticscholar.org/paper/8ae86095f53d2a5735c59d3e6b1b7b0090c88e7f](https://www.semanticscholar.org/paper/8ae86095f53d2a5735c59d3e6b1b7b0090c88e7f) · cites≈313

- **Two Tales of Persona in LLMs: A Survey of Role-Playing and Personalization** (2024) — [https://arxiv.org/abs/2406.01171](https://arxiv.org/abs/2406.01171) · cites≈290

- **Transformers are Minimax Optimal Nonparametric In-Context Learners** (2024) — [https://arxiv.org/abs/2408.12186](https://arxiv.org/abs/2408.12186) · cites≈39

- **DataDecide: How to Predict Best Pretraining Data with Small Experiments** (2025) — [https://arxiv.org/abs/2504.11393](https://arxiv.org/abs/2504.11393) · cites≈36

- **Benchmarking of Deep Architectures for Segmentation of Medical Images** (2022) — [https://www.semanticscholar.org/paper/2bc737f92a5729b31f76ac67daad9a93a9630c80](https://www.semanticscholar.org/paper/2bc737f92a5729b31f76ac67daad9a93a9630c80) · cites≈31

- **MVPTR: Multi-Level Semantic Alignment for Vision-Language Pre-Training via Multi-Stage Learning** (2022) — [https://arxiv.org/abs/2201.12596](https://arxiv.org/abs/2201.12596) · cites≈25

- **Aligning VLM Assistants with Personalized Situated Cognition** (2025) — [https://arxiv.org/abs/2506.00930](https://arxiv.org/abs/2506.00930) · cites≈2

- **Fast high-resolution 6891 Authorized licensed use limited to the terms of the applicable** (None) · cites≈None

- **DeepFloyd-IF-I-XL-v1.0: DeepFloyd’s Image Generation Model** (None) · cites≈None

- **Fast high-resolution 6832** (None) · cites≈None

- **Hal-lusionbench: An advanced diagnostic suite for entangled language hallucination and visual illusion in large vision-language models** (None) · cites≈None

- **Gra-6890 license agreement with IEEE. Restrictions apply** (None) · cites≈None


#### Must-read ancestors (curated)

1. **DALL·E 3 — Improving Image Generation with Better Captions** ([PDF](https://cdn.openai.com/papers/dall-e-3.pdf)) — the claim Brack nuances.
2. **Playground v3** ([arXiv:2409.10695](https://arxiv.org/abs/2409.10695)) — varying density + inter-epoch diversity arguments.
3. **LAION-5B** ([arXiv:2210.08402](https://arxiv.org/abs/2210.08402)) — noisy alt-text baseline.
4. **BLIP-2** ([arXiv:2301.12597](https://arxiv.org/abs/2301.12597)) — “weak VLM captioner” baseline in practice.
5. **LDM/SD** ([arXiv:2112.10752](https://arxiv.org/abs/2112.10752)) — experimental backbone.
6. **Pick-a-Pic / PickScore** ([arXiv:2305.01569](https://arxiv.org/abs/2305.01569)) — preference metric used by Brack.
7. **Imagen** ([arXiv:2205.11487](https://arxiv.org/abs/2205.11487)) — language-quality → image-quality lineage.

---

## Closest papers with a *similar approach* (not just citations)

These are the works that, like Brack, try to **answer a scientific question about training text** with comparisons/ablations — not only ship a model.

| Paper | Why it is “Brack-like” | Differs how |
|-------|------------------------|-------------|
| RECAP (2310.16656) | Short vs Long vs Mix caption ablation on SD | Under hard CLIP-77; fine-tune setting |
| DALL·E 3 Better Captions | Origin of the long-caption doctrine + infer upsampling | Less public controlled ablations |
| Playground v3 | Argues density variation & epoch diversity | Mostly system paper with recipe claims |
| i1 (2606.11289) | Long vs short train + length-alignment diagnostic | Focus on infer rewrite to match long train |
| FIBO (2511.06876) | Long structured vs short under same backbone | Extreme ~1000-token structured captions |
| DetailMaster (2505.16915) | Dense long training vs capacity | Evaluation/ablation on long prompts |
| Altogether / Recap-DataComp | Synthetic vs alt-text mixing / web-scale recaption | Dataset-scale rather than continual SD lab |
| How-to-Train (seed) | Hypotheses + controlled caption-only ablations | — |

**Practical reading order:** DALL·E 3 Better Captions → RECAP → Brack seed → Playground v3 → i1 → FIBO/DetailMaster.

---

## ~100 similar papers in the same subject area

Selected from citation ancestors, targeted arXiv retrieval, and hand-curated siblings. Buckets:

- **synthetic_vs_web_captions**: 20
- **length_density_diversity**: 48
- **broader_conditioning_data**: 13
- **inference_distribution_match**: 2
- **datasets_benchmarks**: 15
- **caption_bias**: 2

### Bucket: synthetic_vs_web_captions

#### 1. Improving Image Generation with Better Captions (DALL·E 3)

- **Link:** [https://cdn.openai.com/papers/dall-e-3.pdf](https://cdn.openai.com/papers/dall-e-3.pdf)
- **id:** `dalle3-better-captions` · **published:** 2023 · **origin:** hand

DALL·E 3 Better Captions is the key claim ancestor behind Brack Hypothesis H1.

It popularized training on long, highly descriptive synthetic captions and rewriting short user prompts at inference.

Brack shows the recommendation is incomplete: long dense captions help alignment but can hurt aesthetics, diversity, and short-prompt behavior.

Any reading list around Brack must start here as the claim being stress-tested.


#### 2. What If We Recaption Billions of Web Images with LLaMA-3? (Recap-DataComp-1B)

- **Link:** [https://arxiv.org/abs/2406.08478](https://arxiv.org/abs/2406.08478)
- **id:** `2406.08478` · **published:** 2024-06-12 · **origin:** hand

Recap-DataComp-1B asks what happens if we recaption a billion-scale web dataset with a modern VLM.

With max_new_tokens=128, mean caption length jumps from ~10 to ~49 tokens and vocabulary coverage expands.

It supplies the large-scale data recipe that Brack-style ablations assume when arguing synthetic captions beat alt-text.

Use it when you care about operating points of offline recaptioners (decode budget -> realized length).


#### 3. LAION-5B

- **Link:** [https://arxiv.org/abs/2210.08402](https://arxiv.org/abs/2210.08402)
- **id:** `2210.08402` · **published:** n.d. · **origin:** hand

"LAION-5B" (n.d.) is related to the Brack et al. synthetic-caption training design line.

noisy web alt-text baseline that synthetic captions replace.

Its results speak to caption quality, length/density, diversity, or train-infer text matching.

Same paradigm shift Brack studies: replace noisy web text with synthetic captions.


#### 4. SD3

- **Link:** [https://arxiv.org/abs/2403.03206](https://arxiv.org/abs/2403.03206)
- **id:** `2403.03206` · **published:** n.d. · **origin:** hand

"SD3" (n.d.) is related to the Brack et al. synthetic-caption training design line.

It studies captioning, recaptioning, or training-data composition for text-to-image models.

Its results speak to caption quality, length/density, diversity, or train-infer text matching.

Same paradigm shift Brack studies: replace noisy web text with synthetic captions.


#### 5. Low-hallucination Synthetic Captions for Large-Scale Vision-Language Model Pre-training

- **Link:** [https://arxiv.org/abs/2504.13123](https://arxiv.org/abs/2504.13123)
- **id:** `2504.13123` · **published:** 2025-04-17 · **origin:** arxiv_search

"Low-hallucination Synthetic Captions for Large-Scale Vision-Language Model Pre-training" (2025) is related to the Brack et al. synthetic-caption training design line.

In recent years, the field of vision-language model pre-training has experienced rapid advancements, driven primarily by the continuous enhancement of textual capabilities in large language models.

However, existing training paradigms for multimodal large language models heavily rely on high-quality image-text pairs.

Same paradigm shift Brack studies: replace noisy web text with synthetic captions.


#### 6. What Media Frames Reveal About Stance: A Dataset and Study about Memes in Climate Change Discourse

- **Link:** [https://arxiv.org/abs/2505.16592](https://arxiv.org/abs/2505.16592)
- **id:** `2505.16592` · **published:** 2025-05-22 · **origin:** arxiv_search

"What Media Frames Reveal About Stance: A Dataset and Study about Memes in Climate Change Discourse" (2025) is related to the Brack et al. synthetic-caption training design line.

Media framing refers to the emphasis on specific aspects of perceived reality to shape how an issue is defined and understood.

Its primary purpose is to shape public perceptions often in alignment with the authors' opinions and stances.

Same paradigm shift Brack studies: replace noisy web text with synthetic captions.


#### 7. Improving Explicit Spatial Relationships in Text-to-Image Generation through an Automatically Derived Dataset

- **Link:** [https://arxiv.org/abs/2403.00587](https://arxiv.org/abs/2403.00587)
- **id:** `2403.00587` · **published:** 2024-03-01 · **origin:** arxiv_extra

"Improving Explicit Spatial Relationships in Text-to-Image Generation through an Automatically Derived Dataset" (2024) is related to the Brack et al. synthetic-caption training design line.

Existing work has observed that current text-to-image systems do not accurately reflect explicit spatial relations between objects such as 'left of' or 'below'.

We hypothesize that this is because explicit spatial relations rarely appear in the image captions used to train these models.

Same paradigm shift Brack studies: replace noisy web text with synthetic captions.


#### 8. Generate Any Scene: Scene Graph Driven Data Synthesis for Visual Generation Training

- **Link:** [https://arxiv.org/abs/2412.08221](https://arxiv.org/abs/2412.08221)
- **id:** `2412.08221` · **published:** 2024-12-11 · **origin:** arxiv_extra

"Generate Any Scene: Scene Graph Driven Data Synthesis for Visual Generation Training" (2024) is related to the Brack et al. synthetic-caption training design line.

Recent advances in text-to-vision generation excel in visual fidelity but struggle with compositional generalization and semantic alignment.

Existing datasets are noisy and weakly compositional, limiting models' understanding of complex scenes, while scalable solutions for dense, high-quality annotations remain a challenge.

Same paradigm shift Brack studies: replace noisy web text with synthetic captions.


#### 9. CommonCanvas: An Open Diffusion Model Trained with Creative-Commons Images

- **Link:** [https://arxiv.org/abs/2310.16825](https://arxiv.org/abs/2310.16825)
- **id:** `2310.16825` · **published:** 2023 · **origin:** s2_ref

"CommonCanvas: An Open Diffusion Model Trained with Creative-Commons Images" (2023) is related to the Brack et al. synthetic-caption training design line.

We assemble a dataset of Creative-Commons-licensed (CC) images, which we use to train a set of open diffusion models that are qualitatively competitive with Stable Diffusion 2 (SD2).

This task presents two challenges: (1) high-resolution CC images lack the captions necessary to train text-to-image generative models; (2) CC images are relatively scarce.

Same paradigm shift Brack studies: replace noisy web text with synthetic captions.


#### 10. Improving face generation quality and prompt following with synthetic captions

- **Link:** [https://arxiv.org/abs/2405.10864](https://arxiv.org/abs/2405.10864)
- **id:** `2405.10864` · **published:** 2024-05-17 · **origin:** arxiv_extra

"Improving face generation quality and prompt following with synthetic captions" (2024) is related to the Brack et al. synthetic-caption training design line.

Recent advancements in text-to-image generation using diffusion models have significantly improved the quality of generated images and expanded the ability to depict a wide range of objects.

However, ensuring that these models adhere closely to the text prompts remains a considerable challenge.

Same paradigm shift Brack studies: replace noisy web text with synthetic captions.


#### 11. Sound event detection with audio-text models and heterogeneous temporal annotations

- **Link:** [https://arxiv.org/abs/2508.20703](https://arxiv.org/abs/2508.20703)
- **id:** `2508.20703` · **published:** 2025-08-28 · **origin:** arxiv_search

"Sound event detection with audio-text models and heterogeneous temporal annotations" (2025) is related to the Brack et al. synthetic-caption training design line.

Recent advances in generating synthetic captions based on audio and related metadata allow using the information contained in natural language as input for other audio tasks.

In this paper, we propose a novel method to guide a sound event detection system with free-form text.

Same paradigm shift Brack studies: replace noisy web text with synthetic captions.


#### 12. Precision or Recall? An Analysis of Image Captions for Training Text-to-Image Generation Model

- **Link:** [https://arxiv.org/abs/2411.05079](https://arxiv.org/abs/2411.05079)
- **id:** `2411.05079` · **published:** 2024-11-07 · **origin:** arxiv_search

"Precision or Recall? An Analysis of Image Captions for Training Text-to-Image Generation Model" (2024) is related to the Brack et al. synthetic-caption training design line.

Despite advancements in text-to-image models, generating images that precisely align with textual descriptions remains challenging due to misalignment in training data.

In this paper, we analyze the critical role of caption precision and recall in text-to-image model training.

Same paradigm shift Brack studies: replace noisy web text with synthetic captions.


#### 13. Public Domain 12M: A Highly Aesthetic Image-Text Dataset with Novel Governance Mechanisms

- **Link:** [https://arxiv.org/abs/2410.23144](https://arxiv.org/abs/2410.23144)
- **id:** `2410.23144` · **published:** 2024-10-30 · **origin:** arxiv_search

"Public Domain 12M: A Highly Aesthetic Image-Text Dataset with Novel Governance Mechanisms" (2024) is related to the Brack et al. synthetic-caption training design line.

We present Public Domain 12M (PD12M), a dataset of 12.4 million high-quality public domain and CC0-licensed images with synthetic captions, designed for training text-to-image models.

PD12M is the largest public domain image-text dataset to date, with sufficient size to train foundation models while minimizing copyright concerns.

Same paradigm shift Brack studies: replace noisy web text with synthetic captions.


#### 14. Mastering Text-to-Image Diffusion: Recaptioning, Planning, and Generating with Multimodal LLMs

- **Link:** [https://arxiv.org/abs/2401.11708](https://arxiv.org/abs/2401.11708)
- **id:** `2401.11708` · **published:** 2024-01-22 · **origin:** arxiv_extra

"Mastering Text-to-Image Diffusion: Recaptioning, Planning, and Generating with Multimodal LLMs" (2024) is related to the Brack et al. synthetic-caption training design line.

Diffusion models have exhibit exceptional performance in text-to-image generation and editing.

However, existing methods often face challenges when handling complex text prompts that involve multiple objects with multiple attributes and relationships.

Same paradigm shift Brack studies: replace noisy web text with synthetic captions.


#### 15. HAIC: Improving Human Action Understanding and Generation with Better Captions for Multi-modal Large Language Models

- **Link:** [https://arxiv.org/abs/2502.20811](https://arxiv.org/abs/2502.20811)
- **id:** `2502.20811` · **published:** 2025-02-28 · **origin:** arxiv_search

"HAIC: Improving Human Action Understanding and Generation with Better Captions for Multi-modal Large Language Models" (2025) is related to the Brack et al. synthetic-caption training design line.

Recent Multi-modal Large Language Models (MLLMs) have made great progress in video understanding.

However, their performance on videos involving human actions is still limited by the lack of high-quality data.

Same paradigm shift Brack studies: replace noisy web text with synthetic captions.


#### 16. RICO: Improving Accuracy and Completeness in Image Recaptioning via Visual Reconstruction

- **Link:** [https://arxiv.org/abs/2505.22613](https://arxiv.org/abs/2505.22613)
- **id:** `2505.22613` · **published:** 2025-05-28 · **origin:** arxiv_extra

"RICO: Improving Accuracy and Completeness in Image Recaptioning via Visual Reconstruction" (2025) is related to the Brack et al. synthetic-caption training design line.

Image recaptioning is widely used to generate training datasets with enhanced quality for various multimodal tasks.

Existing recaptioning methods typically rely on powerful multimodal large language models (MLLMs) to enhance textual descriptions, but often suffer from inaccuracies due to hallucinations and incompleteness caused by missing fine-grained details.

Same paradigm shift Brack studies: replace noisy web text with synthetic captions.


#### 17. NLIP: Noise-robust Language-Image Pre-training

- **Link:** [https://arxiv.org/abs/2212.07086](https://arxiv.org/abs/2212.07086)
- **id:** `2212.07086` · **published:** 2022-12-14 · **origin:** arxiv_search

"NLIP: Noise-robust Language-Image Pre-training" (2022) is related to the Brack et al. synthetic-caption training design line.

Large-scale cross-modal pre-training paradigms have recently shown ubiquitous success on a wide range of downstream tasks, e.g., zero-shot classification, retrieval and image captioning.

However, their successes highly rely on the scale and quality of web-crawled data that naturally contain incomplete and noisy information (e.g., wrong or irrelevant content).

Same paradigm shift Brack studies: replace noisy web text with synthetic captions.


#### 18. MoTrans: Customized Motion Transfer with Text-driven Video Diffusion Models

- **Link:** [https://arxiv.org/abs/2412.01343](https://arxiv.org/abs/2412.01343)
- **id:** `2412.01343` · **published:** 2024-12-02 · **origin:** arxiv_extra

"MoTrans: Customized Motion Transfer with Text-driven Video Diffusion Models" (2024) is related to the Brack et al. synthetic-caption training design line.

Existing pretrained text-to-video (T2V) models have demonstrated impressive abilities in generating realistic videos with basic motion or camera movement.

However, these models exhibit significant limitations when generating intricate, human-centric motions.

Same paradigm shift Brack studies: replace noisy web text with synthetic captions.


#### 19. ALIP: Adaptive Language-Image Pre-training with Synthetic Caption

- **Link:** [https://arxiv.org/abs/2308.08428](https://arxiv.org/abs/2308.08428)
- **id:** `2308.08428` · **published:** 2023-08-16 · **origin:** arxiv_search

"ALIP: Adaptive Language-Image Pre-training with Synthetic Caption" (2023) is related to the Brack et al. synthetic-caption training design line.

Contrastive Language-Image Pre-training (CLIP) has significantly boosted the performance of various vision-language tasks by scaling up the dataset with image-text pairs collected from the web.

However, the presence of intrinsic noise and unmatched image-text pairs in web data can potentially affect the performance of representation learning.

Same paradigm shift Brack studies: replace noisy web text with synthetic captions.


#### 20. Altogether: Image Captioning via Re-aligning Alt-text

- **Link:** [https://arxiv.org/abs/2410.17251](https://arxiv.org/abs/2410.17251)
- **id:** `2410.17251` · **published:** 2024-10-22 · **origin:** arxiv_search

"Altogether: Image Captioning via Re-aligning Alt-text" (2024) is related to the Brack et al. synthetic-caption training design line.

This paper focuses on creating synthetic data to improve the quality of image captions.

Existing works typically have two shortcomings.

Same paradigm shift Brack studies: replace noisy web text with synthetic captions.


### Bucket: length_density_diversity

#### 21. A Picture is Worth a Thousand Words: Principled Recaptioning Improves Image Generation (RECAP)

- **Link:** [https://arxiv.org/abs/2310.16656](https://arxiv.org/abs/2310.16656)
- **id:** `2310.16656` · **published:** 2023-10-25 · **origin:** hand

"RECAP" (2023) is the closest earlier empirical sibling to Brack et al.: it ablates short vs long vs mixed recaptions for T2I fine-tuning.

RECAP-Short improves FID faster; RECAP-Long improves semantics; a 50/50 mix achieves both under the CLIP 77-token limit.

Captions longer than 77 tokens were dropped (<1%), so the study is budget-constrained but methodologically parallel.

Read together with Brack: RECAP is mixture-under-hard-limit; Brack is randomized density/length under continual SD pretraining with modern VLMs.


#### 22. Playground v3: Improving Text-to-Image Alignment with Deep-Fusion LLMs

- **Link:** [https://arxiv.org/abs/2409.10695](https://arxiv.org/abs/2409.10695)
- **id:** `2409.10695` · **published:** n.d. · **origin:** hand

"Playground v3: Improving Text-to-Image Alignment with Deep-Fusion LLMs" (n.d.) is related to the Brack et al. synthetic-caption training design line.

argues varying caption density + inter-epoch diversity; cited by Brack as H2 motivation.

Its results speak to caption quality, length/density, diversity, or train-infer text matching.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 23. i1: A Simple and Fully Open Recipe for Strong Text-to-Image Models

- **Link:** [https://arxiv.org/abs/2606.11289](https://arxiv.org/abs/2606.11289)
- **id:** `2606.11289` · **published:** n.d. · **origin:** hand

"i1: A Simple and Fully Open Recipe for Strong Text-to-Image Models" (n.d.) is related to the Brack et al. synthetic-caption training design line.

controlled long vs short caption training + infer rewrite alignment.

Its results speak to caption quality, length/density, diversity, or train-infer text matching.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 24. Generating an Image From 1,000 Words (FIBO)

- **Link:** [https://arxiv.org/abs/2511.06876](https://arxiv.org/abs/2511.06876)
- **id:** `2511.06876` · **published:** n.d. · **origin:** hand

"Generating an Image From 1,000 Words (FIBO)" (n.d.) is related to the Brack et al. synthetic-caption training design line.

long structured vs short caption ablation under same backbone.

Its results speak to caption quality, length/density, diversity, or train-infer text matching.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 25. Altogether: Image Captioning via Re-aligning Alt-text

- **Link:** [https://arxiv.org/abs/2406.18583](https://arxiv.org/abs/2406.18583)
- **id:** `2406.18583` · **published:** n.d. · **origin:** hand

"Altogether: Image Captioning via Re-aligning Alt-text" (n.d.) is related to the Brack et al. synthetic-caption training design line.

mixing ratio synthetic vs alt-text for T2I vs CLIP.

Its results speak to caption quality, length/density, diversity, or train-infer text matching.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 26. ImageInWords

- **Link:** [https://arxiv.org/abs/2406.09411](https://arxiv.org/abs/2406.09411)
- **id:** `2406.09411` · **published:** n.d. · **origin:** hand

"ImageInWords" (n.d.) is related to the Brack et al. synthetic-caption training design line.

It studies captioning, recaptioning, or training-data composition for text-to-image models.

Its results speak to caption quality, length/density, diversity, or train-infer text matching.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 27. Lens: Rethinking Training Efficiency for Foundational Text-to-Image Models

- **Link:** [https://arxiv.org/abs/2605.21573](https://arxiv.org/abs/2605.21573)
- **id:** `2605.21573` · **published:** 2026-05-20 · **origin:** arxiv_search

"Lens: Rethinking Training Efficiency for Foundational Text-to-Image Models" (2026) is related to the Brack et al. synthetic-caption training design line.

We introduce Lens, a 3.8B-parameter T2I model that achieves performance competitive with, and in several cases surpassing, state-of-the-art models with more than 6B parameters across various benchmarks, while requiring significantly less training compute.

For example, Lens requires only about 19.3% of the training compute used by Z-Image.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 28. PixArt-$α$: Fast Training of Diffusion Transformer for Photorealistic Text-to-Image Synthesis

- **Link:** [https://arxiv.org/abs/2310.00426](https://arxiv.org/abs/2310.00426)
- **id:** `2310.00426` · **published:** 2023-09-30 · **origin:** arxiv_search

"PixArt-$α$: Fast Training of Diffusion Transformer for Photorealistic Text-to-Image Synthesis" (2023) is related to the Brack et al. synthetic-caption training design line.

The most advanced text-to-image (T2I) models require significant training costs (e.g., millions of GPU hours), seriously hindering the fundamental innovation for the AIGC community while increasing CO2 emissions.

This paper introduces PIXART-$α$, a Transformer-based T2I diffusion model whose image generation quality is competitive with state-of-the-art image generators (e.g., Imagen, SDXL, and even Midjourney), reaching near-commercial application standards.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 29. MONET: A Massive, Open, Non-redundant and Enriched Text-to-image dataset

- **Link:** [https://arxiv.org/abs/2605.21272](https://arxiv.org/abs/2605.21272)
- **id:** `2605.21272` · **published:** 2026-05-20 · **origin:** arxiv_search

"MONET: A Massive, Open, Non-redundant and Enriched Text-to-image dataset" (2026) is related to the Brack et al. synthetic-caption training design line.

Training large text-to-image models requires high-quality, curated datasets with diverse content and detailed captions.

Yet the cost and complexity of collecting, filtering, deduplicating, and re-captioning such corpora at scale hinders open and reproducible research in the field.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 30. ShareGPT4Video: Improving Video Understanding and Generation with Better Captions

- **Link:** [https://arxiv.org/abs/2406.04325](https://arxiv.org/abs/2406.04325)
- **id:** `2406.04325` · **published:** 2024-06-06 · **origin:** arxiv_search

"ShareGPT4Video: Improving Video Understanding and Generation with Better Captions" (2024) is related to the Brack et al. synthetic-caption training design line.

We present the ShareGPT4Video series, aiming to facilitate the video understanding of large video-language models (LVLMs) and the video generation of text-to-video models (T2VMs) via dense and precise captions.

The series comprises: 1) ShareGPT4Video, 40K GPT4V annotated dense captions of videos with various lengths and sources, developed through carefully designed data filtering and annotating strategy.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 31. MobileCLIP2: Improving Multi-Modal Reinforced Training

- **Link:** [https://arxiv.org/abs/2508.20691](https://arxiv.org/abs/2508.20691)
- **id:** `2508.20691` · **published:** 2025-08-28 · **origin:** arxiv_search

"MobileCLIP2: Improving Multi-Modal Reinforced Training" (2025) is related to the Brack et al. synthetic-caption training design line.

Foundation image-text models such as CLIP with zero-shot capabilities enable a wide array of applications.

MobileCLIP is a recent family of image-text models at 3-15ms latency and 50-150M parameters with state-of-the-art zero-shot accuracy.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 32. ITIScore: An Image-to-Text-to-Image Rating Framework for the Image Captioning Ability of MLLMs

- **Link:** [https://arxiv.org/abs/2604.03765](https://arxiv.org/abs/2604.03765)
- **id:** `2604.03765` · **published:** 2026-04-04 · **origin:** arxiv_search

"ITIScore: An Image-to-Text-to-Image Rating Framework for the Image Captioning Ability of MLLMs" (2026) is related to the Brack et al. synthetic-caption training design line.

Recent advances in multimodal large language models (MLLMs) have greatly improved image understanding and captioning capabilities.

However, existing image captioning benchmarks typically suffer from limited diversity in caption length, the absence of recent advanced MLLMs, and insufficient human annotations, which potentially introduces bias and limits the ability to comprehensively assess the performance of modern MLLMs.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 33. PromptEcho: Annotation-Free Reward from Vision-Language Models for Text-to-Image Reinforcement Learning

- **Link:** [https://arxiv.org/abs/2604.12652](https://arxiv.org/abs/2604.12652)
- **id:** `2604.12652` · **published:** 2026-04-14 · **origin:** arxiv_search

"PromptEcho: Annotation-Free Reward from Vision-Language Models for Text-to-Image Reinforcement Learning" (2026) is related to the Brack et al. synthetic-caption training design line.

Reinforcement learning (RL) can improve the prompt following capability of text-to-image (T2I) models, yet obtaining high-quality reward signals remains challenging: CLIP Score is too coarse-grained, while VLM-based reward models (e.g., RewardDance) require costly human-annotated preference data and additional fine-...

We propose PromptEcho, a reward construction method that requires \emph{no} annotation and \emph{no} reward model training.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 34. MM1.5: Methods, Analysis & Insights from Multimodal LLM Fine-tuning

- **Link:** [https://arxiv.org/abs/2409.20566](https://arxiv.org/abs/2409.20566)
- **id:** `2409.20566` · **published:** 2024-09-30 · **origin:** arxiv_search

"MM1.5: Methods, Analysis & Insights from Multimodal LLM Fine-tuning" (2024) is related to the Brack et al. synthetic-caption training design line.

We present MM1.5, a new family of multimodal large language models (MLLMs) designed to enhance capabilities in text-rich image understanding, visual referring and grounding, and multi-image reasoning.

Building upon the MM1 architecture, MM1.5 adopts a data-centric approach to model training, systematically exploring the impact of diverse data mixtures across the entire model training lifecycle.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 35. Revisit Large-Scale Image-Caption Data in Pre-training Multimodal Foundation Models

- **Link:** [https://arxiv.org/abs/2410.02740](https://arxiv.org/abs/2410.02740)
- **id:** `2410.02740` · **published:** 2024-10-03 · **origin:** arxiv_search

"Revisit Large-Scale Image-Caption Data in Pre-training Multimodal Foundation Models" (2024) is related to the Brack et al. synthetic-caption training design line.

Recent advancements in multimodal models highlight the value of rewritten captions for improving performance, yet key challenges remain.

For example, while synthetic captions often provide superior quality and image-text alignment, it is not clear whether they can fully replace AltTexts: the role of synthetic captions and their interaction with original web-crawled AltTexts in pre-training is still not well understood.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 36. Randomizing training caption length does not adversely affect text alignment while providing the beneﬁts out-lined in Sec. 4.2

- **Link:** [https://arxiv.org/abs/Randomizing training caption length does not adversely affect text alignment whi](https://arxiv.org/abs/Randomizing training caption length does not adversely affect text alignment whi)
- **id:** `Randomizing training caption length does not adversely affect text alignment whi` · **published:** n.d. · **origin:** s2_ref

"Randomizing training caption length does not adversely affect text alignment while providing the beneﬁts out-lined in Sec. 4.2" (n.d.) is related to the Brack et al. synthetic-caption training design line.

It studies captioning, recaptioning, or training-data composition for text-to-image models.

Its results speak to caption quality, length/density, diversity, or train-infer text matching.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 37. On the Scalability of Diffusion-based Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2404.02883](https://arxiv.org/abs/2404.02883)
- **id:** `2404.02883` · **published:** 2024 · **origin:** s2_ref

"On the Scalability of Diffusion-based Text-to-Image Generation" (2024) is related to the Brack et al. synthetic-caption training design line.

Scaling up model and data size has been quite successful for the evolution of LLMs.

However, the scaling law for the diffusion based text-to-image (T2I) models is not fully explored.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 38. CLIP Is Shortsighted: Paying Attention Beyond the First Sentence

- **Link:** [https://arxiv.org/abs/2602.22419](https://arxiv.org/abs/2602.22419)
- **id:** `2602.22419` · **published:** 2026-02-25 · **origin:** arxiv_search

"CLIP Is Shortsighted: Paying Attention Beyond the First Sentence" (2026) is related to the Brack et al. synthetic-caption training design line.

CLIP models learn transferable multi-modal features via image-text contrastive learning on internet-scale data.

They are widely used in zero-shot classification, multi-modal retrieval, text-to-image diffusion, and as image encoders in large vision-language models.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 39. IIITD-20K: Dense captioning for Text-Image ReID

- **Link:** [https://arxiv.org/abs/2305.04497](https://arxiv.org/abs/2305.04497)
- **id:** `2305.04497` · **published:** 2023-05-08 · **origin:** arxiv_search

"IIITD-20K: Dense captioning for Text-Image ReID" (2023) is related to the Brack et al. synthetic-caption training design line.

Text-to-Image (T2I) ReID has attracted a lot of attention in the recent past.

CUHK-PEDES, RSTPReid and ICFG-PEDES are the three available benchmarks to evaluate T2I ReID methods.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 40. RealignDiff: Boosting Text-to-Image Diffusion Model with Coarse-to-fine Semantic Re-alignment

- **Link:** [https://arxiv.org/abs/2305.19599](https://arxiv.org/abs/2305.19599)
- **id:** `2305.19599` · **published:** 2023-05-31 · **origin:** arxiv_search

"RealignDiff: Boosting Text-to-Image Diffusion Model with Coarse-to-fine Semantic Re-alignment" (2023) is related to the Brack et al. synthetic-caption training design line.

Recent advances in text-to-image diffusion models have achieved remarkable success in generating high-quality, realistic images from textual descriptions.

However, these approaches have faced challenges in precisely aligning the generated visual content with the textual concepts described in the prompts.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 41. A Whisper transformer for audio captioning trained with synthetic captions and transfer learning

- **Link:** [https://arxiv.org/abs/2305.09690](https://arxiv.org/abs/2305.09690)
- **id:** `2305.09690` · **published:** 2023-05-15 · **origin:** arxiv_search

"A Whisper transformer for audio captioning trained with synthetic captions and transfer learning" (2023) is related to the Brack et al. synthetic-caption training design line.

The field of audio captioning has seen significant advancements in recent years, driven by the availability of large-scale audio datasets and advancements in deep learning techniques.

In this technical report, we present our approach to audio captioning, focusing on the use of a pretrained speech-to-text Whisper model and pretraining on synthetic captions.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 42. Harnessing Caption Detailness for Data-Efficient Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2505.15172](https://arxiv.org/abs/2505.15172)
- **id:** `2505.15172` · **published:** 2025-05-21 · **origin:** arxiv_search

"Harnessing Caption Detailness for Data-Efficient Text-to-Image Generation" (2025) is related to the Brack et al. synthetic-caption training design line.

Training text-to-image (T2I) models with detailed captions can significantly improve their generation quality.

Existing methods often rely on simplistic metrics like caption length to represent the detailness of the caption in the T2I training set.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 43. Explainable, Multi-modal Wound Infection Classification from Images Augmented with Generated Captions

- **Link:** [https://arxiv.org/abs/2502.20277](https://arxiv.org/abs/2502.20277)
- **id:** `2502.20277` · **published:** 2025-02-27 · **origin:** arxiv_search

"Explainable, Multi-modal Wound Infection Classification from Images Augmented with Generated Captions" (2025) is related to the Brack et al. synthetic-caption training design line.

Infections in Diabetic Foot Ulcers (DFUs) can cause severe complications, including tissue death and limb amputation, highlighting the need for accurate, timely diagnosis.

Previous machine learning methods have focused on identifying infections by analyzing wound images alone, without utilizing additional metadata such as medical notes.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 44. RubiCap: Rubric-Guided Reinforcement Learning for Dense Image Captioning

- **Link:** [https://arxiv.org/abs/2603.09160](https://arxiv.org/abs/2603.09160)
- **id:** `2603.09160` · **published:** 2026-03-10 · **origin:** arxiv_extra

"RubiCap: Rubric-Guided Reinforcement Learning for Dense Image Captioning" (2026) is related to the Brack et al. synthetic-caption training design line.

Dense image captioning is critical for cross-modal alignment in vision-language pretraining and text-to-image generation, but scaling expert-quality annotations is prohibitively expensive.

While synthetic captioning via strong vision-language models (VLMs) is a practical alternative, supervised distillation often yields limited output diversity and weak generalization.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 45. Integrating Visuospatial, Linguistic and Commonsense Structure into Story Visualization

- **Link:** [https://arxiv.org/abs/2110.10834](https://arxiv.org/abs/2110.10834)
- **id:** `2110.10834` · **published:** 2021-10-21 · **origin:** arxiv_search

"Integrating Visuospatial, Linguistic and Commonsense Structure into Story Visualization" (2021) is related to the Brack et al. synthetic-caption training design line.

While much research has been done in text-to-image synthesis, little work has been done to explore the usage of linguistic structure of the input text.

Such information is even more important for story visualization since its inputs have an explicit narrative structure that needs to be translated into an image sequence (or visual story).

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 46. Cytoarchitecture in Words: Weakly Supervised Vision-Language Modeling for Human Brain Microscopy

- **Link:** [https://arxiv.org/abs/2602.23088](https://arxiv.org/abs/2602.23088)
- **id:** `2602.23088` · **published:** 2026-02-26 · **origin:** arxiv_search

"Cytoarchitecture in Words: Weakly Supervised Vision-Language Modeling for Human Brain Microscopy" (2026) is related to the Brack et al. synthetic-caption training design line.

Foundation models increasingly offer potential to support interactive, agentic workflows that assist researchers during analysis and interpretation of image data.

Such workflows often require coupling vision to language to provide a natural-language interface.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 47. EFSA: Episodic Few-Shot Adaptation for Text-to-Image Retrieval

- **Link:** [https://arxiv.org/abs/2412.00139](https://arxiv.org/abs/2412.00139)
- **id:** `2412.00139` · **published:** 2024-11-28 · **origin:** arxiv_extra

"EFSA: Episodic Few-Shot Adaptation for Text-to-Image Retrieval" (2024) is related to the Brack et al. synthetic-caption training design line.

Text-to-image retrieval is a critical task for managing diverse visual content, but common benchmarks for the task rely on small, single-domain datasets that fail to capture real-world complexity.

Pre-trained vision-language models tend to perform well with easy negatives but struggle with hard negatives--visually similar yet incorrect images--especially in open-domain scenarios.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 48. Improving Text Generation on Images with Synthetic Captions

- **Link:** [https://arxiv.org/abs/2406.00505](https://arxiv.org/abs/2406.00505)
- **id:** `2406.00505` · **published:** 2024-06-01 · **origin:** arxiv_extra

"Improving Text Generation on Images with Synthetic Captions" (2024) is related to the Brack et al. synthetic-caption training design line.

The recent emergence of latent diffusion models such as SDXL and SD 1.5 has shown significant capability in generating highly detailed and realistic images.

Despite their remarkable ability to produce images, generating accurate text within images still remains a challenging task.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 49. Image Captioning with Multi-Context Synthetic Data

- **Link:** [https://arxiv.org/abs/2305.18072](https://arxiv.org/abs/2305.18072)
- **id:** `2305.18072` · **published:** 2023-05-29 · **origin:** arxiv_search

"Image Captioning with Multi-Context Synthetic Data" (2023) is related to the Brack et al. synthetic-caption training design line.

Image captioning requires numerous annotated image-text pairs, resulting in substantial annotation costs.

diffusion models and large language models) have excelled in producing high-quality images and text.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 50. Dense Text-to-Image Generation with Attention Modulation

- **Link:** [https://arxiv.org/abs/2308.12964](https://arxiv.org/abs/2308.12964)
- **id:** `2308.12964` · **published:** 2023-08-24 · **origin:** arxiv_search

"Dense Text-to-Image Generation with Attention Modulation" (2023) is related to the Brack et al. synthetic-caption training design line.

Existing text-to-image diffusion models struggle to synthesize realistic images given dense captions, where each text prompt provides a detailed description for a specific image region.

To address this, we propose DenseDiffusion, a training-free method that adapts a pre-trained text-to-image model to handle such dense captions while offering control over the scene layout.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 51. CapsFusion: Rethinking Image-Text Data at Scale

- **Link:** [https://arxiv.org/abs/2310.20550](https://arxiv.org/abs/2310.20550)
- **id:** `2310.20550` · **published:** 2023-10-31 · **origin:** arxiv_search

"CapsFusion: Rethinking Image-Text Data at Scale" (2023) is related to the Brack et al. synthetic-caption training design line.

Large multimodal models demonstrate remarkable generalist ability to perform diverse multimodal tasks in a zero-shot manner.

Large-scale web-based image-text pairs contribute fundamentally to this success, but suffer from excessive noise.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 52. Improving Multimodal Datasets with Image Captioning

- **Link:** [https://arxiv.org/abs/2307.10350](https://arxiv.org/abs/2307.10350)
- **id:** `2307.10350` · **published:** 2023-07-19 · **origin:** arxiv_search

"Improving Multimodal Datasets with Image Captioning" (2023) is related to the Brack et al. synthetic-caption training design line.

Massive web datasets play a key role in the success of large vision-language models like CLIP and Flamingo.

However, the raw web data is noisy, and existing filtering methods to reduce noise often come at the expense of data diversity.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 53. ShareGPT4V: Improving Large Multi-Modal Models with Better Captions

- **Link:** [https://arxiv.org/abs/2311.12793](https://arxiv.org/abs/2311.12793)
- **id:** `2311.12793` · **published:** 2023-11-21 · **origin:** arxiv_search

"ShareGPT4V: Improving Large Multi-Modal Models with Better Captions" (2023) is related to the Brack et al. synthetic-caption training design line.

In the realm of large multi-modal models (LMMs), efficient modality alignment is crucial yet often constrained by the scarcity of high-quality image-text data.

To address this bottleneck, we introduce the ShareGPT4V dataset, a pioneering large-scale resource featuring 1.2 million highly descriptive captions, which surpasses existing datasets in diversity and information content, covering world knowledge, object properties, spatial relationships, and aesthetic evaluations.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 54. Synth$^2$: Boosting Visual-Language Models with Synthetic Captions and Image Embeddings

- **Link:** [https://arxiv.org/abs/2403.07750](https://arxiv.org/abs/2403.07750)
- **id:** `2403.07750` · **published:** 2024-03-12 · **origin:** arxiv_extra

"Synth$^2$: Boosting Visual-Language Models with Synthetic Captions and Image Embeddings" (2024) is related to the Brack et al. synthetic-caption training design line.

The creation of high-quality human-labeled image-caption datasets presents a significant bottleneck in the development of Visual-Language Models (VLMs).

In this work, we investigate an approach that leverages the strengths of Large Language Models (LLMs) and image generation models to create synthetic image-text pairs for efficient and effective VLM training.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 55. Omni-Dish: Photorealistic and Faithful Image Generation and Editing for Arbitrary Chinese Dishes

- **Link:** [https://arxiv.org/abs/2504.09948](https://arxiv.org/abs/2504.09948)
- **id:** `2504.09948` · **published:** 2025-04-14 · **origin:** arxiv_extra

"Omni-Dish: Photorealistic and Faithful Image Generation and Editing for Arbitrary Chinese Dishes" (2025) is related to the Brack et al. synthetic-caption training design line.

Dish images play a crucial role in the digital era, with the demand for culturally distinctive dish images continuously increasing due to the digitization of the food industry and e-commerce.

In general cases, existing text-to-image generation models excel in producing high-quality images; however, they struggle to capture diverse characteristics and faithful details of specific domains, particularly Chinese dishes.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 56. CapOnImage: Context-driven Dense-Captioning on Image

- **Link:** [https://arxiv.org/abs/2204.12974](https://arxiv.org/abs/2204.12974)
- **id:** `2204.12974` · **published:** 2022-04-27 · **origin:** arxiv_search

"CapOnImage: Context-driven Dense-Captioning on Image" (2022) is related to the Brack et al. synthetic-caption training design line.

Existing image captioning systems are dedicated to generating narrative captions for images, which are spatially detached from the image in presentation.

However, texts can also be used as decorations on the image to highlight the key points and increase the attractiveness of images.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 57. One Patch to Caption Them All: A Unified Zero-Shot Captioning Framework

- **Link:** [https://arxiv.org/abs/2510.02898](https://arxiv.org/abs/2510.02898)
- **id:** `2510.02898` · **published:** 2025-10-03 · **origin:** arxiv_search

"One Patch to Caption Them All: A Unified Zero-Shot Captioning Framework" (2025) is related to the Brack et al. synthetic-caption training design line.

Zero-shot captioners are recently proposed models that utilize common-space vision-language representations to caption images without relying on paired image-text data.

To caption an image, they proceed by textually decoding a text-aligned image feature, but they limit their scope to global representations and whole-image captions.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 58. Auditing and instructing text-to-image generation models on fairness

- **Link:** [https://www.semanticscholar.org/paper/f240825e618621eff36510d916b23f6c06af680d](https://www.semanticscholar.org/paper/f240825e618621eff36510d916b23f6c06af680d)
- **id:** `Auditing and instructing text-to-image generation models on fairness` · **published:** 2024 · **origin:** s2_ref

"Auditing and instructing text-to-image generation models on fairness" (2024) is related to the Brack et al. synthetic-caption training design line.

Generative AI models have recently achieved astonishing results in quality and are consequently employed in a fast-growing number of applications.

However, since they are highly data-driven, relying on billion-sized datasets randomly scraped from the internet, they also suffer from degenerated and biased human behavior, as we demonstrate.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 59. Mitigate Replication and Copying in Diffusion Models with Generalized Caption and Dual Fusion Enhancement

- **Link:** [https://arxiv.org/abs/2309.07254](https://arxiv.org/abs/2309.07254)
- **id:** `2309.07254` · **published:** 2023-09-13 · **origin:** arxiv_search

"Mitigate Replication and Copying in Diffusion Models with Generalized Caption and Dual Fusion Enhancement" (2023) is related to the Brack et al. synthetic-caption training design line.

While diffusion models demonstrate a remarkable capability for generating high-quality images, their tendency to `replicate' training data raises privacy concerns.

Although recent research suggests that this replication may stem from the insufficient generalization of training data captions and duplication of training images, effective mitigation strategies remain elusive.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 60. DLIP: Distilling Language-Image Pre-training

- **Link:** [https://arxiv.org/abs/2308.12956](https://arxiv.org/abs/2308.12956)
- **id:** `2308.12956` · **published:** 2023-08-24 · **origin:** arxiv_search

"DLIP: Distilling Language-Image Pre-training" (2023) is related to the Brack et al. synthetic-caption training design line.

Vision-Language Pre-training (VLP) shows remarkable progress with the assistance of extremely heavy parameters, which challenges deployment in real applications.

Knowledge distillation is well recognized as the essential procedure in model compression.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 61. Unified Vision-Language Modeling via Concept Space Alignment

- **Link:** [https://arxiv.org/abs/2603.01096](https://arxiv.org/abs/2603.01096)
- **id:** `2603.01096` · **published:** 2026-03-01 · **origin:** arxiv_search

"Unified Vision-Language Modeling via Concept Space Alignment" (2026) is related to the Brack et al. synthetic-caption training design line.

We introduce V-SONAR, a vision-language embedding space extended from the text-only embedding space SONAR (Omnilingual Embeddings Team et al., 2026), which supports 1500 text languages and 177 speech languages.

To construct V-SONAR, we propose a post-hoc alignment pipeline that maps the representations of an existing vision encoder into the SONAR space.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 62. Diffusion Based Augmentation for Captioning and Retrieval in Cultural Heritage

- **Link:** [https://arxiv.org/abs/2308.07151](https://arxiv.org/abs/2308.07151)
- **id:** `2308.07151` · **published:** 2023-08-14 · **origin:** arxiv_search

"Diffusion Based Augmentation for Captioning and Retrieval in Cultural Heritage" (2023) is related to the Brack et al. synthetic-caption training design line.

Cultural heritage applications and advanced machine learning models are creating a fruitful synergy to provide effective and accessible ways of interacting with artworks.

Smart audio-guides, personalized art-related content and gamification approaches are just a few examples of how technology can be exploited to provide additional value to artists or exhibitions.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 63. Controlling Vision-Language Models for Multi-Task Image Restoration

- **Link:** [https://arxiv.org/abs/2310.01018](https://arxiv.org/abs/2310.01018)
- **id:** `2310.01018` · **published:** 2023-10-02 · **origin:** arxiv_search

"Controlling Vision-Language Models for Multi-Task Image Restoration" (2023) is related to the Brack et al. synthetic-caption training design line.

Vision-language models such as CLIP have shown great impact on diverse downstream tasks for zero-shot or label-free predictions.

However, when it comes to low-level vision such as image restoration their performance deteriorates dramatically due to corrupted inputs.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 64. Factorized-Dreamer: Training A High-Quality Video Generator with Limited and Low-Quality Data

- **Link:** [https://arxiv.org/abs/2408.10119](https://arxiv.org/abs/2408.10119)
- **id:** `2408.10119` · **published:** 2024-08-19 · **origin:** arxiv_extra

"Factorized-Dreamer: Training A High-Quality Video Generator with Limited and Low-Quality Data" (2024) is related to the Brack et al. synthetic-caption training design line.

Text-to-video (T2V) generation has gained significant attention due to its wide applications to video generation, editing, enhancement and translation, \etc.

However, high-quality (HQ) video synthesis is extremely challenging because of the diverse and complex motions existed in real world.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 65. Keep the General, Inject the Specific: Structured Dialogue Fine-Tuning for Knowledge Injection without Catastrophic Forgetting

- **Link:** [https://arxiv.org/abs/2505.00029](https://arxiv.org/abs/2505.00029)
- **id:** `2505.00029` · **published:** 2025-04-27 · **origin:** arxiv_search

"Keep the General, Inject the Specific: Structured Dialogue Fine-Tuning for Knowledge Injection without Catastrophic Forgetting" (2025) is related to the Brack et al. synthetic-caption training design line.

Large Vision Language Models have demonstrated impressive versatile capabilities through extensive multimodal pre-training, but face significant limitations when incorporating specialized knowledge domains beyond their training distribution.

These models struggle with a fundamental dilemma: direct adaptation approaches that inject domain-specific knowledge often trigger catastrophic forgetting of foundational visual-linguistic abilities.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 66. Talk-to-Resolve: Combining scene understanding and spatial dialogue to resolve granular task ambiguity for a collocated robot

- **Link:** [https://arxiv.org/abs/2111.11099](https://arxiv.org/abs/2111.11099)
- **id:** `2111.11099` · **published:** 2021-11-22 · **origin:** arxiv_search

"Talk-to-Resolve: Combining scene understanding and spatial dialogue to resolve granular task ambiguity for a collocated robot" (2021) is related to the Brack et al. synthetic-caption training design line.

The utility of collocating robots largely depends on the easy and intuitive interaction mechanism with the human.

If a robot accepts task instruction in natural language, first, it has to understand the user's intention by decoding the instruction.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 67. Training on long, dense captions results in better prompt following of the downstream text-to-image model

- **Link:** [https://arxiv.org/abs/Training on long, dense captions results in better prompt following of the downs](https://arxiv.org/abs/Training on long, dense captions results in better prompt following of the downs)
- **id:** `Training on long, dense captions results in better prompt following of the downs` · **published:** n.d. · **origin:** s2_ref

"Training on long, dense captions results in better prompt following of the downstream text-to-image model" (n.d.) is related to the Brack et al. synthetic-caption training design line.

It studies captioning, recaptioning, or training-data composition for text-to-image models.

Its results speak to caption quality, length/density, diversity, or train-infer text matching.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


#### 68. Safe Latent Diffusion: Mitigating Inappropriate Degeneration in Diffusion Models

- **Link:** [https://arxiv.org/abs/2211.05105](https://arxiv.org/abs/2211.05105)
- **id:** `2211.05105` · **published:** 2022 · **origin:** s2_ref

"Safe Latent Diffusion: Mitigating Inappropriate Degeneration in Diffusion Models" (2022) is related to the Brack et al. synthetic-caption training design line.

Text-conditioned image generation models have recently achieved astonishing results in image quality and text alignment and are consequently employed in a fast-growing number of applications.

Since they are highly data-driven, relying on billion-sized datasets randomly scraped from the internet, they also suffer, as we demonstrate, from degenerated and biased human behavior.

Closest in spirit: ablates how long/dense/variable captions change T2I trade-offs.


### Bucket: inference_distribution_match

#### 69. TIPO

- **Link:** [https://arxiv.org/abs/2411.08127](https://arxiv.org/abs/2411.08127)
- **id:** `2411.08127` · **published:** n.d. · **origin:** hand

"TIPO" (n.d.) is related to the Brack et al. synthetic-caption training design line.

rewriter should match training caption distribution.

Its results speak to caption quality, length/density, diversity, or train-infer text matching.

Complementary: if train captions change, inference prompts may need rewriting to match.


#### 70. PromptEnhancer

- **Link:** [https://arxiv.org/abs/2509.04545](https://arxiv.org/abs/2509.04545)
- **id:** `2509.04545` · **published:** n.d. · **origin:** hand

"PromptEnhancer" (n.d.) is related to the Brack et al. synthetic-caption training design line.

It studies captioning, recaptioning, or training-data composition for text-to-image models.

Its results speak to caption quality, length/density, diversity, or train-infer text matching.

Complementary: if train captions change, inference prompts may need rewriting to match.


### Bucket: caption_bias

#### 71. Analyzing CLIP's Performance Limitations in Multi-Object Scenarios: A Controlled High-Resolution Study

- **Link:** [https://arxiv.org/abs/2502.19828](https://arxiv.org/abs/2502.19828)
- **id:** `2502.19828` · **published:** 2025-02-27 · **origin:** arxiv_search

"Analyzing CLIP's Performance Limitations in Multi-Object Scenarios: A Controlled High-Resolution Study" (2025) is related to the Brack et al. synthetic-caption training design line.

Contrastive Language-Image Pre-training (CLIP) models have demonstrated remarkable performance in zero-shot classification tasks, yet their efficacy in handling complex multi-object scenarios remains challenging.

This study presents a comprehensive analysis of CLIP's performance limitations in multi-object contexts through controlled experiments.

Aligns with Brack H3: caption term distributions shape model bias.


#### 72. The Bias Amplification Paradox in Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2308.00755](https://arxiv.org/abs/2308.00755)
- **id:** `2308.00755` · **published:** 2023-08-01 · **origin:** arxiv_search

"The Bias Amplification Paradox in Text-to-Image Generation" (2023) is related to the Brack et al. synthetic-caption training design line.

Bias amplification is a phenomenon in which models exacerbate biases or stereotypes present in the training data.

In this paper, we study bias amplification in the text-to-image domain using Stable Diffusion by comparing gender ratios in training vs.

Aligns with Brack H3: caption term distributions shape model bias.


### Bucket: datasets_benchmarks

#### 73. DCI: A Picture is Worth More Than 77 Text Tokens

- **Link:** [https://arxiv.org/abs/2312.08578](https://arxiv.org/abs/2312.08578)
- **id:** `2312.08578` · **published:** n.d. · **origin:** hand

"DCI: A Picture is Worth More Than 77 Text Tokens" (n.d.) is related to the Brack et al. synthetic-caption training design line.

dense human captions beyond 77; sDCI summaries.

Its results speak to caption quality, length/density, diversity, or train-infer text matching.

Provides data/eval substrate for caption-design experiments.


#### 74. DOCCI

- **Link:** [https://arxiv.org/abs/2310.01400](https://arxiv.org/abs/2310.01400)
- **id:** `2310.01400` · **published:** n.d. · **origin:** hand

"DOCCI" (n.d.) is related to the Brack et al. synthetic-caption training design line.

human detailed descriptions for T2I-relevant evaluation.

Its results speak to caption quality, length/density, diversity, or train-infer text matching.

Provides data/eval substrate for caption-design experiments.


#### 75. CoVR-2: Automatic Data Construction for Composed Video Retrieval

- **Link:** [https://arxiv.org/abs/2308.14746](https://arxiv.org/abs/2308.14746)
- **id:** `2308.14746` · **published:** 2023-08-28 · **origin:** arxiv_search

"CoVR-2: Automatic Data Construction for Composed Video Retrieval" (2023) is related to the Brack et al. synthetic-caption training design line.

Composed Image Retrieval (CoIR) has recently gained popularity as a task that considers both text and image queries together, to search for relevant images in a database.

Most CoIR approaches require manually annotated datasets, comprising image-text-image triplets, where the text describes a modification from the query image to the target image.

Provides data/eval substrate for caption-design experiments.


#### 76. VIVECaption: A Split Approach to Caption Quality Improvement

- **Link:** [https://arxiv.org/abs/2603.07401](https://arxiv.org/abs/2603.07401)
- **id:** `2603.07401` · **published:** 2026-03-08 · **origin:** arxiv_extra

"VIVECaption: A Split Approach to Caption Quality Improvement" (2026) is related to the Brack et al. synthetic-caption training design line.

Caption quality has emerged as a critical bottleneck in training high-quality text-to-image (T2I) and text-to-video (T2V) generative models.

While visual language models (VLMs) are commonly deployed to generate captions from visual data, they suffer from hallucinations, poor compositional reasoning, and limited fine-grained understanding, resulting in misaligned image-caption pairs that degrade downstream model performance.

Provides data/eval substrate for caption-design experiments.


#### 77. The Role of Data Curation in Image Captioning

- **Link:** [https://arxiv.org/abs/2305.03610](https://arxiv.org/abs/2305.03610)
- **id:** `2305.03610` · **published:** 2023-05-05 · **origin:** arxiv_search

"The Role of Data Curation in Image Captioning" (2023) is related to the Brack et al. synthetic-caption training design line.

Image captioning models are typically trained by treating all samples equally, neglecting to account for mismatched or otherwise difficult data points.

In contrast, recent work has shown the effectiveness of training models by scheduling the data using curriculum learning strategies.

Provides data/eval substrate for caption-design experiments.


#### 78. NeIn: Telling What You Don't Want

- **Link:** [https://arxiv.org/abs/2409.06481](https://arxiv.org/abs/2409.06481)
- **id:** `2409.06481` · **published:** 2024-09-09 · **origin:** arxiv_search

"NeIn: Telling What You Don't Want" (2024) is related to the Brack et al. synthetic-caption training design line.

Negation is a fundamental linguistic concept used by humans to convey information that they do not desire.

Despite this, minimal research has focused on negation within text-guided image editing.

Provides data/eval substrate for caption-design experiments.


#### 79. View Selection for 3D Captioning via Diffusion Ranking

- **Link:** [https://arxiv.org/abs/2404.07984](https://arxiv.org/abs/2404.07984)
- **id:** `2404.07984` · **published:** 2024-04-11 · **origin:** arxiv_extra

"View Selection for 3D Captioning via Diffusion Ranking" (2024) is related to the Brack et al. synthetic-caption training design line.

Scalable annotation approaches are crucial for constructing extensive 3D-text datasets, facilitating a broader range of applications.

However, existing methods sometimes lead to the generation of hallucinated captions, compromising caption quality.

Provides data/eval substrate for caption-design experiments.


#### 80. Cycle Consistency as Reward: Learning Image-Text Alignment without Human Preferences

- **Link:** [https://arxiv.org/abs/2506.02095](https://arxiv.org/abs/2506.02095)
- **id:** `2506.02095` · **published:** 2025-06-02 · **origin:** arxiv_search

"Cycle Consistency as Reward: Learning Image-Text Alignment without Human Preferences" (2025) is related to the Brack et al. synthetic-caption training design line.

Measuring alignment between language and vision is a fundamental challenge, especially as multimodal data becomes increasingly detailed and complex.

Existing methods often rely on collecting human or AI preferences, which can be costly and time-intensive.

Provides data/eval substrate for caption-design experiments.


#### 81. FreeSeg-Diff: Training-Free Open-Vocabulary Segmentation with Diffusion Models

- **Link:** [https://arxiv.org/abs/2403.20105](https://arxiv.org/abs/2403.20105)
- **id:** `2403.20105` · **published:** 2024-03-29 · **origin:** arxiv_search

"FreeSeg-Diff: Training-Free Open-Vocabulary Segmentation with Diffusion Models" (2024) is related to the Brack et al. synthetic-caption training design line.

Foundation models have exhibited unprecedented capabilities in tackling many domains and tasks.

Models such as CLIP are currently widely used to bridge cross-modal representations, and text-to-image diffusion models are arguably the leading models in terms of realistic image generation.

Provides data/eval substrate for caption-design experiments.


#### 82. SynthVLM: Towards High-Quality and Efficient Synthesis of Image-Caption Datasets for Vision-Language Models

- **Link:** [https://arxiv.org/abs/2407.20756](https://arxiv.org/abs/2407.20756)
- **id:** `2407.20756` · **published:** 2024-07-30 · **origin:** arxiv_search

"SynthVLM: Towards High-Quality and Efficient Synthesis of Image-Caption Datasets for Vision-Language Models" (2024) is related to the Brack et al. synthetic-caption training design line.

Vision-Language Models (VLMs) have recently emerged, demonstrating remarkable vision-understanding capabilities.

However, training these models requires large-scale datasets, which brings challenges related to efficiency, effectiveness, and quality of web data.

Provides data/eval substrate for caption-design experiments.


#### 83. FodFoM: Fake Outlier Data by Foundation Models Creates Stronger Visual Out-of-Distribution Detector

- **Link:** [https://arxiv.org/abs/2412.05293](https://arxiv.org/abs/2412.05293)
- **id:** `2412.05293` · **published:** 2024-11-22 · **origin:** arxiv_search

"FodFoM: Fake Outlier Data by Foundation Models Creates Stronger Visual Out-of-Distribution Detector" (2024) is related to the Brack et al. synthetic-caption training design line.

Out-of-Distribution (OOD) detection is crucial when deploying machine learning models in open-world applications.

The core challenge in OOD detection is mitigating the model's overconfidence on OOD data.

Provides data/eval substrate for caption-design experiments.


#### 84. Pick-a-Pic: An Open Dataset of User Preferences for Text-to-Image Generation

- **Link:** [https://arxiv.org/abs/2305.01569](https://arxiv.org/abs/2305.01569)
- **id:** `2305.01569` · **published:** 2023 · **origin:** s2_ref

"Pick-a-Pic: An Open Dataset of User Preferences for Text-to-Image Generation" (2023) is related to the Brack et al. synthetic-caption training design line.

The ability to collect a large dataset of human preferences from text-to-image users is usually limited to companies, making such datasets inaccessible to the public.

To address this issue, we create a web app that enables text-to-image users to generate images and specify their preferences.

Provides data/eval substrate for caption-design experiments.


#### 85. Fine-grained Textual Inversion Network for Zero-Shot Composed Image Retrieval

- **Link:** [https://arxiv.org/abs/2503.19296](https://arxiv.org/abs/2503.19296)
- **id:** `2503.19296` · **published:** 2025-03-25 · **origin:** arxiv_search

"Fine-grained Textual Inversion Network for Zero-Shot Composed Image Retrieval" (2025) is related to the Brack et al. synthetic-caption training design line.

Composed Image Retrieval (CIR) allows users to search target images with a multimodal query, comprising a reference image and a modification text that describes the user's modification demand over the reference image.

Nevertheless, due to the expensive labor cost of training data annotation, recent researchers have shifted to the challenging task of zero-shot CIR (ZS-CIR), which targets fulfilling CIR without annotated triplets.

Provides data/eval substrate for caption-design experiments.


#### 86. Coordinated Robustness Evaluation Framework for Vision-Language Models

- **Link:** [https://arxiv.org/abs/2506.05429](https://arxiv.org/abs/2506.05429)
- **id:** `2506.05429` · **published:** 2025-06-05 · **origin:** arxiv_search

"Coordinated Robustness Evaluation Framework for Vision-Language Models" (2025) is related to the Brack et al. synthetic-caption training design line.

Vision-language models, which integrate computer vision and natural language processing capabilities, have demonstrated significant advancements in tasks such as image captioning and visual question and answering.

However, similar to traditional models, they are susceptible to small perturbations, posing a challenge to their robustness, particularly in deployment scenarios.

Provides data/eval substrate for caption-design experiments.


#### 87. Text-to-Image Generation Via Energy-Based CLIP

- **Link:** [https://arxiv.org/abs/2408.17046](https://arxiv.org/abs/2408.17046)
- **id:** `2408.17046` · **published:** 2024-08-30 · **origin:** arxiv_search

"Text-to-Image Generation Via Energy-Based CLIP" (2024) is related to the Brack et al. synthetic-caption training design line.

Joint Energy Models (JEMs), while drawing significant research attention, have not been successfully scaled to real-world, high-resolution datasets.

We present CLIP-JEM, a novel approach extending JEMs to the multimodal vision-language domain using CLIP, integrating both generative and discriminative objectives.

Provides data/eval substrate for caption-design experiments.


### Bucket: broader_conditioning_data

#### 88. DetailMaster

- **Link:** [https://arxiv.org/abs/2505.16915](https://arxiv.org/abs/2505.16915)
- **id:** `2505.16915` · **published:** n.d. · **origin:** hand

"DetailMaster" (n.d.) is related to the Brack et al. synthetic-caption training design line.

shows dense long training > capacity alone on long prompts.

Its results speak to caption quality, length/density, diversity, or train-infer text matching.

Broader but still informative for training-text design.


#### 89. HunyuanImage 3.0 Technical Report

- **Link:** [https://arxiv.org/abs/2509.23951](https://arxiv.org/abs/2509.23951)
- **id:** `2509.23951` · **published:** n.d. · **origin:** hand

"HunyuanImage 3.0 Technical Report" (n.d.) is related to the Brack et al. synthetic-caption training design line.

compositional caption synthesis with 30-1000 word variability.

Its results speak to caption quality, length/density, diversity, or train-infer text matching.

Broader but still informative for training-text design.


#### 90. PixArt-Sigma

- **Link:** [https://arxiv.org/abs/2403.04692](https://arxiv.org/abs/2403.04692)
- **id:** `2403.04692` · **published:** n.d. · **origin:** hand

"PixArt-Sigma" (n.d.) is related to the Brack et al. synthetic-caption training design line.

raises token length 120->300 because denser captions.

Its results speak to caption quality, length/density, diversity, or train-infer text matching.

Broader but still informative for training-text design.


#### 91. Input-Side Inference-Time Scaling

- **Link:** [https://arxiv.org/abs/2510.12041](https://arxiv.org/abs/2510.12041)
- **id:** `2510.12041` · **published:** n.d. · **origin:** hand

"Input-Side Inference-Time Scaling" (n.d.) is related to the Brack et al. synthetic-caption training design line.

PE closes train/user caption distribution gap.

Its results speak to caption quality, length/density, diversity, or train-infer text matching.

Broader but still informative for training-text design.


#### 92. BLIP-2

- **Link:** [https://arxiv.org/abs/2301.12597](https://arxiv.org/abs/2301.12597)
- **id:** `2301.12597` · **published:** n.d. · **origin:** hand

"BLIP-2" (n.d.) is related to the Brack et al. synthetic-caption training design line.

weak captioner often used in synthetic T2I pipelines; Brack compares VLM strength.

Its results speak to caption quality, length/density, diversity, or train-infer text matching.

Broader but still informative for training-text design.


#### 93. Imagen

- **Link:** [https://arxiv.org/abs/2205.11487](https://arxiv.org/abs/2205.11487)
- **id:** `2205.11487` · **published:** n.d. · **origin:** hand

"Imagen" (n.d.) is related to the Brack et al. synthetic-caption training design line.

LM text encoder / caption quality lineage.

Its results speak to caption quality, length/density, diversity, or train-infer text matching.

Broader but still informative for training-text design.


#### 94. LDM / Stable Diffusion

- **Link:** [https://arxiv.org/abs/2112.10752](https://arxiv.org/abs/2112.10752)
- **id:** `2112.10752` · **published:** n.d. · **origin:** hand

"LDM / Stable Diffusion" (n.d.) is related to the Brack et al. synthetic-caption training design line.

architecture Brack continually pretrains from SDv1.1.

Its results speak to caption quality, length/density, diversity, or train-infer text matching.

Broader but still informative for training-text design.


#### 95. ? skip

- **Link:** [https://arxiv.org/abs/2303.05511](https://arxiv.org/abs/2303.05511)
- **id:** `2303.05511` · **published:** n.d. · **origin:** hand

"? skip" (n.d.) is related to the Brack et al. synthetic-caption training design line.

It studies captioning, recaptioning, or training-data composition for text-to-image models.

Its results speak to caption quality, length/density, diversity, or train-infer text matching.

Broader but still informative for training-text design.


#### 96. LaViDa: A Large Diffusion Language Model for Multimodal Understanding

- **Link:** [https://arxiv.org/abs/2505.16839](https://arxiv.org/abs/2505.16839)
- **id:** `2505.16839` · **published:** 2025-05-22 · **origin:** arxiv_search

"LaViDa: A Large Diffusion Language Model for Multimodal Understanding" (2025) is related to the Brack et al. synthetic-caption training design line.

Modern Vision-Language Models (VLMs) can solve a wide range of tasks requiring visual reasoning.

In real-world scenarios, desirable properties for VLMs include fast inference and controllable generation (e.g., constraining outputs to adhere to a desired format).

Broader but still informative for training-text design.


#### 97. Fast High-Resolution Image Synthesis with Latent Adversarial Diffusion Distillation

- **Link:** [https://arxiv.org/abs/2403.12015](https://arxiv.org/abs/2403.12015)
- **id:** `2403.12015` · **published:** 2024 · **origin:** s2_ref

"Fast High-Resolution Image Synthesis with Latent Adversarial Diffusion Distillation" (2024) is related to the Brack et al. synthetic-caption training design line.

Diffusion models are the main driver of progress in image and video synthesis, but suffer from slow inference speed.

Distillation methods, like the recently introduced adversarial diffusion distillation (ADD) aim to shift the model from many-shot to single-step inference, albeit at the cost of expensive and difficult optimization due to its reliance on a fixed pretrained DINOv2 discriminator.

Broader but still informative for training-text design.


#### 98. GenAI-Bench: Evaluating and Improving Compositional Text-to-Visual Generation

- **Link:** [https://arxiv.org/abs/2406.13743](https://arxiv.org/abs/2406.13743)
- **id:** `2406.13743` · **published:** 2024 · **origin:** s2_ref

"GenAI-Bench: Evaluating and Improving Compositional Text-to-Visual Generation" (2024) is related to the Brack et al. synthetic-caption training design line.

While text-to-visual models now produce photo-realistic images and videos, they struggle with compositional text prompts involving attributes, relationships, and higher-order reasoning such as logic and comparison.

In this work, we conduct an extensive human study on GenAI-Bench to evaluate the performance of leading image and video generation models in various aspects of compositional text-to-visual generation.

Broader but still informative for training-text design.


#### 99. Evaluating and Improving Compositional Text-to-Visual Generation

- **Link:** [https://www.semanticscholar.org/paper/befc322dd67db943e66fff57553056fe78009dff](https://www.semanticscholar.org/paper/befc322dd67db943e66fff57553056fe78009dff)
- **id:** `Evaluating and Improving Compositional Text-to-Visual Generation` · **published:** 2024 · **origin:** s2_ref

"Evaluating and Improving Compositional Text-to-Visual Generation" (2024) is related to the Brack et al. synthetic-caption training design line.

While text-to-visual models now produce photo-realistic images and videos, they struggle with compositional text prompts involving attributes, relationships, and higher-order reasoning such as logic and comparison.

In this work, we conduct an extensive human study on GenAI-Bench to evaluate the performance of leading image and video generation models in various aspects of compositional text-to-visual generation.

Broader but still informative for training-text design.


#### 100. What Makes Linguistic Representations Good Models of High-Level Visual Perception in the Human Brain?

- **Link:** [https://arxiv.org/abs/2607.16214](https://arxiv.org/abs/2607.16214)
- **id:** `2607.16214` · **published:** 2026-05-22 · **origin:** arxiv_search

"What Makes Linguistic Representations Good Models of High-Level Visual Perception in the Human Brain?" (2026) is related to the Brack et al. synthetic-caption training design line.

Image descriptions represented with language models (LMs) predict human brain responses to naturalistic images in high-level visual regions, but the factors driving this predictivity remain unclear.

To investigate this, we systematically studied how images are described and which language models are used to embed those descriptions.

Broader but still informative for training-text design.


---

## What this neighborhood implies for our questions

1. **Is there a sequel as rigorous as Brack?** Not yet as a direct citation child. The real “continuations” are methodological siblings: RECAP, i1, FIBO, DetailMaster, Playground v3’s caption recipe claims.
2. **Key ancestor claim:** DALL·E 3’s “long descriptive captions are better” is true only conditionally; Brack supplies the missing trade-off surface (alignment ↑, aesthetics/diversity/short-prompt behavior ↓) and the remedy (**randomize length/density**).
3. **Two research forks after Brack:**
   - **Train-side variability** (Brack / RECAP / Hunyuan wide-band): make `μ_train` cover short and long.
   - **Infer-side transport** (DALL·E 3 / i1 / TIPO / PE): keep `μ_train` long; map users into it with a rewriter.
4. **If you want another Brack-style paper to read next:** start with **RECAP**, then **i1 Table 5**, then **FIBO long-vs-short**, then **DetailMaster** dense-training vs capacity.
5. **Gap / opportunity:** a modern replication of Brack on a **Qwen-VLM / FLUX-class encoder** with `L≈256–512`, measuring the same aesthetics–alignment–diversity surface under both random-length training and PE default-on — that paper essentially does not exist yet as a public controlled study.

---

## Outlook specific to this research line

The synthetic-caption paradigm is settled as industry default; the open scientific problem is **which caption law to use**. Brack shows the community overfit to “longer is better.” The frontier is moving toward **explicit caption curricula**: mixtures over length/density, persona/style diversity, bias-aware term distributions, and—when products keep users short—**coupled PE policies** that match the chosen train law without reward-hacking verbosity. Expect more papers that look like Brack (controlled caption-only ablations) but on stronger backbones and longer context windows; those will matter more than additional tech reports that only say “we used synthetic captions.”

---

## Machine-readable artifacts

- `research/prompt-length/citation_tree/around_2506_16679.json` — structured tree + similar-100
- `research/prompt-length/citation_tree/2506.16679_enriched.json` — raw S2/OA/bib/author pulls
- `research/prompt-length/citation_tree/2506.16679_tree_raw.json` — initial S2 pull
