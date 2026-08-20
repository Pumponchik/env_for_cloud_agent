# How to Build the User→Generator Bridge: Re-Prompt System Architecture (2025–2026)

**Date:** 2026-07-29  
**Scope:** Modern (mostly 2025–2026) academic answer to: *why a re-prompter is needed*, *what structure should sit between the user and the generator*, *what degrees of freedom exist*, and *how to do it correctly*.  
**Companion (earlier, broader digest):** [`report_reprompt_systems.md`](./report_reprompt_systems.md)  
**Paper catalog:** см. связанные отчёты в этом репозитории.

> **Method note.** Built from fresh arXiv sweeps (2024–2026), citation ancestry/descendants of current PE hubs, lab tech reports (Qwen-Image-2.0, Wan, Seedream/Seedance, HunyuanImage 3.0, FLUX.2, Ideogram 4), and three parallel literature agents.  
> `www.derevutstat.ru` did not resolve; search used arXiv / Semantic Scholar / OpenReview / ACL / primary lab docs.  
> **Important negative finding:** there is still **no dedicated survey** of T2I re-prompt systems. Closest reviews are LLM-centric APO surveys (`2502.16923`, `2502.11560`, `2502.18746`) and multimodal test-time scaling (`2606.08231`). The architecture below is synthesized from primary papers, not from one existing handbook.

---

## 0. Direct answer (read this first)

### Why do we need a re-prompter?

Because the **user utterance and the generator’s training text live in different distributions**, and the generator must fill the gap somehow. Left alone, it fills arbitrarily (average aesthetics, wrong physics, missing counts). A re-prompter is the component that **explicitly manages that gap** instead of leaving it to chance.

Modern papers name **six different problems** (not one). Choosing which one you solve decides the architecture:

| # | Problem formulation | Typical 2025–26 source |
|---|---------------------|-------------------------|
| F1 | Train↔user **caption distribution mismatch** | Wan, TIPO, RAPO++, DetailMaster |
| F2 | Underspecification → **arbitrary detail completion** / “average user” bias | FIBO |
| F3 | Enumerable **fine-grained failure modes** (binding, negation, counting, …) | PromptEnhancer (24 keypoints), TARA |
| F4 | Text-only rewrite is **fluent but visually unrealizable** (textual hallucination) | FaithRewriter |
| F5 | External rewriter↔generator **representation mismatch** | SEER / Endogenous Reprompting |
| F6 | Re-prompt as **input-side inference-time scaling** | Input-Side Scaling, PRIS |

### What should sit between user prompt and generator?

There is **no single “correct” wire format**. The 2026 consensus is:

1. **The generator dictates the wire format** (what it was trained to consume).  
2. **Structure often lives inside the bridge** (JSON fields, DSG atoms, typed repairs), while the **wire** is usually prose — *unless* the generator is JSON-native (FIBO, Ideogram 4).  
3. **Always-on uniform expansion is wrong.** Gate: skip / light-touch / typed repair / full rewrite / accept-or-revert.

### Degrees of freedom (the real design space)

| DoF | Options | 2026 default |
|-----|---------|--------------|
| **Wire IR** | prose · JSON schema · layout/boxes · weighted tokens · continuous embeddings · internalized CoT | Prose for frozen SD/FLUX/Qwen-class; JSON only if co-trained |
| **Internal IR** | flat text · FIBO-like fields · DSG atoms · typed repairs · evolving spec | Prefer **internal structure**, prose on the wire |
| **Length** | fixed short · fixed long · variable · match train histogram | **Match generator train distribution**; not “as long as possible” |
| **Trigger** | always-on · default-on · opt-in · length-adaptive · failure-gated | **Gated** (TARA / APE / Ideogram AUTO) |
| **Coupling** | model-agnostic rewriter · generator-coupled PE · endogenous CoT | Agnostic for APIs; coupled for owned models |
| **Feedback** | none · train-time visual · test-time visual · latent | Visual at train or one gated test-time pass |
| **Objective** | faithfulness · aesthetics · diversity · safety | Separate modes; never one scalar aesthetic reward |
| **Action** | expand · append · typed repair · re-seed · no-rewrite | Portfolio, not one operator |

---

## 1. History of the area (direction of motion) — separate track

This section is **developmental context**, not the design answer.

**2021–2022 — HCI / modifiers.**  
Prompt writing is manual. Oppenlaender’s modifier taxonomy and CHI design guidelines establish *slots* (subject, style, quality boosters), not systems.

**2022–2023 — First automation.**  
Promptist (SFT→PPO, aesthetic+CLIP reward) defines the method template. DALL·E 3 Better Captions independently creates the *theory*: train on long synthetic captions → short user text is OOD → GPT “upsample”. BeautifulPrompt industrializes aesthetic RL. These are **foundational**, but their objective (beautify / lengthen) is exactly what 2026 papers show can *hurt* semantics.

