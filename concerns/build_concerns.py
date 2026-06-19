#!/usr/bin/env python3
"""
Generate concerns/*.yaml from the editorial concerns tool's matrixData.
Source: /home/rik/Documents/github/knowledge-management/webs/ideation/tool/index.html
Schema: ../schema/concept.schema.json

Run: python concerns/build_concerns.py
Output: concerns/{id}.yaml (one file per concept)
"""

import re
import json
import yaml
from pathlib import Path

TOOL_HTML = Path("/home/rik/Documents/github/knowledge-management/webs/ideation/tool/index.html")
OUT_DIR = Path(__file__).parent

# ── Layer mapping ──────────────────────────────────────────────────────────────

LAYER_MAP = {
    "1. Functional Layer":                        "functional",
    "2. Computational Layer (AI/Tokenomics)":     "computational",
    "3. Mechanical Layer":                        "mechanical",
    "4. Structural Layer (Logic & Boundaries)":   "structural",
    "5. Editorial Layer":                         "editorial",
}

# ── D2 Compositional stage by layer ───────────────────────────────────────────

COMP_STAGE = {
    "functional":    ["post-compositional"],
    "computational": ["compositional", "post-compositional"],
    "mechanical":    ["post-compositional"],
    "structural":    ["compositional", "post-compositional"],
    "editorial":     ["post-compositional"],
}

# ── D3 Scale by concept id ─────────────────────────────────────────────────────

SCALE = {
    "func-link-integrity":  ["document-level"],
    "func-link-relevance":  ["document-level"],
    "func-media-load":      ["document-level"],
    "func-media-context":   ["paragraph-level", "document-level"],
    "comp-token-budget":    ["document-level", "system-level"],
    "comp-chunkability":    ["paragraph-level", "document-level"],
    "comp-density":         ["sentence-level", "paragraph-level"],
    "micro-grammar":        ["sentence-level"],
    "micro-orthography":    ["word-level"],
    "micro-punctuation":    ["word-level", "sentence-level"],
    "micro-tangled":        ["sentence-level"],
    "micro-concision":      ["word-level", "sentence-level"],
    "struct-precision":     ["word-level"],
    "struct-strawman":      ["paragraph-level", "document-level"],
    "struct-adhominem":     ["paragraph-level", "document-level"],
    "struct-falsedilemma":  ["paragraph-level"],
    "struct-cohesion":      ["sentence-level", "paragraph-level"],
    "struct-coherence":     ["paragraph-level", "document-level"],
    "struct-signposting":   ["sentence-level", "paragraph-level"],
    "struct-voltas":        ["paragraph-level", "document-level"],
    "struct-clause":        ["sentence-level"],
    "struct-paragraph":     ["paragraph-level"],
    "struct-section":       ["document-level"],
    "struct-discrete-doc":  ["document-level"],
    "struct-system-arch":   ["system-level"],
    "struct-unity":         ["paragraph-level", "document-level"],
    "struct-toc":           ["document-level"],
    "struct-index":         ["document-level"],
    "struct-annotations":   ["document-level"],
    "struct-glossary":      ["document-level"],
    "style-rhetorical":     ["document-level"],
    "style-localization":   ["document-level"],
    "style-compliance":     ["document-level"],
    "style-tone":           ["document-level"],
    "style-typography":     ["document-level"],
    "style-scannability":   ["paragraph-level", "document-level"],
    "style-layout-nits":    ["document-level"],
}

# ── D4 Concern type by concept id ─────────────────────────────────────────────

CONCERN_TYPE = {
    "func-link-integrity":  ["technical"],
    "func-link-relevance":  ["technical"],
    "func-media-load":      ["technical"],
    "func-media-context":   ["technical"],
    "comp-token-budget":    ["computational"],
    "comp-chunkability":    ["computational"],
    "comp-density":         ["computational"],
    "micro-grammar":        ["grammatical"],
    "micro-orthography":    ["grammatical"],
    "micro-punctuation":    ["grammatical"],
    "micro-tangled":        ["grammatical"],
    "micro-concision":      ["grammatical", "stylistic"],
    "struct-precision":     ["logical"],
    "struct-strawman":      ["logical", "rhetorical"],
    "struct-adhominem":     ["logical", "rhetorical"],
    "struct-falsedilemma":  ["logical", "rhetorical"],
    "struct-cohesion":      ["logical"],
    "struct-coherence":     ["logical"],
    "struct-signposting":   ["architectural"],
    "struct-voltas":        ["architectural"],
    "struct-clause":        ["grammatical", "logical"],
    "struct-paragraph":     ["architectural"],
    "struct-section":       ["architectural"],
    "struct-discrete-doc":  ["architectural"],
    "struct-system-arch":   ["architectural"],
    "struct-unity":         ["logical", "architectural"],
    "struct-toc":           ["architectural"],
    "struct-index":         ["architectural"],
    "struct-annotations":   ["architectural"],
    "struct-glossary":      ["architectural"],
    "style-rhetorical":     ["rhetorical"],
    "style-localization":   ["stylistic"],
    "style-compliance":     ["stylistic"],
    "style-tone":           ["rhetorical", "stylistic"],
    "style-typography":     ["stylistic"],
    "style-scannability":   ["stylistic", "architectural"],
    "style-layout-nits":    ["stylistic"],
}

