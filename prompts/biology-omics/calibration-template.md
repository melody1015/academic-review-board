# Calibration Template — 生物与组学科学

> 校准会议用：包含已知缺陷的测试文档模板。

## 植入缺陷清单

### FATAL（必须 100% 发现）
1. **批次效应混淆**: Condition A 的样本全在 batch 1 处理，Condition B 全在 batch 2，差异表达结果可能完全是技术伪影

### MAJOR（应 ≥80% 发现）
2. **FDR 未校正**: 对 20,000 个基因做差异表达检验，仅用 raw p < 0.05 筛选，实际期望假阳性 ~1000 个
3. **无正交验证**: RNA-seq 发现的 top hits 未用 qPCR 或 Western blot 验证任何一个

### MINOR（应 ≥50% 发现）
4. **生物重复 vs 技术重复混淆**: 报告 N=6 但实际是 2 个生物样本 × 3 个技术重复
5. **原始数据未存储**: 未提供 GEO/SRA accession number，无法获取原始 FASTQ 文件
