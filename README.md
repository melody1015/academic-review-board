# 🎓 Academic Review Board

**AI-powered multi-agent peer review for research papers — catch fatal flaws before submission.**

> N specialized expert agents (paradigm-adaptive) + 4-phase deliberation protocol + weighted voting. 10 paradigms supported. Built on insights from AgentReview (EMNLP 2024), MARG (Allen AI 2024), and PRE (CIKM 2024).

---

## Why This Exists

You've written a paper. You think it's good. You submit it. Three months later, Reviewer 2 finds a fatal flaw you could have caught on day one.

This project simulates that process **before** you submit — with N AI experts (dynamically loaded per paradigm) who independently review your work, debate each other's findings anonymously, and vote on what matters most. In our first real deployment, all experts unanimously identified a tautological flaw in our variable definition that the human author missed entirely.

## What Makes This Different

| Feature | Single-Agent Review | AgentReview | MARG | **This Project** |
|---------|-------------------|-------------|------|-----------------|
| Multi-perspective | ❌ | ✅ 3-dim | ✅ dimension-split | ✅ **N paradigm-specific expert roles** |
| Cross-discussion | ❌ | ✅ rebuttal | ✅ internal | ✅ **anonymous + randomized** |
| Weighted voting | ❌ | ❌ | ❌ | ✅ **core 5 votes / general 3** |
| Expert memory | ❌ | ❌ | ❌ | ✅ **persistent .memory.md** |
| Calibration | ❌ | ❌ | ❌ | ✅ **Planted Error Test** |
| Code integration | ❌ | ❌ | ❌ | ✅ **GitNexus knowledge graph** |
| Anti-bias | ❌ | partial | partial | ✅ **randomization + anonymization + refinement** |
| Author-facing | ❌ | ❌ (research) | ❌ (research) | ✅ **practical tool** |

## Architecture

```
                    ┌──────────────┐
                    │  Knowledge   │
                    │    Pack      │ ← paper draft + experiment design + code architecture
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
     ┌─────────────┐ ┌──────────┐ ┌─────────────┐
     │ Methodology  │ │Experiment│ │Econometri-  │  ← Core experts (5 votes each)
     │   Critic     │ │ Designer │ │   cian      │
     └──────┬───────┘ └────┬─────┘ └──────┬──────┘
            │              │              │
     ┌──────┴──────┐ ┌────┴─────┐ ┌──────┴──────┐ ┌──────────────┐
     │   Devil     │ │ Domain   │ │ Literature  │ │Reproducibility│ ← General (3 votes)
     │  Reviewer   │ │  Expert  │ │   Scout     │ │   Auditor    │
     └──────┬──────┘ └────┬─────┘ └──────┬──────┘ └──────┬───────┘
            │              │              │               │
            └──────────────┼──────────────┼───────────────┘
                           ▼
              ┌─────────────────────────┐
              │  Phase 1: Independent   │  N×3 proposals (3 per expert)
              │  Phase 2: Cross-review  │  Anonymous debate, random order
              │  Phase 3: Refinement    │  GM merges/prunes → 10-14
              │  Phase 4: Weighted vote │  Core 5票 + General 3票 + FATAL +3
              └────────────┬────────────┘
                           ▼
                    ┌──────────────┐
                    │  GM Ruling   │ ← Inclusive style (AgentReview best practice)
                    └──────────────┘
```

## Expert Roles (Paradigm-Adaptive)

Experts are loaded dynamically from `prompts/{paradigm}/roster.md`. Each paradigm defines 7-8 roles across 3 layers:

### Layer 2 — Core Experts (5 votes each — "Methodology Triangle")

| Role | Paradigm-Specific Name | What They Catch |
|------|----------------------|----------------|
| Methodology Critic | (shared) | Identification failures, causal inference gaps |
| Experiment Designer | (shared) | Design contamination, look-ahead bias |
| Statistician | Econometrician / ML Statistician / Biostatistician / Psychometrician / Metrologist / Bioinformatician | Wrong tests, missing corrections, effect size inflation |

### Layer 1 + 3 — General + Optional (3 votes each)

| Role | What They Catch | Quality Assurance |
|------|----------------|-------------------|
| Devil Reviewer | Fatal flaws, claim-evidence gaps | **Red Flags** (paradigm-specific) |
| Domain Expert | Theory-methodology disconnect | **Rejection Triggers** |
| Literature Scout | Missing papers, counter-evidence | **Rejection Triggers** |
| Reproducibility Auditor | Data provenance, FAIR violations | **Graded Rubric** (authority-backed ✅/⚠️/❌) |
| Ethics Auditor (optional) | IRB/consent/data ethics | **Rejection Triggers** (COPE/Helsinki) |

