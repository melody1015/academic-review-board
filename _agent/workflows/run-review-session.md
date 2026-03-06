---
description: Launch a full academic review board session from input files to PDF report
---

# Academic Review Board — Session Launch Workflow

Run this workflow when a user wants to review a paper (DOCX, PDF, or similar files).

## Step 1: Identify input files and paradigm

Ask the user (or infer from context):
- Session ID (e.g. `NS-001`, `ECO-002`)
- Paradigm (see roster options below)
- Input file paths (DOCX, PDF, etc.)

**Paradigm selection** (based on methodology, not department):
| Paradigm | Key | Example |
|----------|-----|---------|
| Natural Science & Engineering | `natural-science-engineering` | 材料、物理、化学、工程 |
| CS & AI | `cs-ai` | 机器学习、NLP、软件 |
| Economics & Finance | `economics-finance` | 金融、计量经济、会计 |
| Clinical | `clinical-epidemiology` | 临床试验、流行病学 |
| Behavioral | `experimental-behavioral` | 心理、教育、行为经济 |
| Biology & Omics | `biology-omics` | 基因组、转录组、蛋白质 |

## Step 2: Initialize session

// turbo
```bash
python3 /Users/songzixu/academic-review-board/scripts/run_review.py \
  --session {SESSION_ID} \
  --paradigm {PARADIGM} \
  --files {FILE_PATHS} \
  --topic "{REVIEW_TOPIC}"
```

This will:
- Create `sessions/{SESSION_ID}/` directory structure
- Copy input files to `input/`
- Convert DOCX → PDF via LibreOffice → `input_pdf/`
- Generate `knowledge-pack.md` template
- Run `build-knowledge.py` for code-heavy paradigms

## Step 3: Read all PDFs via browser

Open each PDF in `sessions/{SESSION_ID}/input_pdf/` using the browser subagent:
```
file:///Users/songzixu/academic-review-board/sessions/{SESSION_ID}/input_pdf/{filename}.pdf
```

Extract for knowledge pack:
- Title, authors, abstract
- Methods (instruments, conditions, software)
- Results (all quantitative numbers)
- Figure descriptions (axes, trends, key values)
- SI: supplementary figures, tables, protocols

> [!IMPORTANT]
> **File Reading Gate — MUST PASS before continuing**
>
> Before proceeding to Phase 1 review, verify ALL of the following:
> - [ ] Every PDF opens successfully in the browser
> - [ ] Text is selectable/readable (not a scanned image)
> - [ ] At least 1 figure is visible with readable axes/labels
> - [ ] Key result tables are legible
>
> **If ANY check fails → STOP. Notify the user with the specific failure reason:**
> - PDF won't open → file may be corrupt; ask user to re-upload
> - Text unreadable (scanned image) → request OCR or text version
> - Figures invisible or blank → ask user to check LibreOffice conversion quality
> - Low-resolution figures → warn user that figure review will be incomplete
>
> Do NOT proceed to Phase 1 with incomplete file access.


## Step 4: Build knowledge pack

Fill in `sessions/{SESSION_ID}/knowledge-pack.md` with extracted content.
Add the "评审重点问题" section based on preliminary reading.

## Step 5: Run Phase 1 — Independent Expert Review

Load paradigm roster from `prompts/{PARADIGM}/roster.md`.
For each expert in the roster, generate 3 proposals independently:
- Core experts (Methodology Critic, Experiment Designer, Statistician) → 5 votes each
- General experts (Devil Reviewer, Domain Expert, Literature Scout, Reproducibility Auditor) → 3 votes each
- Each expert sees ONLY: knowledge-pack.md + their own role prompt

Output format: follow `prompts/_shared/output-format-phase1.md`

## Step 6: Run Phase 2 — Cross-Review

Randomize and anonymize all proposals. Each expert reviews others' proposals.
Devil Reviewer can add FATAL marks (+3 vote bonus).

## Step 7: Run Phase 3 — GM Refinement

GM merges duplicates, prunes generic proposals, splits compound issues.
Target: 21 proposals → 10-14 refined items.

## Step 8: Run Phase 4 — Weighted Voting + GM Ruling

Each expert votes (cannot vote for own proposals).
GM synthesizes votes + discussion → Final Ruling with P0/P1/P2 action plan.

## Step 9: Save report and convert to PDF

Save review output as `sessions/{SESSION_ID}/review-report.md`, then:

// turbo
```bash
python3 /Users/songzixu/academic-review-board/scripts/run_review.py \
  --session {SESSION_ID} \
  --finalize
```

Final output: `sessions/{SESSION_ID}/review-report.pdf`