**2023–2024 — Closed loops & alternatives.**  
OPT2I (iterative consistency), Idea2Img (VLM self-refine), LMD/RPG (layout instead of prose), PAE (weights+timesteps), Prompt Expansion (diversity). The field discovers that **scalar rewards are too coarse** and that the bridge need not be plain text.

**2025 — Industrial PE modules + RL rewriters.**  
Wan / Seedance / Qwen / Hunyuan / FLUX ship prompt_extend / PE / upsampling. Academic: TIPO (distribution alignment), RePrompt (reasoning+RL), PromptEnhancer (24-keypoint reward), VisualPrompter (atomic visual repair), Input-Side Scaling (DPO, transferability), RAPO++ (retrieval+test-time+distill), FIBO (JSON-native generator).

**2026 — Diagnosis, gating, structure, internalization.**  
FaithRewriter (visual anchors, anti-hallucination), TARA (typed repair allocation + accept-or-revert), APE (router→field rewriters→composer + `no_rewrite`), PRISM (self-rewarding), SEER (endogenous), GenEval 2 (rewriting can *lower* human alignment), SCOPE/BBQ (spec / numeric structured language).

**Direction of travel:**  
`always lengthen` → `match train distribution` → `diagnose then repair` → `gate when not needed` → either **JSON-native generators** or **structure-inside / prose-on-wire** → optionally **absorb PE into the generator’s CoT**.

---

## 2. Why a re-prompter is needed (modern formulations)

### 2.1 Distribution mismatch (F1)

Generators are trained on **dense, long, often synthetic captions**. Users type **short, underspecified** text. Wan states the objective almost as a definition of PE:

> align refined prompts with the **distribution of training captions**.

DetailMaster: COCO ~10.5 tokens, CC12M ~20.2 — far below what modern long-caption training uses. RAPO++ shows that *good* PE length histograms hug the **training** histogram; methods that overshoot with ornate vocabulary can be counterproductive.

**Design implication:** the re-prompter’s target is a **caption law**, not “more adjectives”.

### 2.2 Arbitrary completion / average preference (F2)

FIBO: short prompts force the model to **guess**; preference tuning then pulls guesses toward an “AI aesthetic” average. Professionals lose precision and disentangled control.

**Design implication:** if you need control, the bridge may need a **schema** (JSON fields), not denser prose.

### 2.3 Failure taxonomy (F3)

PromptEnhancer: 24 keypoints / 6 categories. A CLIP score cannot tell “fix wrong” from “count wrong”. TARA: each failure type needs **different repair language**; one uniform expansion is a degenerate policy.

**Design implication:** either train against a **decomposed reward**, or **route repairs by type**.

### 2.4 Textual hallucination (F4)

FaithRewriter: high textual likelihood with near-zero visual realizability. Example — upside-down glass of water rewritten into floating water. Blind expansion **pollutes intent**.

**Design implication:** preference pairs must be **length-matched expansions**; visual grounding (at least at training time) beats text-only critique.

### 2.5 Coupling debate (F5)

SEER: disjoint LLM+generator causes **representation mismatch**. PromptEnhancer / Input-Side Scaling: decoupling is a **feature** (transfer across backbones).

**Design implication:** unresolved. Practical rule — agnostic PE for third-party APIs; endogenous/coupled PE when you own the generator.

### 2.6 Input-side scaling (F6)

If you cannot unify output-side test-time compute across generators, optimizing the **prompt** is the portable axis. PRIS: holding the prompt fixed while scaling visuals hits a plateau.

---

## 3. The bridge: structural shapes in 2025–2026

Canonical pipeline:

```
user_prompt  x
    │
    ├─[gate: already good / already long / user Off?]──► pass-through
    │
    ▼
 internal reasoning IR   (optional: CoT, JSON fields, DSG atoms, typed repairs)
    │
    ▼
 wire artifact  y        (what the generator actually consumes)
    │
    ▼
 generator G(y) → image
    │
    └─[optional: score vs x; accept or revert]
```

### Shape A — Monolithic CoT rewriter → prose wire
**PromptEnhancer, RePrompt, Qwen-Image-2.0 PE, many lab `prompt_extend`s.**  
SFT on (short, CoT?, long) then RL (GRPO/DPO) against visual reward.  
Best when: frozen black-box generator, underspecified user text.

### Shape B — Diagnose → Allocate → Compile → Adopt
**TARA.**  
Atomic failures → type-conditioned repair operators → fuse → one extra generation → accept iff better than raw.  
Best when: you can afford ~1–2 generations and care about **net semantic gain**.

### Shape C — Router → field rewriters → composer
**APE MAPE.**  
FIBO-like semantic fields; router may set `no_rewrite`; composer emits **one prose paragraph** (JSON is scaffolding).  
Best when: compositional prompts and editing; small deployable enhancers.

