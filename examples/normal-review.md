# Example: Normal Review — IPL Paper Pre-Submission

> Session IPL-001 | Model: glm-5 | Outcome: 8 improvements, no fatal flaws

---

## The Setup

A working paper on information diffusion and return predictability (I→C→T decomposition), targeting SSRN → top finance journals.

**Core claims**:
1. Return predictability concentrates in C→T segment (attention to price), not I→C
2. Mode B events (price before attention) earn +3.94 pp more alpha than Mode A
3. Pre-event volatility predicts forward alpha (Q5-Q1 = 6.45 pp)

---

## Review Results

| Metric | Value |
|--------|-------|
| Phase 1 proposals | 21 (7 experts × 3) |
| Refined proposals | 10 |
| Final actions | 8 (5 Accept, 3 Modify) |
| Fatal flaws | 0 |

---

## Top 3 Issues

### #1: Scope Limitation Not in Abstract (P0)

**Issue**: Only 27.5% of events can be classified into Mode A/B by Granger causality. The paper is transparent about this in the body, but the abstract doesn't mention it.

**Fix**: Rewrite abstract opening: "Among the 27.5% of events where C-T ordering can be statistically distinguished (Granger causality), Mode B events earn..."

**Votes**: 7/7

---

### #2: B2 Window Overlap (P0)

**Issue**: The high-coverage B2 classification method uses a ±6-week window that overlaps with the forward alpha measurement window. Granger (clean, no overlap) should be the headline.

**Fix**: Either relegate B2 to appendix, or add explicit caveat: "B2 estimates are directionally consistent but subject to mechanical overlap; Granger estimates (Δ=+3.94pp, p=0.006) are the clean causal-inference benchmark."

**Votes**: 6/7

---

### #3: No Code/Data Availability Statement (P0)

**Issue**: Top journals now expect explicit data and code availability statements. The paper doesn't have one.

**Fix**: Add section: "Code will be posted to GitHub upon publication; data available from sources listed in Table 1."

**Votes**: 5/7

---

## Remaining Actions (P1)

| # | Issue | Fix |
|---|-------|-----|
| 4 | Multiplicity testing | Create "multiplicity budget" table showing all hypothesis tests and which survive adjustment |
| 5 | Volatility-momentum orthogonality | Run multivariate regression (alpha ~ pre_vol + momentum + D1) to prove orthogonality |
| 6 | Mechanism vs Ben-Rephael | Add explicit comparison: Mode B may capture institutional vs retail timing, but direct test requires institutional data |
| 7 | Iterative process disclosure | Add to limitations: predictors chosen after exploratory analysis; COVID provides partial out-of-sample validation |
| 8 | COVID in abstract | (Optional) Add one sentence about COVID natural experiment |

---

## What's Strong

| Area | Assessment |
|------|------------|
| Transparency | Openly disclosed prior tautological predictor (PLT) failure |
| Methodology | Granger estimates (Δ=+3.94pp, p=0.006) are clean causal inference |
| Natural experiment | COVID analysis shows 88% I→C compression under high salience |
| Appropriate modesty | Explicitly does not extrapolate Mode A/B to unclassifiable events |

---

## What This Demonstrates

| Feature | Why It Matters |
|---------|----------------|
| **No fatal flaws** | Paper is fundamentally sound, only needs refinement |
| **Actionable feedback** | Each finding has a specific fix, not vague criticism |
| **Constructive tone** | Experts acknowledge strengths alongside issues |
| **Prioritization** | P0/P1/P2 helps author focus on what matters most |

---

## Verdict

**Submission-ready after implementing 3 P0 fixes.** The paper makes a genuine contribution to the attention-return literature. Main feedback is about *framing and transparency*, not methodology.

This is what a "normal" review looks like — good paper, constructive polish.
