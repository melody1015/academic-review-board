# Calibration Template — 临床与流行病学

> 校准会议用：包含已知缺陷的测试文档模板。

## 植入缺陷清单

### FATAL（必须 100% 发现）
1. **Immortal time bias**: 观察性研究中组别分配依赖于未来事件，导致治疗组人为获得"不死时间"

### MAJOR（应 ≥80% 发现）
2. **ITT 替代为 per-protocol**: 未申明 ITT 分析，仅报告了完成全部治疗的患者（per-protocol），未分析脱落者
3. **PH 假设违反**: Cox 回归的比例风险假设未检验（Schoenfeld 残差或 log-log plot）

### MINOR（应 ≥50% 发现）
4. **CONSORT 流程图不完整**: 缺少每个阶段的排除人数和原因
5. **亚组分析未预先指定**: 事后亚组发现了"显著效果"但未做交互检验
