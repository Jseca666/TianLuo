# V0.8 Main Export Quality Benchmark Note

## 当前目的

这一版的重点不是继续新增 façade，而是先给 `main export` 与 `quality export` 建立一套更稳定的固定 benchmark 任务集。

这样后续推进时，comparison 不再只依赖单个 demo task，而是可以围绕一组更接近真实通用任务模式的样例持续观察：

- `todo_count`
- `unsupported_count`
- `asset_file_count`
- `validation_ok`

---

## 当前新增内容

本次新增：

- `examples/main_export_quality_benchmark_task_factory.py`
- `examples/main_export_comparison_benchmark_poc.py`

其中 benchmark task factory 当前覆盖四类代表性模式：

1. `exists -> wait -> tap_locator -> text assert -> back`
2. `wait -> swipe cycle -> text equals`
3. `wait -> tap_area -> number bounds -> back`
4. `direct runtime-like actions mix`

---

## 当前价值

这一批 benchmark 的价值是：

1. 让 quality 线后续补动作时，有更固定的回归样本
2. 让 comparison 更容易观察 TODO / unsupported 是否持续下降
3. 为后续把成熟动作逐步并回 main export 主入口提供更稳定依据

---

## 当前边界

这一版 benchmark 仍然是轻量的，重点是：

- 覆盖更常见的通用动作组合
- 保持 task specs 易读
- 便于后续继续追加更真实的任务链路

它还不是最终 benchmark 集合，后续应继续往：

- 页面进入
- 页面检查
- 点击 / 滑动
- OCR 判断
- 返回 / 恢复

这样的完整流程扩展。
