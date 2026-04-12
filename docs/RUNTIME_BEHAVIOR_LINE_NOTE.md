# Runtime Behavior Line Note

## 当前目的

这一轮不是继续往高层治理链上加工具，而是把上一轮 decision / release gate 的结论，真正反推到底层实现。

当前新增的是一条新的 `runtime-behavior` 导出线，重点不是再引入更多参数，而是让导出的 Kotlin 任务开始显式暴露：

- `usedSemanticEngine`
- `kernelSizeHintApplied`
- `excludedNumberFiltered`

也就是把 OCR 语义从“有 contract / 有 helper”推进到“有行为可观测性”。

---

## 当前新增内容

本次新增：

- `android_runtime_template/.../ocr/OcrSemanticBehaviorResult.kt`
- `android_runtime_template/.../ocr/OcrSemanticBehaviorSupport.kt`
- `task_exporters/main_export_quality_runtime_behavior_kotlin_step_renderer.py`
- `task_exporters/main_export_quality_runtime_behavior_task_export_session.py`
- `apk_exporter/main_export_quality_runtime_behavior_project_export_workflow.py`
- `apk_exporter/main_export_quality_runtime_behavior_project_export_facade.py`
- `apk_exporter/main_export_quality_runtime_behavior_project_export_report_facade.py`
- `apk_exporter/runtime_behavior_readiness_summary.py`
- `apk_exporter/runtime_behavior_readiness_analyzer.py`
- `apk_exporter/runtime_behavior_comparison_workflow.py`
- `apk_exporter/runtime_behavior_comparison_writer.py`
- `apk_exporter/runtime_behavior_gap_backlog_builder.py`
- `apk_exporter/runtime_behavior_gap_backlog_workflow.py`
- `apk_exporter/runtime_behavior_gap_backlog_writer.py`
- `examples/runtime_behavior_gap_backlog_poc.py`

---

## 当前推进的核心点

### 1. runtime helper 从“返回值”推进到“行为结果”

新增的 behavior helper 不再只返回 OCR 文本或数字，而是会显式返回：

- 是否使用了 `SemanticOcrEngine`
- `kernelSize` 提示是否真正被 runtime 承接
- `excludedNumber` 是否真的发生了过滤

这让当前导出线第一次开始具备“行为可观测性”。

### 2. runtime-behavior renderer 会把这些行为信息带进生成代码

新的 renderer 在导出的 Kotlin 里会显式生成：

- `usedSemanticEngine...`
- `kernelSizeHintApplied...`
- `excludedNumberFiltered...`

这比上一条 runtime-semantic 线更进一步，因为上一条线主要体现的是：

- contract 进入了 runtime helper
- helper 被调用了

而这一条线已经开始体现：

- behavior 是否被真正观测到

### 3. comparison / backlog 也已同步接上

当前新增的 runtime-behavior comparison 与 backlog，会开始比较：

- runtime-semantic 线
- runtime-behavior 线

在行为可观测性层面的差异，例如：

- `kernelSizeHintApplied`
- `excludedNumberFiltered`
- `usedSemanticEngine`

---

## 当前价值

这一轮的价值不是：

- 又多一条平行导出线

而是：

- 把 OCR runtime 语义进一步推进到“行为可观测性”层面
- 为后续真正实现 `kernel_size` 的底层行为逻辑提供更清晰的观察窗口
- 让 release gate / dashboard 未来不只看 contract / backlog，还能逐步看 behavior 真实推进情况

---

## 推荐入口

当前推荐新增入口：

- `python examples/runtime_behavior_gap_backlog_poc.py`

它会串行跑：

1. runtime-behavior comparison
2. runtime-behavior gap backlog
3. 输出 JSON 报告

---

## 当前结论

这一轮的核心意义是：

> 项目开始把 OCR runtime 语义从“有 helper、能调用”推进到“行为是否真正发生、是否能被观察到”。

这会让下一阶段继续推进 `kernel_size` 真实行为实现时，不再只是扩参数或扩 helper，而是在已有行为观测基础上继续做真正落地。
