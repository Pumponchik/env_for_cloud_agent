#!/usr/bin/env python3
"""Generate markdown report from T2I prompt-length research JSON results."""
from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
FIELDS_PATH = ROOT / "fields.yaml"
RESULTS_DIR = ROOT / "results"
OUT_PATH = ROOT / "report.md"

SKIP_KEYS = {"_source_file", "uncertain"}
NESTED_TOP = {
    "basic_info", "Basic Info", "Identity",
    "technical_features", "Text Encoder Limits",
    "Training Prompt Length", "Inference Prompt Length",
    "Train-Infer Consistency", "Re-prompt / Recaption",
    "Empirical Findings and Motivation",
}


def load_fields():
    data = yaml.safe_load(FIELDS_PATH.read_text())
    cats = []
    for cat in data.get("field_categories", []):
        cats.append((cat["category"], [f["name"] for f in cat.get("fields", [])]))
    return cats


def is_uncertain(name, value, uncertain_list):
    if name in uncertain_list:
        return True
    if value is None or value == "":
        return True
    if isinstance(value, str) and "[uncertain]" in value:
        return True
    return False


def fmt_value(value):
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, list):
        if not value:
            return ""
        if all(isinstance(x, dict) for x in value):
            lines = []
            for item in value:
                lines.append(" | ".join(f"{k}: {v}" for k, v in item.items()))
            return "<br>".join(lines)
        if len(value) <= 5:
            return ", ".join(map(str, value))
        return "<br>".join(f"- {x}" for x in value)
    if isinstance(value, dict):
        return "; ".join(f"{k}: {v}" for k, v in value.items())
    s = str(value)
    if len(s) > 100:
        return s
    return s


def flatten(data):
    flat = {}
    for k, v in data.items():
        if k in SKIP_KEYS:
            continue
        if isinstance(v, dict) and (k in NESTED_TOP or k.endswith("Info")):
            for kk, vv in v.items():
                flat[kk] = vv
        else:
            flat[k] = v
    return flat


