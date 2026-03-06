#!/usr/bin/env python3
"""
Academic Review Board — Knowledge Pack Generator (with GitNexus)

通用模板。为学术委员会生成知识包附录。
GitNexus 代码架构上下文注入知识包，所有专家共享（使用指南见 _shared/code-context-guide.md）。

用法:
  python3 scripts/build-knowledge.py --topic "实验设计评审" --paradigm economics-finance
  python3 scripts/build-knowledge.py --topic "Complete Paper Review"  # 自动检测 repo, 默认 economics-finance
  python3 scripts/build-knowledge.py --topic "ML模型评审" --paradigm cs-ai

输出:
  review-board/cache/code-architecture-digest.md  (注入知识包，所有专家共享)
  review-board/cache/build-knowledge-log.json     (运行日志)

设计原则 (2026-03-04):
  GitNexus 集成在知识包生成层，不在编排层。
  跨语言映射（中文议题 → 英文代码关键词）在此脚本中完成。
  orchestration.md 只需读取输出文件，不需要跑 GitNexus CLI。
  范式感知：部分范式（clinical, behavioral）可能无代码库，自动跳过 GitNexus。
"""

import argparse
import json
import os
import string
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO_NAME = None  # Auto-detected or passed via --repo
SCRIPT_DIR = Path(__file__).parent
CACHE_DIR = SCRIPT_DIR.parent / "cache"
DIGEST_PATH = CACHE_DIR / "code-architecture-digest.md"
LOG_PATH = CACHE_DIR / "build-knowledge-log.json"


def _detect_repo_name() -> str:
    """从 gitnexus status 或目录名自动检测 repo name"""
    try:
        r = subprocess.run(
            ["gitnexus", "status"],
            capture_output=True, text=True, timeout=10,
            cwd=SCRIPT_DIR.parent.parent  # project root
        )
        for line in (r.stdout + r.stderr).splitlines():
            if "Repository:" in line or "name:" in line.lower():
                # Extract repo name from status output
                parts = line.split(":")
                if len(parts) >= 2:
                    return parts[-1].strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    # Fallback: use parent directory name
    return SCRIPT_DIR.parent.parent.name

# ── GitNexus 基础函数 ─────────────────────────────────────────────

def gitnexus_available() -> bool:
    """检查 gitnexus CLI 是否可用且目标 repo 已索引"""
    try:
        r = subprocess.run(["gitnexus", "list"], capture_output=True, text=True, timeout=10)
        return r.returncode == 0 and REPO_NAME in (r.stderr + r.stdout)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def _gitnexus_run(args: list) -> dict:
    """运行 gitnexus CLI，解析 JSON 输出（可能在 stdout 或 stderr）"""
    try:
        r = subprocess.run(
            ["gitnexus"] + args,
            capture_output=True, text=True, timeout=30
        )
        for output in [r.stdout, r.stderr]:
            text = output.strip()
            if text and text.startswith("{"):
                return json.loads(text)
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
        pass
    return {}


def gitnexus_query(topic: str) -> dict:
    return _gitnexus_run(["query", "--repo", REPO_NAME, topic])


def gitnexus_impact(symbol: str) -> dict:
    return _gitnexus_run(["impact", "--repo", REPO_NAME, symbol])


def gitnexus_context(symbol: str) -> dict:
    return _gitnexus_run(["context", "--repo", REPO_NAME, symbol])


# ── Step 1: 跨语言关键词提取 ──────────────────────────────────────

def extract_code_keywords(topic: str) -> str:
    """
    用 LLM 将任意语言的议题翻译为英文代码搜索关键词。
    跨项目通用 prompt，不硬编码项目描述。
    """
    # 如果议题已经主要是英文，跳过 LLM
    ascii_ratio = sum(1 for c in topic if c in string.ascii_letters + string.digits) / max(len(topic), 1)
    if ascii_ratio > 0.7:
        print(f"  ℹ️  议题主要是英文，跳过 LLM 翻译")
        return topic

    prompt = (
        "You are a code search keyword extractor. "
        "Given a discussion topic about a research project's codebase, "
        "extract 5-10 English keywords that would match relevant Python "
        "function names, file names, and variable names in the codebase. "
        "Output ONLY the keywords separated by spaces, nothing else.\n\n"
        f"Topic: {topic}\n"
        "Keywords:"
    )

    try:
        env = os.environ.copy()
        env.pop("ANTHROPIC_API_KEY", None)  # 走 OAuth，不走 API key
        r = subprocess.run(
            ["claude", "--print", "--model", "sonnet", prompt],
            capture_output=True, text=True, timeout=20, env=env,
        )
        if r.returncode == 0 and r.stdout.strip():
            raw = r.stdout.strip()
            words = raw.replace("\n", " ").split()
            clean = " ".join(
                w.strip(".,;:()[]0-9") for w in words
                if any(c in string.ascii_letters for c in w)
            )
            if clean:
                print(f"  🤖 LLM 关键词提取 (Sonnet): {clean[:100]}")
                return clean
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        print(f"  ⚠️  Claude CLI 调用失败: {e}")

    # Fallback: 提取议题中已有的英文词
    words = topic.replace("-", " ").replace("_", " ").split()
    en_words = [w for w in words if any(c in string.ascii_letters for c in w)]
    fallback = " ".join(en_words) if en_words else topic
    print(f"  ⚠️  Fallback 关键词: {fallback}")
    return fallback


