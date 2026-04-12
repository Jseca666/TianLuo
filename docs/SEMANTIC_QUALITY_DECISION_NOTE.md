# Semantic Quality Decision Note

## 当前目的

这一轮在现有的：

- suite
- stage status
- work item plan

之上，再往前推进一层，补上“当前应该优先做什么、哪些东西暂时不要大动”的决策层。

这样项目的自动化判断链就从：

- 能比较
- 能看 backlog
- 能判断阶段
- 能列计划

继续推进到：

- 能形成主攻方向
- 能形成次级方向
- 能形成冻结建议

---

## 当前新增内容

本次新增：

- `apk_exporter/semantic_quality_decision_summary.py`
- `apk_exporter/semantic_quality_decision_builder.py`
- `apk_exporter/semantic_quality_decision_writer.py`
- `apk_exporter/semantic_quality_decision_runner.py`
- `examples/semantic_quality_decision_poc.py`

---

## decision 层当前会输出什么

当前 decision summary 会输出：

- `primary_focus`
- `secondary_focus`
- `freeze_recommendations`
- `items`
- `notes`

其中 decision items 当前会给出：

- `lane`
- `priority`
- `decision`
- `rationale`
- `related_work_items`

---

## 当前 decision 的价值

当前项目已经不是没有分析结果，而是已经有很多：

- comparison
- backlog
- suite
- stage status
- work item plan

但如果没有决策层，后续推进仍然很容易出现：

- 什么都想做
- 主线和旁线一起大动
- 没有冻结边界

这一轮新增的 decision layer，当前就是为了解决这个问题。

它会更明确地给出类似这样的结论：

- 主攻 runtime semantic behavior
- 次级关注 runtime contract completion
- 暂时冻结已稳定的 parameter mapping / contract shape

---

## 推荐入口

当前推荐新增入口：

- `python examples/semantic_quality_decision_poc.py`

它会串行跑：

1. work item plan runner
2. decision builder
3. decision writer

最后输出一份带有决策结果的 JSON 报告。

---

## 当前结论

这一轮的核心意义是：

> 项目已经从“能自动分析当前状态和计划”推进到“能自动形成下一阶段的推进决策”。

这让后续继续推进 OCR runtime 真实能力时，更接近一个工程化版本节奏，而不是很多并行方向同时发散。
