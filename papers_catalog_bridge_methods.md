# Papers Catalog — User→Generator Bridge Methods

**Дата:** 2026-07-31  
**Полный отчёт:** [`report_bridge_methods_taxonomy.md`](./report_bridge_methods_taxonomy.md)  
**Корпус:** [`research/bridge-methods/corpus/bridge_methods_corpus.json`](./research/bridge-methods/corpus/bridge_methods_corpus.json)

Приоритет: 1 = must · 2 = strong · 3 = context · 4 = peripheral

---

## F1 — Textual external rewrite

| Pri | arXiv | Paper | Зачем читать |
|-----|-------|-------|--------------|
| 1 | `2509.04545` | PromptEnhancer | Decoupled CoT rewriter + 24-keypoint reward |
| 1 | `2606.00204` | APE (NVIDIA) | Small LM agents; router / no_rewrite |
| 1 | `2607.18724` | TARA | Typed repair + accept-or-revert |
| 1 | `2512.16853` | GenEval 2 | Rewriting can hurt human alignment |
| 2 | `2510.12041` | Input-Side Scaling | PE as portable scaling |
| 2 | `2505.17540` | RePrompt | RL + structured self-reflection |
| 2 | `2606.08492` | FaithRewriter | Visual anchors vs textual hallucination |
| 2 | `2506.23138` | VisualPrompter | Atomic visual repair |
| 3 | `2212.09611` | Promptist | Ancestor RL PE |
| 3 | `2503.20314` | Wan | Lab formulation: align to train captions |

---

## F2 — Embeddings / adapters / soft prompts

| Pri | arXiv | Paper | Зачем читать |
|-----|-------|-------|--------------|
| 1 | `2403.05135` | ELLA | Frozen-generator LLM connector + DPG-Bench |
| 1 | `2406.11831` | LI-DiT | Why naive LLM-as-encoder fails |
| 1 | `2302.03668` | PEZ | Soft vs hard prompts; projected optimization |
| 1 | `2511.06876` | FIBO / DimFusion | Embedding-dim fusion for long structured captions |
| 2 | `2305.05189` | SUR-adapter | Short casual prompts without emitting rewrite |
| 2 | `2308.06721` | IP-Adapter | Image prompt as bridge |
| 2 | `2305.17216` | GILL | Minimal mapper between frozen LLM and SD |
| 2 | `2504.06256` | MetaQueries | Learnable queries MLLM→diffusion |
| 2 | `2407.01606` | DPO-Diff | Gradient discrete prompt opt for diffusion |
| 2 | `2510.02599` | PEO | Training-free embedding opt vs rewriting |
| 3 | `2208.01618` | Textual Inversion | Soft-prompt foundation |
| 3 | `2305.15391` | NeTI | Depth×time soft prompts (anticipates ELLA) |
| 3 | `2204.06125` | unCLIP / DALL·E 2 | Text→image embedding prior |
| 3 | `2602.03510` | Semantic Routing | Which LLM layer(s) to bridge from |
| 3 | `2403.07860` | LaVi-Bridge | Arbitrary LM × vision model |

---

## F3 — Layout / plan

| Pri | arXiv | Paper | Зачем читать |
|-----|-------|-------|--------------|
| 1 | `2305.13655` | LMD | Canonical boxes bridge; 99% layouts vs 76% images |
| 1 | `2401.11708` | RPG | Recaption+Plan+Generate hybrid |
| 1 | `2602.11980` | SCoT | **Bridge-type ablation** text CoT vs boxes |
| 1 | `2301.07093` | GLIGEN | Layout executor / grounded adapter |
| 2 | `2607.16409` | ATLAS | Layout as shared Think/Plan/Paint representation |
| 2 | `2512.05112` | DraCo | Draft-as-CoT with self-verify |
| 2 | `2603.08652` | CoCo | Code-as-CoT (verifiable plan) |
| 2 | `2512.11464` | MetaCanvas | Plan in spatial latent space |
| 2 | `2510.24133` | ReFocus | Layout + sample-efficient TTS |
| 2 | `2403.13589` | ReGround | Spatial can suppress textual grounding |
| 2 | `2311.17002` | Ranni | Semantic panel middleware |
| 3 | `2307.10816` | BoxDiff | Training-free box constraints |
| 3 | `2405.08246` | BlobGEN | Blobs between boxes and masks |
| 3 | `2410.12669` | 3DIS | Depth as portable layout indirection |
| 3 | `2404.01197` | SPRIGHT | Data-level spatial caption fix |
| 3 | `2406.10210` | Make It Count | Counting without layout |
| 3 | `2508.12919` | 7Bench | Joint semantic+spatial eval of layout methods |

