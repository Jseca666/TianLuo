"""V4 default export delivery POC: 走默认导出通道并输出带 readiness 的默认结果。"""

from pathlib import Path

from apk_exporter.default_android_project_export_delivery_facade import DefaultAndroidProjectExportDeliveryFacade
from examples.exportable_api_delivery_ready_advanced_poc_task_factory import build_delivery_ready_advanced_task_specs


def main():
    repo_root = Path(__file__).resolve().parents[1]
    facade = DefaultAndroidProjectExportDeliveryFacade(repo_root)
    result = facade.export(
        task_specs=build_delivery_ready_advanced_task_specs(),
        output_root=repo_root / "generated_output_default_export_delivery",
        project_name="GeneratedAndroidProjectDefaultExportDelivery",
        report_output_dir=repo_root / "generated_output_default_export_delivery_reports",
    )
    print(result)


if __name__ == "__main__":
    main()
