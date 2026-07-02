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
    "style-rhetorical":              ["document-level"],
    "style-localization":            ["document-level"],
    "style-compliance":              ["document-level"],
    "style-tone":                    ["document-level"],
    "style-typography":              ["document-level"],
    "style-scannability":            ["paragraph-level", "document-level"],
    "style-layout-nits":             ["document-level"],
    # Supplementary concepts
    "func-code-doc-drift":           ["document-level", "system-level"],
    "struct-completeness":           ["document-level"],
    "func-faq-antipattern":          ["document-level"],
    "func-source-integrity":         ["document-level"],
    "comp-rendering-fidelity":       ["document-level", "system-level"],
    "func-metadata-complete":        ["document-level"],
    "func-accessibility-compliance": ["document-level", "system-level"],
    "func-seo-discoverability":      ["document-level", "system-level"],
    "func-version-integrity":        ["document-level", "system-level"],
    "func-translation-pipeline":     ["document-level", "system-level"],
    "comp-hallucination-risk":       ["sentence-level", "paragraph-level", "document-level"],
    "comp-retrieval-writing":        ["paragraph-level", "document-level"],
    "comp-embedding-quality":        ["paragraph-level", "document-level"],
    "comp-context-window":           ["document-level", "system-level"],
    "micro-parallel-structure":      ["sentence-level", "paragraph-level"],
    "struct-definition-complete":    ["word-level", "document-level"],
    "func-citation-complete":        ["sentence-level", "document-level"],
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
    "style-rhetorical":              ["rhetorical"],
    "style-localization":            ["stylistic"],
    "style-compliance":              ["stylistic"],
    "style-tone":                    ["rhetorical", "stylistic"],
    "style-typography":              ["stylistic"],
    "style-scannability":            ["stylistic", "architectural"],
    "style-layout-nits":             ["stylistic"],
    # Supplementary concepts
    "func-code-doc-drift":           ["technical"],
    "struct-completeness":           ["architectural"],
    "func-faq-antipattern":          ["architectural"],
    "func-source-integrity":         ["technical"],
    "comp-rendering-fidelity":       ["technical"],
    "func-metadata-complete":        ["technical"],
    "func-accessibility-compliance": ["technical"],
    "func-seo-discoverability":      ["technical"],
    "func-version-integrity":        ["technical"],
    "func-translation-pipeline":     ["technical"],
    "comp-hallucination-risk":       ["computational", "technical"],
    "comp-retrieval-writing":        ["computational", "architectural"],
    "comp-embedding-quality":        ["computational"],
    "comp-context-window":           ["computational"],
    "micro-parallel-structure":      ["grammatical"],
    "struct-definition-complete":    ["logical", "architectural"],
    "func-citation-complete":        ["technical", "logical"],
}

# ── D7 Writing stage: from address_when onward ────────────────────────────────

STAGE_ORDER = ["prewriting", "drafting", "revising", "peer-review", "editing", "publishing"]

def writing_stages(address_when):
    try:
        return STAGE_ORDER[STAGE_ORDER.index(address_when):]
    except ValueError:
        return [address_when]

# ── D10 Impact overrides (fixes pre-v0.5.0 stale `accessibility` value) ──────

IMPACT_OVERRIDE = {
    "func-media-load":    ["rendering", "reader-trust", "accessibility-technical", "accessibility-presentation"],
    "struct-toc":         ["reader-comprehension", "accessibility-technical"],
    "struct-index":       ["reader-comprehension", "accessibility-technical"],
    "struct-glossary":    ["reader-comprehension", "accessibility-cognitive"],
    "style-typography":   ["accessibility-presentation", "rendering", "reader-comprehension"],
    "style-scannability": ["reader-comprehension", "accessibility-cognitive", "seo-discoverability"],
    "style-layout-nits":  ["rendering", "accessibility-presentation"],
}

# ── D13 Audience sensitivity (non-empty only where meaningful) ────────────────

