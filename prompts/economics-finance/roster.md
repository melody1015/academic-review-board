# Roster — 实证经济学与金融 (Economics & Finance)

> 版本: 1.0 | 更新: 2026-03-06


> 本文件定义该研究范式的专家角色配置。编排层（orchestration.md）读取此文件来确定角色列表、投票权重和文件映射。

## 范式信息

- **范式名**: economics-finance
- **适用领域**: 金融学、宏观经济学、微观经济学、会计学、公共经济学
- **方法论核心**: 观测型因果推断（DID/IV/RDD）、面板计量、资产定价检验
- **关键差异点**: look-ahead bias、存活偏差、经济显著性 vs 统计显著性

## 专家配置

### 核心专家（Core — 5 票/人）

| 角色 | 文件 | ID 前缀 | 覆盖维度 |
|------|------|---------|---------|
| Methodology Critic | `methodology-critic.md` | MC | Rigor — 研究设计 |
| Experiment Designer | `experiment-designer.md` | ED | Rigor — 实验/回测设计 |
| Econometrician | `econometrician.md` | EC | Rigor — 统计分析 |

### 一般专家（General — 3 票/人）

| 角色 | 文件 | ID 前缀 | 覆盖维度 |
|------|------|---------|---------|
| Devil Reviewer | `devil-reviewer.md` | DR | Novelty + Significance |
| Domain Expert — Finance | `domain-expert-finance.md` | DE | Significance + Theory |
| Literature Scout | `literature-scout.md` | LS | Novelty + Positioning |
| Reproducibility Auditor | `reproducibility-auditor.md` | RA | Reproducibility |

### 可选专家（Optional — 3 票/人，默认关闭）

| 角色 | 文件 | ID 前缀 | 覆盖维度 | 启用条件 |
|------|------|---------|---------|---------|
| Ethics & Compliance Auditor | `ethics-auditor.md` | EA | Ethics | 涉及个人交易数据、行业资助利益冲突、内幕信息使用时启用 |

## 投票权分布

| 配置 | 核心票 | 一般票 | 总票 | 核心占比 |
|------|-------|-------|------|---------|
| 7 角色（默认） | 3×5 = 15 | 4×3 = 12 | **27** | 56% |
| 8 角色（含 Ethics） | 3×5 = 15 | 5×3 = 15 | **30** | 50% |

## 特殊规则

- **FATAL 机制**: Devil Reviewer 标记 FATAL 的提案自动 +3 票
- **安全边界**: GM 拥有一票否决权（不泄露安全边界清单中的内容）

## 共享模板引用

| 用途 | 文件 |
|------|------|
| Phase 1 输出格式 | `../_shared/output-format-phase1.md` |
| Phase 2 输出格式 | `../_shared/output-format-phase2.md` |
| Phase 4 核心投票 | `../_shared/output-format-phase4-core.md` |
| Phase 4 一般投票 | `../_shared/output-format-phase4-general.md` |
