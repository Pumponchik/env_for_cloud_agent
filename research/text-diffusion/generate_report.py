#!/usr/bin/env python3
"""Generate a compact markdown report from text-diffusion deep-research JSONs."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
OUT = ROOT / "report.md"


def load_items():
    items = []
    for path in sorted(RESULTS.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        data["_source_file"] = path.name
        items.append(data)
    return items


def skip(val, uncertain_list, key):
    if key in uncertain_list:
        return True
    if val is None or val == "":
        return True
    if isinstance(val, str) and "[uncertain]" in val:
        return True
    return False


def main():
    items = load_items()
    lines = [
        "# Text Diffusion — Deep Research Report",
        "",
        f"Items: **{len(items)}** · Source: `research/text-diffusion/results/`",
        "",
        "## Table of contents",
        "",
    ]
    for i, it in enumerate(items, 1):
        name = it.get("name", it["_source_file"])
        year = it.get("year", "?")
        mtype = it.get("model_type", "")
        anchor = name.lower().replace(" ", "-").replace("/", "").replace(",", "")
        lines.append(f"{i}. [{name}](#{anchor}) — {year} | {mtype}")

    lines += ["", "---", ""]

    fields_prefer = [
        ("Identity", ["name", "year", "organization", "model_type", "paper_or_source", "arxiv_id", "primary_url"]),
        ("Representation", ["state_space", "corruption_process", "time_formulation", "noise_or_mask_schedule", "absorbing_token"]),
        ("Training", ["parameterization", "training_objective", "architecture_backbone", "init_from_ar", "scale_params", "conditioning_mechanism"]),
        ("Inference", ["sampling_algorithm", "typical_num_steps", "unmasking_or_remasking_policy", "guidance_methods", "claimed_throughput"]),
        ("Evidence", ["reported_benchmarks", "strengths_claimed", "known_failure_modes", "isolation_quality"]),
        ("DOF relevance", ["primary_dofs_touched", "sota_claim_summary", "remaining_ambiguity", "suggested_followup_experiment", "practical_takeaway"]),
    ]

    for it in items:
        name = it.get("name", it["_source_file"])
        uncertain = set(it.get("uncertain") or [])
        lines.append(f"## {name}")
        lines.append("")
        for cat, keys in fields_prefer:
            block = []
            for k in keys:
                if k not in it:
                    continue
                if skip(it[k], uncertain, k):
                    continue
                block.append(f"- **{k}**: {it[k]}")
            if block:
                lines.append(f"### {cat}")
                lines.extend(block)
                lines.append("")
        if uncertain:
            lines.append("### Uncertain fields")
            for u in sorted(uncertain):
                lines.append(f"- {u}")
            lines.append("")
        lines.append("---")
        lines.append("")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT} ({len(items)} items)")


if __name__ == "__main__":
    main()
