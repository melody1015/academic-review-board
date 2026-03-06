# Phase 2: 交叉讨论 — 评论输出格式

> 本模板定义所有专家在 Phase 2 交叉讨论阶段的输出结构。
> 所有角色使用相同格式，仅"角度"描述由角色 prompt 指定。

## 输入条件

- 收到所有 Phase 1 提案（已随机打乱顺序、隐去来源角色）
- 每位专家必须对**至少 5 个**非自己的提案发表意见

## 输出格式

对每个非自己的提案，提供：

- **Proposal ID**: （原提案 ID）
- **Stance**: `SUPPORT` / `CHALLENGE` / `SUPPLEMENT` / `MERGE(with your proposal X)`
- **Reasoning**: 2-3 句话，从你的专业角度解释立场

## 特殊规则

- 你可以**修改**或**撤回**自己的提案
- **Devil Reviewer 特权**：可在此阶段对任何提案追加 **FATAL** 标记

## 格式规范

- 只输出结构化 JSON，不要输出任何摘要或说明