# ── Step 2-3: GitNexus 查询 + 深度展开 ───────────────────────────

def build_gitnexus_pack(topic: str) -> dict:
    """
    5 步知识包生成流程的 Step 2-3:
    查询 GitNexus → 对关键符号做 impact 分析
    """
    if not gitnexus_available():
        print(f"  ⚠️  GitNexus 不可用或 {REPO_NAME} 未索引")
        return {}

    # Step 1: 关键词提取
    search_query = extract_code_keywords(topic)
    print(f"  🔍 GitNexus query: [{search_query}]")

    # Step 2: 查询相关代码
    query_result = gitnexus_query(search_query)
    definitions = query_result.get("definitions", [])
    processes = query_result.get("processes", [])
    process_symbols = query_result.get("process_symbols", [])

    # Step 3: 对关键函数做 impact 分析（最多 5 个）
    key_functions = [d for d in definitions if d.get("id", "").startswith("Function:")][:5]
    impacts = {}
    for sym in key_functions:
        name = sym.get("name", "")
        if name:
            impact = gitnexus_impact(name)
            if impact and impact.get("impactedCount", 0) > 0:
                impacts[name] = {
                    "file": sym.get("filePath", ""),
                    "risk": impact.get("risk", "UNKNOWN"),
                    "impacted_count": impact.get("impactedCount", 0),
                    "affected_modules": [
                        m.get("name", "") for m in impact.get("affected_modules", [])
                    ],
                    "direct_dependants": [
                        {
                            "name": d.get("name", ""),
                            "file": d.get("filePath", ""),
                        }
                        for d in impact.get("byDepth", {}).get("1", [])
                    ][:5],
                }

    return {
        "search_query": search_query,
        "related_files": sorted(set(
            d.get("filePath", "") for d in definitions if d.get("filePath")
        )),
        "related_functions": [
            {"name": d.get("name"), "file": d.get("filePath"), "line": d.get("startLine")}
            for d in definitions if d.get("id", "").startswith("Function:")
        ][:15],
        "execution_flows": [
            {"summary": p.get("summary"), "steps": p.get("step_count")}
            for p in processes
        ],
        "impact_analysis": impacts,
        "flow_symbols": [
            {"function": ps.get("name"), "file": ps.get("filePath")}
            for ps in process_symbols
        ],
    }


# ── Step 4-5: 角色过滤 + 格式化输出 ──────────────────────────────

def format_digest(topic: str, pack: dict, paradigm: str = "") -> str:
    """
    生成所有专家共享的 Code Architecture Digest。
    各角色按 _shared/code-context-guide.md 从自身视角利用。
    """
    lines = [
        "## Code Architecture Digest (GitNexus)",
        "",
        f"> Auto-generated for all experts | Paradigm: {paradigm} | Topic: {topic}",
        f"> Search query: `{pack.get('search_query', 'N/A')}`",
        "",
    ]

    # 数据加载依赖
    functions = pack.get("related_functions", [])
    if functions:
        lines.append("### Key Functions")
        for f in functions:
            line_info = f" (line {f['line']})" if f.get("line") else ""
            lines.append(f"- `{f['name']}` — `{f['file']}`{line_info}")
        lines.append("")

    # 执行流
    flows = pack.get("execution_flows", [])
    if flows:
        lines.append("### Execution Flows")
        for fl in flows:
            lines.append(f"- {fl['summary']} ({fl['steps']} steps)")
        lines.append("")

    # 爆炸半径
    impacts = pack.get("impact_analysis", {})
    if impacts:
        lines.append("### Blast Radius")
        for name, info in impacts.items():
            lines.append(f"- **`{name}`** (`{info['file']}`) — risk: {info['risk']}, impacts {info['impacted_count']} symbols")
            for dep in info.get("direct_dependants", []):
                lines.append(f"  - → `{dep['name']}` (`{dep['file']}`)")
        lines.append("")

    # 代码复制风险检测
    func_names = [f["name"] for f in functions]
    duplicated = [name for name in set(func_names) if func_names.count(name) > 1]
    # 也检查跨文件同名函数
    name_to_files = {}
    for f in functions:
        name_to_files.setdefault(f["name"], []).append(f["file"])
    duplicated_across = {
        name: files for name, files in name_to_files.items()
        if len(set(files)) > 1
    }

    if duplicated_across:
        lines.append("### ⚠️ Code Duplication Risk")
        lines.append("The following functions are defined in multiple files (inconsistent implementations may affect reproducibility):")
        for name, files in duplicated_across.items():
            lines.append(f"- `{name}` defined in: {', '.join(f'`{f}`' for f in sorted(set(files)))}")
        lines.append("")

    # 涉及的文件清单
    files = pack.get("related_files", [])
    if files:
        lines.append("### Related Files")
        for f in sorted(files):
            lines.append(f"- `{f}`")
        lines.append("")

    return "\n".join(lines)


