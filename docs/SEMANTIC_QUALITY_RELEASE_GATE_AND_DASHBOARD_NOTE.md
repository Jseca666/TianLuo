# Semantic Quality Release Gate And Dashboard Note

## 当前目的

这一轮继续把已有的：

- suite
- stage status
- work item plan
- decision

再往前推进一层，补上：

- `release gate`
- `dashboard`

这样当前项目不只会告诉我们：

- 该做什么
- 哪些线先别乱动

还会进一步告诉我们：

- 哪些推进通道现在是 `open`
- 哪些只能 `partial`
- 哪些仍然应该 `hold`

并给出一个统一的语义质量态势入口。

---

## 当前新增内容

本次新增：

- `apk_exporter/semantic_quality_release_gate_summary.py`
- `apk_exporter/semantic_quality_release_gate_builder.py`
- `apk_exporter/semantic_quality_release_gate_writer.py`
- `apk_exporter/semantic_quality_release_gate_runner.py`
- `apk_exporter/semantic_quality_dashboard_writer.py`
- `apk_exporter/semantic_quality_dashboard_runner.py`
- `examples/semantic_quality_dashboard_poc.py`

---

## release gate 当前会判断什么

当前 release gate 会重点判断这些 gate：

- `main_entry_convergence`
- `runtime_contract_expansion`
- `runtime_behavior_promotion`
- `benchmark_scope_expansion`

每个 gate 当前会给出：

- `status`: `hold / partial / open`
- `rationale`
- `unblock_actions`
- `evidence`

这意味着项目现在开始不只是有“建议”，而是开始有更明确的推进门控判断。

---

## dashboard 的作用

当前新增的 dashboard runner 并没有重复造新逻辑，而是把：

- decision runner
- release gate runner

的结果统一收口成一份 JSON dashboard 输出。

这让当前项目第一次有了一个更完整的“语义质量态势入口”。

---

## 推荐入口

当前推荐新增入口：

- `python examples/semantic_quality_dashboard_poc.py`

它会串行收口：

1. suite
2. stage status
3. work item plan
4. decision
5. release gate
6. dashboard report

---

## 当前结论

这一轮的核心意义是：

> 项目已经从“能自动形成计划和决策”推进到“能自动形成带门控判断的语义质量态势面板”。

这让后续继续推进 OCR runtime 真正能力时，更容易形成稳定的版本推进节奏：

- 哪些东西可以继续扩展
- 哪些东西应该保持冻结
- 哪些东西还不适合并回主线
