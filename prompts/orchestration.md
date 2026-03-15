# Academic Review Board — Orchestration Protocol (Template)

> 参考框架: AgentReview (EMNLP 2024) + MARG (Allen AI 2024) + PRE (CIKM 2024)
> 版本: v2.0 (2026-03-06) — 支持多范式动态 roster 加载

---

## 1. 角色与权重

### 1.1 范式选择

GM 在 Phase 0 确定本次评审使用的研究范式。可用范式存放在 `prompts/` 子目录中：

| 范式目录 | 名称 | 状态 |
|---------|------|------|
| `economics-finance/` | 实证经济学与金融 | ✅ 可用 |
| `clinical-epidemiology/` | 临床与流行病学 | ✅ 可用 |
| `cs-ai/` | 计算机科学与 AI | ✅ 可用 |
| `experimental-behavioral/` | 实验与行为科学 | ✅ 可用 |
| `natural-science-engineering/` | 自然科学与工程 | ✅ 可用 |
| `biology-omics/` | 生物与组学科学 | ✅ 可用 |
| `qualitative-research/` | 质性研究 | ✅ 可用 |
| `normative-policy/` | 规范性与政策论证 | ✅ 可用 |
| `systematic-review/` | 系统综述与 Meta 分析 | ✅ 可用 |
| `mixed-methods/` | 混合方法 | ✅ 可用 |

> 范式选择指南见 `paradigm_role_structure.md` 的 §1.4 范式选择指南。

#### 边界案例判定（混合方法论）

| 论文类型 | 方法论核心 | 选择 | 理由 |
|----------|----------|------|------|
| 计算社会科学（NLP + 行为分析） | 若核心贡献是 NLP 模型 | `cs-ai` | 审核 ML 管线质量 |
| 计算社会科学（NLP + 行为分析） | 若核心贡献是行为发现 | `experimental-behavioral` | 审核构念效度和样本 |
| 生物信息 + 深度学习 | 若核心是新算法 | `cs-ai` | 审核消融/基线公平 |
| 生物信息 + 深度学习 | 若核心是生物发现 | `biology-omics` | 审核正交验证/FDR |
| 数字健康（可穿戴 + RCT） | 若有临床终点 | `clinical-epidemiology` | 审核 ITT/CONSORT |
| 数字健康（可穿戴 + RCT） | 若重点在传感器设计 | `natural-science-engineering` | 审核测量不确定度 |
| 计量经济 + ML 预测 | 若核心是因果推断 | `economics-finance` | 审核内生性/IV |
| 计量经济 + ML 预测 | 若核心是预测精度 | `cs-ai` | 审核 test leakage |
| 材料学 + 计算模拟 | 若有实验验证 | `natural-science-engineering` | 审核仿真-实验一致性 |
| 神经科学 + 影像 | 看是否有组学数据 | `biology-omics` 或 `experimental-behavioral` | 有基因/蛋白→生物；纯行为→行为 |
| 政策评估 + RCT | 若核心是因果效果估计 | `economics-finance` 或 `clinical-epidemiology` | 审核内生性/ITT |
| 政策评估 + RCT | 若核心是政策建议/规范论证 | `normative-policy` | 审核论证链和价值前提 |
| 质性 + 量化混合方法 | 若核心贡献是质性发现 | `qualitative-research` | 审核可信性框架 |
| 质性 + 量化混合方法 | 若核心贡献是量化发现 | 对应实证范式 | 审核统计/因果推断 |
| 教育/卫生政策实证 | 若用实验方法 | `experimental-behavioral` | 审核被试/效应量 |
| 教育/卫生政策实证 | 若做规范性建议 | `normative-policy` | 审核论证链 |
| 社会学/人类学田野研究 | 质性方法为主 | `qualitative-research` | 审核编码/饱和/可信性 |
| 政治哲学/社会正义 | 规范论证为主 | `normative-policy` | 审核价值前提/论证逻辑 |
| 系统综述 + 原始数据分析 | 若核心是合成已有证据 | `systematic-review` | 审搜索/合成/偏倚 |
| 系统综述 + 原始数据分析 | 若核心是新的一手分析 | 对应实证范式 | 审一手数据方法 |
| 质性 + 量化（有意整合） | 两种方法有整合设计 | `mixed-methods` | 审整合质量 |
| 质性 + 量化（无整合） | 各说各话 | 分别跑两个范式 | 无整合可审 |
| 范围综述（Scoping review） | 系统搜索但不做 meta 分析 | `systematic-review` | 审搜索策略和报告质量 |
| 伞状综述（Umbrella review） | 综述的综述 | `systematic-review` | 审搜索+纳入 SR 的质量评估 |

> **原则**：看方法论核心（statistical engine），不看学科归属。若仍难以判断，选对核心 claim 审查最严格的范式。

