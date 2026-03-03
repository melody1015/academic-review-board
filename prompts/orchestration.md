# Academic Review Board — Orchestration Protocol (Template)

> 参考框架: AgentReview (EMNLP 2024) + MARG (Allen AI 2024) + PRE (CIKM 2024)
> 版本: v1.1 (2026-03-04) — 从 ipl-paper 提取为通用模板

---

## 1. 角色与权重

### 1.1 专家分层

**核心专家（方法论三角）— 每人5票：**
| 角色 | 文件 | 权重根据 |
|------|------|---------|
| Methodology Critic | methodology-critic.md | 方法论缺陷=~30%拒稿原因 |
| Experiment Designer | experiment-designer.md | 实证设计=方法论的另一面 |
| Econometrician | econometrician.md | 统计问题=~25%拒稿原因 |

**一般专家 — 每人3票：**
| 角色 | 文件 | 权重根据 |
|------|------|---------|
| Devil Reviewer | devil-reviewer.md | 跨维度fatal flaw检测 |
| Domain Expert Finance | domain-expert-finance.md | 理论贡献+机制审查 |
| Literature Scout | literature-scout.md | 文献定位 |
| Reproducibility Auditor | reproducibility-auditor.md | 数据复现 |

**投票力分布：** 核心 3×5=15 (56%) / 一般 4×3=12 (44%)

**Devil Reviewer特权：** FATAL标记的提案自动+3分

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
7位专家各自独立生成3个提案
     ↓
产出：21个提案（每个含ID/标题/优先级/详情/行动）
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
产出：精炼后的提案列表（通常15-18个 → 10-14个）
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
2. 7位专家独立评审（和正式Phase 1相同流程）
3. GM比对所有输出：
   - 哪些已知缺陷被发现了？哪些漏掉了？（检出率）
   - 专家之间对同一问题的判断是否一致？（inter-rater agreement）
   - 哪些专家产出了generic vs specific的提案？
4. 根据calibration结果，在正式评审前微调prompt
5. calibration记录保存到 `cache/calibration-log.json`

**Cochrane的发现：** inter-rater agreement依赖于审稿人对（κ range 0.38-1.0），
事前校准可以显著缩小分歧。我们的目标：确保7位专家在"什么算P0/P1/P2"上有共识。

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
每位专家维护独立的学习记忆文件（对标TAVB导师带教的持续反馈）：

```markdown
# [Expert Name] — Learning Memory

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
      "topic": "Phase 1 experiment design review",
      "proposals_total": 21,
      "proposals_after_refinement": 12,
      "proposals_accepted": 8,
      "expert_stats": {
        "methodology-critic": {"proposed": 3, "accepted": 3, "votes_received": 12},
        "experiment-designer": {"proposed": 3, "accepted": 2, "votes_received": 10},
        "econometrician": {"proposed": 3, "accepted": 2, "votes_received": 9},
        "devil-reviewer": {"proposed": 3, "accepted": 1, "fatal_used": 1, "votes_received": 7},
        "domain-expert": {"proposed": 3, "accepted": 0, "votes_received": 3},
        "literature-scout": {"proposed": 3, "accepted": 0, "votes_received": 2},
        "reproducibility-auditor": {"proposed": 3, "accepted": 0, "votes_received": 1}
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
└── 数据/结果快照（如有）
```

**重要：知识包不包含其他专家的历史提案或评审记录（防止锚定）**

---

## 5. 执行实现

### 5.0 Phase 0: 知识包预生成（含 GitNexus 代码架构）

> 2026-03-04 新增。GitNexus 集成在知识包生成层，不在编排层。

**Phase 1 启动前**，运行知识包生成脚本：

```bash
python3 review-board/scripts/build-knowledge.py --topic "{本次评审议题}"
```

脚本自动完成（5 步流程）：
1. 跨语言关键词提取（中文议题 → 英文代码关键词，Sonnet LLM）
2. GitNexus 查询（关键词 → 相关代码符号/执行流）
3. 深度展开（关键函数的 blast radius）
4. 角色过滤（仅 Reproducibility Auditor 需要）
5. 格式化输出

**产出文件：**
- `review-board/cache/code-architecture-digest.md` — Reproducibility Auditor 专用附录
- `review-board/cache/build-knowledge-log.json` — 运行日志

**Phase 1 spawn Reproducibility Auditor 时**，读取 `code-architecture-digest.md` 作为知识包附录：
```
指令 = reproducibility-auditor.md + 知识包 + code-architecture-digest.md 内容 + "输出3个提案，只回复JSON"
```

其他 6 位专家的指令不变（不含 code architecture digest）。

如果脚本执行失败或 GitNexus 未索引，Reproducibility Auditor 按原方式工作（向后兼容）。

### 5.1 Sub-Agent调度

```
Phase 1: spawn 7个sub-agent（并行），每个角色一个
         指令 = 角色prompt + 知识包 + "输出3个提案，只回复JSON"
         ⚠️ Reproducibility Auditor 额外附加 code-architecture-digest.md（见 5.0）
         
Phase 2: spawn 7个sub-agent（并行）
         指令 = 角色prompt + 所有提案(随机序,匿名) + "对每个非自己的提案评论"
         
Phase 3: GM自己执行（不spawn）
         合并/去重/淘汰/安全审查
         
Phase 4: spawn 7个sub-agent（并行）
         指令 = 角色prompt + 精炼提案列表(随机序) + "投X票"
         GM综合裁决
```

### 5.2 成本估算
- 每阶段7个sub-agent × ~2000 token/agent = ~14K token
- 4阶段 × 14K = ~56K token + GM综合 ~10K = ~66K token
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
