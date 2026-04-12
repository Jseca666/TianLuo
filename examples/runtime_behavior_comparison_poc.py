from pathlib import Path

from apk_exporter.runtime_behavior_comparison_workflow import RuntimeBehaviorComparisonWorkflow
from apk_exporter.runtime_behavior_comparison_writer import RuntimeBehaviorComparisonWriter
from examples.main_export_quality_semantic_task_factory import build_main_export_quality_semantic_task_specs


def main():
    repo_root = Path(__file__).resolve().parents[1]
    task_specs = build_main_export_quality_semantic_task_specs()
    workflow = RuntimeBehaviorComparisonWorkflow(repo_root)
    result = workflow.compare(
        task_specs=task_specs,
        output_root=repo_root / "generated_output_runtime_behavior_comparison",
    )
    report_path = RuntimeBehaviorComparisonWriter().write(
        result,
        repo_root / "generated_output_runtime_behavior_comparison_reports",
    )
    print({"result": result, "comparison_report_path": report_path})


if __name__ == "__main__":
    main()
