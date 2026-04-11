# Semantic Gap Backlog Note

## 当前目的

这一轮不是直接去改 Android runtime 的 OCR 细节，而是先把当前仍未落下去的语义缺口，正式结构化成 backlog。

目标是把下面这些问题从“聊天里的判断”变成“项目里的固定工作项”：

- `kernel_size` 还没有 runtime support
- `excluded_number` 还没有 runtime support
- 哪些参数语义已经基本解决
- 哪些参数语义仍然是下一阶段的主攻点

---

## 当前新增内容

本次新增：

- `apk_exporter/semantic_gap_backlog_summary.py`
- `apk_exporter/semantic_gap_backlog_builder.py`
- `apk_exporter/semantic_gap_backlog_workflow.py`
- `apk_exporter/semantic_gap_backlog_writer.py`
- `examples/semantic_gap_backlog_poc.py`

---

## 当前 backlog 的来源

当前 backlog 不是手写结论，而是基于前一轮已经建立的：

- semantic parameter comparison workflow
- semantic parameter readiness analyzer

在对比：

- baseline `main export`
- `semantic quality export`

之后，再把剩余缺口整理成 backlog item。

---

## 当前 backlog 覆盖的 gap key

目前 backlog builder 会整理这些语义缺口：

- `threshold_propagation`
- `mask_name_propagation`
- `use_color_propagation`
- `kernel_size_runtime_support`
- `excluded_number_runtime_support`

其中：

- 前三项更偏“renderer / 参数透传完整度”
- 后两项更偏“runtime 还没真正接住的语义能力”

---

## 当前 backlog 的价值

这条 backlog 线的价值是：

1. 不再只知道 semantic 线“更好”
2. 而是能更具体地知道：下一批最该改哪里
3. 给每个 gap 补上：
   - 预期数量
   - 已解决数量
   - 未解决数量
   - 当前可见性
   - 目标代码位点

这样后续推进 `kernel_size / excluded_number` 时，不会只停留在泛泛的路线图，而会变成更明确的工程 work items。

---

## 推荐入口

当前可以直接运行：

- `python examples/semantic_gap_backlog_poc.py`

它会输出：

- semantic parameter comparison result
- semantic gap backlog summary
- backlog report path

---

## 当前结论

这一轮的核心意义是：

> 我们开始把“剩余语义缺口”正式纳入项目 backlog，而不是只停留在分析结论层。

这会让下一阶段继续推进 runtime 语义落地时，更有秩序，也更容易逐步并回主线。
