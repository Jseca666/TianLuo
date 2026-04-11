"""V0.8 main export comparison benchmark POC: 使用更丰富的固定任务集对比 baseline main export 与 quality export。"""

from pathlib import Path

from apk_exporter.main_export_comparison_workflow import MainExportComparisonWorkflow
from apk_exporter.main_export_comparison_writer import MainExportComparisonWriter
from examples.main_export_quality_benchmark_task_factory import build_main_export_quality_benchmark_task_specs


def main():
    repo_root = Path(__file__).resolve().parents[1]
    workflow = MainExportComparisonWorkflow(repo_root)
    result = workflow.compare(
        task_specs=build_main_export_quality_benchmark_task_specs(),
        output_root=repo_root / "generated_output_main_export_benchmark_comparison",
    )
    report_path = MainExportComparisonWriter().write(
        result,
        repo_root / "generated_output_main_export_benchmark_comparison_reports",
    )
    print({"result": result, "comparison_report_path": report_path})


if __name__ == "__main__":
    main()