### 1.2 专家分层（动态加载）

每个范式目录下有 `roster.md`，定义该范式的专家配置。三层结构：

**Layer 2 — 核心专家（方法论三角）— 每人5票：**
- 读取 `prompts/{paradigm}/roster.md` 中 `core` 部分
- 通常 3 个角色：Methodology Critic + Experiment Designer + Statistician（名称可能随范式变化）

**Layer 1 + Layer 3 — 一般专家 — 每人3票：**
- 读取 `prompts/{paradigm}/roster.md` 中 `general` + `optional` 部分
- 通常 4-5 个角色，含 Devil Reviewer、Domain Expert、Literature Scout、Reproducibility Auditor
- 可选角色（如 Ethics Auditor）的启用由 roster.md 配置

**投票力分布：** 核心 3×5=15 / 一般 N×3 / 总票数随角色数动态计算

**Devil Reviewer特权：** FATAL标记的提案自动+3分

**共享输出格式：** 所有角色的输出格式模板在 `prompts/_shared/` 中

**评审标准体系：**
- Reproducibility Auditor: `Practical Checks (Graded Rubric)` — ✅/⚠️/❌ 三级评分，量表见 `_shared/grading-scale.md`
- Devil Reviewer: `Red Flags` — 范式特定致命缺陷标记
- 其余角色: `Rejection Triggers` — ❌ FATAL / ⚠️ MAJOR 二元红线，来源标注权威标准

### 1.2 裁决者

**GM (Inclusive风格，参考AgentReview)：**
- 综合所有评审+讨论+投票结果做最终裁决
- 不偏向任何单一专家，也不简单跟从多数
- 安全边界一票否决权（不泄露项目安全边界清单中的内容）

---

## 2. 评审流程（4阶段）

### Phase 1: 独立评审
```
输入：知识包（议题材料 + 相关文件）
     ↓
N位专家各自独立生成3个提案
     ↓
产出：N×3个提案（每个含ID/标题/优先级/详情/行动）
```

**规则：**
- 专家之间**不可见**彼此提案（防止锚定效应）
- 每位专家只看到知识包和自己的角色定义
- 至少2/3提案必须与会议议题直接相关

### Phase 2: 交叉讨论（借鉴MARG内部讨论）
```
输入：Phase 1的21个提案（随机打乱顺序，隐去来源角色）
     ↓
每位专家看到所有提案，可以：
  - 支持（+理由）
  - 质疑（+具体反驳）
  - 补充（+新信息/角度）
  - 合并建议（指出与自己某提案重叠）
     ↓
原提案作者可修改或撤回自己的提案
     ↓
产出：修订后的提案列表 + 讨论记录
```

**规则：**
- 提案呈现顺序每次**随机打乱**（借鉴PRE位序偏差消除）
- 提案**隐去来源角色**（匿名评审，防止权威偏差）
- 每位专家必须对至少5个非自己的提案发表意见
- Devil Reviewer可在此阶段对任何提案追加FATAL标记

### Phase 3: 精炼与去重（借鉴MARG Refinement阶段）
```
输入：Phase 2修订后的提案列表 + 讨论记录
     ↓
GM执行精炼：
  1. 合并实质重复的提案（保留表述更好的版本）
  2. 淘汰空洞/generic的提案（无具体行动步骤的）
  3. 拆分混合了多个独立问题的提案
  4. 安全审查：标记任何涉及信息泄露风险的提案
     ↓
产出：精炼后的提案列表（通常压缩 30-40%）
```

### Phase 4: 加权投票 + GM裁决
```
输入：精炼后的提案列表
     ↓
核心专家（方法论三角）：每人投5票给最重要的5个提案
一般专家：每人投3票给最重要的3个提案
FATAL提案自动+3分
     ↓
按总票数排序
     ↓
GM综合票数+讨论记录+安全考量做最终裁决
     ↓
产出：优先行动计划 + VETO日志
```

**投票规则：**
- 不能投给自己的提案（防止利益冲突）
- 提案呈现顺序随机打乱（每位专家看到不同顺序）
- GM可推翻投票结果，但必须给出理由

---

## 3. 事后评议与专家改进机制

> 参考：Publons编辑评分 + TAVB导师带教 + Cochrane校准练习 + BMJ植入错误RCT + NSF面板校准

### 3.1 Calibration Session（校准会议，借鉴Cochrane）
**时机：** 首次正式评审前 + 每加入新专家角色时
**做法：**
1. 准备一份"calibration document"——包含已知优缺点的研究设计方案
2. N位专家独立评审（和正式Phase 1相同流程）
3. GM比对所有输出：
   - 哪些已知缺陷被发现了？哪些漏掉了？（检出率）
   - 专家之间对同一问题的判断是否一致？（inter-rater agreement）
   - 哪些专家产出了generic vs specific的提案？
