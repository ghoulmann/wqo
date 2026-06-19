# WQO Design Reference

Full design rationale for the Writing Quality Ontology — schema decisions, two-layer architecture, problem catalog structure, and ecosystem context. See `README.md` for the quick overview.

---

## The 13 Dimensions

The core schema (`schema/concept.schema.json` v0.5.0) classifies any writing-quality concern across 13 independent dimensions:

| Dimension | Field | What it encodes |
|---|---|---|
| D1 | `layer` | Which editorial layer owns it (functional → editorial) |
| D2 | `stage` | Where in the writing lifecycle it applies |
| D3 | `scale` | What unit of text it operates on |
| D4 | `concern_type` | Logical, grammatical, rhetorical, architectural… |
| D5 | `evaluator` | Who or what can detect it |
| D6 | `determinism` | Rule-violation vs. risk-factor vs. philosophy |
| D7 | `writing_stage` | When in the writing process it's active (descriptive) |
| D8 | `address_when` | Earliest stage at which addressing it is not premature (triage) |
| D9 | `engineering_stage` | Analogous stage in the engineering design process |
| D10 | `impact` | Downstream consequences when the concern fails |
| D11 | `risk_severity` | Cosmetic / functional / credibility / safety |
| D12 | `responsible_role` | Who owns fixing it |
| D13 | `audience_sensitivity` | Reader populations with elevated risk above the D11 baseline |

D8 (`address_when`) is the triage dimension — it encodes the earliest stage at which a concern should be raised. Surfacing mechanical concerns before structural ones are resolved is counterproductive; the dimension makes that sequencing machine-readable.

D13 is additive to D11: D11 gives the general-reader severity baseline; D13 names the populations for whom risk is higher.

---

## Five Editorial Layers

WQO concerns are organized into five layers (D1), ordered from highest to lowest abstraction:

| Layer | Prefix | What it owns |
|---|---|---|
| Functional | `func-` | Purpose, audience, task completion |
| Computational | `comp-` | AI/tokenomics, machine consumption, RAG quality |
| Structural | `struct-` | Logic, argumentation, information architecture |
| Mechanical | `micro-` | Grammar, syntax, punctuation, orthography |
| Editorial | `style-` | House style, voice, typography, localization |

Triage runs top-down: don't address mechanical concerns while structural ones are unresolved.

---

## Two-Layer Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  WQO TEXT QUALITY LAYER                                     │
│  schema/concept.schema.json  (13 dimensions, D1–D13)        │
│  concerns/                   (individual concept nodes)     │
│                                                             │
│  37 concerns × 5 editorial layers                           │
│  functional → computational → structural →                  │
│  mechanical → editorial                                     │
│                                                             │
│  "How does text fail?"                                      │
└────────────────────────┬────────────────────────────────────┘
                         │
                  wqo_links + system_boundary
                         │