### Shape D — Schema is the interface (JSON on the wire)
**FIBO, Ideogram 4, BBQ-to-Image.**  
Generator trained **only** (or primarily) on structured captions. Short text → VLM → JSON → (user edits) → generate.  
Best when: you control training and need disentangled, reproducible control.  
**Wrong** when: generator was trained on prose (FLUX/SD class) — Ideogram docs literally warn plain text “will not work”.

### Shape E — Layout / plan side-channel
**LMD, RPG, ReFocus, MetaCanvas, DraCo.**  
Bridge emits boxes, regions, latent plans, or draft images — not (only) prose.  
Best when: counts, spatial layout, multi-object scenes dominate.

### Shape F — Endogenous CoT inside the generator
**T2I-R1, HunyuanImage 3 Instruct, SEER, wan2.7 thinking_mode.**  
No external PE service; thinking/rewrite is a checkpoint behavior.  
Best when: you post-train the generator; want one model in production.

---

## 4. Intermediate representation: text vs JSON vs latent vs YAML

### 4.1 Free-form text (still the default wire format)

Emitted by most rewriters into SD/FLUX/Qwen/Hunyuan-class models.  
**Length is contested:** TARA ~18 words winning; VisualPrompter ~30; lab caps often 80–200 words / ≤77–110 for CLIP-era; FIBO ~1000 words for JSON-native models.  
**Rule:** length is a **property of the generator’s train distribution**, not a universal constant.

### 4.2 Structured JSON / schema

| System | Role of JSON |
|--------|----------------|
| **FIBO** | Wire format; ~10 fields; ~1000 words; DimFusion consumes long structure |
| **Ideogram 4** | Wire format; exclusive; strict key order; Magic Prompt produces JSON |
| **APE MAPE / StruVis / SCOPE** | **Internal** scaffold; composer emits prose |
| **Re-LAION structured captions** (`2507.05300`) | Slot order (subject/setting/aesthetics/camera) improves adherence even when content is fixed |

**When JSON is correct:** generator co-trained on that schema; you need field-level edits and reproducibility.  
**When JSON is wrong:** prose-trained generator; no schema verifier; “JSON prompting” as cargo cult.

### 4.3 Layout / scene graph / atoms

Boxes (LMD), regions (RPG), DSG propositions (VisualPrompter/TARA evaluation+routing).  
These are **control channels** or **repair variables**, not replacements for the text encoder unless the pipeline is built for them.

### 4.4 Continuous embeddings / latents

ELLA / DimFusion / PEZ / DPO-Diff: continuous or soft prompts, connectors, gradient search.  
Powerful when you own training; **not** a human-editable product PE; poor portability.

### 4.5 YAML

**No peer-reviewed T2I system uses YAML as the generator wire format** (searched 2024–2026). YAML appears only in community template tools. JSON won because constrained decoding APIs and Gemini structured outputs are JSON-schema-shaped.

### 4.6 Consensus on IR (2026)

> **Structure internally if helpful; put on the wire only what the generator was trained to read.**  
> For a typical frozen prose generator: `fields/atoms → natural language caption matching train law`.  
> For a JSON-native generator: `short text → JSON schema → generate`.  
> Latents/layouts are alternative bridges, not “the next text”.

---

## 5. Length policy: constant or not?

**Not constant across systems. Prefer variable / matched.**

Evidence:

- Brack / RECAP / Hunyuan caption synthesis: **variable** train lengths (e.g. ~30–1000 words) improve robustness.  
- RAPO++: PE output length should **track the training histogram**.  
- TIPO: explicit length tiers as **control tokens**.  
- DetailMaster / PromptMoG: longer ≠ better — adherence and diversity can fall.  
- GenEval 2 / CLIP-77 models: overlong rewrites **truncate**; put style last.  
- APE: after RL, **different generators prefer different lengths**.

**Practical policy:**

```
L_target ≈ Law(train_captions(G))
if len(user) already ≈ L_target and structured: light touch or skip
else: expand/repair toward L_target, not toward max_context
```

---

## 6. How to do it correctly (normative checklist from newest papers)

1. **State which problem (F1–F6) you solve.** Architecture follows.  
2. **Measure Δ vs raw prompt**, not only vs other PE (VisualPrompter/TARA: BeautifulPrompt can land *below* raw on DSG).  
3. **Gate.** Skip when already good/long/clear (`no_rewrite`, τ≈0.72, Ideogram AUTO). Always-on is a product choice, not a scientific default.  
4. **Decompose the objective.** Faithfulness ≠ aesthetics (Input-Side Scaling: aesthetics↑ alignment↓). Ship two modes or use multi-objective (PRISM/GDPO).  
5. **Prefer typed repair over uniform expansion** when you have failure diagnosis (TARA).  
6. **Length-match preference pairs** if you RL (FaithRewriter).  
7. **Evaluate images against the original user prompt** (GenEval 2 protocol).  
8. **Match image budget** when claiming SOTA (TARA ~1.64 gens).  
9. **Let the generator choose the wire IR.**  
10. **Fallback to original** on rewriter failure (Wan pattern).  
11. **Show `revised_prompt`** and give Off/Auto/On.  
12. **Per-backbone validation** — GenEval 2: rewriting helps some models, hurts others.

