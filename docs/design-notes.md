# AI Academic Review Board — 设计讨论记录

> 脱敏版本，2026-03-01
> 背景：设计一个用LLM multi-agent模拟学术同行评审的系统，用于在论文写作阶段提前发现方法论问题

---

## 1. 问题背景

我们正在写一篇实证金融方向的SSRN工作论文，提出一个新的概念框架（Information-Price Lag），并设计了跨市场实验来验证。论文处于"有实验设计方案、开始采集数据"的早期阶段。

**需求：** 在论文完成前，搭建一个AI评审委员会，模拟真实同行评审的多角度审查，提前发现方法论缺陷和可能的审稿人攻击点。

---

## 2. 文献调研：已有的LLM学术评审框架

我们调研了三个最相关的学术参考：

### 2.1 AgentReview（Georgia Tech, EMNLP 2024）
- 论文: [arxiv.org/abs/2406.12708](https://arxiv.org/abs/2406.12708)
- **第一个用LLM模拟完整同行评审流程的框架**，53,800+条生成评审
- 5阶段流水线：独立评审 → 作者Rebuttal → 审稿人讨论 → Meta-Review → 最终裁决
- 审稿人3维度建模：Commitment / Intention / Knowledgeability
- Area Chair 3种风格：Authoritarian / Conformist / **Inclusive**（效果最好）
- **关键发现：**
  - 审稿人偏见导致37.1%的决策差异
  - 1个不负责审稿人 → 其他人投入度降18.7%（利他疲劳）
  - Rebuttal对最终决策影响极小（锚定效应）
  - 去掉数值评分后决策剧烈变化（Jaccard降至0.20）

### 2.2 MARG（Northwestern / Allen AI, 2024）
- 论文: [arxiv.org/abs/2401.04259](https://arxiv.org/abs/2401.04259)
- **核心创新：专业化Agent分工 + 内部讨论**
- 不同Agent负责不同评审维度（实验/清晰度/影响力）
- Leader-Worker-Expert三层架构
- 包含Refinement阶段（精炼+去重+淘汰低质量评论）
- 结果：generic评论从60%降至29%，有用评论2.2倍提升

### 2.3 PRE / PeerReview-Weighted（清华, CIKM 2024）
- 用多个LLM互评，消除单一LLM偏见
- Dawid-Skene EM算法：估算每个judge的"混淆矩阵"，自动降低有偏judge的权重
- Flipped-triple trick：候选答案正序/逆序各评一次，消除位序偏差
- 资格考试机制：用gold-standard题筛掉不靠谱的reviewer

---

## 3. 我们的设计决策

### 3.1 角色设计：7位专家 + 1位GM

基于"从草稿到可提交论文阶段最容易犯的10个错误"倒推角色需求：

| # | 常见问题 | 主覆盖专家 | 辅覆盖 |
|---|---------|-----------|--------|
| 1 | 方法论-理论脱节 | Methodology Critic | Domain Expert |
| 2 | Look-ahead偏差 | Experiment Designer | Methodology Critic |
| 3 | 贡献不清晰 | Domain Expert | Devil Reviewer |
| 4 | 过度声称因果 | Devil Reviewer | Methodology Critic |
| 5 | 缺naive benchmark | Experiment Designer | Econometrician |
| 6 | 统计方法不匹配 | Econometrician | Methodology Critic |
| 7 | 文献盲点 | Literature Scout | Domain Expert |
| 8 | 理论模糊 | Domain Expert | Literature Scout |
| 9 | 数据局限未承认 | Reproducibility Auditor | Econometrician |
| 10 | 复现性缺口 | Reproducibility Auditor | — |

**7位专家：**

| 角色 | 核心能力 | 对标现实角色 |
|------|---------|------------|
| Methodology Critic | 研究设计、因果推断、look-ahead检测 | 方法论审稿人 |
| Experiment Designer | 样本构建、point-in-time设计、降级预期 | 量化基金研究员 |
| Econometrician | 时间序列/面板方法、多重检验校正、效应量 | 金融计量教授 |
| Devil Reviewer | 致命缺陷检测、claim-evidence差距分析 | Reviewer 2 |
| Domain Expert (Finance) | 理论根基（Hong-Stein/Merton/Da et al.）| 金融学教授 |
| Literature Scout | 系统性文献搜索、引用链追踪、研究空白 | 研究型图书馆员 |
| Reproducibility Auditor | 数据溯源、代码复现、FAIR原则 | 数据审计师 |

**GM（Inclusive风格，参考AgentReview）：** 综合裁决 + 安全边界守卫

### 3.2 为什么是7个？

- **不多不少：** 10个常见问题全覆盖，每个问题至少1主覆盖+1辅覆盖，无盲区
- **不冗余：** 每个角色有明确的独占关注点，两两之间有区分（如Methodology Critic关注"整体策略是否正确"，Econometrician关注"具体统计工具是否正确"）
- **Literature Scout和Reproducibility Auditor在早期阶段价值较低，但不移除**——前者防止方向性文献遗漏，后者在数据采集阶段就能提醒关键细节

### 3.3 权重设计：双层票数制

**核心决策：采用双层票数制，而非加权Borda百分比权重。**

基于top journal拒稿原因分布：
- 方法论缺陷/替代解释: ~30%
- 结果不稳健/统计问题: ~25%
- 贡献不够/不够新: ~20%
- 其他: ~25%

**方法论三角（核心专家）：每人5票**
- Methodology Critic
- Experiment Designer
- Econometrician

**一般专家：每人3票**
- Devil Reviewer（+FATAL标记自动加3分的特权）
- Domain Expert
- Literature Scout
- Reproducibility Auditor

**投票力分布：** 核心 3×5=15票 (56%) / 一般 4×3=12票 (44%)

**为什么不用加权Borda？**
- 7个专家是小样本场景，百分比权重的精度是伪精度（20% vs 18%在统计上和噪声无法区分）
- 5票 vs 3票的差距是真实差距（67%），抗噪声
- 计票透明——"3个核心票+2个一般票"一目了然
- 真实学术界（NSF/ERC评审面板）用的都是简单投票，不用百分比权重

---

## 4. 评审流程：4阶段

借鉴AgentReview的5阶段 + MARG的专业化分工和Refinement + PRE的偏差消除。

### Phase 1: 独立评审
- 7位专家各自独立生成3个提案
- 专家之间不可见彼此提案（防止锚定效应）
- 产出：21个提案

### Phase 2: 交叉讨论（借鉴MARG内部讨论）
- 所有提案**随机打乱顺序 + 隐去来源角色**（借鉴PRE位序偏差消除 + 匿名评审）
- 每位专家对其他人的提案发表意见：支持/质疑/补充/合并
- 原提案作者可修改或撤回
- Devil Reviewer可在此阶段追加FATAL标记

### Phase 3: 精炼与去重（借鉴MARG Refinement）
- GM执行：合并重复、淘汰空洞提案、拆分混合问题、安全审查
- 通常 21个 → 10-14个

### Phase 4: 加权投票 + GM裁决
- 核心专家投5票，一般专家投3票
- 不能投给自己的提案
- 提案呈现顺序每位专家不同（随机化）
- GM综合票数+讨论记录做最终裁决

---

## 5. 事后评议与专家改进机制

### 事前校准（Calibration Session）
参考Cochrane协作网的校准练习：
- **时机：** 首次正式评审前 + 每加入新专家角色时
- **做法：** 准备一份包含已知优缺点的测试文档，7位专家独立评审，GM比对输出
- **目的：** 把所有专家校准到同一标尺——"什么算P0/P1/P2"需要共识
- Cochrane研究发现：审稿人间一致性（κ）range 0.38-1.0，事前校准可显著缩小分歧

### 三层事后评议

**第一层：Session Debrief（每次评审后自动）**
- 对每个提案记录命运：ADOPTED / MERGED / PRUNED(原因) / IGNORED / VETOED
- PRUNED原因分类：GENERIC(太泛) / DUPLICATE(重复) / IRRELEVANT(跑题) / SECURITY(触碰边界)
- 更新历史追踪JSON + 各专家记忆文件
- 对标：Publons编辑评分制（编辑对每次review质量打分）

**第二层：Pattern Analysis（每3次评审后）**

| 失败模式 | 改进动作 | 现实对标 |
|----------|---------|---------|
| GENERIC率 > 50% | prompt加反面范例（generic→specific示范）| TAVB导师modeling |
| DUPLICATE率 > 40% | prompt加差异化指令（明确角色边界）| 角色职责澄清 |
| IRRELEVANT率 > 30% | prompt强化议题锚定要求 | NSF评审指南 |
| IGNORED率 > 60% | 分析质量vs角度，调整关注重点 | Publons编辑反馈 |
| 采纳率 < 20% | 触发第三层深度修订 | — |

**第三层：Expert Revision（触发式，含Planted Error Test）**
- 诊断根因：知识缺口 / 判断力差 / 角色偏移 → 对应修改知识包/校准范例/角色定义
- **Planted Error Test（借鉴BMJ审稿人培训RCT, Schroter et al. 2004）：**
  - 准备包含3-5个已知缺陷的测试文档（1 FATAL + 2 MAJOR + 2 MINOR）
  - BMJ研究证实：针对性培训确实提升了错误检出率和review质量
  - 修改prompt后用此测试验证改善效果
  - 达标标准：FATAL 100%检出，MAJOR ≥80%，MINOR ≥50%

### 专家记忆文件（对标TAVB导师带教的持续反馈）
每位专家维护一个 `.memory.md` 文件，记录：
- 累积统计（采纳率、失败模式分布）
- 校准范例（好提案示范 + 反面教材）——对标TAVB的modeling
- 知识补充（评审中发现的知识缺口补丁）
- 关注调整（根据历史重叠分析的聚焦方向修正）
- Planted Error Test记录

### 现实学术界参考来源

| 机制 | 来源 | 核心思路 |
|------|------|---------|
| 编辑评分制 | Publons / Web of Science | 编辑对每次review打分，记入审稿人Profile |
| 导师带教制 | TAVB期刊 Reviewer Mentoring Program | 资深编委配对初级审稿人，3-5篇审稿+反馈 |
| 校准练习 | Cochrane AMSTAR-2 | 评审前统一标尺，测inter-rater agreement |
| 植入错误训练 | BMJ RCT (Schroter et al., 2004) | 故意植入缺陷，测审稿人检出率 |
| 面板校准 | NSF Grant Review | 独立打分→聚焦分歧讨论→PO裁决 |

---

## 6. 从三个参考框架借鉴的具体机制

| 机制 | 来源 | 我们的应用 |
|------|------|-----------|
| Inclusive AC风格 | AgentReview | GM综合所有信息裁决，不偏向任一专家 |
| 强制排序（batch decision） | AgentReview | 有限票数迫使专家做取舍，不能"全部重要" |
| 数值评分是关键锚点 | AgentReview | 保留票数计数作为GM裁决的重要参考 |
| 专业化Agent分工 | MARG | 7个角色各有明确独占领域 |
| 内部讨论轮 | MARG | Phase 2交叉讨论 |
| Refinement阶段 | MARG | Phase 3精炼去重 |
| 位序随机化 | PRE | Phase 2/4提案顺序随机打乱 |
| 匿名评审 | PRE | Phase 2隐去提案来源角色 |
| 历史质量追踪 | PRE | JSON记录+Pattern Analysis |

---

## 7. 成本估算

- 每阶段7个sub-agent × ~2000 token/agent = ~14K token
- 4阶段 × 14K + GM综合 ~10K = ~66K token
- 约 $2-3/次评审（Claude Opus定价）
- 月度频率的话，约 $6-9/月

---

## 8. 开放问题（欢迎建议）

1. **交叉讨论的深度：** 目前设计为1轮讨论。是否需要多轮？（AgentReview发现rebuttal效果有限——锚定效应。但我们的场景不同于accept/reject，而是改进建议。）

2. **GM的角色边界：** GM既做Phase 3精炼又做Phase 4裁决，是否权力过大？是否需要"程序公正"约束（如：GM不能VETO得票最高的提案，除非安全原因）？

3. **专家数量：** 7个是否够？是否需要增加"Narrative/Framing Expert"（关注论文叙事弧线和contribution framing）？我们目前认为Domain Expert和Devil Reviewer部分覆盖了这个职能。

4. **跨次评审的连贯性：** 如果Phase 1评审发现问题X，修改后Phase 2评审是否应该验证X已修复？目前没有显式的"问题追踪"机制。

5. **评审频率与论文进度匹配：** 不同阶段（实验设计 vs 写作 vs 投稿前）应该侧重不同专家吗？是否需要"阶段性核心专家轮换"？

---

*欢迎从学术同行评审实践角度提供反馈。*
