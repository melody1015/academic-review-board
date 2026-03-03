# 🎓 Academic Review Board

**AI-powered multi-agent peer review for research papers — catch fatal flaws before submission.**

> 7 specialized expert agents + 4-phase deliberation protocol + weighted voting. Built on insights from AgentReview (EMNLP 2024), MARG (Allen AI 2024), and PRE (CIKM 2024).

---

## Why This Exists

You've written a paper. You think it's good. You submit it. Three months later, Reviewer 2 finds a fatal flaw you could have caught on day one.

This project simulates that process **before** you submit — with 7 AI experts who independently review your work, debate each other's findings anonymously, and vote on what matters most. In our first real deployment, all 7 experts unanimously identified a tautological flaw in our variable definition that the human author missed entirely.

## What Makes This Different

| Feature | Single-Agent Review | AgentReview | MARG | **This Project** |
|---------|-------------------|-------------|------|-----------------|
| Multi-perspective | ❌ | ✅ 3-dim | ✅ dimension-split | ✅ **7 deep expert roles** |
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
              │  Phase 1: Independent   │  21 proposals (3 per expert)
              │  Phase 2: Cross-review  │  Anonymous debate, random order
              │  Phase 3: Refinement    │  GM merges/prunes → 10-14
              │  Phase 4: Weighted vote │  Core 5票 + General 3票 + FATAL +3
              └────────────┬────────────┘
                           ▼
                    ┌──────────────┐
                    │  GM Ruling   │ ← Inclusive style (AgentReview best practice)
                    └──────────────┘
```

## The 7 Experts

### Core Experts (5 votes each — "Methodology Triangle")

| Role | What They Catch | Real-World Analog |
|------|----------------|-------------------|
| **Methodology Critic** | Look-ahead bias, identification failures, causal inference gaps | Methods referee at JF/JFE/RFS |
| **Experiment Designer** | Sample contamination, point-in-time violations, out-of-sample degradation | Quant fund researcher (ex-AQR/Two Sigma) |
| **Econometrician** | Wrong statistical tests, missing multiple-testing corrections, effect size inflation | Financial econometrics professor |

### General Experts (3 votes each)

| Role | What They Catch | Real-World Analog |
|------|----------------|-------------------|
| **Devil Reviewer** | Fatal flaws, claim-evidence gaps, incremental contribution | The dreaded "Reviewer 2" |
| **Domain Expert** | Theory-methodology disconnect, wrong literature anchoring | Finance professor (replaceable for other fields) |
| **Literature Scout** | Missing seminal papers, incorrect positioning, counter-evidence | Research librarian + systematic review specialist |
| **Reproducibility Auditor** | Data provenance gaps, code duplication, FAIR violations | Data auditor (RFS code-sharing policy) |

## Real Results

### Session 002: Complete Paper Review

**Input**: An empirical finance paper claiming that a novel timing variable predicts cross-sectional stock returns with ρ=0.62 (p<0.001) and perfect quintile monotonicity.

**Result**: All 7 experts independently flagged the same fatal flaw — the core variable was defined using future price data (information unavailable at the time of the investment decision), creating a **mechanical tautological correlation** with forward returns. The impressive statistics were an artifact of the variable construction, not a genuine predictive relationship.

> "This is the strongest convergence I have ever seen in this review board." — GM Ruling

**Verdict**: MAJOR_REVISION_REQUIRED. The variable needed to be redefined using only ex-ante information. The theoretical framework was preserved (genuinely novel), but the empirical evidence was invalid.

*The human author — who had run 10 robustness tests that all "passed" — missed this because they were too close to the work. This single finding justified the entire system's existence.*

## Quick Start

### Prerequisites
- Any LLM API access (Claude, GPT-4, etc.) or [OpenClaw](https://github.com/openclaw/openclaw) for agent orchestration
- Python 3.10+ (for knowledge pack generator)
- [GitNexus](https://github.com/abhigyanpatwari/GitNexus) (optional, for code architecture analysis)

### Setup

```bash
# Clone
git clone https://github.com/melody1015/academic-review-board.git
cd academic-review-board

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
# 1. (Optional) Generate code architecture context
cd /path/to/your-project
gitnexus analyze                    # Index your codebase
python3 review-board/scripts/build-knowledge.py --topic "Your review topic"

# 2. Prepare knowledge pack
# Copy templates/knowledge-pack-template.md → review-board/sessions/session-NNN/knowledge-pack.md
# Fill in: paper summary, key questions, security boundaries

# 3. Run 4-phase protocol (via OpenClaw or manually)
# Phase 1: Spawn 7 agents with role prompt + knowledge pack
# Phase 2: Collect proposals, randomize, anonymize, spawn 7 agents for cross-review
# Phase 3: GM merges/prunes/security-checks
# Phase 4: Spawn 7 agents to vote, GM makes final ruling
```

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

For papers with a codebase (empirical studies, computational experiments), the Reproducibility Auditor receives a **code architecture digest** generated from [GitNexus](https://github.com/abhigyanpatwari/GitNexus):

```bash
python3 scripts/build-knowledge.py --topic "实验设计look-ahead bias审查" --repo my-project
```

The generator automatically:
1. **Translates** non-English topics to English code keywords (via LLM)
2. **Queries** the code knowledge graph for relevant functions and data flows
3. **Analyzes** blast radius of key symbols
4. **Detects** code duplication risks (same function defined in multiple files)
5. **Formats** a Markdown digest for the Reproducibility Auditor

Example output:
```
### ⚠️ Code Duplication Risk
- `load_data` defined in: main_experiment.py, robustness_check.py, sensitivity_analysis.py
- `compute_returns` defined in: main_experiment.py, alternative_spec.py
```

## Configuration

| Option | Default | Description |
|--------|---------|-------------|
| Expert count | 7 | Add/remove roles; keep the "methodology triangle" |
| Vote weights | Core 5 / General 3 | Set in each expert's Phase 4 section |
| Phase 2 (cross-review) | On | Skip to save time (reduces quality) |
| Phase 3 (refinement) | On | Skip to let GM go straight to voting |
| FATAL bonus | +3 votes | Adjust in GM prompt |
| Domain Expert | Finance | Replace `domain-expert-finance.md` for CS/med/physics |
| GitNexus | On | Auto-skips if not indexed |
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
  author = {Song, Zixu},
  title = {Academic Review Board: Multi-Agent Peer Review for Research Papers},
  year = {2026},
  url = {https://github.com/melody1015/academic-review-board}
}
```
