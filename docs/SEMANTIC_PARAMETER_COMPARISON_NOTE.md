# Semantic Parameter Comparison Note

## 当前目的

这一轮在 semantic parameter propagation 线之上，继续补了一条更有针对性的 comparison 能力。

目标不再只是看：

- `TODO`
- `unsupported`

而是开始直接比较：

- `threshold` 是否被真正透传进生成代码
- `mask_name` 是否被真正透传进生成代码
- `use_color` 是否被真正透传进生成代码
- 尚未实现的 `kernel_size / excluded_number` 是否至少被保留为 semantic notes

---

## 当前新增内容

本次新增：

- `apk_exporter/semantic_parameter_readiness_summary.py`
- `apk_exporter/semantic_parameter_readiness_analyzer.py`
- `apk_exporter/semantic_parameter_comparison_workflow.py`
- `apk_exporter/semantic_parameter_comparison_writer.py`
- `examples/semantic_parameter_comparison_poc.py`

---

## semantic readiness 的观察维度

当前 semantic parameter readiness analyzer 会统计：

### 预期侧

- `expected_threshold_steps`
- `expected_mask_steps`
- `expected_use_color_steps`
- `expected_kernel_size_steps`
- `expected_excluded_number_steps`

这些值来自 task specs 本身。

### 生成代码侧

- `propagated_threshold_count`
- `propagated_mask_name_count`
- `propagated_use_color_count`
- `semantic_kernel_note_count`
- `semantic_excluded_number_note_count`

这些值来自生成后的 Kotlin 任务文件内容。

---

## 当前 comparison 的意义

`semantic_parameter_comparison_workflow.py` 会直接对比：

- baseline `main export`
- `semantic quality export`

在参数语义透传层面的差异。

这一步的意义是：

1. 不再只说 semantic 线“更高级”
2. 而是能更具体地证明 semantic 线是否真的把参数语义推进到了生成代码里
3. 为后续把这部分能力择机并回主线提供依据

---

## 推荐入口

当前可以直接运行：

- `python examples/semantic_parameter_comparison_poc.py`

它会输出：

- baseline export 结果
- semantic quality export 结果
- 两侧 semantic readiness 摘要
- comparison report path

---

## 当前结论

从项目目标来看，这条 comparison 线的价值在于：

> 它开始把“动作名映射是否存在”推进到“动作参数语义是否真的落地”。

这比只统计 `TODO / unsupported` 更接近“PC 端同逻辑导出”的核心要求。
