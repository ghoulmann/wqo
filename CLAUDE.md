# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A pure data/schema repository — no runtime, no tests, no package manager. All "build" steps are Python generator scripts that produce YAML from source data.

Strategy and architecture are documented in `.notes/ideation.md`.

## Generators

### Concerns (`concerns/build_concerns.py`)

Reads `matrixData` from an external HTML file at `~/Documents/github/knowledge-management/webs/ideation/tool/index.html` and writes one YAML file per concept to `concerns/`.

```
python concerns/build_concerns.py
```

**The `concerns/*.yaml` files are generated — do not edit them by hand.** To change a concern's classification, edit the lookup tables inside `build_concerns.py` (SCALE, CONCERN_TYPE, AUDIENCE_SENSITIVITY, etc.), then regenerate.

### Problems (`problems/build_problems.py`)

Contains all 96 problem entries as inline Python data structures and writes `problems/problems.yaml`.

```
python problems/build_problems.py
```

Edit problem entries in `build_problems.py`, then regenerate `problems.yaml`. The YAML file is the output artifact; the Python file is the source of truth.

## Architecture: two layers

```
WQO TEXT QUALITY LAYER          concerns/*.yaml  (37 nodes, generated)
                                schema/concept.schema.json  (13 dimensions D1–D13)

        ↕  bridged via wqo_links + system_boundary

OPERATIONAL PROBLEMS LAYER      problems/problems.yaml  (96 entries, generated)
                                schema/problem.schema.json
```

**WQO concerns** (`concerns/*.yaml`) describe *how text fails* — intrinsic properties of written content. Each file's `classification` block maps to the 13 schema dimensions (layer, stage, scale, concern_type, evaluator, determinism, writing_stage, address_when, impact, risk_severity, responsible_role, audience_sensitivity). The `id` used as filename prefix (e.g. `struct-coherence`) is the canonical WQO concept ID referenced in `wqo_links`.

**Operational problems** (`problems/problems.yaml`) describe *where in the doc lifecycle failure occurs* — process, tool, and governance gaps. The `system_boundary` field (authoring → versioning → build-publish → consumption → governance → infrastructure) is the bridging dimension. The `wqo_links` array on each problem entry points to the WQO concept IDs that address it.

**Tool types** (`tool-types/tool-types.yaml`) are a supporting vocabulary of instrument categories (digital-software, method-framework, physical-analog, platform-infrastructure) referenced by concept nodes via `evaluation_tools`. Schema: `schema/tool-type.schema.json`.

## Concern ID naming convention

`{layer-prefix}-{concept}` where layer prefixes are:
- `func-` — functional layer
- `comp-` — computational layer
- `micro-` — mechanical layer
- `struct-` — structural layer
- `style-` — editorial layer

## Schema files

| File | Governs | Version |
|---|---|---|
| `schema/concept.schema.json` | `concerns/*.yaml` | v0.5.0 |
| `schema/problem.schema.json` | `problems/problems.yaml` | v1.0.0 |
| `schema/tool-type.schema.json` | `tool-types/tool-types.yaml` | v1.0.0 |

`concept.schema.json` is the authoritative reference for D1–D13 enum values used throughout `build_concerns.py`. When adding a new concern dimension or changing an enum, update the schema first, then the generator.

## `patterns/` directory

Currently empty (`.gitkeep` only). Intended for a future resolution pattern library (ci-gate, ownership-protocol, content-audit, etc.).

## Architectural lineage

WQO is a CAMEO-analogous domain ontology. CAMEO (Conflict and Mediation Event Observations) classifies geopolitical events across systematic dimensions; WQO applies the same structural approach — systematic multi-dimensional domain classification — to the literacy/composition/rhetoric/publishing/writing-tech domain. The `dateline/` project is the geopolitics instantiation of CAMEO; this repo is the literacy/rhetoric instantiation.

The current 37 concerns and 96 problems are one instantiation of a potentially much larger domain ontology. They represent the first systematized scope, not a complete enumeration of the full literacy domain.

## Ecosystem

This repo is the schema hub. Upstream and downstream neighbors:

| Direction | Repo | Relationship |
|---|---|---|
| Upstream | `knowledge-management/webs/ideation/tool/index.html` (132KB) | Data source for `build_concerns.py`; do not swap with sibling 77KB `ideation/index.html` |
| Downstream | `quartz-site/` | Publishes `lexicon/*.md` as the navigable ontology browser |
| Downstream | `rhetor-linter/` | Rule coverage mapped against WQO concern IDs |
| Downstream | `jtbd-tool/` | Gap signals from job manifest feed back to WQO coverage |
| Lineage | `dateline/` | CAMEO geopolitics instantiation; structural template for WQO |

Two WQO representations exist and are intentionally parallel (different schemas, different audiences):
- `concerns/*.yaml` — tool-facing, 13 dimensions D1–D13, used by linters
- `quartz-site/content/lexicon/*.md` — ontology-facing, includes WordNet, typed relationships, `engineering_stage`

Full ecosystem context: `~/Documents/github/wqo/.notes/ecosystem.md`
Full pipeline diagram: `~/Documents/github/writing-map/diagrams/ecosystem.mmd`