4. 根据calibration结果，在正式评审前微调prompt
5. calibration记录保存到 `cache/calibration-log.json`

**Cochrane的发现：** inter-rater agreement依赖于审稿人对（κ range 0.38-1.0），
事前校准可以显著缩小分歧。我们的目标：确保所有专家在"什么算P0/P1/P2"上有共识。

### 3.2 三层事后评议

#### Layer 1: Session Debrief（每次评审后自动）
GM在Phase 4裁决完成后，对每位专家的每个提案记录命运：
```
ADOPTED   — 被采纳进入行动计划
MERGED    — 与其他提案合并（部分价值）
PRUNED    — Phase 3被精炼掉，附原因：
            ├── GENERIC（无具体行动步骤）
            ├── DUPLICATE（与其他提案重复）
            ├── IRRELEVANT（偏离会议议题）
            └── SECURITY（触碰安全边界）
IGNORED   — 进入投票但得0票
VETOED    — GM否决，附原因
```
更新 `academic-board-history.json` + 各专家 `.memory.md`

#### Layer 2: Pattern Analysis（每3次评审后）
累积3次数据后，分析失败模式并执行对应改进：

| 失败模式 | 阈值 | 改进动作 | 对标 |
|----------|------|---------|------|
| GENERIC率高 | >50% | prompt加反面范例（generic→specific示范） | TAVB导师modeling |
| DUPLICATE率高 | >40% | prompt加差异化指令（明确与其他角色边界） | 角色边界澄清 |
| IRRELEVANT率高 | >30% | prompt强化议题锚定要求 | NSF评审指南 |
| IGNORED率高 | >60% | 分析是质量差还是角度偏，调整关注重点 | Publons编辑反馈 |
| 采纳率低 | <20% | 触发Layer 3深度修订 | — |

#### Layer 3: Expert Revision（触发式，含Planted Error Test）
当某专家累积采纳率 < 20%，执行深度修订：

**Step 1: 诊断根因**
- 知识缺口？（不知道某方法/论文）→ 补充知识包
- 判断力差？（知道但优先级判断错）→ 加校准范例
- 角色偏移？（做了别人的事）→ 修改Review Focus

**Step 2: 修改prompt / knowledge pack**

**Step 3: Planted Error Test（借鉴BMJ RCT）**
- 准备一份包含3-5个**已知缺陷**的测试文档
- 缺陷按严重度分级：1个FATAL + 2个MAJOR + 2个MINOR
- 让修改后的专家评审此文档
- 检查检出率：FATAL必须100%发现，MAJOR≥80%，MINOR≥50%
- 如未达标，继续调整prompt并重测

**Step 4: 记录到 `.memory.md`**

### 3.3 专家记忆文件（.memory.md）
每位专家维护独立的学习记忆文件（对标TAVB导师带教的持续反馈）。

**文件路径规范（按范式隔离）：**
```
cache/memory/{paradigm}/{role-name}.memory.md
```
> 同名角色（如 methodology-critic）在不同范式下是完全不同的人设，记忆不能混用。

**模板**：`templates/expert-memory.md`（含范式和角色元信息字段）。

```markdown
# [Expert Name] — Learning Memory

## 元信息
- **范式**: economics-finance
- **角色**: methodology-critic
- **版本**: 1.0

## 累积统计
- 总提案: N | 采纳: X (Y%) | 合并: A | 精炼掉: B | 忽略: C

## 校准范例（对标TAVB的modeling）
### 高质量提案示范
- [提案ID] (Session N): "[具体内容]" → 被N个核心票采纳

### 反面教材
- [提案ID] (Session N): "[具体内容]" → PRUNED(GENERIC)

## 知识补充
- [Session N后] [补充的具体知识点]

## 关注调整
- [Session N后] [调整的关注方向和原因]

## Planted Error Test记录
- [日期]: 测试文档含5个缺陷，检出: FATAL 1/1, MAJOR 2/2, MINOR 1/2
```

### 3.4 历史采纳率追踪（借鉴PRE质量追踪）

### 3.1 追踪文件
```json
// cache/academic-board-history.json
{
  "sessions": [
    {
      "date": "2026-03-01",
      "paradigm": "economics-finance",
      "topic": "Phase 1 experiment design review",
      "proposals_total": "N×3",
      "proposals_after_refinement": 12,
      "proposals_accepted": 8,
      "expert_stats": {
        "{role-from-roster}": {"proposed": 3, "accepted": 3, "votes_received": 12}
      }
    }
  ]
}
```

