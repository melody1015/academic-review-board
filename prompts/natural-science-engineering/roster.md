# Roster — 自然科学与工程 (Natural Science & Engineering)

> 版本: 1.0 | 更新: 2026-03-06


> 编排层读取此文件确定角色列表、投票权重和文件映射。

## 范式信息

- **范式名**: natural-science-engineering
- **适用领域**: 物理、化学、材料科学、电子工程、机械工程
- **方法论核心**: 测量不确定度、误差传播、仿真验证、实验控制
- **关键差异点**: GUM 标准、SI 单位一致性、仿真-实验交叉验证、数值精度

## 专家配置

### 核心专家（Core — 5 票/人）

| 角色 | 文件 | ID 前缀 | 覆盖维度 |
|------|------|---------|---------|
| Methodology Critic | `methodology-critic.md` | MC | Rigor — 测量不确定度/实验控制 |
| Experiment Designer | `experiment-designer.md` | ED | Rigor — 标定/环境控制/重复 |
| Metrologist | `metrologist.md` | MT | Rigor — GUM/误差传播/拟合 |

### 一般专家（General — 3 票/人）

| 角色 | 文件 | ID 前缀 | 覆盖维度 |
|------|------|---------|---------|
| Devil Reviewer | `devil-reviewer.md` | DR | Novelty + Significance |
| Domain Expert — Physics/Eng | `domain-expert-physics.md` | DE | Significance + Theory |
| Literature Scout | `literature-scout.md` | LS | Novelty + Positioning |
| Reproducibility Auditor | `reproducibility-auditor.md` | RA | Reproducibility |

### 可选专家（Optional — 3 票/人，默认关闭）

| 角色 | 文件 | ID 前缀 | 覆盖维度 | 启用条件 |
|------|------|---------|---------|---------|
| Ethics & Compliance Auditor | `ethics-auditor.md` | EA | Ethics | 涉及辐射/化学品安全、军民两用或环境影响时启用 |

## 投票权分布

| 配置 | 核心票 | 一般票 | 总票 | 核心占比 |
|------|-------|-------|------|---------|
| 7 角色（默认） | 3×5 = 15 | 4×3 = 12 | **27** | 56% |
| 8 角色（含 Ethics） | 3×5 = 15 | 5×3 = 15 | **30** | 50% |

## 共享模板引用

| 用途 | 文件 |
|------|------|
| Phase 1 输出格式 | `../_shared/output-format-phase1.md` |
| Phase 2 输出格式 | `../_shared/output-format-phase2.md` |
| Phase 4 核心投票 | `../_shared/output-format-phase4-core.md` |
| Phase 4 一般投票 | `../_shared/output-format-phase4-general.md` |
