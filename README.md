# Writing Quality Ontology (WQO)

A systematic, multi-dimensional domain ontology for literacy, composition, rhetoric, publishing, and writing technology.

**Browse the ontology:** [ghoulmann.github.io/word](https://ghoulmann.github.io/word)

## What this is

WQO classifies writing-quality concerns the way CAMEO (Conflict and Mediation Event Observations) classifies geopolitical events: systematically, across multiple independent dimensions, covering a domain completely rather than enumerating known instances ad hoc.

Each concern is classified across 13 independent dimensions:

| Dimension | What it encodes |
|---|---|
| D1 layer | Which editorial layer owns it (functional → editorial) |
| D2 stage | Where in the writing lifecycle it applies |
| D3 scale | What unit of text it operates on |
| D4 concern_type | Logical, grammatical, rhetorical, architectural… |
| D5 evaluator | Who or what can detect it |
| D6 determinism | Rule-violation vs. risk-factor vs. philosophy |
| D7 writing_stage | When in the writing process it's active |
| D8 address_when | Earliest stage at which addressing it is not premature (triage) |
| D9 engineering_stage | Analogous stage in the engineering design process |
| D10 impact | Downstream consequences when the concern fails |
| D11 risk_severity | Cosmetic / functional / credibility / safety |
| D12 responsible_role | Who owns fixing it |
| D13 audience_sensitivity | Reader populations with elevated risk above the D11 baseline |

**Current scope:** 37 concerns × 13 dimensions + 96 operational problems. This is the first systematized instantiation — not a complete enumeration of the full literacy/composition/rhetoric/publishing/writing-tech domain.

## Two-layer architecture

```
┌───────────────────────────────────────────────────┐
│  TEXT QUALITY LAYER                               │
│  concerns/*.yaml  ·  schema/concept.schema.json   │
│  "How does text fail?"                            │
└────────────────────────┬──────────────────────────┘
                         │  wqo_links + system_boundary
┌────────────────────────▼──────────────────────────┐
│  OPERATIONAL PROBLEMS LAYER                       │
│  problems/problems.yaml  ·  schema/problem.schema.json │
│  "Where in the lifecycle does failure occur?"     │
└───────────────────────────────────────────────────┘
```

The text quality layer describes intrinsic content properties. The problems layer catalogs process, tooling, and governance failures that produce or allow those content failures. `wqo_links` on each problem entry bridges the two.

See [`docs/design.md`](docs/design.md) for full schema rationale, problem catalog structure, lifecycle mapping, and ecosystem coverage gaps.

## Structural lineage

CAMEO is the methodological ancestor:

| Project | Domain | CAMEO relationship |
|---|---|---|
| [dateline](../dateline/) | Geopolitical crisis reporting | Direct application of CAMEO event taxonomy |
| **wqo** (this repo) | Writing quality / literacy | CAMEO-analogous: same structural approach, different domain |
| [jtbd-tool](../jtbd-tool/) | Software job coverage auditing | Uses CAMEO organizational verbs for job classification |

## Two representations

WQO content exists in two intentionally parallel forms:

| Form | Location | Audience | Fields |
|---|---|---|---|
| YAML concern files | `concerns/*.yaml` (this repo) | Tools and linters | 13 classification dimensions |
| Concept nodes | `quartz-site/content/lexicon/*.md` | Practitioners | + WordNet, typed relationships, engineering stage |

These are complementary, not competing. The tool-facing YAML intentionally excludes the ontology-browser dimensions.

## Ecosystem

| Repo | Role |
|---|---|
| **wqo** (this repo) | Schema hub — concern YAML, problem catalog, shared schemas |
| [quartz-site](../quartz-site/) | Deployed ontology browser at `ghoulmann.github.io/word` |
| [rhetor-linter](../rhetor-linter/) | Rhetoric linter; rule coverage mapped against WQO concern IDs |
| [jtbd-tool](../jtbd-tool/) | Job coverage auditor; feeds gap signals back to WQO coverage decisions |
| [dateline](../dateline/) | CAMEO geopolitics exemplar; structural template for WQO |
| [wqo-components](../wqo-components/) | Preact component library consumed by quartz-site |
| [knowledge-management](../knowledge-management/) | Source data (`webs/ideation/tool/index.html`) and schemas |

## Generators

```bash
python concerns/build_concerns.py    # generates concerns/*.yaml from source HTML
python problems/build_problems.py    # generates problems/problems.yaml from inline data
```

Source data: `~/Documents/github/knowledge-management/webs/ideation/tool/index.html`

See `CLAUDE.md` for schema documentation and architectural notes.
