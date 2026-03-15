# Roster — 系统综述与 Meta 分析 (Systematic Review & Meta-Analysis)

> 版本: 1.0 | 更新: 2026-03-15

> 编排层读取此文件确定角色列表、投票权重和文件映射。

## 范式信息

- **范式名**: systematic-review
- **适用领域**: 医学/公共卫生（Cochrane）、社会科学（Campbell）、教育（EPPI-Centre）、环境科学、管理学
- **方法论核心**: 二次研究——搜索、筛选、提取、合成已发表的证据
- **关键差异点**: "数据"是已发表的研究而非原始观测；搜索策略是核心审查对象；评审标准高度标准化（PRISMA 2020）；发表偏倚是基本威胁

## 专家配置

### 核心专家（Core — 5 票/人）

| 角色 | 文件 | ID 前缀 | 覆盖维度 |
|------|------|---------|---------|
| Methodology Critic | `methodology-critic.md` | MC | Rigor — 综述设计、PICO、方案注册、综述类型选择 |
| Search Strategist | `search-strategist.md` | SS | Rigor — 搜索策略设计、数据库选择、灰色文献 |
| Meta-Analyst | `meta-analyst.md` | MA | Rigor — 效应量、异质性、亚组分析、发表偏倚 |

### 一般专家（General — 3 票/人）

| 角色 | 文件 | ID 前缀 | 覆盖维度 |
|------|------|---------|---------|
| Devil Reviewer | `devil-reviewer.md` | DR | Novelty + Significance |
| Domain Expert — General | `domain-expert-general.md` | DE | Significance + 领域适当性 |
| Literature Scout | `literature-scout.md` | LS | 搜索完整性（角色翻转：审搜索本身，非论文引文） |
| PRISMA & Reporting Auditor | `prisma-reporting-auditor.md` | PR | 报告合规 + 可复现性 |

### 可选专家（Optional — 3 票/人，**默认关闭**）

| 角色 | 文件 | ID 前缀 | 覆盖维度 | 启用条件 |
|------|------|---------|---------|---------|
| Ethics & Compliance Auditor | `ethics-auditor.md` | EA | Ethics | 综述直接指导临床实践或政策决策时启用 |

## 投票权分布

| 配置 | 核心票 | 一般票 | 总票 | 核心占比 |
|------|-------|-------|------|---------|
| 7 角色（默认） | 3×5 = 15 | 4×3 = 12 | **27** | 56% |
| 8 角色（含 Ethics） | 3×5 = 15 | 5×3 = 15 | **30** | 50% |

## 特殊规则

- **FATAL 机制**: Devil Reviewer 标记 FATAL 的提案自动 +3 票
- **安全边界**: GM 拥有一票否决权
- **Ethics 默认关闭**: 系统综述无一手数据采集，仅在有直接临床/政策指导意义时启用

## 共享模板引用

| 用途 | 文件 |
|------|------|
| Phase 1 输出格式 | `../_shared/output-format-phase1.md` |
| Phase 2 输出格式 | `../_shared/output-format-phase2.md` |
| Phase 4 核心投票 | `../_shared/output-format-phase4-core.md` |
| Phase 4 一般投票 | `../_shared/output-format-phase4-general.md` |
