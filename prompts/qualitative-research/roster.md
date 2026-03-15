# Roster — 质性研究 (Qualitative Research)

> 版本: 1.0 | 更新: 2026-03-15


> 编排层读取此文件确定角色列表、投票权重和文件映射。

## 范式信息

- **范式名**: qualitative-research
- **适用领域**: 社会学、人类学、教育学、护理学、管理学（质性方向）、传播学、认知科学（质性方向）
- **方法论核心**: 解释性理解（Verstehen）——扎根理论、现象学、民族志、叙事分析、案例研究
- **关键差异点**: 评价体系从"效度/信度"转为"可信性/可迁移性/可靠性/可确认性"（Lincoln & Guba 1985）；无统计分析环节；编码过程和 reflexivity 是核心审查对象

## 专家配置

### 核心专家（Core — 5 票/人）

| 角色 | 文件 | ID 前缀 | 覆盖维度 |
|------|------|---------|---------|
| Methodology Critic | `methodology-critic.md` | MC | Rigor — 方法论选择合理性、理论抽样、分析框架 |
| Research Designer | `research-designer.md` | RD | Rigor — 案例/样本选取、田野设计、数据收集、三角验证 |
| Qualitative Analyst | `qualitative-analyst.md` | QA | Rigor — 编码过程、主题发展、分析饱和度、reflexivity |

### 一般专家（General — 3 票/人）

| 角色 | 文件 | ID 前缀 | 覆盖维度 |
|------|------|---------|---------|
| Devil Reviewer | `devil-reviewer.md` | DR | Novelty + Significance |
| Domain Expert — Social Science | `domain-expert-social-science.md` | DE | Significance + Theory |
| Literature Scout | `literature-scout.md` | LS | Novelty + Positioning + 方法论传统谱系 |
| Trustworthiness Auditor | `trustworthiness-auditor.md` | TA | Trustworthiness (替代 Reproducibility) |

### 可选专家（Optional — 3 票/人，**默认必须启用**）

| 角色 | 文件 | ID 前缀 | 覆盖维度 | 启用条件 |
|------|------|---------|---------|---------|
| Ethics & Compliance Auditor | `ethics-auditor.md` | EA | Ethics | **必须** — 质性研究必然涉及人类参与者 |

## 投票权分布

| 配置 | 核心票 | 一般票 | 总票 | 核心占比 |
|------|-------|-------|------|---------|
| 8 角色（标准） | 3×5 = 15 | 5×3 = 15 | **30** | 50% |

## 特殊规则

- **FATAL 机制**: Devil Reviewer 标记 FATAL 的提案自动 +3 票
- **安全边界**: GM 拥有一票否决权
- **Ethics 必选**: 质性研究涉及人类参与者，Ethics Auditor 默认必须启用

## 共享模板引用

| 用途 | 文件 |
|------|------|
| Phase 1 输出格式 | `../_shared/output-format-phase1.md` |
| Phase 2 输出格式 | `../_shared/output-format-phase2.md` |
| Phase 4 核心投票 | `../_shared/output-format-phase4-core.md` |
| Phase 4 一般投票 | `../_shared/output-format-phase4-general.md` |
