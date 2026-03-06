# Roster — 临床与流行病学 (Clinical & Epidemiology)

> 版本: 1.0 | 更新: 2026-03-06


> 编排层读取此文件确定角色列表、投票权重和文件映射。

## 范式信息

- **范式名**: clinical-epidemiology
- **适用领域**: 临床医学、药学、公共卫生、流行病学
- **方法论核心**: RCT、生存分析、前瞻性队列、系统综述
- **关键差异点**: CONSORT/STROBE、IRB 伦理、临床显著性 vs 统计显著性

## 专家配置

### 核心专家（Core — 5 票/人）

| 角色 | 文件 | ID 前缀 | 覆盖维度 |
|------|------|---------|---------|
| Methodology Critic | `methodology-critic.md` | MC | Rigor — RCT设计/偏倚风险 |
| Experiment Designer | `experiment-designer.md` | ED | Rigor — 样本量/随机化/终点 |
| Biostatistician | `biostatistician.md` | BS | Rigor — 生存分析/缺失数据 |

### 一般专家（General — 3 票/人）

| 角色 | 文件 | ID 前缀 | 覆盖维度 |
|------|------|---------|---------|
| Devil Reviewer | `devil-reviewer.md` | DR | Novelty + Significance |
| Domain Expert — Clinical | `domain-expert-clinical.md` | DE | Significance + Theory |
| Literature Scout | `literature-scout.md` | LS | Novelty + Positioning |
| Reproducibility Auditor | `reproducibility-auditor.md` | RA | Reproducibility |

### 可选专家（Optional — 3 票/人，**默认必须启用**）

| 角色 | 文件 | ID 前缀 | 覆盖维度 | 启用条件 |
|------|------|---------|---------|---------|
| Ethics & Compliance Auditor | `ethics-auditor.md` | EA | Ethics | **必须** — 知情同意、IRB、DSMB、受试者保护 |

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
