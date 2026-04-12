# Core Actions Export Line Note

## 当前目的

这一轮的目标，是把项目推进重点重新拉回最终产品目标本身：

> 先把不依赖复杂 OCR 的 PC 端通用动作，明确导出成安卓独立运行任务。

因此本次新增的是一条新的 `core-actions` 导出线，优先覆盖：

- `tap_point`
- `swipe_points`
- `back`
- `sleep`

这条线的价值在于：

- 它更贴近“ADB 通用动作脚本 -> 安卓独立运行脚本”
- 它不需要先解决复杂 OCR 语义一致性
- 它可以作为真正更接近最终验收目标的一条直接导出线

---

## 当前新增内容

本次新增：

- `task_exporters/main_export_core_actions_step_mapper.py`
- `task_exporters/main_export_core_actions_task_builder.py`
- `task_exporters/main_export_core_actions_kotlin_step_renderer.py`
- `task_exporters/main_export_core_actions_task_export_session.py`
- `apk_exporter/main_export_core_actions_project_export_workflow.py`
- `apk_exporter/main_export_core_actions_project_export_facade.py`
- `apk_exporter/main_export_core_actions_project_export_report_facade.py`
- `examples/main_export_core_actions_task_factory.py`
- `examples/main_export_core_actions_project_export_report_poc.py`

---

## 当前覆盖的动作

当前 `core-actions` 线优先覆盖这些动作：

### 1. `tap_point`

支持别名：

- `tap`
- `tap_xy`
- `tap_coordinate`
- `click_point`
- `click_xy`

支持参数归一化：

- `x / y`
- `point_x / point_y`
- `target_x / target_y`

导出后会直接生成：

- `PointAsset(x, y)`
- `context.gestureEngine.tap(...)`

### 2. `swipe_points`

支持别名：

- `swipe`
- `swipe_xy`
- `swipe_points_xy`

支持参数归一化：

- `start_x / start_y / end_x / end_y`
- `x1 / y1 / x2 / y2`
- `duration / duration_ms`

导出后会直接生成：

- 起点 `PointAsset`
- 终点 `PointAsset`
- `context.gestureEngine.swipe(...)`

### 3. `back`

直接导出：

- `context.gestureEngine.back()`

### 4. `sleep`

支持别名：

- `sleep_seconds`
- `wait_seconds`

导出后会生成：

- `kotlinx.coroutines.delay(...)`

---

## 当前意义

这条线和前面大量 semantic / runtime-semantic / runtime-behavior 工作不同。

它不是优先去解决：

- OCR 参数一致性
- 行为可观测性
- helper / contract / backlog 治理

而是优先解决一个更直接的问题：

> 仓库里是否已经存在一条能把“简单通用动作任务”直接导出成安卓工程的明确主线。

当前答案已经变成：

- 是，已经有了 `core-actions` 导出线

---

## 推荐入口

当前推荐直接运行：

- `python examples/main_export_core_actions_project_export_report_poc.py`

它会使用一组只包含通用动作的 task specs，直接导出 Android 工程和报告。

如果你要从项目最终目标的角度理解，这个入口比最近几轮 OCR semantic 治理链更接近：

- PC 通用动作脚本
- 安卓独立运行任务

之间的直接映射。

---

## 当前结论

这一轮的核心意义是：

> 项目里终于补出了一条更贴近最终目标的“通用动作直接导出线”。

它还不是最终 APK 验收闭环，但它已经明显比前面那些偏 OCR 语义治理的工作，更接近你最终想要的产品方向。
