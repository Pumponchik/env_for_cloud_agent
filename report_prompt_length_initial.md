# Prompt Length for Diffusion Text-to-Image Models

Research synthesis on **training prompt length**, **inference prompt length**, and **re-prompt/recaption output length**, with author motivations.

## Table of Contents

1. [CLIP 77-token limit](#clip-77-token-limit) — 2021 | If the diffusion backbone uses CLIP, design training and inference prompts to fit ≤77 t...
2. [DALL-E 3 Better Captions](#dall-e-3-better-captions) — 2023 | If using a re-prompt model: train the T2I on long detailed captions and set the rewrite...
3. [DetailMaster](#detailmaster) — 2025 | Raise token capacity AND train on dense/long captions; evaluating only short prompts hi...
4. [FIBO 1000 Words](#fibo-1000-words) — 2025 | If you need fine-grained control, train and infer with long structured captions (~1e3 t...
5. [How to Train your T2I Model](#how-to-train-your-t2i-model) — 2025 | If you will not deploy a rewriter: train with randomized caption lengths (within encode...
6. [Imagen family](#imagen-family) — 2022-2025 | Prefer LM-style encoders (T5/LLM) with hundreds of tokens (Imagen 4: 480) over CLIP 77 ...
7. [LongAlign](#longalign) — 2024 | Segmented CLIP encoding can extend past 77, but train on prompt lengths that cover your...
8. [Padding Tone and Memorization Length Effects](#padding-tone-and-memorization-length-effects) — 2025-2026 | When using pad-to-max CLIP encoders, treat very short prompts carefully (mask pads / av...
9. [PixArt-alpha and PixArt-Sigma](#pixart-alpha-and-pixart-sigma) — 2023-2024 | When training captions get denser, raise the text encoder sequence length accordingly (...
10. [PromptEnhancer and HunyuanImage](#promptenhancer-and-hunyuanimage) — 2025 | Train across a wide caption-length band (tens to ~1000 words) and use a content-focused...
11. [Qwen-Image and FLUX.2 Re-prompt](#qwen-image-and-flux-2-re-prompt) — 2025-2026 | For modern stacks: encoder max ~512, turn prompt extend ON, and set rewriter max_new_to...
12. [RECAP Principled Recaptioning](#recap-principled-recaptioning) — 2023 | Under a 77-token CLIP limit, mix short and long recaptions (~50/50) instead of long-onl...
13. [Recap-DataComp-1B and Dense Caption Datasets](#recap-datacomp-1b-and-dense-caption-datasets) — 2024 | For web-scale recaptioning under mid-size encoders: captioner max_new_tokens≈128 (mean ...
14. [Stable Diffusion 1.x and 2.x](#stable-diffusion-1-x-and-2-x) — 2022 | For CLIP-SD: train with mixed/random caption lengths ≤77 tokens; at inference keep prom...
15. [Stable Diffusion 3 and FLUX.1](#stable-diffusion-3-and-flux-1) — 2024 | Train/serve with T5 sequence length consistently (often 256-512 for FLUX-class); write ...
16. [Stable Diffusion XL](#stable-diffusion-xl) — 2023 | SDXL remains a 77-token system; for long prompts either rewrite into 77 tokens or use l...
17. [TIPO and Input-Side Inference Scaling](#tipo-and-input-side-inference-scaling) — 2024-2025 | Set rewriter output length/style to the backbone's training caption distribution (not m...
18. [i1 Open Recipe](#i1-open-recipe) — 2026 | Train long (≤256 tokens here) and always lengthen short user prompts at inference with ...

---

## Direct answers (cross-paper)

### 1. At what length should the model be trained?

- **CLIP/SD1/SDXL era:** within **77 tokens**; short web alt-text historically ~10–20 tokens (COCO 10.5, CC12M 20.2, DataComp 10.22).
- **Dense-caption CLIP fine-tunes:** still ≤77, but use **short+long mix (RECAP 50/50)** or **random lengths** (How-to-Train, arXiv 2506.16679).
- **T5/PixArt lineage:** raise encoder with caption density — **120 (PixArt-α) → ~300 (PixArt-Σ)**.
- **FLUX-class / i1:** long captions with truncation **~256–512 tokens** (i1: 256; FLUX.1/2 often 512).
- **Extreme structured:** FIBO-scale **~1000 tokens/words** (mean ~1160 tokens).
- **Wide-band randomization:** HunyuanImage 3.0 samples **30–1000 words**.
- **Consensus:** train on captions **at least as dense/long as the prompts you care about at inference**; capacity alone (77→512) without dense data is weaker than dense training (DetailMaster).

### 2. At what length should inference run?

- **Match the training caption length distribution** (i1 Table 5; TIPO; Wan/video reports same principle).
- If users write short prompts but the model was trained long: **rewrite/expand at inference** (DALL·E 3, i1, Qwen `prompt_extend`, FLUX.2 upsampler).
- Diagnostic (i1): GenEval **0.17** (short) → **0.49** (repeat 12×) → **0.73** (LLM rewrite) for a long-caption-trained model.
- Long-prompt benchmarks (~285 tokens, DetailMaster) still stress even FLUX/SD3.5; accuracy falls as length grows past ~250–400 tokens.
- Product limits examples: **Imagen 4 = 480 tokens**; Qwen Image API ~**800–1300**; CLIP path hard **77**.

### 3. Re-prompt / recaption output length (train & infer)

- **Offline recaption (train):** Recap-DataComp `max_new_tokens=128` → mean **49.43** tokens (vs 10.22 alt-text); PixArt/Share-Captioner denser for 120–300 windows; FIBO structured ~1000; Hunyuan 30–1000 words.
- **Online re-prompt (infer):** target the **same distribution as training captions**, not max verbosity (TIPO; PromptEnhancer; FaithRewriter warns about hallucination/reward-hacked length).
- **Concrete modern defaults:** FLUX.2 upsampler `max_new_tokens=512`; Qwen prompt extend default-on toward encoder/API budget (~512–1300).
- **DALL·E 3 pattern:** train on long synthetic captions; at inference always upsample short user prompts (`revised_prompt`).

### 4. Why (motivations repeated across papers)

1. **Train–infer distribution match** (especially length) dominates reported metrics.
2. **Short noisy alt-text underteaches** composition/attributes; dense captions improve alignment.
3. **Encoder capacity is necessary but not sufficient** — dense long training matters more (DetailMaster).
4. **Long-only training makes short user prompts OOD** unless you randomize train lengths or rewrite at infer.
5. **Padding mechanics:** very short prompts fill 77 with EOT pads that can dominate (Padding Tone / memorization <40 tokens).

---

## CLIP 77-token limit

### Identity

- **name**: CLIP 77-token limit
- **year**: 2021
- **organization**: OpenAI
- **model_type**: text encoder foundation
- **paper_or_source**: Learning Transferable Visual Models From Natural Language Supervision (CLIP)
- **arxiv_id**: 2103.00020
- **primary_url**: https://arxiv.org/abs/2103.00020

### Text Encoder Limits

- **text_encoder**: CLIP Transformer text encoder (e.g. ViT-L/14 companion text tower)
- **max_token_length_architecture**: 77 tokens including start-of-text and end-of-text special tokens (75 content tokens typically usable)
- **effective_token_length**: Long-CLIP and follow-up analyses report effective usable length far below 77 (often cited ~20 tokens for contrastive CLIP); mid/late positions underutilized
- **tokenizer**: CLIP BPE tokenizer (lowercase English-centric)
- **truncation_or_padding_policy**: Right truncation to 77; pad with EOT/pad tokens to fixed length; pooled embedding often taken from EOT position

### Training Prompt Length

- **train_prompt_length_tokens**: CLIP itself trained on web image-text pairs; captions typically short (order of tens of tokens), truncated at 77
- **train_caption_length_distribution**: Web-scale noisy short captions; hard max 77 tokens
- **train_caption_source**: Web image-alt-text pairs (WIT-style)
- **caption_length_randomization**: No explicit length randomization; truncation only
- **recommended_train_prompt_length**: For any T2I using frozen CLIP: keep training captions within 77 tokens or accept truncation; denser content must fit early in the string

### Inference Prompt Length

- **infer_prompt_length_tokens**: Hard cap 77 tokens at inference for CLIP-conditioned models
- **infer_prompt_length_words**: Roughly up to ~50-60 English words before truncation, often less for dense punctuation
- **recommended_user_prompt_length**: Keep user prompts under ~75 content tokens; put critical entities early; or use community chunking (A1111 BREAK / Compel) knowing it is not native CLIP context
- **api_or_hard_limit**: 77 tokens architectural hard limit

### Train-Infer Consistency

- **train_infer_length_match**: Both train and infer truncated to 77; mismatch arises when training captions are short (~10-20) but users write long prompts that truncate
- **mismatch_effects_reported**: DetailMaster: CLIP-based SD1.5/SDXL fail hardest on ~285-token prompts due to token constraints; Davidsonian Scene Graph analyses report sharp drop after ~position 30 and periodic artifacts under chunk concatenation
- **short_prompt_regression**: N/A for CLIP pretraining; for T2I, short prompts match CLIP training better than truncated long prompts
- **length_extrapolation_beyond_training**: Not possible natively beyond 77 without Long-CLIP/TULIP/segment encoding

### Re-prompt / Recaption

- **uses_reprompt**: no
- **reprompt_model**: N/A
- **reprompt_output_length_train**: N/A
- **reprompt_output_length_infer**: N/A
- **rewrite_is_default_on**: no
- **reprompt_motivation**: N/A

### Empirical Findings and Motivation

- **length_ablation_results**: Downstream: models limited to CLIP 77 underperform T5-based models on long-prompt benchmarks (DetailMaster Table 2)
- **quality_vs_length_findings**: Nominal 77 != effective length; padding-to-77 can inject EOT-dominated semantics (Padding Tone / memorization studies)
- **motivation_or_rationale**: 77 chosen as CLIP contrastive training context; became de-facto T2I prompt budget for SD1/SD2/SDXL CLIP towers, creating systemic short-prompt bias
- **key_quotes**: DetailMaster: Most text encoders impose strict upper bounds on input tokens (e.g., CLIP's 77-token limit).
- **practical_recommendation**: If the diffusion backbone uses CLIP, design training and inference prompts to fit ≤77 tokens (critical info first); do not expect faithful use of text beyond that without another encoder or long-prompt method.

### Uncertain fields

- train_prompt_length_words

---

## DALL-E 3 Better Captions

### Identity

- **name**: DALL-E 3 Better Captions
- **year**: 2023
- **organization**: OpenAI
- **model_type**: re-prompt and recaption + proprietary T2I
- **paper_or_source**: Improving Image Generation with Better Captions (DALL·E 3 technical report)
- **primary_url**: https://cdn.openai.com/papers/dall-e-3.pdf

### Text Encoder Limits

- **text_encoder**: Proprietary (not CLIP-77 limited in product behavior)
- **effective_token_length**: Designed for highly detailed captions; API returns revised_prompt showing expansion

### Training Prompt Length

- **train_prompt_length_words**: Detailed multi-sentence captions (qualitatively long)
- **train_caption_length_distribution**: Mostly synthetic detailed captions mixed with a small fraction of ground-truth alt-text (commonly cited ~95% synthetic / 5% alt-text; Altogether later argues 100% synthetic may be better for T2I)
- **train_caption_source**: Dedicated image captioner / LLM synthetic captions over training images
- **caption_length_randomization**: Length/detail increased via better captioner rather than random sampling emphasized
- **recommended_train_prompt_length**: Train on long, detailed, faithful synthetic captions rather than short noisy alt-text

### Inference Prompt Length

- **infer_prompt_length_tokens**: User short prompts are upsampled/revised into longer detailed prompts before generation
- **infer_prompt_length_words**: Revised prompts typically much longer than user input
- **recommended_user_prompt_length**: Users may write short prompts; system rewrites to match training caption style/length
- **api_or_hard_limit**: API exposes revised_prompt; character/token limits product-dependent

### Train-Infer Consistency

- **train_infer_length_match**: Achieved by prompt upsampling at inference to resemble detailed training captions
- **mismatch_effects_reported**: Paper argues poor prompt following of prior systems stems largely from noisy/short training captions and train-test prompt mismatch
- **short_prompt_regression**: Mitigated by always rewriting short user prompts into detailed ones

### Re-prompt / Recaption

- **uses_reprompt**: yes
- **reprompt_model**: LLM prompt upsampler / reviser (details proprietary); API returns revised_prompt
- **rewrite_is_default_on**: yes
- **reprompt_motivation**: Match inference text distribution to detailed synthetic training captions; improve prompt following without user learning prompt engineering

### Empirical Findings and Motivation

- **length_ablation_results**: Better captions improve prompt following dramatically vs same model on alt-text; exact numeric length sweep not the focus
- **quality_vs_length_findings**: Caption quality/detail (length+faithfulness) dominates over leaving short alt-text
- **motivation_or_rationale**: Core thesis: text-to-image failures are largely a data/caption problem; longer faithful captions + inference upsampling align train and user distributions
- **key_quotes**: Improving captions improves image generation; prompt upsampling bridges short user prompts and detailed training captions.
- **practical_recommendation**: If using a re-prompt model: train the T2I on long detailed captions and set the rewriter to output captions of that same long/detailed distribution at inference (default-on).

### Uncertain fields

- arxiv_id
- length_extrapolation_beyond_training
- max_token_length_architecture
- reprompt_output_length_infer
- reprompt_output_length_train
- tokenizer
- train_prompt_length_tokens
- truncation_or_padding_policy

---

## DetailMaster

### Identity

- **name**: DetailMaster
- **year**: 2025
- **organization**: Sun Yat-Sen University; Alibaba Group
- **model_type**: benchmark and ablation
- **paper_or_source**: DetailMaster: Can Your Text-to-Image Model Handle Long Prompts?
- **arxiv_id**: 2505.16915
- **primary_url**: https://arxiv.org/abs/2505.16915

### Text Encoder Limits

- **text_encoder**: Evaluates CLIP-based and T5/LLM-based T2I models
- **max_token_length_architecture**: Benchmark prompts avg 284.89 tokens; compares models with 77 (CLIP), 128 (LLM4GEN/ELLA training limits), 512 (ParaDiffusion)
- **effective_token_length**: Accuracy declines across bins <250, 250-300, 300-350, 350-400, >400 for 10 models
- **tokenizer**: CLIP tokenizer used to measure prompt token length in length analysis
- **truncation_or_padding_policy**: N/A (benchmark)

### Training Prompt Length

- **train_prompt_length_tokens**: Analysis of existing models: mainstream training on short prompts (COCO 10.5, CC12M 20.2 tokens)
- **train_prompt_length_words**: Short web/COCO-style
- **train_caption_length_distribution**: Industry bias toward short captions; long-prompt optimized models train denser/longer
- **train_caption_source**: Varies by evaluated model
- **caption_length_randomization**: N/A
- **recommended_train_prompt_length**: Dense/long prompt training yields greater gains than only raising token capacity; capacity still necessary infrastructure

### Inference Prompt Length

- **infer_prompt_length_tokens**: Benchmark mean 284.89; distribution 100-200:285, 200-300:2399, 300-400:1151, >400:281
- **infer_prompt_length_words**: Detail-rich multi-attribute prompts
- **recommended_user_prompt_length**: Current SOTA still unreliable above ~250-400 tokens; expect degradation as length grows
- **api_or_hard_limit**: N/A

### Train-Infer Consistency

- **train_infer_length_match**: Key finding: models trained on short prompts fail on long inference prompts; long-prompt training + adequate token limit both needed
- **mismatch_effects_reported**: CLIP SD1.5/SDXL collapse on long prompts; even FLUX/GPT-Image ~50% on character attributes
- **short_prompt_regression**: Not the focus; focuses on long-prompt failures
- **length_extrapolation_beyond_training**: Negative correlation length vs adherence across models

### Re-prompt / Recaption

- **uses_reprompt**: no
- **reprompt_model**: N/A
- **reprompt_output_length_train**: N/A
- **reprompt_output_length_infer**: N/A
- **rewrite_is_default_on**: no
- **reprompt_motivation**: N/A

### Empirical Findings and Motivation

- **length_ablation_results**: LLM4GEN 128-token training: slight gains; ELLA same limit but dense prompts: more gains; ParaDiffusion 512 + long training: best among open long-prompt methods. Quote: dense prompt training matters more than increasing token capacity.
- **quality_vs_length_findings**: Monotone accuracy decline as prompt length increases; attribute binding and spatial relations hardest
- **motivation_or_rationale**: Four failure causes: (1) short training data bias, (2) structural comprehension deficiency, (3) detail overload, (4) token length constraints
- **key_quotes**: These results validate that while expanded token capacity provides necessary infrastructure, dense prompt training yields greater gains.
- **practical_recommendation**: Raise token capacity AND train on dense/long captions; evaluating only short prompts hides failure on ~285-token professional prompts.

---

## FIBO 1000 Words

### Identity

- **name**: FIBO 1000 Words
- **year**: 2025
- **organization**: FIBO authors (Bria AI / collaborators per paper)
- **model_type**: diffusion T2I model
- **paper_or_source**: Generating an Image From 1,000 Words: Enhancing Text-to-Image With Structured Captions
- **arxiv_id**: 2511.06876
- **primary_url**: https://arxiv.org/abs/2511.06876

### Text Encoder Limits

- **text_encoder**: Lightweight LLM (SmolLM3-3B) with DimFusion; compared to T5-XXL baseline
- **max_token_length_architecture**: Designed for thousand-token structured captions; DimFusion fuses intermediate LLM layers without growing token count (vs TokenFusion which doubles tokens)
- **effective_token_length**: Mean caption length reported ~1160.3 tokens (median ~1176, std ~316, range ~192-1800) in related reporting
- **tokenizer**: LLM tokenizer
- **truncation_or_padding_policy**: Structured JSON-schema captions; DimFusion keeps sequence length fixed while merging layers

### Training Prompt Length

- **train_prompt_length_tokens**: Long structured captions ~O(1000) tokens every sample
- **train_prompt_length_words**: Order of 1,000 words scale (paper title)
- **train_caption_length_distribution**: All samples long structured; mean ~1160 tokens class regime
- **train_caption_source**: Structured attribute schema captions (same fine-grained fields per image)
- **caption_length_randomization**: No — consistently long structured; short vs long ablated separately
- **recommended_train_prompt_length**: Train on long structured captions (~1000 tokens/words scale) for controllability

### Inference Prompt Length

- **infer_prompt_length_tokens**: Same long structured regime; GenEval short prompts noted as mismatch case
- **infer_prompt_length_words**: Long structured or attribute-edited prompts
- **recommended_user_prompt_length**: Use structured/long prompts matching training schema for best control; short GenEval-like prompts are not the design target

### Train-Infer Consistency

- **train_infer_length_match**: Matched at long structured length; short benchmarks not the strength focus
- **mismatch_effects_reported**: Paper notes GenEval uses relatively short captions — FIBO comparable there despite fewer params
- **short_prompt_regression**: Expected if users stay short; design assumes long structured inputs
- **length_extrapolation_beyond_training**: DimFusion enables efficient long processing

### Re-prompt / Recaption

- **uses_reprompt**: no
- **reprompt_model**: N/A (structured captioner for data)
- **reprompt_output_length_train**: Structured captions ~1000-token scale
- **reprompt_output_length_infer**: N/A unless UI builds structured JSON
- **rewrite_is_default_on**: no
- **reprompt_motivation**: Structure + length for disentangled control

### Empirical Findings and Motivation

- **length_ablation_results**: Long structured vs short: long converges faster, better FID/quality (Figure 5); DimFusion ≈ TokenFusion quality with ~1.6× less step time
- **quality_vs_length_findings**: Long structured captions accelerate convergence and improve expressiveness/controllability
- **motivation_or_rationale**: Short free-form captions under-specify images; thousand-word structured captions unlock attribute disentanglement; efficiency requires DimFusion
- **key_quotes**: Training with long structured captions substantially improves controllability and expressiveness. Training with long captions produces more coherent and visually detailed images, showing faster convergence.
- **practical_recommendation**: If you need fine-grained control, train and infer with long structured captions (~1e3 tokens) and use a fusion method that does not explode attention cost.

### Uncertain fields

- api_or_hard_limit

---

## How to Train your T2I Model

### Identity

- **name**: How to Train your T2I Model
- **year**: 2025
- **organization**: Academic (synthetic training captions study)
- **model_type**: training caption strategy
- **paper_or_source**: How to Train your Text-to-Image Model: Synthetic Training Captions
- **arxiv_id**: 2506.16679
- **primary_url**: https://arxiv.org/abs/2506.16679

### Text Encoder Limits

- **text_encoder**: CLIP (Stable Diffusion v1.1 backbone) — all captions forced ≤77 tokens
- **max_token_length_architecture**: 77 (SD limit)
- **effective_token_length**: ≤77 enforced for all experiments
- **tokenizer**: CLIP
- **truncation_or_padding_policy**: Fit within 77; no over-length captions

### Training Prompt Length

- **train_prompt_length_tokens**: Short vs long dense vs random length, all ≤77; example target length for dense ~60 words via InternVL2 instruction
- **train_prompt_length_words**: Instruct captioner with target length X (e.g., 60 for dense)
- **train_caption_length_distribution**: Fixed short, fixed long, or randomized length per image (best)
- **train_caption_source**: InternVL2-76B preferred; LLaVA variants compared
- **caption_length_randomization**: Yes — recommended; also different random length each epoch
- **recommended_train_prompt_length**: Randomize length/density of training captions rather than long-only or short-only

### Inference Prompt Length

- **infer_prompt_length_tokens**: Evaluate across minimal to complex prompts within 77
- **infer_prompt_length_words**: Sweep of prompt complexities
- **recommended_user_prompt_length**: Random-length training makes model robust to both short and long user prompts (within 77)
- **api_or_hard_limit**: 77

### Train-Infer Consistency

- **train_infer_length_match**: Randomized training covers both short and long inference without needing rewrite
- **mismatch_effects_reported**: Long-only training: better on long prompts, worse aesthetics/diversity on minimal prompts (OOD)
- **short_prompt_regression**: Long dense training yields bland images for minimal prompts
- **length_extrapolation_beyond_training**: Constrained by 77

### Re-prompt / Recaption

- **uses_reprompt**: no
- **reprompt_model**: N/A (diversity via training caption sampling)
- **reprompt_output_length_train**: Captioner controlled to target lengths; temperature 1.5 recommended to close aesthetics gap
- **reprompt_output_length_infer**: N/A
- **rewrite_is_default_on**: no
- **reprompt_motivation**: Prefer training-time length diversity over inference rewrite

### Empirical Findings and Motivation

- **length_ablation_results**: Fixed-length → aesthetics/alignment trade-off; random length → best PickScores, no trade-off, less diversity loss
- **quality_vs_length_findings**: Long dense ≠ unequivocally better; randomize length
- **motivation_or_rationale**: Short prompts become OOD under long-only training; randomizing length keeps both modes in-distribution
- **key_quotes**: Recommendation: Randomly sample length/density of training captions. Randomizing the caption length at training results in the overall best model.
- **practical_recommendation**: If you will not deploy a rewriter: train with randomized caption lengths (within encoder limit). If you will deploy a rewriter: long-only + rewrite (i1) is an alternative.

---

## Imagen family

### Identity

- **name**: Imagen family
- **year**: 2022-2025
- **organization**: Google
- **model_type**: diffusion T2I model
- **paper_or_source**: Photorealistic Text-to-Image Diffusion Models with Deep Language Understanding (Imagen); Imagen API docs
- **arxiv_id**: 2205.11487
- **primary_url**: https://arxiv.org/abs/2205.11487

### Text Encoder Limits

- **text_encoder**: Frozen T5-XXL (preferred over CLIP/BERT in ablations)
- **max_token_length_architecture**: T5 can encode long sequences; Imagen 4 API documents a 480-token input limit
- **effective_token_length**: Human preference strongly favors T5-XXL over CLIP on DrawBench compositional prompts
- **tokenizer**: T5 SentencePiece

### Training Prompt Length

- **train_caption_source**: Internal paired data + classifier-free guidance
- **recommended_train_prompt_length**: Use a large LM encoder (T5-XXL) capable of long linguistic context rather than CLIP 77

### Inference Prompt Length

- **infer_prompt_length_tokens**: Imagen 4 API hard limit 480 tokens
- **infer_prompt_length_words**: Detailed DrawBench-style compositional prompts
- **recommended_user_prompt_length**: Detailed natural-language prompts; for in-image text Imagen docs historically recommend short rendered strings (e.g. ≤25 characters)
- **api_or_hard_limit**: Imagen 4: 480 tokens

### Empirical Findings and Motivation

- **length_ablation_results**: Larger T5 variants improve CLIP score and human preference; T5-XXL preferred over CLIP on DrawBench alignment in all 11 categories
- **quality_vs_length_findings**: Language-model text encoders outperform contrastive CLIP text encoders for complex prompts even when COCO FID/CLIP scores look similar
- **motivation_or_rationale**: Fundamental claim: scaling frozen LM text encoders transfers deep language understanding to T2I, enabling longer/more compositional prompts than CLIP
- **key_quotes**: Imagen: language models are better than text encoders trained on image-text contrastive objectives for text-to-image generation on challenging prompts.
- **practical_recommendation**: Prefer LM-style encoders (T5/LLM) with hundreds of tokens (Imagen 4: 480) over CLIP 77 when the goal is long compositional prompts.

### Uncertain fields

- caption_length_randomization
- length_extrapolation_beyond_training
- mismatch_effects_reported
- reprompt_model
- reprompt_motivation
- reprompt_output_length_infer
- reprompt_output_length_train
- rewrite_is_default_on
- short_prompt_regression
- train_caption_length_distribution
- train_infer_length_match
- train_prompt_length_tokens
- train_prompt_length_words
- truncation_or_padding_policy
- uses_reprompt

---

## LongAlign

### Identity

- **name**: LongAlign
- **year**: 2024
- **organization**: LongAlign authors
- **model_type**: long prompt method
- **paper_or_source**: Improving Long-Text Alignment for Text-to-Image Diffusion Models
- **arxiv_id**: 2410.11817
- **primary_url**: https://arxiv.org/abs/2410.11817

### Text Encoder Limits

- **text_encoder**: CLIP with segment-level encoding (split long text → encode segments → concatenate)
- **max_token_length_architecture**: Effectively multiplies 77-token windows via segmentation; training data mostly described as under ~300 tokens in later critiques
- **effective_token_length**: Hundreds of tokens via segments; PRISM paper later reports LongAlign degrades up to ~30% on >500-token prompts
- **tokenizer**: CLIP
- **truncation_or_padding_policy**: Segment then encode; careful handling of duplicated special tokens (keep sot; distinct pad*)

### Training Prompt Length

- **train_prompt_length_tokens**: Long multi-sentence texts spanning hundreds of tokens
- **train_prompt_length_words**: Multi-sentence long descriptions
- **train_caption_length_distribution**: Long-text alignment training set
- **train_caption_source**: Long-text paired data + preference optimization
- **recommended_train_prompt_length**: Train with long segmented texts; keep training distribution covering target inference lengths

### Inference Prompt Length

- **infer_prompt_length_tokens**: Long prompts via segment encoding
- **infer_prompt_length_words**: Hundreds of tokens
- **recommended_user_prompt_length**: Works best near training length (often <300); caution above 500 tokens
- **api_or_hard_limit**: Multiple of 77 via segments

### Train-Infer Consistency

- **train_infer_length_match**: Critical: later work shows failure when infer >> train length
- **mismatch_effects_reported**: PRISM (arXiv 2604.18258): LongAlign −30% on >500-token prompts when training mostly <300
- **length_extrapolation_beyond_training**: Weak; need compositional methods for extreme lengths

### Re-prompt / Recaption

- **uses_reprompt**: no
- **reprompt_model**: N/A
- **reprompt_output_length_train**: N/A
- **reprompt_output_length_infer**: N/A
- **rewrite_is_default_on**: no
- **reprompt_motivation**: N/A

### Empirical Findings and Motivation

- **length_ablation_results**: DetailMaster: LongAlign improves SD1.5 on long prompts but still backbone-limited
- **quality_vs_length_findings**: Helps mid-long prompts; extrapolates poorly past training lengths
- **motivation_or_rationale**: CLIP 77 cannot encode long text; segment-level encoding + preference optimization improves long-text alignment
- **key_quotes**: As text length increases, the maximum token limit of CLIP becomes a significant constraint... we explore segment-level encoding.
- **practical_recommendation**: Segmented CLIP encoding can extend past 77, but train on prompt lengths that cover your inference regime; do not assume >500-token generalization.

### Uncertain fields

- caption_length_randomization
- short_prompt_regression

---

## Padding Tone and Memorization Length Effects

### Identity

- **name**: Padding Tone and Memorization Length Effects
- **year**: 2025-2026
- **organization**: NAACL 2025 Padding Tone authors; memorization study authors
- **model_type**: mechanistic analysis
- **paper_or_source**: Padding Tone: A Mechanistic Analysis of Padding Tokens in T2I Models; Memorization In Stable Diffusion Is Unexpectedly Driven by CLIP Embeddings
- **arxiv_id**: 2605.02908 (memorization); Padding Tone NAACL 2025
- **primary_url**: https://arxiv.org/abs/2605.02908

### Text Encoder Limits

- **text_encoder**: CLIP-based SD analyses primarily
- **max_token_length_architecture**: 77 with pad-to-max
- **effective_token_length**: Short prompts ⇒ many pad/EOT tokens that can dominate generation
- **tokenizer**: CLIP
- **truncation_or_padding_policy**: Pad-to-77 with EOT reuse vs dedicated pad; whether pads are attention-masked determines padding tone regimes

### Training Prompt Length

- **train_prompt_length_tokens**: Memorized prompts studied are typically <40 tokens → 30+ near-duplicate EOT pads
- **train_prompt_length_words**: Short
- **train_caption_length_distribution**: Short prompts create large padding fractions
- **train_caption_source**: N/A
- **caption_length_randomization**: N/A
- **recommended_train_prompt_length**: Be aware short prompts create padding-dominated embeddings; consider masking pads or distinct pad tokens

### Inference Prompt Length

- **infer_prompt_length_tokens**: Same 77; shorter prompts = more pads
- **infer_prompt_length_words**: Short
- **recommended_user_prompt_length**: Extremely short prompts may behave differently due to padding tone, not only due to less semantic content
- **api_or_hard_limit**: 77

### Train-Infer Consistency

- **train_infer_length_match**: Padding count is a direct function of prompt length — length choice changes pad semantics
- **mismatch_effects_reported**: Three regimes: padding affects text encoding, affects diffusion, or ignored — depends on attention/frozen encoder
- **short_prompt_regression**: Short prompts can trigger memorization via pad/EOT domination
- **length_extrapolation_beyond_training**: N/A

### Re-prompt / Recaption

- **uses_reprompt**: no
- **reprompt_model**: N/A
- **reprompt_output_length_train**: N/A
- **reprompt_output_length_infer**: N/A
- **rewrite_is_default_on**: no
- **reprompt_motivation**: N/A

### Empirical Findings and Motivation

- **length_ablation_results**: All previously reported memorized prompts <40 tokens in the memorization study; mitigations include swapping pad token / masking v_eot
- **quality_vs_length_findings**: Prompt length controls padding fraction, which can be a causal factor in outputs beyond semantics
- **motivation_or_rationale**: Length is not only about how much text fits — it changes how many pad tokens condition the model
- **key_quotes**: Padding count is a direct function of prompt length; memorized prompts are typically under 40 tokens producing many EOT pads.
- **practical_recommendation**: When using pad-to-max CLIP encoders, treat very short prompts carefully (mask pads / avoid EOT-as-pad domination); length policy interacts with padding mechanics.

---

## PixArt-alpha and PixArt-Sigma

### Identity

- **name**: PixArt-alpha and PixArt-Sigma
- **year**: 2023-2024
- **organization**: Huawei Noah's Ark Lab et al.
- **model_type**: diffusion T2I model
- **paper_or_source**: PixArt-α: Fast Training of Diffusion Transformer for Photorealistic Text-to-Image Synthesis; PixArt-Σ
- **arxiv_id**: 2310.00426; 2403.04692
- **primary_url**: https://arxiv.org/abs/2310.00426

### Text Encoder Limits

- **text_encoder**: Flan-T5-XXL
- **max_token_length_architecture**: PixArt-α: 120 text tokens (vs common 77); PixArt-Σ: extended to ~300 tokens/words
- **effective_token_length**: Explicitly increased because Share-Captioner / dense captions exceed 77
- **tokenizer**: T5 tokenizer
- **truncation_or_padding_policy**: Extract longer than 77 fixed tokens to fit denser captions

### Training Prompt Length

- **train_prompt_length_tokens**: α: up to 120; Σ: up to ~300
- **train_prompt_length_words**: Σ paper: extend text encoder token length to approximately 300 words
- **train_caption_length_distribution**: Dense LLaVA/Share-Captioner style detailed captions much longer than LAION alt-text
- **train_caption_source**: LLaVA / Share-Captioner style detailed captions over images (plus original LAION text for concepts)
- **caption_length_randomization**: Not primary; focus on denser fixed longer budget
- **recommended_train_prompt_length**: Match encoder length to caption density: 120 (α) then 300 (Σ) as captions get denser

### Inference Prompt Length

- **infer_prompt_length_tokens**: Same budgets: 120 / ~300
- **infer_prompt_length_words**: Detailed multi-sentence user prompts encouraged
- **recommended_user_prompt_length**: Use detailed prompts within the configured 120 or 300 token budget
- **api_or_hard_limit**: 120 (α) / ~300 (Σ)

### Train-Infer Consistency

- **train_infer_length_match**: Matched by raising encoder length with caption density
- **mismatch_effects_reported**: Motivation: standard 77 insufficient for dense captions

### Re-prompt / Recaption

- **uses_reprompt**: no
- **reprompt_model**: N/A (offline recaptioning for training data)
- **reprompt_output_length_train**: Dense captions sized for 120 then 300 token windows
- **reprompt_output_length_infer**: N/A
- **rewrite_is_default_on**: no
- **reprompt_motivation**: Recaption training images to denser text so each step teaches more concepts

### Empirical Findings and Motivation

- **length_ablation_results**: Authors explicitly raised token length from 77→120→300 because curated captions were denser
- **quality_vs_length_findings**: Denser longer captions improve alignment efficiency / concept learning
- **motivation_or_rationale**: Dense captions contain more concepts per sample; encoder context must grow with caption density
- **key_quotes**: PixArt-α: Unlike previous works that extract a standard and fixed 77 text tokens, we adjust the length of extracted text tokens to 120, as the caption curated in PixArt-α is much denser. PixArt-Σ: adjust the length of text tokens from PixArt-α's 120 to 300.
- **practical_recommendation**: When training captions get denser, raise the text encoder sequence length accordingly (77→120→300 in this lineage) and keep inference within that budget.

### Uncertain fields

- length_extrapolation_beyond_training
- short_prompt_regression

---

## PromptEnhancer and HunyuanImage

### Identity

- **name**: PromptEnhancer and HunyuanImage
- **year**: 2025
- **organization**: Tencent Hunyuan
- **model_type**: re-prompt rewriter + T2I model
- **paper_or_source**: PromptEnhancer (arXiv 2509.04545); HunyuanImage 3.0 Technical Report (arXiv 2509.23951)
- **arxiv_id**: 2509.04545; 2509.23951
- **primary_url**: https://arxiv.org/abs/2509.23951

### Text Encoder Limits

- **text_encoder**: HunyuanImage 3.0: native autoregressive unified model; PromptEnhancer: VLM policy rewriter upstream of any T2I
- **max_token_length_architecture**: Training captions sampled from ~30 to 1,000 words (bilingual EN/ZH)
- **effective_token_length**: Wide range deliberately covered in training
- **tokenizer**: Multilingual (EN/ZH); CJK inflates token counts for same words

### Training Prompt Length

- **train_prompt_length_tokens**: Corresponds to 30–1000 words via Compositional Caption Synthesis field sampling
- **train_prompt_length_words**: About 30 to 1,000 words
- **train_caption_length_distribution**: Strategically sample/combine caption fields → variable length and pattern
- **train_caption_source**: Compositional hierarchical caption fields; PromptEnhancer trained with RL vs AlignEvaluator
- **caption_length_randomization**: Yes — deliberate length and pattern randomization during training
- **recommended_train_prompt_length**: Cover a wide band (30–1000 words) rather than a single fixed length

### Inference Prompt Length

- **infer_prompt_length_tokens**: Optional CoT think_recaption / rewrite modes; PromptEnhancer rewrites user prompts
- **infer_prompt_length_words**: Rewriter enriches content; authors argue against pure stylistic verbosity
- **recommended_user_prompt_length**: Short user prompts OK if rewriter on; training already saw short→long spectrum

### Train-Infer Consistency

- **train_infer_length_match**: Randomized training reduces mismatch; rewriter further aligns short users to richer text
- **mismatch_effects_reported**: HunyuanImage 2.1 PromptEnhancer built ~2.26M proxy short user prompts to simulate real brevity
- **short_prompt_regression**: Mitigated by length randomization + rewriter
- **length_extrapolation_beyond_training**: Up to ~1000 words covered

### Re-prompt / Recaption

- **uses_reprompt**: yes
- **reprompt_model**: PromptEnhancer CoT VLM rewriter; HunyuanImage 3.0 think_recaption modes
- **reprompt_output_length_train**: Training captions span 30–1000 words
- **reprompt_output_length_infer**: Enriched prompts targeting failure-mode fixes (24-point AlignEvaluator taxonomy), not unconstrained verbosity
- **rewrite_is_default_on**: Optional/modes; product may enable
- **reprompt_motivation**: Rewrite should change content to fix T2I failure modes, not add empty stylistic verbosity; also bridge short users to training distribution

### Empirical Findings and Motivation

- **length_ablation_results**: Compositional Caption Synthesis with variable lengths is a core training design of HunyuanImage 3.0
- **quality_vs_length_findings**: Variable-length bilingual captions support robust following across prompt styles
- **motivation_or_rationale**: Real users write short; models train on rich captions — rewriter + randomized train lengths address the gap
- **key_quotes**: During training, we strategically sample and combine different fields to generate captions varying in both length and pattern, supporting bilingual outputs from about 30 words up to 1,000 words.
- **practical_recommendation**: Train across a wide caption-length band (tens to ~1000 words) and use a content-focused rewriter so short user prompts map into that band.

### Uncertain fields

- api_or_hard_limit
- truncation_or_padding_policy

---

## Qwen-Image and FLUX.2 Re-prompt

### Identity

- **name**: Qwen-Image and FLUX.2 Re-prompt
- **year**: 2025-2026
- **organization**: Alibaba Qwen; Black Forest Labs
- **model_type**: re-prompt and modern T2I
- **paper_or_source**: Qwen-Image / Qwen-Image-2.0 reports; FLUX.2 text encoder / diffusers docs
- **arxiv_id**: 2605.10730 (Qwen-Image-2.0)
- **primary_url**: https://arxiv.org/abs/2605.10730

### Text Encoder Limits

- **text_encoder**: Qwen-Image: Qwen LLM/VLM family; FLUX.2: single Mistral Small 3.1 / Qwen3-style encoder (replaces CLIP+T5 dual)
- **max_token_length_architecture**: Common max_sequence_length 512 (configurable higher, e.g. 1024 in some pipelines); FLUX.2 MAX_LENGTH=512 with padding=max_length, truncation=True; stacks hidden states from layers [10,20,30]
- **effective_token_length**: API accepts ~800 tokens (older) to ~1300 (2.0 series) with hard truncation
- **tokenizer**: LLM tokenizers; chat templates consume overhead tokens
- **truncation_or_padding_policy**: Pad to max length; documented padding bugs if embeddings not padded to max seq len (train/infer inconsistency risk)

### Training Prompt Length

- **train_caption_source**: Synthetic / curated; PE via SFT→GRPO
- **recommended_train_prompt_length**: Align with 512 encoder budget and PE output budget

### Inference Prompt Length

- **infer_prompt_length_tokens**: 512 encoder path; API up to ~800-1300 before truncate
- **infer_prompt_length_words**: Detailed extended prompts via prompt_extend
- **recommended_user_prompt_length**: Short OK when prompt_extend default-on; final conditioning should fill toward training/PE length
- **api_or_hard_limit**: Qwen image API ~800–1300 tokens depending on version; negative prompt limits may be smaller (e.g. 500 chars)

### Train-Infer Consistency

- **train_infer_length_match**: Built-in caption upsampling / prompt_extend intended to match training distribution
- **mismatch_effects_reported**: Padding-to-max bugs can break length consistency
- **short_prompt_regression**: Mitigated by default-on extend
- **length_extrapolation_beyond_training**: API truncation at product limit

### Re-prompt / Recaption

- **uses_reprompt**: yes
- **reprompt_model**: Qwen: prompt_extend (Qwen3.5-9B PE); FLUX.2: caption upsampler inside text encoder module (max_new_tokens=512, chat-template budget 2048)
- **reprompt_output_length_infer**: FLUX.2 upsampler max_new_tokens=512; Qwen PE expands toward API/encoder limits
- **rewrite_is_default_on**: yes
- **reprompt_motivation**: Make re-prompt a first-class component so short user text matches long training captions

### Empirical Findings and Motivation

- **quality_vs_length_findings**: Industry convergence toward ~512 token encoder budgets + default rewrite
- **motivation_or_rationale**: Re-prompt is no longer an optional wrapper — it is part of the text conditioning stack
- **key_quotes**: FLUX.2 ships caption upsampling inside the text encoder module; Qwen prompt_extend defaults to true.
- **practical_recommendation**: For modern stacks: encoder max ~512, turn prompt extend ON, and set rewriter max_new_tokens on the order of the encoder budget (e.g. 512).

### Uncertain fields

- caption_length_randomization
- length_ablation_results
- reprompt_output_length_train
- train_caption_length_distribution
- train_prompt_length_tokens
- train_prompt_length_words

---

## RECAP Principled Recaptioning

### Identity

- **name**: RECAP Principled Recaptioning
- **year**: 2023
- **organization**: Google Research et al.
- **model_type**: training caption strategy
- **paper_or_source**: A Picture is Worth a Thousand Words: Principled Recaptioning Improves Image Generation
- **arxiv_id**: 2310.16656
- **primary_url**: https://arxiv.org/abs/2310.16656

### Text Encoder Limits

- **text_encoder**: CLIP (Stable Diffusion 1.4 fine-tunes)
- **max_token_length_architecture**: 77; captions >77 tokens dropped (<1%)
- **effective_token_length**: ≤77
- **tokenizer**: CLIP
- **truncation_or_padding_policy**: Drop >77 token prompts rather than truncate for training sets noted

### Training Prompt Length

- **train_prompt_length_tokens**: RECAP Short: ~1-2 detailed sentences within 77; RECAP Long: longer but still ≤77; Mix 50/50
- **train_prompt_length_words**: Short vs long prefixes control captioner verbosity
- **train_caption_length_distribution**: Short / Long / Mix; Mix best
- **train_caption_source**: Fine-tuned PaLI captioner conditioned on short vs long prefixes
- **caption_length_randomization**: Discrete mix 50% short + 50% long (best)
- **recommended_train_prompt_length**: 50/50 mix of short and long recaptions within CLIP 77

### Inference Prompt Length

- **infer_prompt_length_tokens**: Eval on COCO/DrawBench; drop >77 token eval prompts
- **infer_prompt_length_words**: Standard short benchmarks
- **recommended_user_prompt_length**: Within 77; mix training helps both FID and semantics
- **api_or_hard_limit**: 77

### Train-Infer Consistency

- **train_infer_length_match**: Mix reduces train-inference skew vs long-only
- **mismatch_effects_reported**: Long improves semantics; Short improves FID/speed; Mix both
- **short_prompt_regression**: Addressed by including Short captions
- **length_extrapolation_beyond_training**: N/A beyond 77

### Re-prompt / Recaption

- **uses_reprompt**: no
- **reprompt_model**: PaLI recaptioner for dataset creation
- **reprompt_output_length_train**: Controlled short vs long prefixes; human faithfulness scores Short 3.58 / Long 4.3 vs Alttext 2.9
- **reprompt_output_length_infer**: N/A
- **rewrite_is_default_on**: no
- **reprompt_motivation**: Replace noisy alt-text with faithful captions of controllable length

### Empirical Findings and Motivation

- **length_ablation_results**: RECAP Short best FID; Long best semantics; Mix best overall when fine-tuning UNet+CLIP
- **quality_vs_length_findings**: Length/detail trade-off exists; mixing resolves it under CLIP 77
- **motivation_or_rationale**: Alt-text is noisy/incomplete; principled recaptioning with length control improves T2I fine-tuning
- **key_quotes**: RECAP Short achieves better FID and faster, but with little semantic improvement, while RECAP Long captions exhibit significant semantic improvement... RECAP Mix achieves both.
- **practical_recommendation**: Under a 77-token CLIP limit, mix short and long recaptions (~50/50) instead of long-only or alt-text-only.

---

## Recap-DataComp-1B and Dense Caption Datasets

### Identity

- **name**: Recap-DataComp-1B and Dense Caption Datasets
- **year**: 2024
- **organization**: Multiple (Recap-DataComp; DCI; DOCCI; ImageInWords)
- **model_type**: training caption strategy / datasets
- **paper_or_source**: What If We Recaption Billions of Web Images with LLaMA-3?; DCI; DOCCI; ImageInWords
- **arxiv_id**: 2406.08478; 2312.08578; DOCCI ECCV 2024; ImageInWords EMNLP 2024
- **primary_url**: https://arxiv.org/abs/2406.08478

### Text Encoder Limits

- **text_encoder**: Used downstream with CLIP/T5/etc. depending on T2I model
- **max_token_length_architecture**: Recap-DataComp sets text token length 128 to learn long captions; DCI human captions average 1282 CLIP tokens (far beyond 77)
- **effective_token_length**: Dataset lengths often exceed CLIP 77 — requires T5/LLM encoders or truncation/summarization (sDCI)
- **tokenizer**: CLIP tokens cited for DCI/DOCCI comparisons; LLaMA tokenizer for Recap generation
- **truncation_or_padding_policy**: Recap decode max_new_tokens=128; sDCI summarizes to fit 77

### Training Prompt Length

- **train_prompt_length_tokens**: Recap-DataComp mean 49.43 vs original DataComp 10.22; DCI ~1282; DOCCI ~135.7; ImageInWords ~217.2; COCO ~10.5; CC12M ~20.2
- **train_prompt_length_words**: DOCCI ~136 words average; DCI ~1111 words scale
- **train_caption_length_distribution**: See means above; Recap greedy decode capped at 128 new tokens
- **train_caption_source**: LLaVA-1.5-LLaMA3-8B (Recap); human dense captions (DCI/DOCCI/IIW)
- **caption_length_randomization**: sDCI provides shortened variants of DCI for 77-token models
- **recommended_train_prompt_length**: Prefer denser captions than raw alt-text (~10 tokens); choose length to match encoder (49–128 for Recap/CLIP-extended, 100–300+ for T5, 1000+ only with long-context architectures)

### Inference Prompt Length

- **infer_prompt_length_tokens**: Should reflect training caption statistics of the chosen dataset mix
- **infer_prompt_length_words**: Match dataset
- **recommended_user_prompt_length**: If model trained on Recap ~50-token mean, user/rewrite targets should be similar order; if trained on DCI-scale, need long-context model
- **api_or_hard_limit**: N/A (datasets)

### Train-Infer Consistency

- **train_infer_length_match**: sDCI exists specifically because 77-token models cannot consume raw DCI
- **mismatch_effects_reported**: Training on ultra-long human captions without encoder support requires summarization
- **short_prompt_regression**: Switching from 10-token alt-text to 50-token Recap shifts the in-distribution length upward
- **length_extrapolation_beyond_training**: N/A

### Re-prompt / Recaption

- **uses_reprompt**: yes
- **reprompt_model**: LLaVA-1.5-LLaMA3-8B for Recap-DataComp
- **reprompt_output_length_train**: max_new_tokens=128; realized mean 49.43 tokens
- **reprompt_output_length_infer**: N/A (dataset prep)
- **rewrite_is_default_on**: N/A (offline)
- **reprompt_motivation**: Replace short noisy web alt-text with longer higher-quality captions at scale

### Empirical Findings and Motivation

- **length_ablation_results**: Recap shows large vocabulary/length gains vs DataComp originals; DCI table compares COCO 13.54, LNCOCO 49.11, sDCI 49.21, DCI-sub 199.33, DCI 1282.09 tokens/caption
- **quality_vs_length_findings**: Human dense captions >>77 tokens; practical T2I training often uses summarized or mid-length synthetic captions
- **motivation_or_rationale**: Alt-text underdescribes images; dense captions improve learning but must fit or reshape to encoder limits
- **key_quotes**: Recap-DataComp: On average, our recaptioned data demonstrates a longer sequence length of 49.43, whereas the original DataComp captions have a much shorter length of 10.22. We set the text token length to 128... maximum output token length set to 128.
- **practical_recommendation**: For web-scale recaptioning under mid-size encoders: captioner max_new_tokens≈128 (mean ~50) is a proven operating point; for CLIP-only keep ≤77 or use sDCI-style summaries.

---

## Stable Diffusion 1.x and 2.x

### Identity

- **name**: Stable Diffusion 1.x and 2.x
- **year**: 2022
- **organization**: Stability AI / CompVis / LAION
- **model_type**: diffusion T2I model
- **paper_or_source**: High-Resolution Image Synthesis with Latent Diffusion Models; SD2 release notes
- **arxiv_id**: 2112.10752
- **primary_url**: https://arxiv.org/abs/2112.10752

### Text Encoder Limits

- **text_encoder**: SD1.x: CLIP ViT-L/14; SD2.x: OpenCLIP ViT-H/14
- **max_token_length_architecture**: 77 tokens (CLIP/OpenCLIP)
- **effective_token_length**: ~20-40 tokens practically influential; rest often padding/EOT
- **tokenizer**: CLIP/OpenCLIP BPE
- **truncation_or_padding_policy**: Pad/truncate to 77; empty prompt dropout ~10-20% for CFG; community long-prompt: chunk into 75-token segments and concatenate embeddings (lpw_stable_diffusion)

### Training Prompt Length

- **train_prompt_length_tokens**: Primarily LAION alt-text: COCO-like short captions ~10-20 tokens common; hard truncate at 77
- **train_prompt_length_words**: Typically short web captions (~5-20 words); DetailMaster cites COCO 10.5 / CC12M 20.2 tokens as mainstream short-prompt bias
- **train_caption_length_distribution**: Skewed short; rare captions >77 dropped or truncated
- **train_caption_source**: LAION-2B / LAION-5B alt-text
- **caption_length_randomization**: No systematic randomization in original SD training
- **recommended_train_prompt_length**: Original recipe: short alt-text within 77. Later recaption papers recommend short+long mix or random length still truncated to 77 for CLIP-backed SD

### Inference Prompt Length

- **infer_prompt_length_tokens**: Native 77; with Compel/lpw can exceed via chunking (154, 231, ...)
- **infer_prompt_length_words**: User prompts often longer than training captions, causing truncation
- **recommended_user_prompt_length**: ≤75 tokens native; for longer prompts use chunking knowing quality may oscillate every 77 tokens
- **api_or_hard_limit**: 77 native

### Train-Infer Consistency

- **train_infer_length_match**: Both capped at 77, but distribution mismatch: train short vs user long/complex
- **mismatch_effects_reported**: RECAP and How-to-Train papers: long-only fine-tunes hurt short prompts; DetailMaster: SD1.5 worst on long prompts
- **short_prompt_regression**: After long-caption fine-tunes, short prompts become OOD (How-to-Train Fig.5 bland outputs)
- **length_extrapolation_beyond_training**: Chunking extrapolates sequence length but not true long-context understanding

### Re-prompt / Recaption

- **uses_reprompt**: no
- **reprompt_model**: N/A (community prompt engineering only)
- **reprompt_output_length_train**: N/A
- **reprompt_output_length_infer**: N/A
- **rewrite_is_default_on**: no
- **reprompt_motivation**: N/A

### Empirical Findings and Motivation

- **length_ablation_results**: RECAP on SD1.4: Short better FID; Long better semantics; 50/50 Mix best overall; drop >77-token captions (<1%)
- **quality_vs_length_findings**: Short captions favor FID/aesthetics; long favor alignment; random length (within 77) best balance (How-to-Train)
- **motivation_or_rationale**: Inherited CLIP 77 limit; LAION alt-text short; CFG empty-prompt dropout
- **key_quotes**: How-to-Train: Ensure that all captions and prompts used in our experiment fit SD's maximum token length of 77.
- **practical_recommendation**: For CLIP-SD: train with mixed/random caption lengths ≤77 tokens; at inference keep prompts ≤77 or rewrite into that budget; do not rely on naive long user prompts.

---

## Stable Diffusion 3 and FLUX.1

### Identity

- **name**: Stable Diffusion 3 and FLUX.1
- **year**: 2024
- **organization**: Stability AI; Black Forest Labs
- **model_type**: diffusion / flow-matching T2I
- **paper_or_source**: Scaling Rectified Flow Transformers for High-Resolution Image Synthesis (SD3); FLUX.1 release
- **arxiv_id**: 2403.03206
- **primary_url**: https://arxiv.org/abs/2403.03206

### Text Encoder Limits

- **text_encoder**: SD3: CLIP-L + CLIP-G/OpenCLIP + T5-XXL; FLUX.1: CLIP-L + T5-XXL
- **max_token_length_architecture**: SD3 paper figure encodes T5 to 77 tokens (c_ctxt^T5 in R^{77x4096}) concatenated with CLIP 77; community/diffusers often allow T5 up to 256-512. FLUX.1 commonly uses max_sequence_length up to 512 for T5
- **effective_token_length**: T5 path enables substantially longer usable prompts than CLIP-only; DetailMaster still shows degradation as length grows past ~250-400 tokens
- **tokenizer**: CLIP + T5 SentencePiece
- **truncation_or_padding_policy**: Right truncation; pad to configured max_sequence_length; attention masking of pads implementation-dependent

### Training Prompt Length

- **train_caption_length_distribution**: Richer than SD1 but not FIBO-scale thousand-token captions
- **train_caption_source**: Curated + synthetic captions (undisclosed full recipe for FLUX)
- **recommended_train_prompt_length**: Use dense captions matching the T5 sequence length you will serve (commonly 256-512 for FLUX-class); SD3 paper used 77-length T5 features in reported architecture diagram

### Inference Prompt Length

- **infer_prompt_length_tokens**: FLUX.1: up to ~512 T5 tokens typical; SD3: often 77-256 depending on checkpoint/pipeline
- **infer_prompt_length_words**: Hundreds of words possible on T5 path
- **recommended_user_prompt_length**: Prefer detailed prompts aligned with training caption density; DetailMaster shows accuracy falling for bins >250 and especially >400 tokens
- **api_or_hard_limit**: Implementation max_sequence_length (often 512 for FLUX)

### Train-Infer Consistency

- **train_infer_length_match**: Should match configured T5 length; removing T5 at SD3 inference still competitive on aesthetics (paper) but hurts adherence
- **mismatch_effects_reported**: DetailMaster: FLUX/SD3.5 ~50% on hard attribute tasks at ~285 tokens; monotone degradation with length
- **length_extrapolation_beyond_training**: Limited; long-prompt specialized methods still needed

### Re-prompt / Recaption

- **uses_reprompt**: Often used in products wrapping these models
- **reprompt_model**: Product-dependent (not core paper)
- **reprompt_motivation**: Align user short prompts with denser training captions

### Empirical Findings and Motivation

- **length_ablation_results**: SD3: T5 helps prompt adherence; w/o T5 aesthetics similar. DetailMaster: T5 models >> CLIP models on long prompts
- **quality_vs_length_findings**: Longer encoder capacity necessary but not sufficient; dense training data more important (DetailMaster)
- **motivation_or_rationale**: T5 language-model encodings capture compositionality better than CLIP contrastive text for complex prompts (also Imagen finding)
- **key_quotes**: SD3: Removing T5 has no effect on aesthetic quality ratings (50% win rate), and only a small impact on prompt adherence (46%).
- **practical_recommendation**: Train/serve with T5 sequence length consistently (often 256-512 for FLUX-class); write inference prompts at training caption density or use a rewriter; do not assume 512 tokens alone fixes long-prompt fidelity.

### Uncertain fields

- caption_length_randomization
- reprompt_output_length_infer
- reprompt_output_length_train
- rewrite_is_default_on
- short_prompt_regression
- train_prompt_length_tokens
- train_prompt_length_words

---

## Stable Diffusion XL

### Identity

- **name**: Stable Diffusion XL
- **year**: 2023
- **organization**: Stability AI
- **model_type**: diffusion T2I model
- **paper_or_source**: SDXL: Improving Latent Diffusion Models for High-Resolution Image Synthesis
- **arxiv_id**: 2307.01952
- **primary_url**: https://arxiv.org/abs/2307.01952

### Text Encoder Limits

- **text_encoder**: Dual: CLIP ViT-L/14 + OpenCLIP ViT-bigG/14; concatenated context + pooled embeddings
- **max_token_length_architecture**: 77 tokens per encoder (still CLIP-limited)
- **effective_token_length**: Still ~77 nominal / much lower effective; dual encoder improves semantics but not context length
- **tokenizer**: CLIP + OpenCLIP tokenizers
- **truncation_or_padding_policy**: Pad/truncate each tower to 77; pooled prompt embeds from one path; long-prompt pipelines must also supply pooled embeds carefully

### Training Prompt Length

- **train_prompt_length_tokens**: Web captions / curated aesthetic subsets; still within 77
- **train_prompt_length_words**: Mostly short-to-medium captions
- **train_caption_length_distribution**: Short-biased like SD1
- **train_caption_source**: Internal multi-stage datasets (aesthetic filtering)
- **recommended_train_prompt_length**: Stay within 77 per encoder; for long-prompt ability need dense captions + methods like ParaDiffusion (512) on SDXL backbone

### Inference Prompt Length

- **infer_prompt_length_tokens**: 77 native; community chunking beyond
- **infer_prompt_length_words**: Similar to SD1
- **recommended_user_prompt_length**: ≤77 tokens unless using long-prompt adapters
- **api_or_hard_limit**: 77 per text encoder

### Train-Infer Consistency

- **train_infer_length_match**: Matched at 77; long user prompts truncated
- **mismatch_effects_reported**: DetailMaster: SDXL far below T5 models on ~285-token prompts
- **length_extrapolation_beyond_training**: Chunking / ParaDiffusion / ELLA-style adapters

### Re-prompt / Recaption

- **uses_reprompt**: no
- **reprompt_model**: N/A
- **reprompt_output_length_train**: N/A
- **reprompt_output_length_infer**: N/A
- **rewrite_is_default_on**: no
- **reprompt_motivation**: N/A

### Empirical Findings and Motivation

- **length_ablation_results**: DetailMaster: ParaDiffusion (SDXL backbone, 512-token training) beats DeepFloyd with same capacity but conventional training — dense long training > capacity alone
- **quality_vs_length_findings**: Dual CLIP helps quality vs SD1 but does not solve long prompts
- **motivation_or_rationale**: Dual encoders improve representation quality within the same 77-token budget rather than extending length
- **key_quotes**: DetailMaster: Dense prompt training matters more than increasing token capacity.
- **practical_recommendation**: SDXL remains a 77-token system; for long prompts either rewrite into 77 tokens or use long-prompt fine-tunes/adapters with matching train/infer lengths.

### Uncertain fields

- caption_length_randomization
- short_prompt_regression

---

## TIPO and Input-Side Inference Scaling

### Identity

- **name**: TIPO and Input-Side Inference Scaling
- **year**: 2024-2025
- **organization**: TIPO / input-side scaling authors
- **model_type**: re-prompt rewriter research
- **paper_or_source**: TIPO: Text to Image with Text Presampling for Prompt Optimization; Improving Text-to-Image Generation with Input-Side Inference-Time Scaling
- **arxiv_id**: 2411.08127; 2510.12041
- **primary_url**: https://arxiv.org/abs/2411.08127

### Text Encoder Limits

- **text_encoder**: Model-agnostic rewriters upstream of frozen T2I backbones
- **max_token_length_architecture**: Inherited from target T2I encoder
- **effective_token_length**: Rewriter expands toward training text distribution length
- **tokenizer**: Depends on rewriter LLM
- **truncation_or_padding_policy**: Must respect backbone token limit after rewrite

### Training Prompt Length

- **train_prompt_length_tokens**: TIPO cites curated large caption corpora (30M-pair / 40B-token scale) as target distribution
- **train_caption_length_distribution**: Rewriter aims to match training caption distribution rather than arbitrary verbosity
- **train_caption_source**: Large caption corpora for TIPO; DPO preference data for input-side scaling paper
- **caption_length_randomization**: N/A
- **recommended_train_prompt_length**: Whatever the backbone was trained on — rewriter should target that length/style

### Inference Prompt Length

- **infer_prompt_length_tokens**: Expanded from short user prompts toward training distribution
- **infer_prompt_length_words**: Longer than typical user prompts
- **recommended_user_prompt_length**: Short allowed; rewriter expands
- **api_or_hard_limit**: Backbone limit

### Train-Infer Consistency

- **train_infer_length_match**: Primary goal of rewriting: close train/user distributional gap including length
- **mismatch_effects_reported**: Input-side scaling attributes gains to training/user distributional gap; rewriters transfer across T2I backbones
- **short_prompt_regression**: Addressed by expansion
- **length_extrapolation_beyond_training**: Should not rewrite longer than backbone/training support

### Re-prompt / Recaption

- **uses_reprompt**: yes
- **reprompt_model**: TIPO; iterative DPO rewriter (2510.12041)
- **reprompt_output_length_train**: N/A
- **reprompt_output_length_infer**: Expanded prompts matching training caption length/style; TIPO deliberately expands rather than fully unconstrained rewrite; reports up to 29.4% runtime improvement and 62.8% human win rate
- **rewrite_is_default_on**: Research/optional component
- **reprompt_motivation**: Match training text distribution; inference-time scaling on the input side without retraining T2I

### Empirical Findings and Motivation

- **length_ablation_results**: Transfer across backbones without rewriter retraining (2510.12041)
- **quality_vs_length_findings**: Length alone insufficient — FaithRewriter warns text-only rewriters can hallucinate impossible details; reward models may hack verbosity
- **motivation_or_rationale**: User prompts ≠ training captions in length and style; fixing inputs is cheaper than retraining diffusion
- **key_quotes**: TIPO frames the goal as matching the training text distribution; input-side scaling shows rewriters transfer across T2I backbones.
- **practical_recommendation**: Set rewriter output length/style to the backbone's training caption distribution (not maximized verbosity), and keep final tokens within the encoder limit.

### Uncertain fields

- train_prompt_length_words

---

## i1 Open Recipe

### Identity

- **name**: i1 Open Recipe
- **year**: 2026
- **organization**: i1 authors (open recipe paper)
- **model_type**: diffusion T2I model + ablation study
- **paper_or_source**: i1: A Simple and Fully Open Recipe for Strong Text-to-Image Models
- **arxiv_id**: 2606.11289
- **primary_url**: https://arxiv.org/abs/2606.11289

### Text Encoder Limits

- **text_encoder**: T5Gemma-2B (encoder); ablations vs FG-CLIP2, Qwen3, Qwen3-VL
- **max_token_length_architecture**: Right truncation to 256 tokens for T5Gemma; FG-CLIP2 truncated to 196
- **effective_token_length**: 256 used throughout final recipe
- **tokenizer**: T5Gemma tokenizer
- **truncation_or_padding_policy**: Right truncation (mainstream practice); pad as implemented in training stack

### Training Prompt Length

- **train_prompt_length_tokens**: Long synthetic captions only in final recipe ("Describe the image in detail using one paragraph."); short-caption mixes ablated
- **train_prompt_length_words**: Example long captions ~77-170+ words shown; distributions in Fig.14/48/49
- **train_caption_length_distribution**: Long-only for final i1; Table 5 sweeps % long captions 0/20/.../100%
- **train_caption_source**: Qwen3-VL-30B-A3B synthetic captions
- **caption_length_randomization**: Ablated mixes of short+long; final choice: long-only + inference rewrite
- **recommended_train_prompt_length**: Train on long captions (within 256-token truncation)

### Inference Prompt Length

- **infer_prompt_length_tokens**: Match training: expand short prompts via LLM rewrite (or naive 12× repetition as diagnostic)
- **infer_prompt_length_words**: Rewritten GenEval prompts much longer than originals
- **recommended_user_prompt_length**: If users write short prompts, rewrite them to long distribution before generation
- **api_or_hard_limit**: 256 tokens truncation

### Train-Infer Consistency

- **train_infer_length_match**: Explicit thesis: training captions and inference prompts should have aligned lengths
- **mismatch_effects_reported**: Long-caption model on original GenEval: 0.17; after repeating short prompt 12×: 0.49; after LLM rewrite: 0.73
- **short_prompt_regression**: Severe when trained long-only and tested short (0.17 GenEval)
- **length_extrapolation_beyond_training**: Not primary; focus on short-infer mismatch

### Re-prompt / Recaption

- **uses_reprompt**: yes
- **reprompt_model**: Qwen3-4B with simple meta-prompt to expand short prompts
- **reprompt_output_length_train**: N/A (training uses VLM captions, not rewriter)
- **reprompt_output_length_infer**: Expanded to roughly match long training caption length distribution (Fig.14)
- **rewrite_is_default_on**: yes
- **reprompt_motivation**: Increase inference prompt length to match long training distribution rather than training short to match users

### Empirical Findings and Motivation

- **length_ablation_results**: Long+rewrite (0.73) beats any short-caption training variant on GenEval; short training helps original short prompts but weaker overall
- **quality_vs_length_findings**: Train long > train short overall, conditional on lengthening inference prompts
- **motivation_or_rationale**: Distributional alignment of sequence length between train captions and inference prompts is load-bearing for scores
- **key_quotes**: Even when inference prompts are originally short, it is preferable to train on long captions and increase the inference prompt length to match the training distribution (e.g., via prompt rewriting), rather than training on short captions to match the original inference prompt length.
- **practical_recommendation**: Train long (≤256 tokens here) and always lengthen short user prompts at inference with an LLM rewriter to match that length.

---
