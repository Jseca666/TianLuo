# Runtime Semantic Gap Backlog And Suite Note

## 当前目的

这一轮做了两件相互配合的事情：

1. 把 `runtime-semantic` 线正式接入 backlog 体系
2. 把现有的 semantic / runtime-semantic comparison 与 backlog 统一收口成一个 suite runner

这样后续回归时，不需要分别手动跑多条入口。

---

## 当前新增内容

本次新增：

- `apk_exporter/runtime_semantic_gap_backlog_builder.py`
- `apk_exporter/runtime_semantic_gap_backlog_workflow.py`
- `apk_exporter/runtime_semantic_gap_backlog_writer.py`
- `examples/runtime_semantic_gap_backlog_poc.py`
- `apk_exporter/semantic_quality_suite_workflow.py`
- `apk_exporter/semantic_quality_suite_writer.py`
- `examples/semantic_quality_suite_poc.py`

---

## runtime-semantic backlog 当前覆盖的核心 gap

当前 builder 会重点整理：

- `kernel_size_runtime_contract`
- `excluded_number_runtime_contract`
- `excluded_number_runtime_behavior`
- `kernel_size_runtime_behavior`

这里故意区分了：

- contract
- behavior

因为当前项目状态已经不是“什么都没有”，而是：

- `kernel_size / excluded_number` 已经有 runtime contract
- `excluded_number` 已经有 helper fallback behavior
- `kernel_size` 仍然缺少真正的 runtime behavior

这比之前只说“还没支持”更精确。

---

## semantic quality suite 当前收口了什么

新增的 suite workflow 会一次性跑完：

1. `semantic parameter comparison`
2. `semantic gap backlog`
3. `runtime-semantic comparison`
4. `runtime-semantic gap backlog`

这样当前就有了一个统一入口，用来观察：

- 参数语义是否透传
- 旧 semantic 线还剩多少 gap
- runtime-semantic 线推进了多少
- runtime-semantic 线还剩多少 contract / behavior gap

---

## 推荐入口

当前优先推荐两个入口：

- `python examples/runtime_semantic_gap_backlog_poc.py`
- `python examples/semantic_quality_suite_poc.py`

其中：

- 前者更聚焦 runtime-semantic backlog
- 后者更适合作为整套语义质量回归入口

---

## 当前结论

这一轮的核心意义是：

> runtime-semantic 线已经不再只是“更高级的一条导出线”，而是已经正式接入 comparison + backlog + suite 回归体系。

这意味着后续继续推进 OCR runtime 真实能力时，已经具备更完整的工程化闭环：

- 有导出线
- 有 readiness
- 有 comparison
- 有 backlog
- 有 suite runner
