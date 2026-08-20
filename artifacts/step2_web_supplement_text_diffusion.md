# Step 2 — Web supplement (merged from searches + agents)

**Topic:** Diffusion models for text  
**Date:** 2026-08-20  
**Time range used:** since 2023, emphasize 2024–2026

## Supplementary Items (beyond Step 1)

- **Scaling Masked Diffusion Models on Text (2410.18514):** bridge from MDLM-scale to ~1B before LLaDA.
- **LLaDA-V / LLaDA 1.5 / LLaDA-MoE:** multimodal, preference (VRPO), MoE efficiency follow-ups.
- **RND1 / LLaDA2.0 (cited in dLLM framework):** larger AR→diffusion / block-level scaling mentions.
- **Soft-Masked Diffusion LMs (2510.17206):** soft corruption revisit.
- **Why mask diffusion does not work (2510.03289):** critical stress-test thread.
- **CDLM / consistency diffusion LMs:** block-wise consistency + KV cache post-training.
- **Infinite Mask Diffusion for Few-Step Distillation (2605.10518):** few-step frontier.
- **Edit-Based Refinement for Parallel MDM (2605.09603):** edit/refinement inference.
- **Dynamic Chunking for DLMs (2605.15676):** long-context engineering.
- **Commitment Before Realization / CFG unnecessary (2608.08082):** guidance schedule science.
- **dLLM unified framework (2602.22661):** tooling as research object.
- **Awesome-DLMs curated list:** living bibliography for 2025–2026 inference papers.

## Recommended Supplementary Fields

- `bits_per_byte` — fair tokenizer comparisons
- `nfe_vs_quality_curve` — mandatory systems evidence
- `block_size` — hybrid DOF
- `unmask_policy_name` — inference identity
- `remask_enabled` / `remask_budget_nfe`
- `cfg_schedule` (constant vs late vs adaptive)
- `train_infer_mask_mismatch` — distribution distance proxy
- `init_from_ar_checkpoint` — scaling path label
- `industrial_closed_details` — flag for non-reproducible claims

## Active frontiers (2025–2026)

1. Unmasking / remasking / learned decode policies  
2. Block hybrids + KV cache  
3. Few-step distillation  
4. CFG schedules & commitment  
5. AR-adaptation vs from-scratch scaling  
6. dMLLM / alignment for diffusion  
7. Product throughput (Mercury-class)

## Sources

- https://arxiv.org/abs/2502.09992 (LLaDA)
- https://arxiv.org/abs/2406.07524 (MDLM)
- https://arxiv.org/abs/2406.04329 (MD4)
- https://arxiv.org/abs/2503.09573 (BD3-LM)
- https://arxiv.org/abs/2505.22618 (Fast-dLLM)
- https://arxiv.org/abs/2506.13759 (Discrete diffusion survey)
- https://arxiv.org/abs/2508.10875 (DLM survey)
- https://arxiv.org/abs/2506.17298 (Mercury)
- https://arxiv.org/abs/2508.15487 (Dream)
- https://arxiv.org/abs/2410.17891 (DiffuLLaMA)
- https://github.com/VILA-Lab/Awesome-DLMs
