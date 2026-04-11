# Main Export vs Quality Export Comparison

## 当前定位

`main_export_vs_quality_comparison_facade.py` 用于在同一组 task specs 上同时运行：

- `MainAndroidProjectExportFacade`
- `MainExportQualityProjectExportReportFacade`

然后输出一份并排对比结果。

---

## 当前对比指标

当前已经对比：

- project_root
- task_count
- asset_file_count
- todo_count
- unsupported_count
- validation_ok
- 各类报告路径

---

## 当前价值

这一条对比链的主要价值是：

1. 判断 quality 线是否真正优于 main export 主入口
2. 为后续把成熟动作并回主入口提供依据
3. 减少靠主观感觉判断动作成熟度
