# Android 导出项目交接文档

## 1. 交接目的

本文档用于把当前仓库中“从 PC 端通用自动化能力导出 Android Studio 工程，并最终形成可独立运行 APK”的工作进度、当前主线、未完成事项与下一步规划，完整交接给下一位同事。

本文档重点不是解释旧游戏脚本细节，而是说明当前已经形成的：

- 导出主入口
- 任务代码生成链
- automation 资源打包链
- 质量提升链
- 对比与验收链

---

## 2. 终极目标

目标不是把 Python 直接打包成 APK。

目标是：

1. PC 端保留开发、调试、资源管理与导出能力
2. 复用现有任务逻辑、模板图、locator/坐标/OCR 资产
3. 从 PC 端导出 Android Studio 工程
4. 工程编译后生成可独立运行的 APK
5. APK 在 Android 端不依赖 PC 常驻，可自行执行自动化任务

---

## 3. 当前总体判断

### 3.1 当前最推荐主入口

当前仓库里，**更接近长期主入口** 的是：

- `apk_exporter/main_android_project_export_facade.py`
- `apk_exporter/main_android_project_export_completion_facade.py`

当前仓库里的说明文档也已经明确把 `main_android_project_export_facade.py` 定位为更接近长期主入口的导出通道，并说明它统一了默认导出 summary、deep 资源完整性校验、readiness 视角、package/default/main 报告。`main_android_project_export_completion_facade.py` 则被定位为 main export 的完成态入口。  
参见：
- `docs/MAIN_EXPORT_CHANNEL_NOTE.md`
- `docs/MAIN_EXPORT_COMPLETION_NOTE.md`

### 3.2 当前完成度估算

按“离终极目标还有多远”而不是按代码量估算：

**当前整体进度建议估算为 70% 左右。**

更细一点拆分：

- 导出通道、工程骨架、资源打包、报告/校验体系：**80%~85%**
- 通用动作覆盖率与可编译 Kotlin 生成质量：**55%~65%**
- 真正可长期使用的独立 APK 运行能力：**40%~50%**

这是一个务实估算，不建议往高报。

### 3.3 当前阶段结论

当前项目已经**越过“方案验证期”**，进入：

> **主入口定型 + 提升导出产物质量 + 逐步并回主入口**

的阶段。

---

## 4. 当前已经形成的主线

### 4.1 Default Export 线

作用：把任务规格导出为 Android Studio 工程，并打入 automation 资源，形成默认导出通道。

核心说明见：
- `docs/DEFAULT_EXPORT_CHANNEL_NOTE.md`

当前能力边界文档已经明确说明：默认导出通道已经能做到：

1. 导出 Android Studio 工程骨架
2. 生成任务 Kotlin 文件与注册表
3. 打入 automation 资源
4. 校验 `export_manifest.json`、`locators`、`templates`、`masks.json`
5. 输出默认导出报告

但当前仍存在：
- 不是所有动作都已落到 Runtime 接口
- 仍存在 TODO / unsupported fallback
- 仍需向真实通用任务组合扩展

### 4.2 Main Export 线

作用：在 Default Export 基础上继续收口，作为更接近长期主入口的导出通道。

核心说明见：
- `docs/MAIN_EXPORT_CHANNEL_NOTE.md`
- `docs/MAIN_EXPORT_COMPLETION_NOTE.md`

当前 main export 已形成：

- `MainAndroidProjectExportFacade`
- `MainAndroidProjectExportCompletionFacade`

它统一了：

- 任务规格输入
- Android Studio 工程导出
- automation 资源打包
- deep 资源完整性校验
- readiness 视角
- package/default/main 报告

### 4.3 Main Export Quality 线

作用：**不是新增主入口，而是提升主入口产物质量。**

核心说明见：
- `docs/MAIN_EXPORT_QUALITY_NOTE.md`

当前 quality 线已明确覆盖动作：

- tap / tap_locator / tap_area
- wait_image / exists
- ocr_text / ocr_int
- ocr_text_contains / ocr_text_equals
- ocr_int_min / ocr_int_max
- swipe_up / swipe_down / swipe_left / swipe_right
- sleep / back

quality 线的价值是：

1. 快速验证新增动作是否真正落成 Kotlin
2. 检查质量导出工程的 readiness
3. 为后续把更成熟动作并回 main export 主入口做准备

### 4.4 Main Export Comparison 线

作用：把 baseline `main export` 和 `quality export` 放在一起做结构化比较。

当前对比线核心文件：

