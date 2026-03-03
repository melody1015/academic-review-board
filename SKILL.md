---
name: academic-review-board
description: "AI Academic Review Board — multi-agent peer review for research papers. Use when: user wants to review a paper/experiment design, run a peer review session, set up a review board for a research project, or evaluate research methodology. NOT for: code review, investment decisions, or simple proofreading."
---

# Academic Review Board — AI 学术同行评审

用 LLM multi-agent 模拟学术同行评审，在论文投稿前发现方法论缺陷。

## 文献基础

| 框架 | 来源 | 我们借鉴了什么 |
|------|------|---------------|
| AgentReview | Georgia Tech, EMNLP 2024 | Inclusive AC 风格、强制排序、数值锚点 |
| MARG | Northwestern / Allen AI, 2024 | 专业化分工、内部讨论、Refinement |
| PRE | 清华, CIKM 2024 | 位序随机化、匿名评审、质量追踪 |

## 架构

```
7 位专家 + 1 位 GM (General Manager)
4 阶段: 独立评审 → 交叉讨论 → 精炼去重 → 加权投票 + GM 裁决
```

### 专家分层与投票权

**核心专家（方法论三角）— 每人 5 票：**

| 角色 | Prompt | 覆盖 |
|------|--------|------|
| Methodology Critic | `methodology-critic.md` | 研究设计、因果推断、look-ahead |
| Experiment Designer | `experiment-designer.md` | 样本构建、point-in-time 设计 |
| Econometrician | `econometrician.md` | 统计方法、多重检验、效应量 |

**一般专家 — 每人 3 票：**

| 角色 | Prompt | 覆盖 |
|------|--------|------|
| Devil Reviewer | `devil-reviewer.md` | 致命缺陷、claim-evidence gap |
| Domain Expert | `domain-expert-finance.md` | 理论根基（可替换为其他领域） |
| Literature Scout | `literature-scout.md` | 文献覆盖、定位准确性 |
| Reproducibility Auditor | `reproducibility-auditor.md` | 数据溯源、代码复现 |

**投票力分布：** 核心 3×5=15 (56%) / 一般 4×3=12 (44%)

**Devil Reviewer 特权：** FATAL 标记的提案自动 +3 分

### GM 职责
- Phase 3 精炼执行（合并/去重/淘汰/安全审查）
- Phase 4 综合裁决（可推翻投票，须给理由）
- 安全边界一票否决权
- 更新专家记忆和历史追踪

## 4 阶段评审流程

### Phase 1: 独立评审
- 7 位专家各自独立生成 3 个提案（共 21 个）
- 专家之间**不可见**彼此提案（防锚定）
- 每位专家只看到知识包 + 自己的角色定义

### Phase 2: 交叉讨论（借鉴 MARG）
- 所有提案**随机打乱顺序 + 隐去来源角色**
- 每位专家对其他人的提案发表意见：支持/质疑/补充/合并
- 原提案作者可修改或撤回
- Devil Reviewer 可追加 FATAL 标记

### Phase 3: 精炼（GM 执行，借鉴 MARG Refinement）
- 合并重复、淘汰空洞提案、拆分混合问题、安全审查
- 通常 21 个 → 10-14 个

### Phase 4: 加权投票 + GM 裁决
- 核心 5 票，一般 3 票，不能投自己
- 提案顺序随机（每人不同）
- GM 综合票数 + 讨论记录 + 安全考量做最终裁决

## 知识包生成（含 GitNexus）

评审前运行知识包生成器，为 Reproducibility Auditor 注入代码架构上下文：

```bash
python3 {project}/review-board/scripts/build-knowledge.py --topic "{议题}"
```

5 步流程：跨语言关键词提取 → GitNexus 查询 → blast radius 展开 → 角色过滤 → Markdown 输出。
详见 `scripts/build-knowledge.py`。

**前提**：项目已用 `gitnexus analyze` 索引。未索引时自动跳过，不影响其他专家。

## 专家改进机制

### 三层事后评议

1. **Session Debrief**（每次评审后）：记录每个提案命运 (ADOPTED/MERGED/PRUNED/IGNORED/VETOED)
2. **Pattern Analysis**（每 3 次评审后）：检测 GENERIC>50% / DUPLICATE>40% / IRRELEVANT>30% 等失败模式
3. **Expert Revision**（触发式）：诊断根因 + 修改 prompt + Planted Error Test 验证

### 专家记忆文件 (.memory.md)
每位专家维护独立学习记忆：累积统计、校准范例（好/坏提案示范）、知识补充、关注调整。
模板见 `templates/expert-memory.md`。

### 校准会议（Calibration Session）
首次评审前 + 新增专家时，用包含已知缺陷的测试文档校准所有专家。
目标：确保 7 位专家对 "什么算 P0/P1/P2" 有共识。

## 成本估算
- 每阶段 7 agents × ~2000 token = ~14K token
- 4 阶段 + GM = ~66K token/次
- ~$2-3/次（Opus 定价）

## 在新项目中使用

### 初始化

```bash
# 1. 在项目中创建 review-board 目录
mkdir -p {project}/review-board/{prompts,scripts,sessions,cache}

# 2. 复制模板（从 skill 目录）
cp ~/clawd/skills/academic-review-board/prompts/*.md {project}/review-board/prompts/
cp ~/clawd/skills/academic-review-board/scripts/build-knowledge.py {project}/review-board/scripts/
cp ~/clawd/skills/academic-review-board/templates/* {project}/review-board/cache/

# 3. 自定义
#    - gm-academic.md: 修改 Security Boundaries（每个项目不同）
#    - domain-expert-finance.md: 如果不是金融方向，替换为对应领域专家
#    - build-knowledge.py: 修改 REPO_NAME 为你的项目名

# 4. 索引代码库（可选，Reproducibility Auditor 用）
cd {project} && gitnexus analyze
```

### 运行评审

```bash
# 1. 生成知识包附录
python3 review-board/scripts/build-knowledge.py --topic "{议题}"

# 2. 准备知识包 (knowledge-pack.md)
#    包含：议题说明 + 论文草稿/实验方案 + 参考文献 + 安全边界

# 3. 按 orchestration.md 执行 4 阶段
#    Phase 1-4 通过 sessions_spawn 并行调度 7 位专家
```

### 自定义选项

| 可调项 | 默认 | 说明 |
|--------|------|------|
| 专家数量 | 7 | 可增减，但保持核心三角（方法论/实验/计量） |
| 投票权重 | 核心5/一般3 | 可改为等权（所有人3票） |
| Phase 2 交叉讨论 | 开启 | 时间紧可跳过（牺牲质量换速度） |
| Phase 3 精炼 | 开启 | 可跳过让 GM 直接进投票 |
| FATAL 机制 | +3 分 | 可关闭或调整加分值 |
| Domain Expert | 金融 | 替换为计算机/医学/物理等任何领域 |
| GitNexus 集成 | 开启 | 无代码库的纯理论论文可关闭 |
