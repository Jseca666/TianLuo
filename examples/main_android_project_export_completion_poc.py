"""V4 main export completion POC: 走当前更接近长期主入口的完成态出口。"""

from pathlib import Path

from apk_exporter.main_android_project_export_completion_facade import MainAndroidProjectExportCompletionFacade
from examples.exportable_api_delivery_ready_advanced_poc_task_factory import build_delivery_ready_advanced_task_specs


def main():
    repo_root = Path(__file__).resolve().parents[1]
    facade = MainAndroidProjectExportCompletionFacade(repo_root)
    result = facade.export(
        task_specs=build_delivery_ready_advanced_task_specs(),
        output_root=repo_root / "generated_output_main_export_completion",
        project_name="GeneratedAndroidProjectMainExportCompletion",
        report_output_dir=repo_root / "generated_output_main_export_completion_reports",
    )
    print(result)


if __name__ == "__main__":
    main()