- `apk_exporter/main_export_comparison_summary.py`
- `apk_exporter/main_export_comparison_workflow.py`
- `apk_exporter/main_export_comparison_serializer.py`
- `apk_exporter/main_export_comparison_writer.py`
- `examples/main_export_comparison_poc.py`

它已经会对比：

- baseline / quality 的 `todo_count`
- baseline / quality 的 `unsupported_count`
- baseline / quality 的 `asset_file_count`
- baseline / quality 的 `validation_ok`

并自动生成第一版 notes，例如：

- `Quality export reduces TODO count`
- `Quality export reduces unsupported count`
- `Quality export keeps asset file count aligned with baseline`

---

## 5. 当前关键目录与职责

### 5.1 `android_runtime_template/`

职责：Android Runtime 模板工程。

当前导出链会复制这个模板工程，再向其中写入：

- 生成的 Kotlin 任务类
- 任务注册表
- automation 资源到 `app/src/main/assets`

### 5.2 `task_exporters/`

职责：任务规格 -> `ExportedTaskModel` -> Kotlin 任务代码。

当前已经形成多层 builder / mapper / renderer / session。

建议当前关注：

- `delivery_ready_*`
- `main_export_quality_*`

其中 `main_export_quality_*` 是接下来继续提高动作覆盖率的重点位置。

### 5.3 `apk_exporter/`

职责：

- 复制 Android Runtime 模板工程
- 写入生成任务 Kotlin 文件与注册表
- 打入 automation 资源
- 做 readiness / validation / deep validation
- 输出 package/default/main/quality/comparison 各类报告

### 5.4 `examples/`

职责：所有 POC 示例入口。

后续交接时，下一位同事最适合从 `examples/` 先理解当前链路。

### 5.5 `docs/`

职责：沉淀当前导出通道定位与边界。

当前已经有：

- `DEFAULT_EXPORT_CHANNEL_NOTE.md`
- `MAIN_EXPORT_CHANNEL_NOTE.md`
- `MAIN_EXPORT_COMPLETION_NOTE.md`
- `MAIN_EXPORT_QUALITY_NOTE.md`
- 本交接文档

---

## 6. 当前已经打通的关键能力

### 6.1 工程导出

当前已经能：

- 复制 `android_runtime_template/`
- 写入生成的 Kotlin 任务类
- 写入任务注册表

### 6.2 资源打包

当前已经能把 automation 资源打入导出工程：

- `app/src/main/assets/automation/export_manifest.json`
- `app/src/main/assets/automation/locators`
- `app/src/main/assets/automation/templates`
- `app/src/main/assets/automation/masks.json`

### 6.3 校验与报告

当前已经形成多层校验：

- validation
- readiness
- deep validation

并可输出：

- package 报告
- default 报告
- main 报告
- quality 报告
- comparison 报告

### 6.4 更真实的动作覆盖

当前比最初的 wait/tap/back 已经更实：

- OCR 文本 contains / equals
- OCR 数值 min / max
- 区域内 swipe up/down/left/right

---

## 7. 当前还没有完成的部分

这是交接中最重要的一节。

### 7.1 主入口产物仍然存在 TODO / unsupported

虽然 readiness 已经能统计 `todo_count` / `unsupported_count`，但当前主入口并没有做到“绝大部分通用任务都无占位”。

这是接下来最重要的质量目标。

### 7.2 quality 线还没有完全并回主入口

当前 quality 线已经能：

- 生成更强动作覆盖率的 Kotlin
- 导出真实工程
- 打入 resources
- 输出 quality 报告

但它还没有被系统性并回 `main export` 主入口。

当前仍是：

- 主入口线负责长期主入口形状
- quality 线负责验证更强动作支持

### 7.3 还没有证明“导出的工程大面积真实可编译可跑”

当前链路已经非常接近目标，但仍然要诚实说明：

- 当前仓库里的重点是导出体系、报告体系、动作覆盖率提升
- 还没有形成“可以放心对大量通用脚本直接导出并稳定独立运行”的状态

### 7.4 还缺少更接近真实通用任务的批量验收

当前已有很多 POC，但仍偏向：

- 小规模任务组合
- 单任务或少量任务验证

后续需要往更真实的“页面进入 -> 检查 -> 点击/滑动 -> OCR 判断 -> 返回/恢复”组合上推。

---

## 8. 当前推荐的接手顺序

下一位同事建议不要一上来就改太多底层结构。

推荐顺序如下：

### 第一步：先理解主入口

先看：