┌────────────────────────▼────────────────────────────────────┐
│  OPERATIONAL PROBLEMS LAYER                                 │
│  schema/problem.schema.json                                 │
│  problems/problems.yaml  (96 entries, 10 domain categories) │
│                                                             │
│  "Where in the lifecycle does the failure occur?"           │
└─────────────────────────────────────────────────────────────┘
```

These are distinct abstraction layers. "The paragraph lacks a clear topic sentence" is a WQO concern (`unity`). "The CI pipeline doesn't check for paragraph unity" is a problem (P-15). Merging them would conflate intrinsic text properties with process and tooling failures.

The bridge between layers is `wqo_links` (on each problem entry) and `system_boundary` (which lifecycle stage the problem manifests in). A single problem may link to multiple WQO concerns; a single concern may be linked by multiple problems.

---

## The 96 Problems

`problems/problems.yaml` catalogs operational failure modes — process, tooling, and governance gaps that produce or allow content failures:

| Domain | Range | What fails |
|---|---|---|
| documentation-drift | P-01–P-14 | Content diverges from the systems it describes |
| quality-defects | P-15–P-29 | Text is present but fails readers and machines |
| migration | P-30–P-37 | Platform transitions corrupt or orphan content |
| governance | P-38–P-46 | Ownership, review, and policy structures break down |
| tool-defects | P-47–P-61 | Automation code has bugs or gaps |
| ai-ml-limitations | P-62–P-68 | AI systems are constrained by data and architecture |
| hitl-evaluation | P-69–P-72 | Human review processes produce low-signal results |
| hardware-infrastructure | P-73–P-78 | Compute or storage constraints block quality tooling |
| organizational | P-79–P-85 | Human behavior and incentives undermine documentation |
| pipeline-process | P-86–P-96 | Automation pipelines fail silently or structurally |

### Problem entry structure

Each entry is a solutions-guide record — not a user story (which strips causal mechanism) or FAQ (which is itself P-26's anti-pattern):

```yaml
id: P-XX
title: Short display name
problem_statement: What fails and the observable symptom (1–3 sentences)
causal_mechanism: Why it occurs — the root cause or missing gate
domain_category: High-level grouping
system_boundary: authoring | versioning | build-publish | consumption | governance | infrastructure
impact: [WQO impact vocabulary]
risk_severity: cosmetic | functional | credibility | safety
resolution_pattern: Short name for the fix archetype
wqo_links: [WQO concern IDs that address this]
project_links: [{name, path, relationship}]
```

### Production context

The 96 problems are an example instantiation, not a universal enumeration. They represent failure modes observed in one specific context:

| Dimension | This instantiation |
|---|---|
| Organisation type | Enterprise knowledge engineering team |
| Document domain | Technical and software documentation |
| Production method | Docs-as-Code (VCS + CI pipeline + SSG) |
| Audience | Internal teams and external developers |

Other contexts — legal publishing, academic journals, regulatory filing, news organisations, standards bodies — would produce a parallel problem set under the same `problem.schema.json` schema with different statements and resolution patterns. The schema is general; the 96 problems are one org's worked example.

---

## `system_boundary` — the lifecycle bridge

`system_boundary` appears in `problem.schema.json` as the field that positions each problem in the documentation lifecycle:

| Value | When it manifests |
|---|---|
| `authoring` | While the author is writing — WQO concerns are most applicable here |
| `versioning` | At VCS/commit/PR time — CI gates and drift checks apply |
| `build-publish` | SSG build, migration, CI/CD — tooling defects and compliance gaps |
| `consumption` | At read time by humans or machines — quality defects and RAG failures |
| `governance` | Ownership, review, policy — organizational and process failures |
| `infrastructure` | Hardware and platform constraints |

`concept.schema.json` v0.5.0 does not yet have this field. A planned v0.6.0 update adds `system_boundary` as D14 so WQO concerns can also be lifecycle-positioned.

---

## Tool Types

`tool-types/tool-types.yaml` (schema: `schema/tool-type.schema.json`) provides a controlled vocabulary of instrument categories spanning all eras and media:

| Category | What it covers |
|---|---|
| `digital-software` | Linters, VCS, CMS, AI assistants, spell checkers |
| `method-framework` | Style guides, IA frameworks, genre analysis, evaluation rubrics |
| `physical-analog` | Typewriters, correction fluid, moveable type, manuscript markup |
| `platform-infrastructure` | Git forges, collaboration platforms, project management |

Each entry carries `stage[]` (writing stage affinity, aligned with D7) and `persona[]` (production role affinity, aligned with D12). Tool types are referenced by concern nodes via `evaluation_tools`.

---

## Ecosystem and Project Map

Which projects serve which problem clusters:

| Project | Relevant problems | What it does |
|---|---|---|
| [rhetor-linter](https://github.com/ghoulmann/rhetor-linter) | P-15–P-23, P-48–P-49, P-66, P-74–P-75, P-82, P-91, P-96 | Text quality detection; rule coverage mapped to WQO concern IDs |
| [jtbd-tool](https://github.com/ghoulmann/jtbd-tool) | P-07, P-08, P-26, P-28, P-64 | Genre and persona gap discovery |
| knowledge-management ideation tool | P-15–P-29 | Browser for 37 concerns across 5 layers |
| [quartz-site](https://ghoulmann.github.io/word) | All concerns | Navigable typed-relationship graph |
| [dateline](https://github.com/ghoulmann/dateline) | P-01, P-38 | CAMEO event pattern; structural template for WQO |

### Coverage gaps

**P-15–P-23 (quality-defects)** — rhetor-linter covers coherence, unity, cohesion, sentence length, headings, readability. Gaps: false dilemma (P-23), trade-off analysis (P-23), heading-to-content coherence (P-17, partial).

**P-07, P-08, P-26, P-28 (genre mismatches)** — jtbd-tool handles gap discovery; structural genre linting is not yet implemented.

**P-01, P-04, P-10, P-11, P-62 (drift/staleness)** — no current tool. Resolution pattern: CI gate comparing code and docs.

**P-38–P-46 (governance)** — no current tool; requires platform-level integration.

**P-73–P-78 (hardware)** — not addressable by text tooling; requires model architecture decisions.
