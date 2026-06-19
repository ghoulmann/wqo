# WQO Ecosystem — Claude Session Context

This doc is Claude-facing. For the full human-navigable pipeline map see:
- `~/Documents/github/writing-map/relationships/wqo-pipeline.md`
- `~/Documents/github/writing-map/diagrams/ecosystem.mmd`

## Role of this repo

`wqo/` is the schema hub of the writing-quality ecosystem — a CAMEO-analogous domain ontology for literacy/composition/rhetoric/publishing/writing-tech.

Current scope: 37 concerns × 13 dimensions (D1–D13) + 96 operational problems. This is **one instantiation**, not a complete enumeration of the full domain.

## Two intentionally parallel representations

| Representation | Location | Audience | Fields |
|---|---|---|---|
| `concerns/*.yaml` | this repo | Tools/linters | D1–D13 classification only |
| `content/lexicon/*.md` | `quartz-site/` | Practitioners | WordNet, typed relationships, `engineering_stage`, `cascade_threshold` |

These are not competing sources of truth. The tool's CLAUDE.md explicitly lists the quartz-only dimensions as "Excluded Dimensions (Belong to Quartz Ontology Site)."

## Upstream

Data source for `build_concerns.py`: `~/Documents/github/knowledge-management/webs/ideation/tool/index.html` (132KB, enriched with 15 WQO dimension fields).

**Do not swap with the sibling** `ideation/index.html` (77KB baseline UI version). The generator intentionally reads `tool/index.html`.

## Downstream consumers

| Repo | How it consumes WQO |
|---|---|
| `quartz-site/` | Publishes `lexicon/*.md` as navigable ontology browser at `ghoulmann.github.io/word` |
| `rhetor-linter/` | Rule coverage mapped against WQO concern IDs; gap list in project memory |
| `jtbd-tool/` | Gap signals from job manifest feed back to WQO coverage decisions |

## Key path facts

- `~/github` is a symlink → `~/Documents/github/` (same inode)
- `quartz-site/` lives at `~/Documents/github/quartz-site/` (moved from `~/writing/quartz-site/` during Tier 1 reconciliation)
- `wqo-components/` is a live CI dependency of `quartz-site/`, pinned at commit `a0b3b25` in `quartz.lock.json`

## Chancery Labs product namespace

`~/Documents/github/chancery/` contains product-name symlinks:
- `chancery/shela` → `../rhetor-linter/` (Chancery Labs product name for the linter)
- `chancery/laxa` → `../jtbd-tool/` (Chancery Labs product name for the auditor)
- `chancery/syla.md` — stub; syla (server) has no separate repo yet; lives as `[server]` extra in `rhetor-linter`

Gate 2 is the trigger for formal repo renames. Use real repo paths for development; chancery/ paths are navigation only.

## CAMEO lineage

CAMEO (Conflict and Mediation Event Observations) is the structural ancestor:
- `dateline/` — CAMEO applied to geopolitics (the exemplar)
- `wqo/` — CAMEO approach applied to literacy/writing-tech (this repo)
- `jtbd-tool/` — uses CAMEO verbs (`schema/cameo_verbs.py`) for job classification

## Stale project memory paths (as of 2026-06-19)

Several `~/.claude/projects/` memory files contain stale paths from before directory moves. See the Tier 5c table in the reconciliation plan if you encounter guidance referencing `writing/ideation/`, `writing/wqo/`, or `writing/quartz-site/` — those paths no longer exist.

The `-home-rik-writing-ideation/` project context is orphaned (`~/writing/ideation/` does not exist). Memory there is inaccessible in normal sessions.
