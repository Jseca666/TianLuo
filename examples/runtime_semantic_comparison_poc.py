from pathlib import Path

from apk_exporter.runtime_semantic_comparison_workflow import RuntimeSemanticComparisonWorkflow
from apk_exporter.runtime_semantic_comparison_writer import RuntimeSemanticComparisonWriter
from examples.main_export_quality_semantic_task_factory import build_main_export_quality_semantic_task_specs


def main():
    repo_root = Path(__file__).resolve().parents[1]
    task_specs = build_main_export_quality_semantic_task_specs()
    workflow = RuntimeSemanticComparisonWorkflow(repo_root)
    result = workflow.compare(
        task_specs=task_specs,
        output_root=repo_root / "generated_output_runtime_semantic_comparison",
    )
    report_path = RuntimeSemanticComparisonWriter().write(
        result,
        repo_root / "generated_output_runtime_semantic_comparison_reports",
    )
    print({"result": result, "comparison_report_path": report_path})


if __name__ == "__main__":
    main()
