# Semantic Parameter Propagation Note

## 当前目的

这一轮的目标不是继续扩 façade，而是把前面审计里确认存在缺口的参数语义，真正推进到 renderer 生成出的 Kotlin 调用里。

重点覆盖：

- `threshold`
- `mask_name / mask`
- `use_color / useColor`

并且把这条能力做成一条可以直接导出 Android 工程的质量线。

---

## 当前新增内容

本次新增：

- `task_exporters/main_export_quality_semantic_step_mapper.py`
- `task_exporters/main_export_quality_semantic_task_builder.py`
- `task_exporters/main_export_quality_semantic_kotlin_step_renderer.py`
- `task_exporters/main_export_quality_semantic_task_export_session.py`
- `apk_exporter/main_export_quality_semantic_project_export_workflow.py`
- `apk_exporter/main_export_quality_semantic_project_export_facade.py`
- `apk_exporter/main_export_quality_semantic_project_export_report_facade.py`
- `examples/main_export_quality_semantic_task_factory.py`
- `examples/main_export_quality_semantic_project_export_report_poc.py`

---

## 当前推进的核心点

### 1. 参数归一化

新增 semantic step mapper 后，当前会优先统一：

- `locator_name / template_name / image_name / locator / template / image / target`
- `timeout / timeout_seconds / wait_seconds / wait_timeout`
- `threshold / similarity_threshold / match_threshold`
- `mask_name / maskName / mask`
- `use_color / useColor`
- `min / min_value`
- `max / max_value`
- `duration / duration_ms`

这样可以更自然地兼容 PC 端或历史 task specs 的常见写法。

### 2. renderer 参数透传

新增 semantic renderer 后，以下参数会真正往 runtime 调用里透传：

- `context.templateMatcher.waitFor(... threshold, timeoutMs, maskName, useColor ...)`
- `context.ocrEngine.readText(... maskName = ...)`
- `context.ocrEngine.readNumber(... maskName = ...)`

这比之前只较稳定透传 `timeoutMs` 的状态更接近“同逻辑导出”。

### 3. 仍未完全落下去的语义

本轮也明确保留了现实边界：

- `kernel_size`
- `excluded_number`

这两个参数目前仍未在 Android runtime 里真正实现，只在生成代码里留下 semantic notes，提醒当前 runtime 还未完整接住这部分语义。

---

## 当前价值

这一轮更新的价值不是：

- 多一个 façade 名字
- 多一个旁路线目录

而是：

- 真正补了一层“参数语义完整度”
- 让 benchmark task specs 可以开始验证 threshold / mask / useColor 的导出落地
- 为后续把这部分能力逐步并回主线提供更扎实依据

---

## 推荐入口

当前可以直接运行：

- `python examples/main_export_quality_semantic_project_export_report_poc.py`

它会使用一组带参数语义的 task specs，直接导出 Android 工程和质量报告。
