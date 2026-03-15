# Roster — 混合方法 (Mixed Methods)

> 版本: 1.0 | 更新: 2026-03-15

> 编排层读取此文件确定角色列表、投票权重和文件映射。

## 范式信息

- **范式名**: mixed-methods
- **适用领域**: 教育学、护理学、公共卫生、管理学、社会工作、评估研究
- **方法论核心**: 质性 + 量化的有意整合——不是"各做各的放在一起"，而是两种方法在设计、收集、分析或解释的某个点上真正对话
- **关键差异点**: 核心贡献在第三层——整合；需要同时用三套标准（量化/质性/整合）评估；单独跑质性范式+实证范式无法覆盖整合质量

## 专家配置

### 核心专家（Core — 5 票/人）

| 角色 | 文件 | ID 前缀 | 覆盖维度 |
|------|------|---------|---------|
| Methodology Critic | `methodology-critic.md` | MC | Rigor — 混合设计类型、范式立场、混合理由 |
| Integration Analyst | `integration-analyst.md` | IA | Rigor — 整合点、整合技术、真实 vs 装饰性整合 |
| Methods Auditor | `methods-auditor.md` | MU | Rigor — 双线审查：量化+质性各自的方法论质量 |

### 一般专家（General — 3 票/人）

| 角色 | 文件 | ID 前缀 | 覆盖维度 |
|------|------|---------|---------|
| Devil Reviewer | `devil-reviewer.md` | DR | Novelty + Significance |
| Domain Expert — General | `domain-expert-general.md` | DE | Significance + 领域适当性 |
| Literature Scout | `literature-scout.md` | LS | Novelty + Positioning + 混合方法方法论文献 |
| Reproducibility & Trustworthiness Auditor | `reproducibility-trustworthiness-auditor.md` | RT | 量化复现 + 质性可信性 + 整合审计线索 |

### 可选专家（Optional — 3 票/人，按需启用）

| 角色 | 文件 | ID 前缀 | 覆盖维度 | 启用条件 |
|------|------|---------|---------|---------|
| Ethics & Compliance Auditor | `ethics-auditor.md` | EA | Ethics | 质性部分涉及人类参与者时启用 |

## 投票权分布

| 配置 | 核心票 | 一般票 | 总票 | 核心占比 |
|------|-------|-------|------|---------|
| 7 角色（默认） | 3×5 = 15 | 4×3 = 12 | **27** | 56% |
| 8 角色（含 Ethics） | 3×5 = 15 | 5×3 = 15 | **30** | 50% |

## 特殊规则

- **FATAL 机制**: Devil Reviewer 标记 FATAL 的提案自动 +3 票
- **安全边界**: GM 拥有一票否决权
- **Ethics 按需**: 质性部分涉及人类参与者（访谈/观察/焦点小组）时启用

## 共享模板引用

| 用途 | 文件 |
|------|------|
| Phase 1 输出格式 | `../_shared/output-format-phase1.md` |
| Phase 2 输出格式 | `../_shared/output-format-phase2.md` |
| Phase 4 核心投票 | `../_shared/output-format-phase4-core.md` |
| Phase 4 一般投票 | `../_shared/output-format-phase4-general.md` |
