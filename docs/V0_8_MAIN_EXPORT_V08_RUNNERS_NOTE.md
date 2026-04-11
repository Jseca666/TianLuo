# V0.8 Main Export V08 Runners Note

## 当前目的

这一轮的目标是把前面已经补上的 `quality v0.8` 能力，进一步整理成可以直接运行的入口，便于持续做回归与对比。

---

## 当前新增入口

本次新增：

- `apk_exporter/main_export_v08_comparison_runner.py`
- `examples/main_export_v08_comparison_runner_poc.py`

---

## 当前价值

`main_export_v08_comparison_runner.py` 把下面几件事收口在一起：

1. 读取固定 benchmark task specs
2. 跑 baseline `main export`
3. 跑 `quality v0.8 export`
4. 对 comparison 结果做 enriched benchmark 摘要
5. 写出 enriched comparison 报告

这样后续回归时，不需要在 POC 里重复拼装 workflow / enricher / writer。

---

## 推荐使用方式

当前可以优先跑：

- `python examples/main_export_v08_comparison_runner_poc.py`

它会直接输出：

- comparison result
- enriched result
- comparison report path

---

## 当前边界

这一轮仍然属于 `v0.8` 的验证与收口阶段。

目前已经形成：

- alias-friendly quality task generation 线
- alias-friendly quality project export 线
- baseline vs quality v0.8 comparison workflow
- 可直接运行的 comparison runner

后续下一步应继续推进：

- 把已验证稳定的 alias / comparison 能力逐步并回旧主线
- 补第一批更值得进入主入口的高频动作支持
