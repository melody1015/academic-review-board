#!/usr/bin/env python3
"""
Academic Review Board — Review Launcher

用法:
  python3 scripts/run_review.py --session NS-001 --paradigm natural-science-engineering
  python3 scripts/run_review.py --session ECO-001 --paradigm economics-finance --files paper.docx si.docx

功能:
  1. 在 sessions/{session-id}/ 创建会话目录
  2. 自动发现并转换 DOCX/DOC/TEX → PDF (via LibreOffice)
  3. Step 0.5 自动抽取论文章节/图/表 → cache/paper-figure-pack.{json,md}
  4. 生成知识包模板 (knowledge-pack.md)，自动注入图表资产摘要
  5. 调用 build-knowledge.py 生成代码架构摘要 (如有 GitNexus)
  6. 输出最终评审报告为 PDF

依赖:
  - LibreOffice (brew install --cask libreoffice)
  - Python 3.10+
  - PyMuPDF (PDF 图表/文本提取，可选)
  - python-docx (DOCX 图表/文本提取，可选)

目录结构 (运行后):
  sessions/
  └── {session-id}/
      ├── input/           ← 原始文件 (原样复制)
      ├── input_pdf/       ← 转换后的 PDF
      ├── knowledge-pack.md
      └── review-report.md (评审完成后生成)
      └── review-report.pdf
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# ─── Paths ────────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent.resolve()
REPO_ROOT = SCRIPT_DIR.parent
SESSIONS_DIR = REPO_ROOT / "sessions"
PROMPTS_DIR = REPO_ROOT / "prompts"
CACHE_DIR = REPO_ROOT / "cache"

SOFFICE = "/Applications/LibreOffice.app/Contents/MacOS/soffice"  # macOS path
SUPPORTED_CONVERT = {".docx", ".doc", ".odt", ".pptx", ".xlsx", ".tex"}

# ─── Helpers ──────────────────────────────────────────────────────────────────

def log(msg: str):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")


def find_soffice() -> str | None:
    """Find soffice binary (macOS / Linux)."""
    candidates = [
        SOFFICE,
        "/usr/bin/soffice",
        "/usr/local/bin/soffice",
        shutil.which("soffice") or "",
    ]
    for c in candidates:
        if c and Path(c).exists():
            return c
    return None


def convert_to_pdf(src: Path, out_dir: Path, soffice: str) -> Path | None:
    """Convert a document to PDF using LibreOffice headless."""
    out_dir.mkdir(parents=True, exist_ok=True)
    try:
        result = subprocess.run(
            [soffice, "--headless", "--convert-to", "pdf", "--outdir", str(out_dir), str(src)],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            pdf_name = src.stem + ".pdf"
            pdf_path = out_dir / pdf_name
            if pdf_path.exists() and pdf_path.stat().st_size > 1024:  # must be >1KB
                log(f"  ✅ {src.name} → {pdf_name} ({pdf_path.stat().st_size // 1024} KB)")
                return pdf_path
            else:
                log(f"  ❌ {src.name}: PDF created but appears empty or corrupt")
        else:
            log(f"  ❌ Failed to convert {src.name}: {str(result.stderr)[:200]}")
    except subprocess.TimeoutExpired:
        log(f"  ❌ Timeout converting {src.name}")
    return None


def create_session_dir(session_id: str) -> Path:
    """Create session directory structure."""
    session_dir = SESSIONS_DIR / session_id
    for sub in ["input", "input_pdf"]:
        (session_dir / sub).mkdir(parents=True, exist_ok=True)
    log(f"📁 Session directory: {session_dir}")
    return session_dir


def generate_knowledge_pack_template(
    session_dir: Path,
    session_id: str,
    paradigm: str,
    pdf_files: list[Path],
    figure_pack: str = "",
):
    """Generate a knowledge-pack.md template pre-filled with session info."""
    pdf_list = "\n".join(f"  - {p.name}" for p in pdf_files) if pdf_files else "  - (none)"
    figure_section = ""
    if figure_pack.strip():
        figure_section = f"""
---

## 自动提取图表资产（Step 0.5）

{figure_pack}
"""

    content = f"""# 知识包 — Session {session_id}

**议题**: [填写评审重点问题]
**范式**: {paradigm}
**目标期刊**: [填写]
**日期**: {datetime.now().strftime("%Y-%m-%d")}
**输入文件**:
{pdf_list}

---

## 论文概况

**题目**: [从论文提取]
**核心贡献**: [一句话总结]

---

## 关键结果

[从论文提取核心数据表]

---

## Methods 摘要

[提取关键实验/分析方法]
{figure_section}

