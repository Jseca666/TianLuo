# V0.8 Main Export Quality Alias And Comparison Note

## 当前目的

这一轮补的不是新的 façade，而是两块更贴近 v0.8 阶段目标的增量能力：

1. 让 quality 线先吃下更多 PC 端常见动作叫法
2. 让 benchmark comparison 不只看总数，还能看任务覆盖是否对齐

---

## 当前新增内容

本次新增：

- `task_exporters/main_export_quality_v08_step_mapper.py`
- `task_exporters/main_export_quality_v08_task_builder.py`
- `task_exporters/main_export_quality_v08_task_export_session.py`
- `examples/main_export_quality_v08_alias_task_factory.py`
- `examples/main_export_quality_v08_task_generation_poc.py`
- `apk_exporter/main_export_comparison_benchmark_enricher.py`
- `apk_exporter/main_export_comparison_benchmark_writer.py`
- `examples/main_export_comparison_benchmark_enriched_poc.py`

---

## quality alias 线的价值

`main_export_quality_v08_step_mapper.py` 当前额外兼容了一批更常见的别名，例如：

- `click / click_area / click_template / click_image / click_locator`
- `wait_for_locator / wait_for_template / wait_for_image`
- `assert_exists / exists_locator`
- `read_text / read_number`
- `assert_number_min / assert_number_max`
- `scroll_up / scroll_down / scroll_left / scroll_right`

这样可以先在不改旧入口的前提下，验证更多 PC 端常见叫法是否能平滑落到现有 quality renderer 已支持的动作集合。

---

## enriched comparison 的价值

`main_export_comparison_benchmark_enriched_poc.py` 在原始 comparison 基础上，额外给出：

- expected task count
- baseline / quality task count
- baseline / quality task ids
- shared task ids
- missing tasks in baseline / quality
- 更明确的 benchmark notes

这样后续推进时，不只知道：

- TODO 有没有下降
- unsupported 有没有下降

还会知道：

- baseline / quality 是否把预期任务完整导出来了
- 两边任务覆盖是否对齐

---

## 当前边界

这一轮还是增量验证线，不是最终主入口收敛。

当前做法是：

- 先把增强兼容能力做成可独立跑的新入口
- 先把 richer comparison 做成可独立跑的新 POC
- 等这些增量能力稳定后，再择机并回现有主线