- `docs/MAIN_EXPORT_CHANNEL_NOTE.md`
- `docs/MAIN_EXPORT_COMPLETION_NOTE.md`
- `apk_exporter/main_android_project_export_facade.py`
- `apk_exporter/main_android_project_export_completion_facade.py`

### 第二步：理解 quality 线

再看：

- `docs/MAIN_EXPORT_QUALITY_NOTE.md`
- `task_exporters/main_export_quality_*`
- `apk_exporter/main_export_quality_project_export_*`

### 第三步：理解 comparison 线

再看：

- `apk_exporter/main_export_comparison_*`
- `examples/main_export_comparison_poc.py`

### 第四步：再决定哪些能力并回主入口

不要直接把 quality 线全部粗暴并回。

应先通过 comparison 看：

- 是否显著降低 TODO / unsupported
- 是否保持 resources 打包与 deep validation 稳定

---

## 9. 当前最推荐跑的 POC

### 9.1 默认主入口

- `examples/main_android_project_export_poc.py`
- `examples/main_android_project_export_completion_poc.py`

### 9.2 质量线

- `examples/main_export_quality_task_generation_poc.py`
- `examples/main_export_quality_project_export_poc.py`
- `examples/main_export_quality_project_export_report_poc.py`

### 9.3 对比线

- `examples/main_export_comparison_poc.py`

对下一位同事来说，最推荐优先跑的是：

1. `main_android_project_export_completion_poc.py`
2. `main_export_quality_project_export_report_poc.py`
3. `main_export_comparison_poc.py`

原因：这三者刚好对应：

- 当前主入口
- 当前质量候选线
- 当前主入口与质量线对比

---

## 10. 后续建议路线图

### Phase A：继续提高 quality 线动作覆盖率

目标：继续减少 `unsupported_count`。

建议新增/补强：

- 更丰富的 swipe / drag 类动作
- 更清晰的 OCR 判断类动作
- 更贴近真实页面操作的组合动作

### Phase B：对 quality 线做更系统的 comparison

目标：让“是否应该并回主入口”有结构化依据。

建议做法：

- 固定一批通用任务规格
- baseline / quality 同时导出
- 对比 TODO / unsupported / asset_count / validation
- 记录长期趋势

### Phase C：逐步并回 main export 主入口

目标：把成熟动作真正带回长期主入口。

建议方式：

- 每次只并回一小批已经稳定的动作
- 并回后立即通过 comparison 重新验证
- 避免一次性大改主入口稳定性

### Phase D：逼近真实可独立运行 APK

目标：不只是导出工程，而是让导出的工程越来越接近真正可独立运行。

这一步的重点已经不是 façade 层，而是：

- Runtime 模板实际能力完整度
- Kotlin 生成代码与 Runtime 接口一致性
- 真实任务组合的端到端可用性

---

## 11. 当前不建议做的事

### 11.1 不建议再优先增加新的 façade 名字

原因：入口层已经足够多，也已经基本定型。

继续加 façade 的收益已经远低于继续提高动作覆盖率和减少 TODO。

### 11.2 不建议回头做大规模“理想化重构”

原因：当前项目已经形成了较清晰的导出主线。

现在最值的是把已有主线做实，而不是为了理想结构推翻当前成果。

### 11.3 不建议让主入口和 quality 线同时大改

原因：这样会让 comparison 失去意义。

应该保持：

- 主入口线：更稳定
- quality 线：更激进验证

---

## 12. 对下一位同事的最简接手建议

如果只有半天时间熟悉项目，建议这样做：

1. 先看 `docs/MAIN_EXPORT_CHANNEL_NOTE.md`
2. 再看 `docs/MAIN_EXPORT_QUALITY_NOTE.md`
3. 跑 `examples/main_android_project_export_completion_poc.py`
4. 跑 `examples/main_export_quality_project_export_report_poc.py`
5. 跑 `examples/main_export_comparison_poc.py`
6. 对比三个结果里的：
   - task_count
   - asset_file_count
   - todo_count
   - unsupported_count
   - validation_ok

如果只有一天时间继续推进，建议从：

- `task_exporters/main_export_quality_kotlin_step_renderer.py`

开始，新增一小批真实动作支持，然后走 comparison 验证是否值得并回主入口。

---

## 13. 最终一句话总结

当前仓库已经不是“只有想法”的阶段，而是已经形成：

> **主入口线 + 质量提升线 + 结构化对比线**

下一位同事最值得做的事情，不是重新设计导出架构，而是：

> **持续提升 quality 线动作覆盖率，并在 comparison 结果稳定后，把成熟能力逐步并回 main export 主入口。**
