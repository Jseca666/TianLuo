# Runtime Semantic Comparison Note

## 当前目的

这一轮的目标，是把前面新增的 `runtime-semantic` 导出线接入 comparison 体系。

这样项目里不再只知道：

- 旧 semantic 线会保留 `kernel_size / excluded_number` 的语义痕迹

还会知道：

- 新 runtime-semantic 线是否真的把这些语义进一步推进到了运行时调用层

---

## 当前新增内容

本次新增：

- `apk_exporter/runtime_semantic_readiness_summary.py`
- `apk_exporter/runtime_semantic_readiness_analyzer.py`
- `apk_exporter/runtime_semantic_comparison_workflow.py`
- `apk_exporter/runtime_semantic_comparison_writer.py`
- `examples/runtime_semantic_comparison_poc.py`

---

## 当前 comparison 的比较对象

当前 workflow 直接比较：

- `semantic quality export`
- `runtime-semantic quality export`

它们使用同一组 semantic task specs，但导出线不同。

---

## runtime-semantic readiness 当前关注的指标

当前 analyzer 会统计这些更靠近 runtime 落点的指标：

- `ocr_read_options_count`
- `kernel_size_option_count`
- `excluded_number_option_count`
- `read_text_semantic_count`
- `read_number_semantic_count`

同时也会结合 task specs 统计：

- `expected_kernel_size_steps`
- `expected_excluded_number_steps`

这样可以更具体地回答：

- `kernel_size` 是否已经不再只是 note，而是进入了 `OcrReadOptions`
- `excluded_number` 是否已经不再只是 note，而是进入了 `OcrReadOptions`
- 生成代码是否开始真正调用 `readTextSemantic / readNumberSemantic`

---

## 当前 comparison 的意义

这条 comparison 线的价值在于：

1. 不再只比较参数透传有没有发生
2. 而是开始比较语义是否已经落到 runtime helper 调用层
3. 从而判断 `runtime-semantic` 线相对旧 semantic 线到底推进了多少

---

## 推荐入口

当前可以直接运行：

- `python examples/runtime_semantic_comparison_poc.py`

它会输出：

- semantic quality export 结果
- runtime-semantic quality export 结果
- 两侧 runtime-semantic readiness 摘要
- comparison report path

---

## 当前结论

这一轮的核心意义是：

> 项目开始能定量比较“旧 semantic 线”和“runtime-semantic 线”之间的真实差距。

这让后续继续推进 `kernel_size / excluded_number` 时，不再只是靠直觉判断，而是有一条更贴近运行时落点的 comparison 依据。