---

## F4 — Schema / JSON

| Pri | arXiv / src | Paper | Зачем читать |
|-----|-------------|-------|--------------|
| 1 | `2511.06876` | FIBO | Full schema-native system + TaBR |
| 1 | `2602.20672` | BBQ-to-Image | Parametric gap; numeric bbox+RGB |
| 1 | `2507.05300` | Structured Captions 19M | Structure vs shuffle ablation |
| 1 | Ideogram blog/docs | Ideogram 4 | Exclusive JSON + Magic Prompt compiler |
| 2 | `2304.06720` | Rich Text | Ancestor: continuous attrs in text UI |
| 3 | Ideogram prompting.md | CaptionVerifier | Hard schema reject at inference |

---

## F5 — Endogenous CoT

| Pri | arXiv | Paper | Зачем читать |
|-----|-------|-------|--------------|
| 1 | `2505.00703` | T2I-R1 | Bi-level semantic/token CoT + RL |
| 1 | `2601.20305` | SEER | Cognitive Gap; 300-sample endogenous loop |
| 1 | `2510.05593` | ShortCoTI | Visual overthinking — CoT can hurt |
| 2 | `2509.23951` | HunyuanImage 3 | Native CoT at foundation scale |
| 2 | `2511.22699` | Z-Image | PE-aware SFT (align generator to PE) |
| 2 | `2603.02712` | CoR-Painter | How-to-draw before what-to-draw |
| 2 | `2601.10332` | Think-Then-Generate | Hybrid: rewrite embeddings + Dual-GRPO |
| 3 | `2503.10639` | GoT | Generation CoT with coordinates |

---

## F6 — Non-text action space

| Pri | arXiv | Paper | Зачем читать |
|-----|-------|-------|--------------|
| 1 | `2301.13826` | Attend-and-Excite | GSN; fix neglect without rewrite |
| 1 | `2603.00483` | RAISE | Mixed actions + requirement checklist |
| 1 | `2510.00430` | PromptLoop | Latent-conditioned stepwise refine |
| 2 | `2404.04095` | PAE | Weights + timesteps as actions |
| 2 | `2311.16117` | Predicated Diffusion | Logic over attention as fuzzy predicates |
| 2 | `2306.08877` | SynGen | Syntactic binding via attention loss |
| 2 | `2512.07702` | NPC | Automated negative prompting; cites 8 hubs |
| 2 | `2406.04312` | ReNO | Optimize initial noise vs rewards |
| 3 | `2208.01626` | Prompt-to-Prompt | Attention maps as editable binding |
| 3 | `2505.21488` | Be Decisive | External layout vs noise-induced prior |

---

## Surveys (framing)

| Pri | arXiv | Title |
|-----|-------|-------|
| 1 | `2403.04279` | Controllable Generation with T2I Diffusion Models |
| 1 | `2606.08231` | Test-Time Scaling in Multimodal Foundation Models |
| 2 | `2502.16923` | Automatic Prompt Optimization Techniques |
| 2 | `2502.11560` | APO: Optimization Perspective (discrete/continuous/hybrid) |
| 2 | `2503.12605` | Multimodal Chain-of-Thought Reasoning Survey |
| 2 | `2505.02567` | Unified Multimodal Understanding and Generation |
| 2 | `2508.10316` | Integrating RL with Visual Generative Models |
| 3 | `2406.06608` | The Prompt Report |

---

## Маршрут 2 дня (минимум)

1. Taxonomy report §0–3  
2. SCoT · ELLA · LMD · FIBO/BBQ · T2I-R1/SEER · RAISE · GenEval 2  

Полный 4-дневный маршрут — в §7 отчёта.