### Supported Paradigms

| Paradigm | Layer 2 Statistician | Example Fields |
|----------|---------------------|----------------|
| `economics-finance` | Econometrician | 金融、经济学、会计 |
| `cs-ai` | ML Statistician | 机器学习、NLP、CV |
| `clinical-epidemiology` | Biostatistician | 临床试验、流行病学 |
| `experimental-behavioral` | Psychometrician | 心理学、教育、行为经济 |
| `natural-science-engineering` | Metrologist | 物理、化学、材料、工程 |
| `biology-omics` | Bioinformatician | 基因组学、转录组、蛋白质组 |
| `qualitative-research` | Qualitative Analyst | 社会学、人类学、教育学、护理学 |
| `normative-policy` | Normative Theorist | 社会福利、公共政策、政治哲学 |
| `systematic-review` | Meta-Analyst | 系统综述、Meta 分析、Cochrane/Campbell |
| `mixed-methods` | Integration Analyst | 混合方法、教育学、护理学、公共卫生 |

## Real Results

### Session 002: Complete Paper Review

**Input**: An empirical finance paper claiming that a novel timing variable predicts cross-sectional stock returns with high statistical significance and monotonic portfolio sorts.

**Result**: All 7 experts independently flagged the same fatal flaw — the core variable was defined using future price data (information unavailable at the time of the investment decision), creating a **mechanical tautological correlation** with forward returns. The impressive statistics were an artifact of the variable construction, not a genuine predictive relationship.

> "This is the strongest convergence I have ever seen in this review board." — GM Ruling

**Verdict**: MAJOR_REVISION_REQUIRED. The variable needed to be redefined using only ex-ante information. The theoretical framework was preserved (genuinely novel), but the empirical evidence was invalid.

*The human author — who had run 10 robustness tests that all "passed" — missed this because they were too close to the work. This single finding justified the entire system's existence.*

## When to Use: 4-Stage Research Lifecycle

Don't wait until you've written the full paper. Use the review board at multiple stages — earlier catches save more time.

```
Stage 1 ─ IDEA          "Is this worth pursuing?"
           │              3 experts · 1-page proposal · ~20K tokens · <$1
           │              Domain Expert + Literature Scout + Devil Reviewer
           │              Key question: Has this been done? Is the gap real?
           │
Stage 2 ─ DESIGN         "Is my experiment sound?"
           │              7 experts · experiment plan + data description · ~66K tokens
           │              Focus: Methodology Critic + Experiment Designer + Econometrician
           │              Key question: Look-ahead bias? Identification strategy?
           │              ⚠️ This is the highest-ROI stage — catching a design flaw here
           │              saves weeks of wasted coding and analysis
           │
Stage 3 ─ RESULTS        "Do my findings hold up?"
           │              7 experts · results + tables + robustness checks · ~66K tokens
           │              Focus: Econometrician + Devil Reviewer + Reproducibility Auditor
           │              Key question: Mechanical artifact? Alternative explanations?
           │
Stage 4 ─ PRE-SUBMIT     "Will Reviewer 2 kill this?"
                          7 experts · complete paper draft · ~66K tokens
                          Focus: All experts, especially Devil Reviewer
                          Key question: Fatal flaws? Contribution clarity? Acceptance odds?
```

**Stage 1** is lightweight — skip Phases 2-3, just collect independent assessments. **Stages 2-4** use the full 4-phase protocol.

**Real example**: In our deployment, Stage 2 (design review) identified 9 actionable improvements. Stage 4 (pre-submission) caught a fatal tautological flaw that invalidated the core results. If we had caught it at Stage 2, we would have saved 2+ weeks of coding and analysis.

> **Rule of thumb**: If your research involves writing code, run at least Stage 2 before you start coding.

## Installation & Upgrade

### Fresh Install

```bash
git clone https://github.com/melody1015/academic-review-board.git
cd academic-review-board
```

### Upgrade from Previous Version

```bash
cd academic-review-board
git pull origin main
```

To see what changed between versions:

```bash
git log --oneline v2.0..v2.1   # changes from v2.0 to v2.1
```

### Version History

| Version | Paradigms | What's New |
|---------|-----------|-----------|
| `v1.0` | 6 | Initial release — empirical paradigms (economics-finance, clinical-epidemiology, cs-ai, experimental-behavioral, natural-science-engineering, biology-omics) |
| `v2.0` | 8 | + Qualitative Research, Normative & Policy Argumentation |
| `v2.1` | 10 | + Systematic Review & Meta-Analysis, Mixed Methods |

To pin a specific version: `git checkout v2.1`

## Coverage & Known Limitations

### ✅ What's Covered (10 paradigms, ~90% of academic papers)

