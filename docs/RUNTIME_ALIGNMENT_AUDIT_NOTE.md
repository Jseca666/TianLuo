# Runtime Alignment Audit Note

## 当前目的

这一轮不是继续增加 façade，而是核对当前 `task_exporters` 生成出的 Kotlin runtime 调用，是否和 `android_runtime_template` 里的真实接口一致。

目标是回答两个问题：

1. 当前 renderer 生成的调用是否已经对上 runtime template
2. 距离“PC 端同逻辑导出”为何还差一段

---

## 已核对的 runtime 接口

本次已核对：

- `runtime/task/RuntimeTask.kt`
- `runtime/task/TaskContext.kt`
- `runtime/task/TaskResult.kt`
- `runtime/gesture/GestureEngine.kt`
- `runtime/vision/TemplateMatcher.kt`
- `runtime/ocr/OcrEngine.kt`
- `runtime/assets/AssetLocatorRepository.kt`
- `runtime/vision/ImageComparator.kt`

---

## 当前确认已经基本对齐的部分

### 1. 任务类骨架对齐

当前 `DeliveryReadyCompilableRuntimeTaskExportSession` 生成的 Kotlin 任务类使用：

- `RuntimeTask`
- `TaskContext`
- `TaskResult`

这与 runtime template 的接口定义是一致的。

### 2. 基础动作调用对齐

当前 renderer 生成的这些调用，和 runtime template 接口名是对齐的：

- `context.gestureEngine.tap(...)`
- `context.gestureEngine.swipe(...)`
- `context.gestureEngine.back()`
- `context.templateMatcher.waitFor(...)`
- `context.ocrEngine.readText(...)`
- `context.ocrEngine.readNumber(...)`
- `context.locatorRepository.get(...)`
- `TaskResult.ok(...) / TaskResult.fail(...)`

### 3. quality 线相对 delivery-ready 线的真实增量

当前 `MainExportQualityKotlinStepRenderer` 相比 delivery-ready renderer，已经额外覆盖：

- `ocr_text_equals`
- `ocr_int_max`
- `swipe_up_area / swipe_down_area / swipe_left_area / swipe_right_area`

这说明 quality 线当前的价值，确实主要体现在 renderer 语义覆盖率更高，而不是 façade 名字更多。

---

## 当前确认仍然存在的关键缺口

### 1. 参数透传还不完整

虽然 runtime template 的 `TemplateMatcher.waitFor(...)` 支持：

- `threshold`
- `timeoutMs`
- `maskName`
- `useColor`

但当前 renderer 主要只稳定透传了 `timeoutMs`。

这意味着：

- `threshold` 语义没有真正落下去
- `mask` / `maskName` 语义没有真正落下去
- `use_color` / `useColor` 语义没有真正落下去

### 2. OCR 参数语义还没有完整落下去

runtime template 的 `OcrEngine` 目前支持 `maskName`，但当前 renderer 基本还没有把这部分参数透传进去。

同时，PC 端旧能力里还存在：

- `kernel_size`
- `excluded_number`

这些语义在当前 Android 导出链里还没有完整落地。

### 3. 可导出 API 仍未全覆盖到 renderer

V1 冻结的可导出 API 中还包括：

- `launch_app`
- `stop_app`
- `capture`
- `compare`
- `swipe(start, end, duration_ms)` 这类更通用的 gesture 语义

当前主线 renderer 还没有把这批能力系统性吃下来。

### 4. readiness 仍然是“静态代码 readiness”

当前 readiness analyzer 主要还是统计：

- `TODO`
- `unsupported`

它衡量的是生成代码里还有多少占位，而不是：

- 是否编译通过
- 是否运行通过
- 是否任务逻辑成立

---

## 当前最值得改的代码位点

基于这轮审计，后续最值得优先推进的代码位点是：

### 第一优先级

- `task_exporters/*step_mapper.py`
- `task_exporters/*kotlin_step_renderer.py`

重点是把：

- alias 兼容
- 参数名归一化
- threshold / mask / useColor
- OCR 参数语义

先做实。

### 第二优先级

- `apk_exporter/improved_compilable_runtime_project_readiness_analyzer.py`
- comparison 相关 summary / serializer / writer

重点是逐步补：

- `compile_ok`
- `runtime_smoke_ok`
- benchmark pass rate

### 第三优先级

- `android_runtime_template`

重点不是先重构，而是配合 renderer 实际需要，补齐缺失运行时能力。

---

## 当前结论

当前项目距离目标并不主要差在：

- 工程模板复制
- 资源打包
- façade 继续包装

而是主要差在：

- 语义映射覆盖率
- 参数语义完整度
- 从静态 readiness 到真实编译/运行 readiness 的推进

因此，下一阶段最应该继续推进的是：

> 先把 step mapper / renderer 的语义和参数完整度做实，再把 readiness 从静态占位统计推进到真实编译/运行指标。
