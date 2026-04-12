# Runtime Behavior Release Gate And Dashboard Note

## 当前目的

这一轮继续把 `runtime-behavior` 线从独立的实现与回归线，推进成一条有完整治理闭环的推进线。

当前新增的重点不是新的 OCR 参数，而是把这条线接入：

- `stage status`
- `work item plan`
- `decision`
- `release gate`
- `dashboard`

这样后续继续推进 `kernel_size` 与 `excluded_number` 的真实行为实现时，这条线已经可以独立判断：

- 当前处于什么阶段
- 下一步做什么
- 哪些推进通道可以打开
- 哪些仍然应该保持选择性推进

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
- `apk_exporter/runtime_behavior_release_gate_summary_v2.py`
- `apk_exporter/runtime_behavior_release_gate_builder_v2.py`
- `apk_exporter/runtime_behavior_release_gate_runner_v2.py`
- `apk_exporter/runtime_behavior_dashboard_runner_v2.py`
- `examples/runtime_behavior_decision_poc.py`
- `examples/runtime_behavior_dashboard_poc.py`

---

## 当前 stage status 会判断什么

当前 runtime-behavior stage status 会重点判断：

- `behavior_helper_usage`
- `behavior_observability`
- `behavior_gap_management`

这意味着这条线会独立判断：

- 行为 helper 是否已经真正进入生成代码
- `usedSemanticEngine / kernelSizeHintApplied / excludedNumberFiltered` 这些行为观测信号是否足够
- 当前 behavior backlog 是否仍然有明显缺口

---

## 当前 plan / decision 会收口什么

当前 runtime-behavior plan 会围绕：

- behavior helper adoption
- behavior observability expansion
- behavior gap reduction

当前 runtime-behavior decision 会进一步收口成：

- `primary_focus`
- `secondary_focus`
- `freeze_recommendations`

也就是说，当前这条线不只会说“还有 gap”，而会更明确地判断：

- 现在主攻 observability 还是 helper adoption
- 哪些入口应该先保持稳定
- 下一轮更适合往哪一类 OCR 行为实现推进

---

## 当前 release gate / dashboard 的意义

当前 runtime-behavior release gate 会判断：

- `helper_adoption`
- `observability_expansion`
- `behavior_line_promotion`

每个 gate 会给出：

- `hold / partial / open`
- `rationale`
- `unblock_actions`
- `evidence`

再由 dashboard runner 收口成统一 JSON 输出。

这样当前 `runtime-behavior` 线已经可以独立形成：

> suite → stage status → work item plan → decision → release gate → dashboard

的完整治理闭环。

---

## 推荐入口

当前推荐新增入口：

- `python examples/runtime_behavior_decision_poc.py`
- `python examples/runtime_behavior_dashboard_poc.py`

同时结合前一轮已有的：

- `python examples/runtime_behavior_suite_poc.py`
- `python examples/runtime_behavior_gap_backlog_poc.py`

可以更完整地看到这条线从实现到治理的全链路状态。

---

## 当前结论

这一轮的核心意义是：

> `runtime-behavior` 线已经不再只是一个更强的 OCR runtime 技术分支，而是开始具备和主治理链同等级的闭环判断能力。

这让后续继续推进 `kernel_size` 的真实行为实现时，可以更自然地基于这条线本身持续演进，而不是每次都回到更抽象的总治理链上手动判断。
