from pathlib import Path

from apk_exporter.core_actions_runtime_ready_apk_smoke_workflow import CoreActionsRuntimeReadyApkSmokeWorkflow
from apk_exporter.core_actions_runtime_ready_apk_smoke_writer import CoreActionsRuntimeReadyApkSmokeWriter
from examples.main_export_core_actions_runtime_ready_task_factory import build_main_export_core_actions_runtime_ready_task_specs


def main():
    repo_root = Path(__file__).resolve().parents[1]
    task_specs = build_main_export_core_actions_runtime_ready_task_specs()
    workflow = CoreActionsRuntimeReadyApkSmokeWorkflow(repo_root)
    result = workflow.run(
        task_specs=task_specs,
        output_root=repo_root / "generated_output_core_actions_runtime_ready_apk_smoke",
    )
    report_path = CoreActionsRuntimeReadyApkSmokeWriter().write(
        result,
        repo_root / "generated_output_core_actions_runtime_ready_apk_smoke_reports",
    )
    print({"result": result, "smoke_report_path": report_path})


if __name__ == "__main__":
    main()
