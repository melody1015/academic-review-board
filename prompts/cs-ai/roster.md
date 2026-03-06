# Roster — 计算机科学与 AI (CS & AI)

> 版本: 1.0 | 更新: 2026-03-06


> 本文件定义该研究范式的专家角色配置。编排层（orchestration.md）读取此文件来确定角色列表、投票权重和文件映射。

## 范式信息

- **范式名**: cs-ai
- **适用领域**: 机器学习、自然语言处理、计算机视觉、信息检索、机器人学、信息系统
- **方法论核心**: 基准测试驱动、消融实验、计算复杂度分析
- **关键差异点**: SOTA 比较公平性、test leakage、计算预算、代码可复现性

## 专家配置

### 核心专家（Core — 5 票/人）

| 角色 | 文件 | ID 前缀 | 覆盖维度 |
|------|------|---------|---------|
| Methodology Critic | `methodology-critic.md` | MC | Rigor — 问题设定与方法创新性 |
| Experiment Designer | `experiment-designer.md` | ED | Rigor — 实验设计与公平比较 |
| ML Statistician | `ml-statistician.md` | MS | Rigor — 统计检验与效应量 |

### 一般专家（General — 3 票/人）

| 角色 | 文件 | ID 前缀 | 覆盖维度 |
|------|------|---------|---------|
| Devil Reviewer | `devil-reviewer.md` | DR | Novelty + Significance |
| Domain Expert — ML/AI | `domain-expert-ml.md` | DE | Significance + Theory |
| Literature Scout | `literature-scout.md` | LS | Novelty + Positioning |
| Reproducibility Auditor | `reproducibility-auditor.md` | RA | Reproducibility |

### 可选专家（Optional — 3 票/人，默认推荐启用）

| 角色 | 文件 | ID 前缀 | 覆盖维度 | 启用条件 |
|------|------|---------|---------|---------|
| Ethics & Compliance Auditor | `ethics-auditor.md` | EA | Ethics | 涉及数据集偏见、模型公平性、隐私(PII)、双重用途风险、环境影响时启用 |

## 投票权分布

| 配置 | 核心票 | 一般票 | 总票 | 核心占比 |
|------|-------|-------|------|---------|
| 7 角色（无 Ethics） | 3×5 = 15 | 4×3 = 12 | **27** | 56% |
| 8 角色（含 Ethics） | 3×5 = 15 | 5×3 = 15 | **30** | 50% |

## 特殊规则

- **FATAL 机制**: Devil Reviewer 标记 FATAL 的提案自动 +3 票
- **安全边界**: GM 拥有一票否决权

## 共享模板引用

| 用途 | 文件 |
|------|------|
| Phase 1 输出格式 | `../_shared/output-format-phase1.md` |
| Phase 2 输出格式 | `../_shared/output-format-phase2.md` |
| Phase 4 核心投票 | `../_shared/output-format-phase4-core.md` |
| Phase 4 一般投票 | `../_shared/output-format-phase4-general.md` |
