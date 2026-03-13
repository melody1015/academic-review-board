# Example: Fatal Flaw Detection — The PLT Tautology

> This is a real example from Session 002 of the Academic Review Board.
> **Outcome**: Paper required major redesign before submission.

---

## The Setup

A working paper claimed to discover a novel predictor for stock returns: **PLT (Price Lead Time)** — the number of days from retail attention peak (Google SVI) to subsequent price peak.

**Reported results** (extraordinary):
| Statistic | Value |
|-----------|-------|
| Spearman ρ (PLT vs alpha) | 0.62 |
| Fama-MacBeth t-stat | 38.8 |
| Q5-Q1 spread (90 days) | 33 percentage points |
| % positive months | 100% |

These results are an order of magnitude stronger than typical published effects (ρ ≈ 0.05-0.15, t ≈ 2-5).

---

## The Fatal Flaw

**7 out of 7 experts independently identified the same problem:**

PLT was **mechanically correlated** with forward alpha by construction:

```
PLT = days from SVI peak to FUTURE price peak (within 120-day window)
Forward alpha = cumulative alpha over 90 days from SVI peak

The 90-day alpha window ⊂ the 120-day PLT construction window
```

**The logic:**
- High PLT → price peak is far ahead → prices still rising during measurement → positive alpha
- Low PLT → price peak is near/past → prices declining during measurement → negative alpha
- **This is definitional, not predictive**

This explains all the "extraordinary" statistics — they were measuring a tautology.

---

## Expert Convergence

| Expert | Role | Verdict |
|--------|------|---------|
| MC | Methodology Critic | P0 — "PLT uses future price information" |
| ED | Experiment Designer | P0 — "120-day lookahead window contaminated" |
| EC | Econometrician | P0 — "Mechanical correlation by construction" |
| DR | Devil Reviewer | **FATAL/VETO** — "This is a tautology, not a predictor" |
| DE | Domain Expert | P0 — "Effect size implausibly large" |
| LS | Literature Scout | P0 — "Look-ahead bias literature must be cited" |
| RA | Reproducibility Auditor | P0 — "Reproducibility requires ex-ante definition" |

**Unanimous convergence on the fatal flaw.**

---

## What Happened Next

The author accepted the finding and redesigned the predictor:

**Before** (tautological):
- PLT = days to future price peak

**After** (ex-ante):
- Pre-event volatility (available at SVI peak date)
- Mode A/B classification (based on observable C-T ordering)
- No future price information in predictors

**New results** (after fix):
| Statistic | Old (tautological) | New (ex-ante) |
|-----------|-------------------|---------------|
| Spearman ρ | 0.62 | 0.094 |
| t-stat | 38.8 | 4.56 |
| Q5-Q1 spread | 33 pp | 6.45 pp |

The effect dropped by ~80%, but remained statistically significant — **a genuine, publishable finding**.

---

## Why This Matters

1. **Self-correction before submission** — The fatal flaw was caught before any journal saw the paper
2. **All 7 experts converged** — Not one opinion, but unanimous
3. **Honest science** — The author disclosed the discarded predictor in the final paper
4. **Paper survived** — After redesign, the core contribution (I→C→T decomposition) remained valid

---

## What This Demonstrates

| Feature | Why It Matters |
|---------|----------------|
| **Multi-expert convergence** | 7/7 experts catching the same flaw = high confidence it's real |
| **Devil Reviewer power** | DR flagged as FATAL/VETO, forcing immediate attention |
| **Actionable fix** | Not just "this is wrong" but "here's how to fix it" |
| **Paper survived** | System finds flaws to fix, not reasons to kill |

**Bottom line**: This system saved the author from submitting a paper that would have been desk-rejected at any top journal. The redesigned version is now submission-ready.