---

## 7. Reference architecture (if you build one in 2026)

For a **frozen prose T2I API** (most common case):

```
                 ┌─ Off ──────────────────────────────► G(x)
user x ──► Router ─┼─ Auto: if long/clear or score≥τ ───► G(x)  (optional reseed)
                 └─ On / needs repair
                        │
            ┌───────────┴───────────┐
            │ Internal IR (optional)│  JSON fields / DSG atoms / typed ops
            └───────────┬───────────┘
                        ▼
                 Composer → y  (prose ~ train caption law of G)
                        ▼
                 ŷ = G(y)
                        ▼
            if score(ŷ, x) ≤ score(G(x), x): revert
```

Training recipe that matches SOTA papers:

1. Build pairs by **degrading** fine captions → short user-like prompts (Qwen-Image-2.0) or captioning images as proxy users (PromptEnhancer).  
2. SFT rewriter (CoT optional; PromptEnhancer shows CoT alone ≠ win).  
3. RL with **decomposed / pairwise visual reward**; length-matched hard negatives.  
4. Calibrate **length + gate** on *your* generator.  
5. Optional second head/mode for aesthetics.

If you **own training**:

- Prefer **variable-length / structured captions** at train time (Brack, FIBO, Hunyuan).  
- Then PE becomes thinner: schema expand + gate, or endogenous CoT.

If you need **professional controllability**:

- Train JSON-native (FIBO/Ideogram path) and make the bridge a **schema expander/editor**, not a purple-prose writer.

---

## 8. Are there big studies that already do this for us?

**Partially — not as one T2I-PE handbook.**

| Work | What it systematizes | Gap |
|------|----------------------|-----|
| APO surveys `2502.16923`, `2502.11560`, `2502.18746` | Prompt optimization as search/RL over discrete/continuous/hybrid spaces | T2I is a side branch |
| Multimodal TTS survey `2606.08231` | Test-time scaling taxonomy | Mostly **output**-side |
| Controllable T2I survey `2403.04279` | Layout/spatial conditioning IRs | Not re-prompt training |
| Prompt Report `2406.06608` | Broad PE vocabulary | Catalogue, not bridge design |
| **Primary cluster 2025–26** (PromptEnhancer, Input-Side Scaling, FaithRewriter, TARA, APE, FIBO, VisualPrompter, GenEval 2) | Actual design principles | No unifying survey yet |

So: **the field has the pieces; it does not yet have one review that unifies input-side scaling × IR choice × gating.** This document is that synthesis for builders.

---

## 9. Must-read modern set (prioritize these over 2022–23 foundations)

**Architecture / correctness (P0):**  
`2607.18724` TARA · `2606.08492` FaithRewriter · `2606.00204` APE · `2509.04545` PromptEnhancer · `2510.12041` Input-Side Scaling · `2511.06876` FIBO · `2506.23138` VisualPrompter · `2512.16853` GenEval 2

**Distribution / length / IR:**  
`2411.08127` TIPO · `2510.20206` RAPO++ · `2505.16915` DetailMaster · `2507.05300` Structured Captions · `2503.20314` Wan · `2605.10730` Qwen-Image-2.0 PE · Ideogram 4 JSON docs · FLUX.2 upsampling docs

**Foundations (history only):**  
Promptist `2212.09611` · DALL·E 3 Better Captions PDF · BeautifulPrompt `2311.06752`

---

## 10. Bottom line

A re-prompter is not “an LLM that makes prompts prettier.”  
It is the **policy that maps a user utterance into the conditioning artifact the generator was trained to understand**, under constraints of **faithfulness, length law, and optional refusal to rewrite**.

The degrees of freedom are real and published. The correct 2026 move is not to pick “JSON forever” or “long prose forever,” but to:

1. fix the **problem formulation**,  
2. fix the **generator’s train caption law**,  
3. choose **wire IR = what G consumes**,  
4. put **structure in the bridge**,  
5. **gate**,  
6. optimize for **net gain vs raw**, evaluated on the **original** prompt.

---

## Artifacts

- This report: `report_reprompt_system_architecture_2026.md` (repo root)  
- Earlier digest: `report_reprompt_systems.md`  
- Fresh arXiv keep list: `research/reprompt-systems/raw_searches/arxiv_modern_pe_2024_2026.json`  
- Prior corpora / citation trees: `research/reprompt-systems/`
