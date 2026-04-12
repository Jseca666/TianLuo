# Runtime Behavior Suite Note

## 当前目的

这一轮继续顺着 `runtime-behavior` 线推进，但重点不是再往高层治理链上加模块，而是把已经新增的行为 helper、行为 renderer、behavior comparison 与 behavior backlog 统一收口成一条更容易直接使用的 suite。

这样当前项目里就不仅有：

- runtime-behavior 导出线
- runtime-behavior comparison
- runtime-behavior backlog

还多了一条：

- runtime-behavior suite runner

---

## 当前新增内容

本次新增：

- `examples/main_export_quality_runtime_behavior_project_export_report_poc.py`
- `examples/runtime_behavior_comparison_poc.py`
- `apk_exporter/runtime_behavior_suite_workflow.py`
- `apk_exporter/runtime_behavior_suite_writer.py`
- `examples/runtime_behavior_suite_poc.py`

---

## 当前 suite 收口了什么

当前 `runtime_behavior_suite_workflow.py` 会统一收口：

1. `runtime-behavior comparison`
2. `runtime-behavior backlog`

并输出一组更直接的 notes，说明当前：

- runtime-behavior 线是否比 runtime-semantic 线前进了一步
- 当前是否还存在 unresolved tracked behavior observability gaps

---

## 当前推荐入口

当前推荐直接使用这些入口：

- `python examples/main_export_quality_runtime_behavior_project_export_report_poc.py`
- `python examples/runtime_behavior_comparison_poc.py`
- `python examples/runtime_behavior_gap_backlog_poc.py`
- `python examples/runtime_behavior_suite_poc.py`

其中：

- 第一个更适合直接看这条线的工程导出结果
- 第二个更适合看和 runtime-semantic 线的对比
- 第三个更适合看 behavior gap backlog
- 第四个更适合作为这一整条线的统一入口

---

## 当前结论

这一轮的核心意义是：

> runtime-behavior 线已经从一批底层实现和零散工具，推进成一条更完整、可直接回归的独立推进线。

这会让下一阶段继续推进 `kernel_size` 真实行为实现时，更容易基于这条线持续迭代，而不是每次手动拼装 comparison / backlog / export 链路。
