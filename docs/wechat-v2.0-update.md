# Academic Review Board v2.0：从「只管实证」到「质性和政策也管」

上个月开源了 Academic Review Board——一个用多个 AI 专家模拟同行评审的系统，帮你在投稿前抓出致命缺陷。当时支持 6 个学科范式，清一色的实证研究方向。

有朋友问了一句：做质性研究的呢？写政策建议的呢？

问得好。这两类论文的评审逻辑和实证研究完全不同，硬套实证范式的专家去审，等于让计量经济学家点评你的扎根理论编码，或者让统计学家审你的罗尔斯式论证——不是他们不行，是审错了东西。

v2.0 补上了这个缺口。

---

## 新增两个范式

### 1. 质性研究（qualitative-research）

适用于社会学、人类学、教育学、护理学、管理学等使用质性方法的论文。

实证范式的核心三角是「方法论 + 实验设计 + 统计分析」，质性范式的核心三角换成了：

- **Methodology Critic** → 审的不是因果推断，而是方法论选择的合理性：你选扎根理论还是现象学？跟你的研究问题匹配吗？你的认识论立场跟分析方法一致吗？
- **Research Designer** → 不审回测设计，审的是案例选取策略、田野设计、数据收集方法和三角验证。便利抽样装成目的性抽样？一眼就看出来。
- **Qualitative Analyst** → 替代统计学家。审编码过程的透明度、主题是描述还是解释、负面案例有没有处理、reflexivity 是真做了还是写了一段套话。

其他角色也跟着变：

- Reproducibility Auditor → **Trustworthiness Auditor**。不审代码复现，审的是 Lincoln & Guba 的可信性四标准（credibility / transferability / dependability / confirmability）。
- Ethics Auditor → **必选**。质性研究必然涉及人，知情同意、匿名化与厚描述的张力、研究者权力位置，这些不是可选项。
- Literature Scout → 增加了方法论传统谱系检查。做建构主义扎根理论引的是 Charmaz 还是 Glaser？这不是细节，是认识论立场。

### 2. 规范性与政策论证（normative-policy）

适用于社会福利、公共政策、政治哲学、教育政策、卫生政策等以「应该怎么做」为核心贡献的论文。

这类论文的审稿逻辑跟实证完全不同。不是「你的数据支不支持结论」，而是「你的价值判断和政策推导链条站不站得住」。

核心三角：

- **Methodology Critic** → 审论证结构。从事实到价值有没有桥梁（休谟铡刀）？价值前提是明示的还是藏着的？论证链有没有逻辑跳跃？
- **Policy Analyst** → 审政策推导链。有没有实施路径？反事实只比了「有政策 vs 没政策」还是也比了替代方案？非预期后果考虑了吗？有没有犯涅槃谬误（把真实政策跟理想方案比）？
- **Normative Theorist** → 审规范框架。你用的是功利主义还是罗尔斯？框架内部一致吗？遇到效率和公平冲突时怎么处理的？

同样有对应替换：

- Reproducibility Auditor → **Evidence Auditor**。不审代码，审的是你引用的实证证据质量——那个支撑你政策建议的 RCT，真的是因果推断还是描述性统计？证据链完整吗？
- Ethics Auditor → **Rights & Equity Auditor（必选）**。审分配正义：谁受益谁受损？交叉性考虑了吗？代际影响呢？

---

## 8 个范式，覆盖三大方法论类型

| 类型 | 范式 | 核心审查逻辑 |
|------|------|-------------|
| **实证** | economics-finance | 因果推断、计量方法 |
| | experimental-behavioral | 实验设计、效应量 |
| | clinical-epidemiology | RCT、ITT |
| | biology-omics | FDR、正交验证 |
| | cs-ai | 消融实验、基线公平 |
| | natural-science-engineering | 测量不确定度 |
| **质性** | qualitative-research | 编码/饱和/可信性 |
| **规范** | normative-policy | 论证链/价值前提/政策可行性 |

不知道该选哪个？orchestration.md 里有详细的边界案例判定表。比如一篇教育政策论文——如果核心是 RCT 效果估计，走 experimental-behavioral；如果核心是政策建议，走 normative-policy。看方法论核心，不看学科归属。

---

## 为什么不是换个 prompt 就行

你可能会想：我自己写个提示词让 GPT 审质性论文不就行了？

可以试试。但几个问题你得自己解决：

1. **多视角覆盖**。一个 prompt 很难同时从方法论选择、编码严谨性、可信性框架、伦理合规、文献谱系五个角度审。我们用 8 个专家各管各的。

2. **偏见控制**。单一审稿人容易被第一印象锚定。我们的 Phase 2 是匿名交叉讨论，提案随机排序、隐去来源角色，专门对抗锚定效应和权威偏差。

3. **权重分化**。方法论三角（核心专家）每人 5 票，一般专家 3 票，致命缺陷自动 +3。不是所有意见同等重要。

4. **专家学习**。每个专家有独立记忆文件，跟踪采纳率，累积低于 20% 会触发 prompt 修订和植入错误测试。一个 prompt 做不到这些。

---

## 怎么用

```bash
git clone https://github.com/melody1015/academic-review-board.git
cd academic-review-board

python3 scripts/run_review.py \
  --session QR-001 \
  --paradigm qualitative-research \
  --files your-paper.docx \
  --topic "扎根理论研究的方法论严谨性评审"
```

把 `qualitative-research` 换成 `normative-policy` 就审政策论文。其他 6 个实证范式照旧。

---

## 下一步

P1 优先级还有两个范式在设计中：

- **系统综述 / Meta 分析** — PRISMA 流程、异质性检验、发表偏倚
- **混合方法** — 质性 + 量化的整合逻辑审查

GitHub: github.com/melody1015/academic-review-board

有问题欢迎提 issue 或评论区交流。
