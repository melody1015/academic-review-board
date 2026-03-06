# Roster — 实验与行为科学 (Experimental & Behavioral)

> 版本: 1.0 | 更新: 2026-03-06


> 编排层读取此文件确定角色列表、投票权重和文件映射。

## 范式信息

- **范式名**: experimental-behavioral
- **适用领域**: 心理学、行为经济学、教育学、市场营销、认知科学
- **方法论核心**: 实验室/田野实验、效应量、预注册
- **关键差异点**: 预注册一致性、被试伦理、效应量膨胀、需求特征

## 专家配置

### 核心专家（Core — 5 票/人）

| 角色 | 文件 | ID 前缀 | 覆盖维度 |
|------|------|---------|---------|
| Methodology Critic | `methodology-critic.md` | MC | Rigor — 实验设计/操控检查 |
| Experiment Designer | `experiment-designer.md` | ED | Rigor — 被试/程序/操控 |
| Psychometrician | `psychometrician.md` | PM | Rigor — ANOVA/SEM/效应量 |

### 一般专家（General — 3 票/人）

| 角色 | 文件 | ID 前缀 | 覆盖维度 |
|------|------|---------|---------|
| Devil Reviewer | `devil-reviewer.md` | DR | Novelty + Significance |
| Domain Expert — Behavioral | `domain-expert-behavioral.md` | DE | Significance + Theory |
| Literature Scout | `literature-scout.md` | LS | Novelty + Positioning |
| Reproducibility Auditor | `reproducibility-auditor.md` | RA | Reproducibility |

### 可选专家（Optional — 3 票/人，**默认必须启用**）

| 角色 | 文件 | ID 前缀 | 覆盖维度 | 启用条件 |
|------|------|---------|---------|---------|
| Ethics & Compliance Auditor | `ethics-auditor.md` | EA | Ethics | **必须** — 知情同意、欺骗程序、弱势群体 |

## 投票权分布

| 配置 | 核心票 | 一般票 | 总票 | 核心占比 |
|------|-------|-------|------|---------|
| 8 角色（标准） | 3×5 = 15 | 5×3 = 15 | **30** | 50% |

## 共享模板引用

| 用途 | 文件 |
|------|------|
| Phase 1 输出格式 | `../_shared/output-format-phase1.md` |
| Phase 2 输出格式 | `../_shared/output-format-phase2.md` |
| Phase 4 核心投票 | `../_shared/output-format-phase4-core.md` |
| Phase 4 一般投票 | `../_shared/output-format-phase4-general.md` |
