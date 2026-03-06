# 冒烟测试指南 — Academic Review Board v2.0

> 用于验证每个范式的最小 4-phase 评审流程是否可运行。

## 测试前提

- `prompts/` 目录完整（`_shared/` + 6 个范式目录）
- 每个范式目录含 `roster.md` + 8 个角色 prompt + `calibration-template.md`
- `scripts/build-knowledge.py` 可执行
- LLM API 可用

## 每个范式的冒烟测试流程

### Step 0: 范式选择 + 知识包

```bash
# 替换 {paradigm} 为实际范式名
python3 scripts/build-knowledge.py --topic "smoke test" --paradigm {paradigm} --dry-run
```

**验证**：
- [ ] 脚本无报错退出（code-light 范式可预期 "无结果" 信息）
- [ ] `--paradigm` 参数被正确识别和打印

### Step 1: Roster 解析

**手动检查**：
- [ ] `prompts/{paradigm}/roster.md` 可读
- [ ] `core` 区有 3 个角色，文件路径正确
- [ ] `general` 区有 3 个角色，文件路径正确
- [ ] `optional` 区有 1-2 个角色，启用条件明确
- [ ] 投票权重：core=5, general=3

### Step 2: Phase 1 — 单角色测试

选 1 个核心角色（如 Methodology Critic），给它：
- 一段测试用的研究摘要（可用 calibration-template.md 的场景）
- 对应的角色 prompt

**验证**：
- [ ] 输出包含 3 个提案
- [ ] 提案格式符合 `_shared/output-format-phase1.md`（ID前缀正确、有 Priority/Details/Action）
- [ ] 提案内容与范式相关（不是泛泛而谈）

### Step 3: Phase 2 — 交叉讨论格式

给同一角色 Phase 1 的产出（模拟来自其他角色），验证：
- [ ] 输出格式符合 `_shared/output-format-phase2.md`
- [ ] 有 支持/质疑/补充 中至少一种操作

### Step 4: Phase 3 — GM 精炼

给 GM（`gm-academic.md`）Phase 2 的模拟输出，验证：
- [ ] GM 正确识别范式
- [ ] 精炼日志格式符合 `_shared/output-format-phase3-gm.md`
- [ ] 有 MERGED/PRUNED/KEPT 操作记录

### Step 5: Phase 4 — 投票 + 裁决

验证：
- [ ] 核心角色投 5 票，一般角色投 3 票
- [ ] GM 最终裁决包含 Paradigm 字段

## 范式特定验证点

| 范式 | 额外检查 |
|------|---------|
| economics-finance | Econometrician 提到 Fama-MacBeth / 聚类SE |
| cs-ai | ML Statistician 提到 ablation / bootstrap |
| clinical-epidemiology | Biostatistician 提到 ITT / survival analysis |
| experimental-behavioral | Psychometrician 提到 ANOVA / effect size |
| natural-science-engineering | Metrologist 提到 GUM / uncertainty budget |
| biology-omics | Bioinformatician 提到 FDR / DESeq2 |

## ID 前缀冲突检查

所有范式共享 ID 前缀（MC, ED, DR, LS, RA, DE, EA + 范式特定统计前缀）。
跨范式不会冲突（每次评审只用一个范式），同一评审内各角色前缀不同。

| 角色 | 前缀 |
|------|------|
| Methodology Critic | MC |
| Experiment Designer | ED |
| Statistician (varies) | EC/MS/BS/PM/MT/BI |
| Devil Reviewer | DR |
| Literature Scout | LS |
| Reproducibility Auditor | RA |
| Domain Expert | DE |
| Ethics Auditor | EA |
