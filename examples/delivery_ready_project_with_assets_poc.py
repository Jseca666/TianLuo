"""V4 package POC: 导出 Android Studio 工程、生成任务代码并同时打入 automation 资源。"""

from pathlib import Path

from apk_exporter.delivery_ready_project_with_assets_facade import DeliveryReadyProjectWithAssetsFacade
from examples.exportable_api_delivery_ready_advanced_poc_task_factory import build_delivery_ready_advanced_task_specs


def main():
    repo_root = Path(__file__).resolve().parents[1]
    facade = DeliveryReadyProjectWithAssetsFacade(repo_root)
    result = facade.export(
        task_specs=build_delivery_ready_advanced_task_specs(),
        output_root=repo_root / "generated_output_project_with_assets",
        project_name="GeneratedAndroidProjectWithAssets",
        report_output_dir=repo_root / "generated_output_project_with_assets_reports",
    )
    print(result)


if __name__ == "__main__":
    main()
