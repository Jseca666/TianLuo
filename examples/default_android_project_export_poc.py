"""V4 default export POC: 走默认导出通道生成 Android Studio 工程与默认报告。"""

from pathlib import Path

from apk_exporter.default_android_project_export_facade import DefaultAndroidProjectExportFacade
from examples.exportable_api_delivery_ready_advanced_poc_task_factory import build_delivery_ready_advanced_task_specs


def main():
    repo_root = Path(__file__).resolve().parents[1]
    facade = DefaultAndroidProjectExportFacade(repo_root)
    result = facade.export(
        task_specs=build_delivery_ready_advanced_task_specs(),
        output_root=repo_root / "generated_output_default_export",
        project_name="GeneratedAndroidProjectDefaultExport",
        report_output_dir=repo_root / "generated_output_default_export_reports",
    )
    print(result)


if __name__ == "__main__":
    main()
