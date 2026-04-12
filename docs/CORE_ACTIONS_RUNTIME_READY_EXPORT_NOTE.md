# Core Actions Runtime Ready Export Note

## 当前目的

这一轮在上一版 `core-actions` 直接导出线的基础上，继续往更贴最终目标的方向推进了一步：

> 不只是把通用动作导出来，还要让导出的安卓任务对手势执行结果有明确的运行时检查。

因此本次新增的是一条 `core-actions runtime-ready` 导出线，重点覆盖：

- `tap_point`
- `swipe_points`
- `back`
- `sleep`

并且进一步兼容了更常见的 PC 侧写法：

- `press_back / go_back / back_key`
- `sleep_ms / wait_ms / delay_ms`

---

## 当前新增内容

本次新增：

- `task_exporters/main_export_core_actions_runtime_ready_step_mapper.py`
- `task_exporters/main_export_core_actions_runtime_ready_task_builder.py`
- `task_exporters/main_export_core_actions_runtime_ready_kotlin_step_renderer.py`
- `task_exporters/main_export_core_actions_runtime_ready_task_export_session.py`
- `apk_exporter/main_export_core_actions_runtime_ready_project_export_workflow.py`
- `apk_exporter/main_export_core_actions_runtime_ready_project_export_facade.py`
- `apk_exporter/main_export_core_actions_runtime_ready_project_export_report_facade.py`
- `examples/main_export_core_actions_runtime_ready_task_factory.py`
- `examples/main_export_core_actions_runtime_ready_project_export_report_poc.py`
- `apk_exporter/core_actions_runtime_ready_readiness_summary.py`
- `apk_exporter/core_actions_runtime_ready_readiness_analyzer.py`
- `apk_exporter/core_actions_runtime_ready_validation_workflow.py`
- `apk_exporter/core_actions_runtime_ready_validation_writer.py`
- `examples/core_actions_runtime_ready_validation_poc.py`

---

## 当前 runtime-ready 线相比上一版多了什么

### 1. 更贴近 PC 侧动作别名

当前额外兼容：

- `press_back`
- `go_back`
- `back_key`
- `sleep_ms`
- `wait_ms`
- `delay_ms`

### 2. 更贴近运行时结果

当前 renderer 不再只是调用：

- `gestureEngine.tap(...)`
- `gestureEngine.swipe(...)`
- `gestureEngine.back()`

而是会显式检查返回值，并在失败时生成：

- `TaskResult.fail(...)`

这意味着当前导出的安卓任务，已经开始更明确地表达：

- 动作是否真的执行成功

### 3. 新增导出后自检入口

当前新增的 validation workflow 会在导出后检查：

- 预期的 `tap / swipe / back / sleep` 步数
- 生成代码里的实际 `gestureEngine.tap / swipe / back / delay`
- 生成代码里的 `TaskResult.fail(...)`

这让这条更贴目标的通用动作线，不只是“能导出”，而且开始具备“导出后自检”能力。

---

## 推荐入口

当前推荐直接运行：

- `python examples/main_export_core_actions_runtime_ready_project_export_report_poc.py`
- `python examples/core_actions_runtime_ready_validation_poc.py`

其中：

- 第一个更适合直接看工程导出结果
- 第二个更适合看导出后的动作覆盖与失败处理检查

---

## 当前结论

这一轮的核心意义是：

> 项目里已经不只是有一条“通用动作直接导出线”，而是开始有一条更贴近最终验收目标的“通用动作 runtime-ready 导出线”。

它仍然不是最终 APK 验收闭环，但已经比前面那些偏 OCR 语义治理的工作，更接近：

- PC adb 通用动作脚本
- 安卓独立运行任务

之间的直接映射。