---

## 评审重点问题

1. [Phase 0 识别的核心问题]
2.
3.

---

## 安全边界

- 无（公开投稿审查模式）
"""
    kp_path = session_dir / "knowledge-pack.md"
    kp_path.write_text(content, encoding="utf-8")
    log(f"📝 Knowledge pack template: {kp_path}")
    return kp_path


def run_build_knowledge(session_id: str, paradigm: str, topic: str):
    """Run build-knowledge.py to generate code architecture digest."""
    script = REPO_ROOT / "scripts" / "build-knowledge.py"
    if not script.exists():
        log("⚠️  build-knowledge.py not found, skipping GitNexus step")
        return
    try:
        result = subprocess.run(
            [sys.executable, str(script), "--topic", topic, "--paradigm", paradigm],
            capture_output=True, text=True, timeout=60, cwd=str(REPO_ROOT)
        )
        if result.returncode == 0:
            log("✅ build-knowledge.py completed")
        else:
            log(f"⚠️  build-knowledge.py: {(result.stderr or '')[:200]}")
    except subprocess.TimeoutExpired:
        log("⚠️  build-knowledge.py timeout, skipping")


def run_prepare_assets(
    source_file: Path,
    figures_dir: str | None = None,
    fill_descriptions: str | None = None,
) -> str:
    """Run prepare-review-assets.py to auto-extract sections/tables/figures."""
    script = REPO_ROOT / "scripts" / "prepare-review-assets.py"
    if not script.exists():
        log("⚠️  prepare-review-assets.py not found, skipping asset extraction")
        return ""

    cmd = [sys.executable, str(script), str(source_file)]
    if figures_dir:
        cmd += ["--figures-dir", figures_dir]

    # If caller doesn't specify, auto-use cache/figure-descriptions.json when present
    desc_file = Path(fill_descriptions).expanduser() if fill_descriptions else (CACHE_DIR / "figure-descriptions.json")
    if desc_file.exists():
        cmd += ["--fill-descriptions", str(desc_file)]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=180,
            cwd=str(REPO_ROOT),
        )
        if result.returncode == 0:
            log("✅ prepare-review-assets.py completed")
        else:
            log(f"⚠️  prepare-review-assets.py: {(result.stderr or result.stdout or '')[:200]}")
    except subprocess.TimeoutExpired:
        log("⚠️  prepare-review-assets.py timeout, skipping")

    pack_md = CACHE_DIR / "paper-figure-pack.md"
    if not pack_md.exists():
        return ""

    content = pack_md.read_text(encoding="utf-8").strip()
    if content:
        log(f"📊 Auto assets extracted: {len(content)} chars")
    return content


def convert_report_to_pdf(session_dir: Path, soffice: str) -> Path | None:
    """Convert review-report.md to PDF using LibreOffice."""
    report_md = session_dir / "review-report.md"
    if not report_md.exists():
        log("⚠️  review-report.md not found, skipping PDF conversion")
        return None
    pdf = convert_to_pdf(report_md, session_dir, soffice)
    if pdf:
        log(f"📄 Report PDF saved: {pdf}")
    return pdf


def write_session_meta(session_dir: Path, meta: dict):
    """Write session metadata JSON."""
    meta_path = session_dir / "session-meta.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    log(f"📋 Session metadata: {meta_path}")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Academic Review Board — Launch a review session"
    )
    parser.add_argument("--session", required=True, help="Session ID, e.g. NS-001")
    parser.add_argument(
        "--paradigm",
        default="natural-science-engineering",
        choices=[
            "economics-finance",
            "cs-ai",
            "clinical-epidemiology",
            "experimental-behavioral",
            "natural-science-engineering",
            "biology-omics",
        ],
        help="Research paradigm",
    )
    parser.add_argument(
        "--files",
        nargs="*",
        help="Input files (DOCX, PDF, etc.). If omitted, scans current directory.",
    )
    parser.add_argument(
        "--topic",
        default="Pre-submission full paper review",
        help="Review topic (used for build-knowledge.py keyword extraction)",
    )
    parser.add_argument(
        "--skip-assets",
        action="store_true",
        help="Skip automatic paper asset extraction (sections/tables/figures)",
    )
    parser.add_argument(
        "--figures-dir",
        default=None,
        help="Optional figures directory passed to prepare-review-assets.py",
    )
    parser.add_argument(
        "--fill-descriptions",
        default=None,
        help="Optional visual description JSON for conceptual figures",
    )
    parser.add_argument(
        "--finalize",
        action="store_true",
        help="Convert existing review-report.md to PDF (run after writing the report)",
    )
    args = parser.parse_args()

    session_id = args.session
    paradigm = args.paradigm

    # Find LibreOffice
    soffice = find_soffice()
    if not soffice:
        log("❌ LibreOffice not found. Install: brew install --cask libreoffice")
        sys.exit(1)
    assert soffice is not None  # narrowed for type checker
    log(f"✅ LibreOffice: {soffice}")

    # Create session
    session_dir = create_session_dir(session_id)

    # ── FINALIZE MODE ──
    if args.finalize:
        log("📄 Finalize mode: converting review-report.md → PDF")
        convert_report_to_pdf(session_dir, soffice)
        return

    # ── SETUP MODE ──

    # Collect input files
    input_files: list[Path] = []
    if args.files:
        for f in args.files:
            p = Path(f)
            if not p.exists():
                log(f"⚠️  File not found: {f}")
                continue
            input_files.append(p.resolve())
    else:
        log("🔍 No --files specified, scanning current directory...")
        for ext in SUPPORTED_CONVERT | {".pdf"}:
            input_files.extend(Path(".").glob(f"*{ext}"))

    if not input_files:
        log("⚠️  No input files found. Add files to the session manually.")
    
    # Copy to input/ and convert to PDF
    pdf_files: list[Path] = []
    log(f"\n📂 Processing {len(input_files)} file(s)...")

    for src in input_files:
        # Copy original to input/
        dst = session_dir / "input" / src.name
        shutil.copy2(src, dst)

        if src.suffix.lower() == ".pdf":
            # Already PDF — validate size then copy to input_pdf/
            if src.stat().st_size < 1024:
                log(f"  ❌ {src.name}: file appears empty or corrupt (< 1KB), ABORTING")
                log("🛑 ABORT: cannot proceed with unreadable input files.")
                sys.exit(2)
            pdf_dst = session_dir / "input_pdf" / src.name
            shutil.copy2(src, pdf_dst)
            pdf_files.append(pdf_dst)
            log(f"  📄 {src.name} (already PDF, {src.stat().st_size // 1024} KB)")
        elif src.suffix.lower() in SUPPORTED_CONVERT:
            # Convert to PDF — hard stop on failure
            pdf = convert_to_pdf(dst, session_dir / "input_pdf", soffice)
            if pdf is None:
                log(f"🛑 ABORT: conversion of '{src.name}' failed. Fix the file and retry.")
                log("   Review session directory kept for debugging.")
                sys.exit(2)
            assert pdf is not None  # None case exits above via sys.exit
            pdf_files.append(pdf)
        else:
            log(f"  ⏭️  Skipping unsupported format: {src.name}")

    # Step 0.5: auto extract sections/tables/figures from the first input paper
    figure_pack = ""
    if input_files and not args.skip_assets:
        figure_pack = run_prepare_assets(
            source_file=input_files[0],
            figures_dir=args.figures_dir,
            fill_descriptions=args.fill_descriptions,
        )

    # Generate knowledge pack template (auto-inject figure/table pack if available)
    kp_path = generate_knowledge_pack_template(
        session_dir,
        session_id,
        paradigm,
        pdf_files,
        figure_pack=figure_pack,
    )

    # Run build-knowledge.py (optional, for code repos)
    run_build_knowledge(session_id, paradigm, args.topic)

    # Write session metadata
    meta = {
        "session_id": session_id,
        "paradigm": paradigm,
        "topic": args.topic,
        "created": datetime.now().isoformat(),
        "input_files": [str(f) for f in input_files],
        "pdf_files": [str(f) for f in pdf_files],
        "auto_assets_enabled": not args.skip_assets,
        "figure_pack_chars": len(figure_pack),
        "status": "SETUP_COMPLETE",
    }
    write_session_meta(session_dir, meta)

    # ── Summary ──
    print("\n" + "="*60)
    print(f"✅ Session {session_id} initialized")
    print(f"   Paradigm: {paradigm}")
    print(f"   PDFs ready: {len(pdf_files)}")
    print(f"   Auto assets: {'on' if not args.skip_assets else 'off'} ({len(figure_pack)} chars)")
    print(f"\n📋 NEXT STEPS:")
    print(f"   1. Review PDFs in:  {session_dir}/input_pdf/")
    print(f"   2. Fill in knowledge pack: {kp_path}")
    print(f"   3. Run Phase 1-4 expert review (via AI agent or manually)")
    print(f"   4. Save review output to: {session_dir}/review-report.md")
    print(f"   5. Convert to PDF:")
    print(f"      python3 scripts/run_review.py --session {session_id} --finalize")
    print("="*60)


if __name__ == "__main__":
    main()
