# OCR Runtime Wiring Note

## 当前目的

这一轮的目标，不是假装把 Android OCR 真模型已经接好了，而是先把 OCR 这条链推进到：

- 当前接的是哪个 provider
- 当前是不是 placeholder
- 真实 provider 未来应该从哪里接入

都能在工程里明确表达出来。

这一步的价值是：

> 让 OCR 不再只是“接口 + 空实现 + 一堆外层导出链”，而是开始具备明确的 provider wiring 结构。

---

## 当前新增内容

本次新增：

- `android_runtime_template/.../ocr/OcrRuntimeStatus.kt`
- `android_runtime_template/.../ocr/OcrEngineProvider.kt`
- `android_runtime_template/.../ocr/EmptyOcrEngineProvider.kt`
- `android_runtime_template/.../ocr/OcrEngineProviderRegistry.kt`
- `android_runtime_template/.../task/ProviderWiredTaskContext.kt`
- `android_runtime_template/.../task/ProviderWiredTaskRunner.kt`
- `apk_exporter/ocr_runtime_wiring_summary.py`
- `apk_exporter/ocr_runtime_wiring_workflow.py`
- `apk_exporter/ocr_runtime_wiring_writer.py`
- `examples/ocr_runtime_wiring_poc.py`

---

## 当前 provider wiring 结构

### 1. `OcrEngineProvider`

当前新增了正式的 provider 接口，提供：

- `providerName`
- `createEngine()`
- `describe()`

这意味着未来接真实 OCR 模型时，不再需要先硬改一大堆旧上下文或旧 helper，而是可以先实现一个新的 provider。

### 2. `EmptyOcrEngineProvider`

当前默认 provider 仍然是：

- `empty`

它会返回 `EmptyOcrEngine`，并在 `OcrRuntimeStatus` 里明确说明：

- 当前是 placeholder
- 当前需要外部模型接入

### 3. `OcrEngineProviderRegistry`

当前新增 registry 后，工程里开始具备：

- 安装 provider
- 查询当前 provider
- 重置到默认 provider

这样的基础能力。

### 4. `ProviderWiredTaskContext / ProviderWiredTaskRunner`

当前新增的这组 context / runner，不会直接替换旧的 `DefaultTaskContext`，而是作为一条更安全的新 wiring 路径存在。

这意味着后续接真实 OCR 模型时，可以优先沿这条 provider-wired 路径推进，而不是先拆老默认骨架。

---

## 当前 workflow 会输出什么

当前 `OcrRuntimeWiringWorkflow` 会：

1. 导出 OCR semantic 工程
2. 输出一份 wiring summary

summary 会明确说明：

- 当前 provider 相关文件位于哪里
- 当前 checks 是否已经具备 provider interface / registry / provider-wired context
- 当前默认 provider 仍然是不是 placeholder
- 当前是否仍然需要真实 OCR model/provider 接入

---

## 当前推荐入口

当前推荐直接运行：

- `python examples/ocr_runtime_wiring_poc.py`

它会生成：

- OCR runtime wiring 相关导出结果
- 一份 `ocr_runtime_wiring.json`

这样当前 OCR 这条链的 wiring 状态就不再是隐性的，而是可以直接查看。

---

## 当前结论

这一轮的核心意义是：

> Android OCR 这条链已经开始从“接口层空壳”推进到“provider-wired 可接真模型”的阶段。

它还不是“真机上真实 OCR 已经跑通”，但它已经把后续接入真实 OCR 模型最关键的一层 wiring 结构补出来了。
