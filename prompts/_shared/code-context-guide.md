# 代码架构上下文使用指南（Code Context Guide）

> 本文件被所有角色共享。当知识包中包含 `code-architecture-digest.md` 时，各角色应从自身视角利用代码信息。

## 什么是 code-architecture-digest.md

由 `build-knowledge.py` 调用 GitNexus 代码知识图谱自动生成的附录，包含：
- **代码结构概览**：模块/类/函数的组织关系
- **关键实现细节**：核心算法和数据处理逻辑
- **依赖图谱**：函数调用链、数据流向、blast radius
- **环境信息**：第三方库版本、运行时要求

## 各角色视角

| 角色 | 利用代码上下文的方式 |
|------|-------------------|
| **Methodology Critic** | 论文描述的方法 vs 代码实际实现的差异（如论文说"novel"但代码用标准库函数） |
| **Experiment Designer** | 代码中的实验设置（数据划分、随机种子、训练/测试分离）是否与论文描述一致 |
| **Statistician** | 统计检验代码实现的正确性（参数设置、单双尾、校正方法） |
| **Devil Reviewer** | 论文 claims 与代码实现的 gap 是最致命的缺陷来源 |
| **Domain Expert** | 领域特定逻辑是否正确实现（如金融：point-in-time 数据构建；生物：normalization 管线） |
| **Literature Scout** | 代码依赖的算法库是否对应论文引用的方法（如引用 paper A 的方法但代码用了 paper B 的实现） |
| **Reproducibility Auditor** | 数据溯源链、环境依赖、随机种子、代码复制风险、blast radius 影响评估 |
| **Ethics Auditor** | 数据处理中的隐私保护实现、去标识化逻辑、访问控制 |

## 使用原则

1. **辅助而非替代**：代码架构是辅助信息，不替代你的核心角色职责。不要让代码细节分散你对方法论层面问题的注意力。
2. **claim-code 比对**：最高价值的使用方式是将**论文中的 claim 与代码中的实现**做交叉验证。
3. **blast radius 评估**：当你建议修改某个方法/流程时，参考依赖图理解影响范围，据此评估建议的可行性。
4. **未收到时正常工作**：如果知识包中没有 `code-architecture-digest.md`（无代码库、GitNexus 未索引、纯理论论文），按原有方式评审，不影响核心职能。