AUDIENCE_SENSITIVITY = {
    "func-media-load":                 ["screen-reader-user", "low-vision"],
    "func-media-context":              ["screen-reader-user", "low-vision", "cognitive-disability"],
    "func-accessibility-compliance":   ["screen-reader-user", "low-vision", "cognitive-disability"],
    "func-translation-pipeline":       ["cross-cultural", "second-language-learner"],
    "micro-grammar":                   ["second-language-learner", "cognitive-disability"],
    "micro-orthography":               ["second-language-learner"],
    "micro-tangled":                   ["second-language-learner", "cognitive-disability", "domain-novice"],
    "micro-concision":                 ["second-language-learner", "cognitive-disability"],
    "micro-parallel-structure":        ["second-language-learner", "cognitive-disability"],
    "struct-precision":                ["second-language-learner", "domain-novice", "cognitive-disability"],
    "struct-cohesion":                 ["second-language-learner", "cognitive-disability"],
    "struct-coherence":                ["second-language-learner", "cognitive-disability", "domain-novice"],
    "struct-signposting":              ["cognitive-disability", "domain-novice"],
    "struct-system-arch":              ["domain-novice"],
    "struct-definition-complete":      ["domain-novice", "second-language-learner"],
    "comp-hallucination-risk":         ["domain-novice"],
    "style-localization":              ["cross-cultural", "second-language-learner"],
    "style-tone":                      ["cross-cultural", "cognitive-disability"],
    "style-typography":                ["low-vision", "cognitive-disability"],
    "style-scannability":              ["cognitive-disability", "low-vision", "domain-novice"],
    "style-layout-nits":               ["low-vision"],
}

# ── Supplementary concepts (not in upstream HTML; added to schema directly) ───

