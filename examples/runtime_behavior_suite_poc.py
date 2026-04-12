from pathlib import Path

from apk_exporter.runtime_behavior_suite_workflow import RuntimeBehaviorSuiteWorkflow
from apk_exporter.runtime_behavior_suite_writer import RuntimeBehaviorSuiteWriter
from examples.main_export_quality_semantic_task_factory import build_main_export_quality_semantic_task_specs


def main():
    repo_root = Path(__file__).resolve().parents[1]
    task_specs = build_main_export_quality_semantic_task_specs()
    workflow = RuntimeBehaviorSuiteWorkflow(repo_root)
    result = workflow.run(
        task_specs=task_specs,
        output_root=repo_root / "generated_output_runtime_behavior_suite",
    )
    report_path = RuntimeBehaviorSuiteWriter().write(
        result,
        repo_root / "generated_output_runtime_behavior_suite_reports",
    )
    print({"result": result, "suite_report_path": report_path})


if __name__ == "__main__":
    main()
