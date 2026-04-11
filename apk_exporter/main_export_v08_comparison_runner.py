from pathlib import Path

from .main_export_comparison_benchmark_enricher import MainExportComparisonBenchmarkEnricher
from .main_export_comparison_benchmark_writer import MainExportComparisonBenchmarkWriter
from .main_export_v08_comparison_workflow import MainExportV08ComparisonWorkflow
from examples.main_export_quality_benchmark_task_factory import build_main_export_quality_benchmark_task_specs


def run(repo_root: Path) -> dict:
    task_specs = build_main_export_quality_benchmark_task_specs()
    workflow = MainExportV08ComparisonWorkflow(repo_root)
    comparison_result = workflow.compare(
        task_specs=task_specs,
        output_root=Path(repo_root) / "generated_output_main_export_v08_comparison",
    )
    enriched_result = MainExportComparisonBenchmarkEnricher().enrich(
        task_specs=task_specs,
        comparison_result=comparison_result,
    )
    report_path = MainExportComparisonBenchmarkWriter().write(
        enriched_result,
        Path(repo_root) / "generated_output_main_export_v08_comparison_reports",
    )
    return {
        "comparison_result": comparison_result,
        "enriched_result": enriched_result,
        "comparison_report_path": report_path,
    }