The 10 paradigms cover the vast majority of academic research across all major methodological traditions:

- **Quantitative empirical** (6 paradigms) — hypothesis testing, causal inference, statistical modeling across natural sciences, social sciences, engineering, medicine, and CS/AI
- **Qualitative** — interview studies, ethnography, grounded theory, phenomenology, case studies
- **Mixed methods** — convergent, sequential, embedded designs with integration quality assessment
- **Systematic review & meta-analysis** — PRISMA 2020, Cochrane/Campbell protocols, publication bias, heterogeneity
- **Normative & policy** — value-premise argumentation, policy feasibility, distributional impact

### ⚠️ Not Yet Fully Covered

The following research types can use the **closest available paradigm** as an approximation, but may miss domain-specific evaluation criteria. If you work in these areas and would like dedicated paradigm support, please [open an issue](https://github.com/melody1015/academic-review-board/issues).

| Research Type | Closest Paradigm | What's Missing |
|--------------|-----------------|----------------|
| **Design Science** (IS artifact construction, Hevner's 7 guidelines) | `cs-ai` | Artifact evaluation framework, design cycle assessment, utility demonstration criteria |
| **Case Study Research** (Yin/Eisenhardt single/multiple case) | `qualitative-research` | Case selection logic audit, literal vs theoretical replication, cross-case pattern matching |
| **Action Research** (intervention-reflection cycles) | `qualitative-research` | Cycle quality assessment, researcher-as-participant dual role, democratic validity |
| **Formal/Mathematical Modeling** (pure theorem-proof, axiomatic systems) | `economics-finance` or `cs-ai` | Axiom reasonableness review, proof correctness checking, numerical experiment design for theoretical models |
| **Humanities & Hermeneutics** (literary criticism, historical analysis, philosophical argumentation) | `normative-policy` + `qualitative-research` | Textual interpretation rigor, historiographic method, hermeneutic circle assessment |
| **Computational Simulation** (agent-based models, climate models, CFD) | `natural-science-engineering` | Parameter sensitivity analysis, numerical convergence verification, model validation against empirical benchmarks |

> **Design principle**: Paradigm selection follows "methodological core, not disciplinary affiliation." A psychology paper using fMRI should use `biology-omics` or `clinical-epidemiology`, not `experimental-behavioral`. See `prompts/orchestration.md` for the full selection guide.

## Quick Start

### Prerequisites
- Any LLM API access (Claude, GPT-4, etc.) or [OpenClaw](https://github.com/openclaw/openclaw) for agent orchestration
- Python 3.10+ (for knowledge pack generator)
- LibreOffice (for DOC/DOCX/TEX → PDF conversion)
- PyMuPDF + python-docx (optional, for automatic text/table/figure extraction)
- [GitNexus](https://github.com/abhigyanpatwari/GitNexus) (optional, for code architecture analysis)

### API Key / OAuth Setup

Choose one path:

1. **OpenClaw (recommended)**
```bash
# Interactive auth (OAuth or API key per provider)
openclaw models auth login
```
Auth profiles are stored under `~/.openclaw/agents/<agent>/agent/auth-profiles.json`.

2. **Direct API keys via shell env**
```bash
# Example (pick the provider you actually use)
export ANTHROPIC_API_KEY="your_key"
export OPENAI_API_KEY="your_key"
export GEMINI_API_KEY="your_key"
```
Add them to your shell profile (`~/.zshrc` / `~/.bashrc`) for persistence.

> Never commit real keys into this repo.

### Setup

```bash
# Clone
git clone https://github.com/melody1015/academic-review-board.git
cd academic-review-board

# Optional extractors (for auto figure/table/text ingestion)
pip install PyMuPDF python-docx

# Copy to your research project
mkdir -p /path/to/your-project/review-board/{sessions,cache}
cp -r prompts/ scripts/ templates/ /path/to/your-project/review-board/

# Customize
# 1. Edit prompts/gm-academic.md → add your security boundaries
# 2. If not finance: replace prompts/domain-expert-finance.md with your field
# 3. Edit scripts/build-knowledge.py → set your repo name (or use --repo flag)
```

### Run a Review Session

```bash
cd /path/to/your-project/review-board

# Step A: initialize a session from source files (doc/pdf/tex/markdown)
python3 scripts/run_review.py \
  --session ECO-001 \
  --paradigm economics-finance \
  --files ../drafts/paper.docx ../drafts/appendix.pdf \
  --topic "Pre-submission full paper review"
```

This command now does **Step 0.5 automatically**:
- converts source files to PDF
- extracts text/sections/tables/figures
- writes `cache/paper-figure-pack.json` + `cache/paper-figure-pack.md`
- injects extracted figure/table context into `sessions/{id}/knowledge-pack.md`

Then run the 4-phase board protocol (OpenClaw/manual) using that knowledge pack.

Optional flags:
- `--skip-assets` → skip automatic figure/table extraction
- `--figures-dir <dir>` → set custom figure folder
- `--fill-descriptions <json>` → inject visual descriptions for conceptual figures

See [prompts/orchestration.md](prompts/orchestration.md) for the full protocol.

## Expert Improvement System

Experts get better over time through three mechanisms:

### 1. Session Debrief (after every review)
Every proposal's fate is tracked: `ADOPTED` / `MERGED` / `PRUNED(reason)` / `IGNORED` / `VETOED`

### 2. Pattern Analysis (every 3 reviews)
| Failure Pattern | Threshold | Fix |
|----------------|-----------|-----|
| Generic proposals | >50% | Add counter-examples to prompt |
| Duplicate proposals | >40% | Sharpen role boundaries |
| Irrelevant proposals | >30% | Strengthen topic anchoring |
| Low adoption rate | <20% | Trigger deep revision |

### 3. Planted Error Test (triggered)
Inspired by [BMJ's reviewer training RCT](https://pubmed.ncbi.nlm.nih.gov/15044002/) (Schroter et al. 2004):
- Prepare a document with 5 known flaws (1 FATAL + 2 MAJOR + 2 MINOR)
- Run the expert against it
- Pass criteria: FATAL 100%, MAJOR ≥80%, MINOR ≥50%

## Code Architecture Integration (GitNexus)

For papers with a codebase, **all experts** receive a shared **code architecture digest** generated from [GitNexus](https://github.com/abhigyanpatwari/GitNexus). Each role uses it differently (see `_shared/code-context-guide.md`):

```bash
python3 scripts/build-knowledge.py --topic "实验设计look-ahead bias审查" --paradigm economics-finance
```

The generator is **paradigm-aware** — code-light paradigms (clinical, behavioral) gracefully skip GitNexus if no code repo exists.

The generator automatically:
1. **Translates** non-English topics to English code keywords (via LLM)
2. **Queries** the code knowledge graph for relevant functions and data flows
3. **Analyzes** blast radius of key symbols
4. **Detects** code duplication risks (same function defined in multiple files)
5. **Formats** a Markdown digest shared by all experts

Example output:
```
### ⚠️ Code Duplication Risk
- `load_data` defined in: main_experiment.py, robustness_check.py, sensitivity_analysis.py
- `compute_returns` defined in: main_experiment.py, alternative_spec.py
```

## Configuration

| Option | Default | Description |
|--------|---------|-------------|
| Paradigm | `economics-finance` | Set via `--paradigm` flag; loads roles from `prompts/{paradigm}/roster.md` |
| Expert count | 7-8 (per paradigm) | Defined in roster.md; keep the "methodology triangle" |
| Vote weights | Core 5 / General 3 | Set in each expert's Phase 4 section |
| Phase 2 (cross-review) | On | Skip to save time (reduces quality) |
| Phase 3 (refinement) | On | Skip to let GM go straight to voting |
| FATAL bonus | +3 votes | Adjust in GM prompt |
| GitNexus | Paradigm-aware | Auto-skips for code-light paradigms (clinical, behavioral) |
| Language | Any | Cross-lingual keyword extraction for non-English topics |

## Cost

~66K tokens per session (~$2-3 with Claude Opus pricing). Four phases × 7 agents × ~2K tokens + GM synthesis.

## References

This project synthesizes ideas from three academic frameworks:

- **AgentReview** — Huang et al., EMNLP 2024 (Oral). [Paper](https://arxiv.org/abs/2406.12708) | [Code](https://github.com/Ahren09/AgentReview)
  - *Contribution*: Inclusive AC style, anchoring effect findings, rebuttal dynamics
- **MARG** — D'Arcy et al., 2024. [Paper](https://arxiv.org/abs/2401.04259)
  - *Contribution*: Specialized agent roles, internal discussion, refinement stage
- **PRE** — Tsinghua, CIKM 2024
  - *Contribution*: Position randomization, anonymous review, quality tracking with Dawid-Skene EM

Additional inspirations:
- Cochrane Collaboration calibration exercises (inter-rater agreement)
- BMJ reviewer training RCT (Schroter et al. 2004) → Planted Error Test
- Publons editor scoring → expert adoption rate tracking
- NSF grant review panels → forced ranking with limited votes

## License

MIT

## Citation

If you use this in your research, please cite:

```bibtex
@software{song2026academic,
  author = {Song, Zishee},
  title = {Academic Review Board: Multi-Agent Peer Review for Research Papers},
  year = {2026},
  url = {https://github.com/melody1015/academic-review-board}
}
```
