# Roster — 规范性与政策论证 (Normative & Policy Argumentation)

> 版本: 1.0 | 更新: 2026-03-15


> 编排层读取此文件确定角色列表、投票权重和文件映射。

## 范式信息

- **范式名**: normative-policy
- **适用领域**: 社会福利、公共政策、政治哲学、教育政策、卫生政策、发展经济学（政策建议部分）、环境政策、劳动政策
- **方法论核心**: 规范性论证（what *should* be done）——价值前提辩护、政策推导链、反事实分析、分配正义评估
- **关键差异点**: 核心贡献是"应当"命题而非实证发现；评审重心从数据方法转向论证逻辑、价值前提合理性和政策可行性；is-ought 区分是审查底线

## 专家配置

### 核心专家（Core — 5 票/人）

| 角色 | 文件 | ID 前缀 | 覆盖维度 |
|------|------|---------|---------|
| Methodology Critic | `methodology-critic.md` | MC | Rigor — 论证结构、is-ought 区分、逻辑有效性 |
| Policy Analyst | `policy-analyst.md` | PA | Rigor — 政策机制、反事实构建、实施路径、非预期后果 |
| Normative Theorist | `normative-theorist.md` | NT | Rigor — 规范框架评估、内在一致性、价值冲突处理 |

### 一般专家（General — 3 票/人）

| 角色 | 文件 | ID 前缀 | 覆盖维度 |
|------|------|---------|---------|
| Devil Reviewer | `devil-reviewer.md` | DR | Novelty + Significance |
| Domain Expert — Social Welfare | `domain-expert-social-welfare.md` | DE | Significance + 制度现实 |
| Literature Scout | `literature-scout.md` | LS | Novelty + Positioning + 政策文献 |
| Evidence Auditor | `evidence-auditor.md` | EV | 引用证据质量 (替代 Reproducibility) |

### 可选专家（Optional — 3 票/人，**默认必须启用**）

| 角色 | 文件 | ID 前缀 | 覆盖维度 | 启用条件 |
|------|------|---------|---------|---------|
| Rights & Equity Auditor | `rights-equity-auditor.md` | RE | 分配正义 + 人权 + 弱势群体 | **必须** — 政策论证必然涉及分配影响 |

## 投票权分布

| 配置 | 核心票 | 一般票 | 总票 | 核心占比 |
|------|-------|-------|------|---------|
| 8 角色（标准） | 3×5 = 15 | 5×3 = 15 | **30** | 50% |

## 特殊规则

- **FATAL 机制**: Devil Reviewer 标记 FATAL 的提案自动 +3 票
- **安全边界**: GM 拥有一票否决权
- **Rights & Equity 必选**: 政策论证涉及分配影响，Rights & Equity Auditor 默认必须启用

## 共享模板引用

| 用途 | 文件 |
|------|------|
| Phase 1 输出格式 | `../_shared/output-format-phase1.md` |
| Phase 2 输出格式 | `../_shared/output-format-phase2.md` |
| Phase 4 核心投票 | `../_shared/output-format-phase4-core.md` |
| Phase 4 一般投票 | `../_shared/output-format-phase4-general.md` |