### 3.2 长期权重调整（每3次评审后）
- 累积采纳率 > 70%：权重不变（已证明高质量）
- 累积采纳率 40-70%：权重不变（正常范围）
- 累积采纳率 < 40% 且 票数也低：GM考虑调整该角色prompt或降1票
- **只在累积≥3次评审后才调整，避免小样本过拟合**

---

## 4. 知识包构成

每次评审会议前，GM准备知识包包含：

```
知识包/
├── 议题说明（本次评审重点）
├── 论文草稿（或实验设计方案）
├── 相关参考文献摘要
├── 安全边界清单（不可泄露的内容）
├── 上次评审行动计划完成情况（如有）
├── 数据/结果快照（如有）
├── code-architecture-digest.md（如有代码库 + GitNexus 已索引，所有专家共享）
└── calibration-template.md（范式对应的校准模板，含 FATAL/MAJOR/MINOR 植入缺陷）
```

**重要：知识包不包含其他专家的历史提案或评审记录（防止锚定）**

---

## 5. 执行实现

### 5.0 Phase 0: 范式选择 + 知识包预生成

> v2.0 更新：支持多范式。GitNexus 集成在知识包生成层，不在编排层。

**Step 1: 范式选择**

GM 根据论文的方法论核心确定范式（参考范式选择指南），记录在知识包头部：
```
paradigm: economics-finance   # 或 cs-ai, clinical-epidemiology 等
```

**Step 2: 知识包生成**

```bash
python3 scripts/build-knowledge.py --topic "{议题}" --paradigm "{范式名}"
```

脚本自动完成（5 步流程）：
1. 跨语言关键词提取（中文议题 → 英文代码关键词，Sonnet LLM）
2. GitNexus 查询（关键词 → 相关代码符号/执行流）
3. 深度展开（关键函数的 blast radius）
4. 角色过滤（按范式 roster 决定哪些角色需要附加信息）
5. 格式化输出

**产出文件：**
- `cache/code-architecture-digest.md` — 注入知识包，所有专家共享（使用指南见 `_shared/code-context-guide.md`）
- `cache/build-knowledge-log.json` — 运行日志

`--paradigm` 缺省时默认 `economics-finance`（向后兼容）。

**Step 3: 加载 roster**

读取 `prompts/{paradigm}/roster.md`，获取：
- 激活的角色列表（core + general + 启用的 optional）
- 每个角色的 prompt 文件路径
- 投票权重

### 5.1 Sub-Agent调度（动态）

```
Phase 0: GM 确认范式 → 加载 roster → 运行 build-knowledge.py
         N = len(激活角色列表)   // 通常 7 或 8

Phase 1: spawn N 个 sub-agent（并行），每个角色一个
         for role in roster:
           指令 = prompts/{paradigm}/{role.file}
                + _shared/output-format-phase1.md
                + 知识包
                + "输出3个提案，只回复JSON"
           if role.file == 'reproducibility-auditor.md':
             指令 += code-architecture-digest.md（若存在）
         
Phase 2: spawn N 个 sub-agent（并行）
         指令 = 角色prompt + _shared/output-format-phase2.md
              + 所有提案(随机序,匿名) + "对每个非自己的提案评论"
         
Phase 3: GM自己执行（不spawn）
         合并/去重/淘汰/安全审查
         
Phase 4: spawn N 个 sub-agent（并行）
         for role in roster:
           if role.category == 'core':
             指令 += _shared/output-format-phase4-core.md
           else:
             指令 += _shared/output-format-phase4-general.md
         指令 += 精炼提案列表(随机序) + "投X票"
         GM综合裁决
```

### 5.2 成本估算
- 每阶段 N 个 sub-agent × ~2000 token/agent（N 通常 7-8）
- 4阶段 × N×2K = ~56-64K token + GM综合 ~10K ≈ ~66-74K token
- 约 $2-3/次评审（Opus定价）

### 5.3 静默原则
所有sub-agent任务指令包含：
> "完成后只回复结构化JSON，不要输出任何摘要或说明。"

---

## 6. 自定义指南

| 可调项 | 默认 | 修改方式 |
|--------|------|---------|
| 专家数量 | 7 | 增减角色 prompt 文件，保持核心三角 |
| 投票权重 | 核心5/一般3 | 修改各角色 prompt 的 Phase 4 段 |
| Phase 2 | 开启 | 设为可选，跳过时直接进 Phase 3 |
| Phase 3 | 开启 | 设为可选，跳过时直接进 Phase 4 |
| FATAL +3 | 开启 | 在 GM prompt 中关闭或调整 |
| Domain Expert | 金融 | 替换 `domain-expert-finance.md` 为其他领域 |
| 安全边界 | 空模板 | 在 `gm-academic.md` 中定义 |
| GitNexus | 开启 | 未索引时自动跳过 |
