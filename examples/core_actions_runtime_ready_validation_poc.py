from pathlib import Path

from apk_exporter.core_actions_runtime_ready_validation_workflow import CoreActionsRuntimeReadyValidationWorkflow
from apk_exporter.core_actions_runtime_ready_validation_writer import CoreActionsRuntimeReadyValidationWriter
from examples.main_export_core_actions_runtime_ready_task_factory import build_main_export_core_actions_runtime_ready_task_specs


def main():
    repo_root = Path(__file__).resolve().parents[1]
    task_specs = build_main_export_core_actions_runtime_ready_task_specs()
    workflow = CoreActionsRuntimeReadyValidationWorkflow(repo_root)
    result = workflow.run(
        task_specs=task_specs,
        output_root=repo_root / "generated_output_core_actions_runtime_ready_validation",
    )
    report_path = CoreActionsRuntimeReadyValidationWriter().write(
        result,
        repo_root / "generated_output_core_actions_runtime_ready_validation_reports",
    )
    print({"result": result, "validation_report_path": report_path})


if __name__ == "__main__":
    main()
