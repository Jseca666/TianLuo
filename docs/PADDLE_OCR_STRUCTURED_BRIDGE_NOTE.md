# Paddle OCR Structured Bridge Note

## 当前目的

这一轮的目标不是立刻把 JNI 和 Paddle Lite 细节硬写死，而是先把 TianLuo 里最容易补错的一层 OCR bridge 收口成：

- 对官方 `PP-OCRv5_mobile` 主线有明确目标
- 对检测框 / 置信度 / 多行文本这些真实结果形态有承载位
- 对现有 `readText` / `readNumber` 调用面保持兼容

---

## 为什么新增 structured bridge

当前旧接口 `PaddleOcrRuntimeBridge` 只返回：

- `List<String>`

这对于先做占位 wiring 是够的，但对后续真实 Android OCR 落地并不稳妥。

因为官方 Android on-device OCR 路径本质上不是“只返回文本字符串”，而是检测、方向分类、识别三段串起来的结果链。

如果继续把 bridge 定死成“只回文本列表”，后续一旦要补：

- 文本框位置
- 每行置信度
- 多行顺序
- 调试信息

就容易返工。

因此当前新增：

- `StructuredPaddleOcrRuntimeBridge`
- `PaddleOcrStructuredResult`
- `StructuredPaddleSemanticOcrEngine`
- `StructuredPaddleOcrEngineProvider`
- `StructuredPaddleOcrProviderInstaller`
- `PaddleOcrOfficialModelProfile`

---

## 当前设计原则

### 1. 保留旧 bridge，不直接硬改

旧 `PaddleOcrRuntimeBridge` 仍然保留。

这样当前项目里已经依赖旧 provider / engine 的路径不会被一次性打断。

### 2. 新增 structured bridge 作为更接近真实落地的主线

新的 `StructuredPaddleOcrRuntimeBridge` 会返回：

- 行级文本
- 可选置信度
- 可选 polygon / box 信息
- 可选调试 notes
- 可选耗时

这更接近真实 Android OCR runtime 的实际输出形状。

### 3. 继续兼容 `readText` / `readNumber`

`StructuredPaddleSemanticOcrEngine` 仍然实现：

- `readText`
- `readNumber`

因此上层 task 语义不用先整体重构。

---

## 当前固定的模型主线

当前 `PaddleOcrOfficialModelProfile` 默认固定为：

- `PP-OCRv5_mobile`

并明确约定官方资产文件名：

- `PP-OCRv5_mobile_det.nb`
- `PP-OCRv5_mobile_rec.nb`
- `ch_ppocr_mobile_v2.0_cls_slim_opt.nb`
- `ppocr_keys_v1.txt`

这意味着后续真正实现 Android bridge 时，不需要再重新讨论“先接哪套模型”。

---

## 这一步的意义

这一轮的价值不在于“已经把真模型跑起来”，而在于：

> 现在项目里终于有了一条更不容易补错的 PaddleOCR bridge 主线。

接下来无论是：

- 直接封装官方 Android on-device demo
- 走 JNI + Paddle Lite
- 参考第三方 Android PaddleOCR 项目

都可以优先对接这条 structured bridge，而不是继续把真实结果硬压回 `List<String>`。
