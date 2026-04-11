"""V0.8 main export comparison benchmark enriched POC: 在固定 benchmark 对比结果之上补充任务覆盖与差异摘要。"""

from pathlib import Path

from apk_exporter.main_export_comparison_benchmark_enricher import MainExportComparisonBenchmarkEnricher
from apk_exporter.main_export_comparison_benchmark_writer import MainExportComparisonBenchmarkWriter
from apk_exporter.main_export_comparison_workflow import MainExportComparisonWorkflow
from examples.main_export_quality_benchmark_task_factory import build_main_export_quality_benchmark_task_specs


def main():
    repo_root = Path(__file__).resolve().parents[1]
    task_specs = build_main_export_quality_benchmark_task_specs()
    workflow = MainExportComparisonWorkflow(repo_root)
    comparison_result = workflow.compare(
        task_specs=task_specs,
        output_root=repo_root / "generated_output_main_export_benchmark_enriched_comparison",
    )
    enriched_result = MainExportComparisonBenchmarkEnricher().enrich(
        task_specs=task_specs,
        comparison_result=comparison_result,
    )
    report_path = MainExportComparisonBenchmarkWriter().write(
        enriched_result,
        repo_root / "generated_output_main_export_benchmark_enriched_comparison_reports",
    )
    print({"enriched_result": enriched_result, "comparison_report_path": report_path})


if __name__ == "__main__":
    main()
