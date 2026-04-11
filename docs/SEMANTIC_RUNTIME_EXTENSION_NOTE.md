# Semantic Runtime Extension Note

## 当前目的

这一轮的目标，是把 `kernel_size / excluded_number` 从“只存在 semantic note”推进到：

- runtime 侧有正式扩展接口位置
- 生成侧有正式调用路径
- 旧 `OcrEngine` 未升级时仍然可以优雅回退

---

## 当前新增内容

本次新增：

- `android_runtime_template/.../ocr/OcrReadOptions.kt`
- `android_runtime_template/.../ocr/SemanticOcrEngine.kt`
- `android_runtime_template/.../ocr/OcrSemanticSupport.kt`
- `task_exporters/main_export_quality_runtime_semantic_kotlin_step_renderer.py`
- `task_exporters/main_export_quality_runtime_semantic_task_export_session.py`
- `apk_exporter/main_export_quality_runtime_semantic_project_export_workflow.py`
- `apk_exporter/main_export_quality_runtime_semantic_project_export_facade.py`
- `apk_exporter/main_export_quality_runtime_semantic_project_export_report_facade.py`
- `examples/main_export_quality_runtime_semantic_project_export_report_poc.py`

---

## runtime 侧新增的能力形态

### 1. `OcrReadOptions`

当前 OCR 相关的扩展语义被正式收口到：

- `maskName`
- `kernelSize`
- `excludedNumber`

### 2. `SemanticOcrEngine`

这是一个非破坏式扩展接口：

- 旧 `OcrEngine` 不需要立刻改签名
- 新实现可以逐步实现 `SemanticOcrEngine`
- 这样不会立即破坏已有 runtime template 结构

### 3. `OcrSemanticSupport`

新增 helper 后，当前导出链可以直接调用：

- `readTextSemantic(...)`
- `readNumberSemantic(...)`

其行为是：

- 如果 `context.ocrEngine` 实现了 `SemanticOcrEngine`，就走扩展语义路径
- 否则回退到旧 `OcrEngine`
- 同时先在 helper 层接住 `excludedNumber` 的后置过滤语义

---

## 当前推进的实际意义

这一轮不是已经把 Android OCR runtime 全部做完了。

但它确实把项目往前推进了一步：

- `excluded_number` 不再只是 note，它已经开始有真正的 runtime fallback 语义
- `kernel_size` 虽然仍未真正实现处理逻辑，但已经有了正式的 runtime option 承载位
- 生成出的 Kotlin 任务可以不再只写 semantic notes，而是开始走明确 helper 调用路径

---

## 推荐入口

当前可以直接运行：

- `python examples/main_export_quality_runtime_semantic_project_export_report_poc.py`

它会使用带语义参数的 task specs，走新的 runtime-aware semantic 导出线，输出 Android 工程和质量报告。

---

## 当前结论

这一轮的核心意义是：

> 我们开始把“还没彻底实现的 OCR 语义”从纯记录状态，推进到“有 runtime extension contract + 有 fallback 行为 + 有生成调用路径”的状态。

这会让下一阶段继续推进 `kernel_size / excluded_number` 时，不再是从零开始，而是在已有扩展骨架上继续补真实能力。
