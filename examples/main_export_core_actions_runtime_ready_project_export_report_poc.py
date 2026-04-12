from pathlib import Path

from apk_exporter.main_export_core_actions_runtime_ready_project_export_report_facade import MainExportCoreActionsRuntimeReadyProjectExportReportFacade
from examples.main_export_core_actions_runtime_ready_task_factory import build_main_export_core_actions_runtime_ready_task_specs


def main():
    repo_root = Path(__file__).resolve().parents[1]
    facade = MainExportCoreActionsRuntimeReadyProjectExportReportFacade(repo_root)
    result = facade.export(
        task_specs=build_main_export_core_actions_runtime_ready_task_specs(),
        output_root=repo_root / "generated_output_main_export_core_actions_runtime_ready_project",
        project_name="GeneratedAndroidProjectCoreActionsRuntimeReady",
        report_output_dir=repo_root / "generated_output_main_export_core_actions_runtime_ready_reports",
    )
    print(result)


if __name__ == "__main__":
    main()
