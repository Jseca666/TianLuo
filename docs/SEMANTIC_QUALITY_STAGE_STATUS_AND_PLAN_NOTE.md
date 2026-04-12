# Semantic Quality Stage Status And Plan Note

## 当前目的

这一轮继续把已有的 suite 回归能力往前推进了一层：

1. 从 suite 结果自动判断当前阶段状态
2. 从阶段状态自动生成下一批 work items

这样项目内就不再只是有大量 comparison / backlog 输出，而是开始具备：

- 当前在哪里
- 下一步做什么

这样的结构化判断能力。

---

## 当前新增内容

本次新增：

- `apk_exporter/semantic_quality_stage_status_summary.py`
- `apk_exporter/semantic_quality_stage_status_builder.py`
- `apk_exporter/semantic_quality_stage_status_writer.py`
- `apk_exporter/semantic_quality_stage_status_runner.py`
- `examples/semantic_quality_stage_status_poc.py`
- `apk_exporter/semantic_quality_work_item_plan_summary.py`
- `apk_exporter/semantic_quality_work_item_plan_builder.py`
- `apk_exporter/semantic_quality_work_item_plan_writer.py`
- `apk_exporter/semantic_quality_work_item_plan_runner.py`
- `examples/semantic_quality_work_item_plan_poc.py`

---

## 当前 stage status 会判断哪些阶段

当前 builder 会判断这些 stage：

- `parameter_propagation`
- `semantic_gap_management`
- `runtime_semantic_contract`
- `runtime_semantic_behavior`

每个 stage 当前会给出：

- `status`: `unstarted / partial / stable`
- `reason`
- `evidence`
- `next_actions`

这意味着 suite 结果现在不只是一堆数字，而是开始有阶段性解释。

---

## 当前 work item plan 的来源

`semantic_quality_work_item_plan_runner.py` 的流程是：

1. 先跑 `semantic_quality_stage_status_runner`
2. 再基于 `stage_status` 自动生成 work item plan

当前生成的 plan 会重点围绕：

- 参数透传加固
- semantic gap 缩减
- runtime-semantic contract 完整度
- runtime-semantic behavior 实现

并给出：

- `title`
- `priority`
- `rationale`
- `target_files`
- `depends_on`

---

## 推荐入口

当前推荐新增入口：

- `python examples/semantic_quality_stage_status_poc.py`
- `python examples/semantic_quality_work_item_plan_poc.py`

其中：

- 前者更适合看“当前阶段状态”
- 后者更适合看“下一批该做什么”

---

## 当前结论

这一轮的核心意义是：

> 项目已经从“能回归、能比较、能列 backlog”推进到“能自动判断阶段状态，并自动产出下一批工作项”。

这让后续继续推进 OCR runtime 真实能力时，已经不仅是一个技术实验链，而更像一条可持续演进的工程化交付链。
