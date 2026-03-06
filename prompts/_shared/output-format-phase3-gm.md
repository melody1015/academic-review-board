# Phase 3 输出格式 — GM 精炼日志 (Refinement Log)

> 本模板供 GM 在 Phase 3 精炼阶段使用。

## 精炼操作

对 Phase 2 修订后的每个提案，执行以下操作之一：

| 操作 | 条件 | 格式 |
|------|------|------|
| **MERGED** | 两个以上提案涉及同一问题 | `MERGED: [{ID-1}, {ID-2}] → R-NNN ({共同关切})` |
| **PRUNED** | 无具体行动步骤 | `PRUNED: {ID} ({原因}: GENERIC / DUPLICATE / IRRELEVANT / SECURITY)` |
| **SPLIT** | 一个提案混合多个独立问题 | `SPLIT: {ID} → R-NNN ({问题A}) + R-NNN ({问题B})` |
| **FLAGGED** | 涉及安全边界或合规风险 | `FLAGGED: {ID} ({风险描述}) → VETO candidate` |
| **KEPT** | 无需修改直接进入 Phase 4 | `KEPT: {ID} → R-NNN` |

## 输出格式

```
## Phase 3 Refinement Log

Paradigm: {范式名}
Input proposals: {Phase 2 修订后总数}
Output proposals: {精炼后总数}

### Operations
MERGED: [MC-001, ED-002] → R-001 (同一关切)
PRUNED: LS-003 (GENERIC — 无具体行动步骤)
SPLIT:  BS-001 → R-005 (问题A) + R-006 (问题B)
FLAGGED: DE-002 (涉及安全边界) → VETO candidate
KEPT:   DR-001 → R-002
KEPT:   RA-001 → R-003
...

### Summary
- MERGED: X pairs → Y proposals
- PRUNED: Z proposals (GENERIC: a, DUPLICATE: b, IRRELEVANT: c, SECURITY: d)
- SPLIT:  W proposals → V proposals
- FLAGGED: F proposals
- KEPT:   K proposals
- Compression rate: {input→output}%
```