# ── Main ──────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Academic Review Board — Knowledge Pack Generator (with GitNexus)"
    )
    parser.add_argument("--topic", required=True, help="评审议题")
    parser.add_argument("--paradigm", default="economics-finance",
                        choices=["economics-finance", "clinical-epidemiology",
                                 "cs-ai", "experimental-behavioral",
                                 "natural-science-engineering", "biology-omics"],
                        help="研究范式 (default: economics-finance)")
    parser.add_argument("--repo", help="GitNexus repo name (auto-detected if omitted)")
    parser.add_argument("--dry-run", action="store_true", help="只打印不写文件")
    args = parser.parse_args()

    global REPO_NAME
    REPO_NAME = args.repo or _detect_repo_name()
    print(f"   Repo:     {REPO_NAME}")

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    print(f"📦 Knowledge Pack Generator")
    print(f"   Topic:    {args.topic}")
    print(f"   Paradigm: {args.paradigm}")
    print(f"   Time:     {datetime.now().isoformat()}")
    print()

    # 范式感知：判断是否需要 GitNexus
    CODE_LIGHT_PARADIGMS = {"clinical-epidemiology", "experimental-behavioral"}

    if args.paradigm in CODE_LIGHT_PARADIGMS:
        print(f"  ℹ️  范式 [{args.paradigm}] 通常不涉及代码仓库")
        print(f"      如果本研究确实有代码（如 R/SAS 分析脚本），仍会尝试 GitNexus")
        pack = build_gitnexus_pack(args.topic)
        if not pack:
            print("  ℹ️  GitNexus 无结果（预期行为），跳过 digest 生成")
            log = {
                "timestamp": datetime.now().isoformat(),
                "topic": args.topic,
                "paradigm": args.paradigm,
                "skipped": True,
                "reason": "code-light paradigm, no GitNexus results",
            }
            LOG_PATH.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")
            sys.exit(0)
    else:
        pack = build_gitnexus_pack(args.topic)
        if not pack:
            print("  ❌ GitNexus 未返回结果，跳过 digest 生成")
            sys.exit(0)

    # 格式化为 Markdown
    digest = format_digest(args.topic, pack, paradigm=args.paradigm)

    if args.dry_run:
        print("\n--- DRY RUN (不写文件) ---\n")
        print(digest)
    else:
        DIGEST_PATH.write_text(digest, encoding="utf-8")
        print(f"\n  ✅ Digest 已写入: {DIGEST_PATH}")

        # 写运行日志
        log = {
            "timestamp": datetime.now().isoformat(),
            "topic": args.topic,
            "paradigm": args.paradigm,
            "search_query": pack.get("search_query", ""),
            "related_files_count": len(pack.get("related_files", [])),
            "functions_count": len(pack.get("related_functions", [])),
            "impacts_count": len(pack.get("impact_analysis", {})),
            "flows_count": len(pack.get("execution_flows", [])),
        }
        LOG_PATH.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  📝 日志已写入: {LOG_PATH}")

    print(f"\n  📊 统计: {len(pack.get('related_files', []))} files, "
          f"{len(pack.get('related_functions', []))} functions, "
          f"{len(pack.get('impact_analysis', {}))} impacts, "
          f"{len(pack.get('execution_flows', []))} flows")


if __name__ == "__main__":
    main()
