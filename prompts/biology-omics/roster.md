# Roster — 生物与组学科学 (Biology & Omics)

> 版本: 1.0 | 更新: 2026-03-06


> 编排层读取此文件确定角色列表、投票权重和文件映射。

## 范式信息

- **范式名**: biology-omics
- **适用领域**: 基因组学、蛋白组学、神经科学、生态学、生物信息学
- **方法论核心**: 高维统计、多重校正、批次效应、FAIR 数据
- **关键差异点**: FDR 校正、生物学重复 vs 技术重复、数据共享(GEO/SRA)

## 专家配置

### 核心专家（Core — 5 票/人）

| 角色 | 文件 | ID 前缀 | 覆盖维度 |
|------|------|---------|---------|
| Methodology Critic | `methodology-critic.md` | MC | Rigor — 批次效应/重复设计 |
| Experiment Designer | `experiment-designer.md` | ED | Rigor — 测序策略/对照设置 |
| Bioinformatician | `bioinformatician.md` | BI | Rigor — FDR/富集/降维 |

### 一般专家（General — 3 票/人）

| 角色 | 文件 | ID 前缀 | 覆盖维度 |
|------|------|---------|---------|
| Devil Reviewer | `devil-reviewer.md` | DR | Novelty + Significance |
| Domain Expert — Life Sci | `domain-expert-biology.md` | DE | Significance + Theory |
| Literature Scout | `literature-scout.md` | LS | Novelty + Positioning |
| Reproducibility Auditor | `reproducibility-auditor.md` | RA | Reproducibility |

### 可选专家（Optional — 3 票/人，**默认必须启用**）

| 角色 | 文件 | ID 前缀 | 覆盖维度 | 启用条件 |
|------|------|---------|---------|---------|
| Ethics & Compliance Auditor | `ethics-auditor.md` | EA | Ethics | **必须** — 人类样本伦理、基因隐私、动物实验3R、生物安全 |

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
