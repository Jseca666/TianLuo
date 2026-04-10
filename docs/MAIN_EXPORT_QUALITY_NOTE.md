# Main Export Quality Line

## 当前定位

`main_export_quality_*` 这一组模块用于提升 main export 主入口背后的产物质量。

它的重点不是新增更多主入口名字，而是：

- 扩动作覆盖率
- 降低 TODO / unsupported
- 让生成 Kotlin 更贴近 Runtime 现有接口
- 导出带 resources 的真实 Android Studio 工程

---

## 当前覆盖动作

当前已经明确覆盖：

- tap / tap_locator / tap_area
- wait_image / exists
- ocr_text / ocr_int
- ocr_text_contains / ocr_text_equals
- ocr_int_min / ocr_int_max
- swipe_up / swipe_down / swipe_left / swipe_right
- sleep / back

---

## 当前价值

这一条线适合用来：

1. 快速验证新增动作是否真正落成 Kotlin
2. 检查质量导出工程的 readiness
3. 为后续把更成熟的动作并回 main export 主入口做准备