SUPPLEMENTARY_CONCEPTS = [
    # Ghost concepts: referenced in wqo_links with no existing yaml
    {
        "id": "func-code-doc-drift",
        "elementName": "Code-Documentation Drift",
        "technicalDefinition": (
            "The progressive divergence of documentation from the codebase or system it describes, "
            "caused by code changes that are not reflected in accompanying documentation."
        ),
        "layer": "1. Functional Layer",
        "address_when": "publishing",
        "evaluator": ["automated", "human-technical-qa"],
        "determinism": "risk-factor",
        "impact": ["reader-trust", "rag-retrieval"],
        "risk_severity": "functional",
        "responsible_role": ["author", "technical-qa", "publisher"],
        "diagnostic_question": (
            "Does the documentation reflect the current behavior, API, or architecture "
            "of the system it describes?"
        ),
    },
    {
        "id": "struct-completeness",
        "elementName": "Structural Completeness",
        "technicalDefinition": (
            "The degree to which a document contains all sections and elements required "
            "by its type — no missing prerequisites in a tutorial, no undocumented "
            "parameters in a reference entry."
        ),
        "layer": "4. Structural Layer (Logic & Boundaries)",
        "address_when": "revising",
        "evaluator": ["human-structural-editor", "automated"],
        "determinism": "rule-violation",
        "impact": ["reader-comprehension", "reader-trust"],
        "risk_severity": "functional",
        "responsible_role": ["structural-editor", "author"],
        "diagnostic_question": (
            "Does this document contain all sections required by its genre and topic type?"
        ),
    },
    {
        "id": "func-faq-antipattern",
        "elementName": "FAQ Antipattern",
        "technicalDefinition": (
            "The use of a FAQ (Frequently Asked Questions) format as a substitute for "
            "well-structured base documentation; FAQs signal that the primary documentation "
            "fails to answer reader questions at the natural point of need."
        ),
        "layer": "1. Functional Layer",
        "address_when": "prewriting",
        "evaluator": ["human-information-architect", "human-structural-editor"],
        "determinism": "risk-factor",
        "impact": ["reader-comprehension", "seo-discoverability"],
        "risk_severity": "credibility",
        "responsible_role": ["information-architect", "structural-editor", "author"],
        "diagnostic_question": (
            "Is this FAQ answering questions that should be answered in the primary "
            "documentation structure?"
        ),
    },
    {
        "id": "func-source-integrity",
        "elementName": "Source Integrity",
        "technicalDefinition": (
            "The degree to which claims in a document are traceable to authoritative, "
            "verifiable, and current sources; source integrity fails when claims cannot "
            "be attributed, sources are outdated, or references are fabricated."
        ),
        "layer": "1. Functional Layer",
        "address_when": "drafting",
        "evaluator": ["human-structural-editor", "human-peer-reviewer"],
        "determinism": "risk-factor",
        "impact": ["reader-trust", "author-credibility"],
        "risk_severity": "credibility",
        "responsible_role": ["author", "peer-reviewer", "structural-editor"],
        "diagnostic_question": (
            "Can every non-trivial claim in this document be traced to a verifiable, "
            "current source?"
        ),
    },
    # Publishing stage concerns
    {
        "id": "comp-rendering-fidelity",
        "elementName": "Rendering Fidelity",
        "technicalDefinition": (
            "The degree to which content renders correctly and completely across its "
            "target output formats — HTML, PDF, ePub, mobile — without layout corruption, "
            "missing elements, or format-specific display failures."
        ),
        "layer": "2. Computational Layer (AI/Tokenomics)",
        "address_when": "publishing",
        "evaluator": ["automated", "human-technical-qa"],
        "determinism": "rule-violation",
        "impact": ["rendering", "accessibility-presentation"],
        "risk_severity": "functional",
        "responsible_role": ["technical-qa", "publisher"],
        "diagnostic_question": (
            "Does this content render correctly across all its target output formats?"
        ),
    },
    {
        "id": "func-metadata-complete",
        "elementName": "Metadata Completeness",
        "technicalDefinition": (
            "The presence and accuracy of all machine-readable metadata required for "
            "discovery, sharing, and indexing: page title, meta description, Open Graph "
            "tags, schema.org markup, and canonical URL."
        ),
        "layer": "1. Functional Layer",
        "address_when": "publishing",
        "evaluator": ["automated", "human-technical-qa"],
        "determinism": "rule-violation",
        "impact": ["seo-discoverability", "reader-trust"],
        "risk_severity": "functional",
        "responsible_role": ["publisher", "technical-qa"],
        "diagnostic_question": (
            "Does every published page have a complete and accurate set of metadata "
            "required for indexing and social sharing?"
        ),
    },
    {
        "id": "func-accessibility-compliance",
        "elementName": "Accessibility Compliance",
        "technicalDefinition": (
            "Conformance to WCAG 2.1/2.2 success criteria at the publishing stage: "
            "all non-decorative images have alt text, text contrast meets AA minimums, "
            "interactive components are keyboard-navigable, and content is navigable "
            "by screen reader."
        ),
        "layer": "1. Functional Layer",
        "address_when": "publishing",
        "evaluator": ["automated", "human-technical-qa"],
        "determinism": "rule-violation",
        "impact": ["accessibility-technical", "accessibility-presentation", "accessibility-cognitive"],
        "risk_severity": "functional",
        "responsible_role": ["technical-qa", "publisher", "information-architect"],
        "diagnostic_question": (
            "Does this published content meet WCAG 2.1 Level AA success criteria?"
        ),
    },
    {
        "id": "func-seo-discoverability",
        "elementName": "SEO and Discoverability",
        "technicalDefinition": (
            "The degree to which published content is indexable, findable, and accurately "
            "represented in search results: correct robots.txt configuration, canonical "
            "URL consistency, valid sitemap, and structured data markup."
        ),
        "layer": "1. Functional Layer",
        "address_when": "publishing",
        "evaluator": ["automated", "human-technical-qa"],
        "determinism": "risk-factor",
        "impact": ["seo-discoverability", "reader-trust"],
        "risk_severity": "functional",
        "responsible_role": ["publisher", "technical-qa"],
        "diagnostic_question": (
            "Is this content correctly indexed, canonicalized, and represented "
            "in search results?"
        ),
    },
    {
        "id": "func-version-integrity",
        "elementName": "Version Integrity",
        "technicalDefinition": (
            "The guarantee that published content matches the reviewed, approved draft: "
            "no post-review edits bypass approval, version-tagged documentation matches "
            "the tagged code release, and the correct version is served to the correct audience."
        ),
        "layer": "1. Functional Layer",
        "address_when": "publishing",
        "evaluator": ["automated", "human-technical-qa"],
        "determinism": "risk-factor",
        "impact": ["reader-trust", "rag-retrieval"],
        "risk_severity": "functional",
        "responsible_role": ["publisher", "technical-qa"],
        "diagnostic_question": (
            "Does the published content exactly match the reviewed and approved version?"
        ),
    },
    {
        "id": "func-translation-pipeline",
        "elementName": "Translation Pipeline Quality",
        "technicalDefinition": (
            "The correctness of the localization production process: source strings "
            "extracted without corruption, machine translation reviewed before publish, "
            "all locales receive translated content (no silent English fallback), and "
            "locale-specific formatting (date, currency, number) is applied correctly."
        ),
        "layer": "1. Functional Layer",
        "address_when": "publishing",
        "evaluator": ["automated", "human-technical-qa"],
        "determinism": "risk-factor",
        "impact": ["reader-comprehension", "reader-trust", "accessibility-cognitive"],
        "risk_severity": "functional",
        "responsible_role": ["publisher", "technical-qa", "author"],
        "diagnostic_question": (
            "Has every locale received correctly translated, reviewed content with "
            "locale-specific formatting applied?"
        ),
    },
    # Computational layer
    {
        "id": "comp-hallucination-risk",
        "elementName": "Hallucination Risk",
        "technicalDefinition": (
            "The risk that AI-assisted writing introduces unverifiable, fabricated, or "
            "confidently stated false claims — particularly in factual passages, code "
            "examples, API parameter descriptions, or citations — without the author "
            "detecting them."
        ),
        "layer": "2. Computational Layer (AI/Tokenomics)",
        "address_when": "drafting",
        "evaluator": ["human-peer-reviewer", "human-technical-qa", "automated"],
        "determinism": "risk-factor",
        "impact": ["reader-trust", "author-credibility", "rag-retrieval"],
        "risk_severity": "functional",
        "responsible_role": ["author", "peer-reviewer", "technical-qa", "ai-tool"],
        "diagnostic_question": (
            "Have all factual claims, code examples, and citations in AI-assisted "
            "content been independently verified?"
        ),
    },
    {
        "id": "comp-retrieval-writing",
        "elementName": "Retrieval-Oriented Writing",
        "technicalDefinition": (
            "The practice of structuring content so it can be accurately retrieved by "
            "embedding-based or keyword search systems: self-contained chunks, explicit "
            "context in headings, terminology consistency, and controlled vocabulary."
        ),
        "layer": "2. Computational Layer (AI/Tokenomics)",
        "address_when": "prewriting",
        "evaluator": ["automated", "human-information-architect"],
        "determinism": "risk-factor",
        "impact": ["rag-retrieval", "seo-discoverability"],
        "risk_severity": "functional",
        "responsible_role": ["author", "information-architect", "ai-tool"],
        "diagnostic_question": (
            "Would a retrieval system return this content accurately in response to "
            "the questions it is designed to answer?"
        ),
    },
    {
        "id": "comp-embedding-quality",
        "elementName": "Embedding Quality",
        "technicalDefinition": (
            "The degree to which a text chunk produces a vector embedding that accurately "
            "represents its semantic content — determined by controlled vocabulary, "
            "consistent terminology, minimal noise, and adequate semantic density."
        ),
        "layer": "2. Computational Layer (AI/Tokenomics)",
        "address_when": "revising",
        "evaluator": ["automated", "ai-tool"],
        "determinism": "risk-factor",
        "impact": ["rag-retrieval"],
        "risk_severity": "functional",
        "responsible_role": ["ai-tool", "author", "technical-qa"],
        "diagnostic_question": (
            "Would the embedding of this text place it near semantically related "
            "content in vector space?"
        ),
    },
    {
        "id": "comp-context-window",
        "elementName": "Context Window Planning",
        "technicalDefinition": (
            "The deliberate composition of content to fit within AI model context window "
            "constraints, ensuring that all information required for accurate model "
            "response is present within the context budget without exceeding it."
        ),
        "layer": "2. Computational Layer (AI/Tokenomics)",
        "address_when": "prewriting",
        "evaluator": ["automated", "ai-tool"],
        "determinism": "risk-factor",
        "impact": ["rag-retrieval", "rendering"],
        "risk_severity": "functional",
        "responsible_role": ["author", "ai-tool", "information-architect"],
        "diagnostic_question": (
            "Is all information required for model comprehension present within "
            "the context window budget?"
        ),
    },
    # Mechanical / structural
    {
        "id": "micro-parallel-structure",
        "elementName": "Parallel Structure",
        "technicalDefinition": (
            "The grammatical requirement that items in a list, series, or paired "
            "construction share the same syntactic form — all noun phrases, all "
            "infinitives, all clauses — to reduce processing load and signal "
            "equivalent logical status."
        ),
        "layer": "3. Mechanical Layer",
        "address_when": "revising",
        "evaluator": ["human-line-editor", "automated"],
        "determinism": "rule-violation",
        "impact": ["reader-comprehension", "accessibility-cognitive"],
        "risk_severity": "cosmetic",
        "responsible_role": ["line-editor", "self-editor", "copy-editor"],
        "diagnostic_question": (
            "Do all items in this list, heading series, or paired construction "
            "share the same grammatical form?"
        ),
    },
    {
        "id": "struct-definition-complete",
        "elementName": "Definition Completeness",
        "technicalDefinition": (
            "The requirement that every term of art, acronym, or domain-specific "
            "concept introduced in a document is defined at or before its first use, "
            "ensuring readers can engage with the content without external reference."
        ),
        "layer": "4. Structural Layer (Logic & Boundaries)",
        "address_when": "revising",
        "evaluator": ["human-line-editor", "automated"],
        "determinism": "rule-violation",
        "impact": ["reader-comprehension", "accessibility-cognitive"],
        "risk_severity": "functional",
        "responsible_role": ["author", "line-editor", "structural-editor"],
        "diagnostic_question": (
            "Is every term of art and acronym defined at or before its first use?"
        ),
    },
    {
        "id": "func-citation-complete",
        "elementName": "Citation Completeness",
        "technicalDefinition": (
            "The requirement that all claims requiring attribution — quoted material, "
            "empirical data, regulatory requirements, standards references — include a "
            "verifiable citation that enables readers to locate the source."
        ),
        "layer": "1. Functional Layer",
        "address_when": "revising",
        "evaluator": ["human-peer-reviewer", "human-structural-editor", "automated"],
        "determinism": "rule-violation",
        "impact": ["reader-trust", "author-credibility"],
        "risk_severity": "credibility",
        "responsible_role": ["author", "peer-reviewer", "structural-editor"],
        "diagnostic_question": (
            "Do all claims requiring attribution have a verifiable citation?"
        ),
    },
]

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
    raw_impact = IMPACT_OVERRIDE.get(cid) or c.get("impact")
    if raw_impact:
        clf["impact"] = raw_impact[0] if len(raw_impact) == 1 else raw_impact
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
    data = load_matrix_data() + SUPPLEMENTARY_CONCEPTS
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