# ── D7 Writing stage: from address_when onward ────────────────────────────────

STAGE_ORDER = ["prewriting", "drafting", "revising", "peer-review", "editing", "publishing"]

def writing_stages(address_when):
    try:
        return STAGE_ORDER[STAGE_ORDER.index(address_when):]
    except ValueError:
        return [address_when]

# ── D13 Audience sensitivity (non-empty only where meaningful) ────────────────

AUDIENCE_SENSITIVITY = {
    "func-media-load":     ["screen-reader-user", "low-vision"],
    "func-media-context":  ["screen-reader-user", "low-vision", "cognitive-disability"],
    "micro-grammar":       ["second-language-learner", "cognitive-disability"],
    "micro-orthography":   ["second-language-learner"],
    "micro-tangled":       ["second-language-learner", "cognitive-disability", "domain-novice"],
    "micro-concision":     ["second-language-learner", "cognitive-disability"],
    "struct-precision":    ["second-language-learner", "domain-novice", "cognitive-disability"],
    "struct-cohesion":     ["second-language-learner", "cognitive-disability"],
    "struct-coherence":    ["second-language-learner", "cognitive-disability", "domain-novice"],
    "struct-signposting":  ["cognitive-disability", "domain-novice"],
    "struct-system-arch":  ["domain-novice"],
    "style-localization":  ["cross-cultural", "second-language-learner"],
    "style-tone":          ["cross-cultural", "cognitive-disability"],
    "style-typography":    ["low-vision", "cognitive-disability"],
    "style-scannability":  ["cognitive-disability", "low-vision", "domain-novice"],
    "style-layout-nits":   ["low-vision"],
}

# ── Main ───────────────────────────────────────────────────────────────────────

def load_matrix_data():
    html = TOOL_HTML.read_text(encoding="utf-8")
    m = re.search(r"const matrixData\s*=\s*(\[.*?\]);", html, re.DOTALL)
    if not m:
        raise RuntimeError("matrixData not found in HTML")
    return json.loads(m.group(1))


def build_entry(c):
    cid = c["id"]
    layer = LAYER_MAP.get(c.get("layer", ""), "")
    aw = c.get("address_when", "")

    entry = {}
    entry["title"] = c["elementName"]
    entry["description"] = c.get("technicalDefinition", "")

    if c.get("also_known_as"):
        entry["also_known_as"] = c["also_known_as"]

    entry["wordnet"] = {
        "term": cid.split("-", 1)[-1].replace("-", " "),
        "definitions": [],
        "synonyms": [],
        "related_forms": [],
    }

    clf = {}
    if layer:
        clf["layer"] = layer
    stage = COMP_STAGE.get(layer, [])
    clf["stage"] = stage[0] if len(stage) == 1 else stage
    scale = SCALE.get(cid, [])
    clf["scale"] = scale[0] if len(scale) == 1 else scale
    ct = CONCERN_TYPE.get(cid, [])
    clf["concern_type"] = ct[0] if len(ct) == 1 else ct
    if c.get("evaluator"):
        clf["evaluator"] = c["evaluator"][0] if len(c["evaluator"]) == 1 else c["evaluator"]
    clf["determinism"] = c.get("determinism", "")
    ws = writing_stages(aw)
    clf["writing_stage"] = ws[0] if len(ws) == 1 else ws
    clf["address_when"] = aw
    if c.get("impact"):
        clf["impact"] = c["impact"][0] if len(c["impact"]) == 1 else c["impact"]
    clf["risk_severity"] = c.get("risk_severity", "")
    if c.get("responsible_role"):
        rr = c["responsible_role"]
        clf["responsible_role"] = rr[0] if len(rr) == 1 else rr
    aud = AUDIENCE_SENSITIVITY.get(cid)
    if aud:
        clf["audience_sensitivity"] = aud[0] if len(aud) == 1 else aud

    entry["classification"] = clf
    entry["relationships"] = {}
    entry["diagnostic_question"] = c.get("diagnostic_question", "")

    if c.get("evaluation_tools"):
        entry["evaluation_tools"] = c["evaluation_tools"]

    return entry


def main():
    data = load_matrix_data()
    written = []
    for c in data:
        entry = build_entry(c)
        out_path = OUT_DIR / f"{c['id']}.yaml"
        with open(out_path, "w", encoding="utf-8") as f:
            yaml.dump(entry, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
        written.append(c["id"])
    print(f"Written {len(written)} concept files to {OUT_DIR}/")
    for cid in written:
        print(f"  {cid}.yaml")


if __name__ == "__main__":
    main()
