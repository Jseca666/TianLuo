# Runtime Behavior Governance Note

## 当前目的

这一轮继续把 `runtime-behavior` 线往上接，不让它停在：

- behavior helper
- behavior renderer
- comparison
- backlog

这一层，而是继续推进到：

- stage status
- work item plan
- decision

这样 `runtime-behavior` 线不只是一个更强的实现分支，也开始具备自己的治理闭环。

---

## 当前新增内容

本次新增：

- `apk_exporter/runtime_behavior_stage_status_summary.py`
- `apk_exporter/runtime_behavior_stage_status_builder_v2.py`
- `apk_exporter/runtime_behavior_stage_status_writer_v2.py`
- `apk_exporter/runtime_behavior_stage_status_runner_v2.py`
- `apk_exporter/runtime_behavior_work_item_plan_summary_v2.py`
- `apk_exporter/runtime_behavior_work_item_plan_builder_v2.py`
- `apk_exporter/runtime_behavior_work_item_plan_writer_v2.py`
- `apk_exporter/runtime_behavior_work_item_plan_runner_v2.py`
- `apk_exporter/runtime_behavior_decision_summary_v2.py`
- `apk_exporter/runtime_behavior_decision_builder_v2.py`
- `apk_exporter/runtime_behavior_decision_runner_v2.py`
- `examples/runtime_behavior_decision_poc.py`

---

## 当前 stage status 会判断什么

当前 runtime-behavior stage status 会重点判断：

- `behavior_helper_usage`
- `behavior_observability`
- `behavior_gap_management`

这意味着这条线开始能独立回答：

- 行为 helper 是否已经真正进入生成代码
- `usedSemanticEngine / kernelSizeHintApplied / excludedNumberFiltered` 这些行为可观测性是否足够
- behavior backlog 当前是否还存在明显缺口

---

## 当前 work item plan 会收口什么

当前 runtime-behavior plan 会围绕：

- behavior helper adoption
- behavior observability expansion
- behavior gap reduction

来生成下一批工作项。

这和前面的语义主治理链不同，它更专注于：

> OCR runtime 行为是否真的在往“可观测、可回归、可继续实现”这个方向推进。

---

## 当前 decision 的作用

当前 runtime-behavior decision layer 会进一步把这条线收口成：

- `primary_focus`
- `secondary_focus`
- `freeze_recommendations`

以及若干 lane 级 decision items。

这样后续继续推进这条线时，不会只是“继续加 behavior helper”，而是会更明确地知道：

- 当前是主攻 observability 还是 helper adoption
- 哪些入口应该先保持稳定
- 下一轮更适合往哪一类 OCR 行为实现推进

---

## 推荐入口

当前推荐新增入口：

- `python examples/runtime_behavior_decision_poc.py`

同时结合前一轮已经新增的：

- `python examples/runtime_behavior_suite_poc.py`
- `python examples/runtime_behavior_gap_backlog_poc.py`

可以更完整地看到这条线从实现到治理的状态。

---

## 当前结论

这一轮的核心意义是：

> `runtime-behavior` 线已经不再只是“比 runtime-semantic 更强的一条技术分支”，而是开始具备独立的 stage status / plan / decision 治理能力。

这会让后续继续推进 `kernel_size` 的真实行为实现时，更容易基于这条线持续演进，而不是每次都回到更抽象的主治理链上手动判断。