def slugify(name: str) -> str:
    s = name.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def main():
    cats = load_fields()
    files = sorted(RESULTS_DIR.glob("*.json"))
    items = []
    for f in files:
        data = json.loads(f.read_text())
        flat = flatten(data)
        uncertain = set(data.get("uncertain") or [])
        items.append((f.stem, flat, uncertain))

    lines = []
    lines.append("# Prompt Length for Diffusion Text-to-Image Models")
    lines.append("")
    lines.append(
        "Research synthesis on **training prompt length**, **inference prompt length**, "
        "and **re-prompt/recaption output length**, with author motivations."
    )
    lines.append("")
    lines.append("## Table of Contents")
    lines.append("")
    for i, (stem, flat, _) in enumerate(items, 1):
        name = flat.get("name", stem)
        year = flat.get("year", "")
        rec = flat.get("practical_recommendation", "")
        if isinstance(rec, str) and len(rec) > 90:
            rec = rec[:87] + "..."
        lines.append(f"{i}. [{name}](#{slugify(name)}) — {year} | {rec}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Direct answers section first
    lines.append("## Direct answers (cross-paper)")
    lines.append("")
    lines.append("### 1. At what length should the model be trained?")
    lines.append("")
    lines.append("- **CLIP/SD1/SDXL era:** within **77 tokens**; short web alt-text historically ~10–20 tokens (COCO 10.5, CC12M 20.2, DataComp 10.22).")
    lines.append("- **Dense-caption CLIP fine-tunes:** still ≤77, but use **short+long mix (RECAP 50/50)** or **random lengths** (How-to-Train, arXiv 2506.16679).")
    lines.append("- **T5/PixArt lineage:** raise encoder with caption density — **120 (PixArt-α) → ~300 (PixArt-Σ)**.")
    lines.append("- **FLUX-class / i1:** long captions with truncation **~256–512 tokens** (i1: 256; FLUX.1/2 often 512).")
    lines.append("- **Extreme structured:** FIBO-scale **~1000 tokens/words** (mean ~1160 tokens).")
    lines.append("- **Wide-band randomization:** HunyuanImage 3.0 samples **30–1000 words**.")
    lines.append("- **Consensus:** train on captions **at least as dense/long as the prompts you care about at inference**; capacity alone (77→512) without dense data is weaker than dense training (DetailMaster).")
    lines.append("")
    lines.append("### 2. At what length should inference run?")
    lines.append("")
    lines.append("- **Match the training caption length distribution** (i1 Table 5; TIPO; Wan/video reports same principle).")
    lines.append("- If users write short prompts but the model was trained long: **rewrite/expand at inference** (DALL·E 3, i1, Qwen `prompt_extend`, FLUX.2 upsampler).")
    lines.append("- Diagnostic (i1): GenEval **0.17** (short) → **0.49** (repeat 12×) → **0.73** (LLM rewrite) for a long-caption-trained model.")
    lines.append("- Long-prompt benchmarks (~285 tokens, DetailMaster) still stress even FLUX/SD3.5; accuracy falls as length grows past ~250–400 tokens.")
    lines.append("- Product limits examples: **Imagen 4 = 480 tokens**; Qwen Image API ~**800–1300**; CLIP path hard **77**.")
    lines.append("")
    lines.append("### 3. Re-prompt / recaption output length (train & infer)")
    lines.append("")
    lines.append("- **Offline recaption (train):** Recap-DataComp `max_new_tokens=128` → mean **49.43** tokens (vs 10.22 alt-text); PixArt/Share-Captioner denser for 120–300 windows; FIBO structured ~1000; Hunyuan 30–1000 words.")
    lines.append("- **Online re-prompt (infer):** target the **same distribution as training captions**, not max verbosity (TIPO; PromptEnhancer; FaithRewriter warns about hallucination/reward-hacked length).")
    lines.append("- **Concrete modern defaults:** FLUX.2 upsampler `max_new_tokens=512`; Qwen prompt extend default-on toward encoder/API budget (~512–1300).")
    lines.append("- **DALL·E 3 pattern:** train on long synthetic captions; at inference always upsample short user prompts (`revised_prompt`).")
    lines.append("")
    lines.append("### 4. Why (motivations repeated across papers)")
    lines.append("")
    lines.append("1. **Train–infer distribution match** (especially length) dominates reported metrics.")
    lines.append("2. **Short noisy alt-text underteaches** composition/attributes; dense captions improve alignment.")
    lines.append("3. **Encoder capacity is necessary but not sufficient** — dense long training matters more (DetailMaster).")
    lines.append("4. **Long-only training makes short user prompts OOD** unless you randomize train lengths or rewrite at infer.")
    lines.append("5. **Padding mechanics:** very short prompts fill 77 with EOT pads that can dominate (Padding Tone / memorization <40 tokens).")
    lines.append("")
    lines.append("---")
    lines.append("")

    for stem, flat, uncertain in items:
        name = flat.get("name", stem)
        lines.append(f"## {name}")
        lines.append("")
        for cat_name, field_names in cats:
            block = []
            for fn in field_names:
                if fn not in flat:
                    continue
                val = flat[fn]
                if is_uncertain(fn, val, uncertain):
                    continue
                block.append((fn, val))
            if not block:
                continue
            lines.append(f"### {cat_name}")
            lines.append("")
            for fn, val in block:
                lines.append(f"- **{fn}**: {fmt_value(val)}")
            lines.append("")
        extra = [k for k in flat.keys() if all(k not in fs for _, fs in cats) and k not in SKIP_KEYS]
        if extra:
            lines.append("### Other Info")
            lines.append("")
            for k in extra:
                if is_uncertain(k, flat[k], uncertain):
                    continue
                lines.append(f"- **{k}**: {fmt_value(flat[k])}")
            lines.append("")
        if uncertain:
            lines.append("### Uncertain fields")
            lines.append("")
            for u in sorted(uncertain):
                lines.append(f"- {u}")
            lines.append("")
        lines.append("---")
        lines.append("")

    OUT_PATH.write_text("\n".join(lines))
    print(f"Wrote {OUT_PATH} ({OUT_PATH.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
