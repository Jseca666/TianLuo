"""V4 package summary POC: 导出工程、打入 automation 资源并输出组合包 summary。"""

from pathlib import Path

from apk_exporter.delivery_ready_project_with_assets_summary_facade import DeliveryReadyProjectWithAssetsSummaryFacade
from examples.exportable_api_delivery_ready_advanced_poc_task_factory import build_delivery_ready_advanced_task_specs


def main():
    repo_root = Path(__file__).resolve().parents[1]
    facade = DeliveryReadyProjectWithAssetsSummaryFacade(repo_root)
    result = facade.export(
        task_specs=build_delivery_ready_advanced_task_specs(),
        output_root=repo_root / "generated_output_project_with_assets_summary",
        project_name="GeneratedAndroidProjectWithAssetsSummary",
        report_output_dir=repo_root / "generated_output_project_with_assets_summary_reports",
    )
    print(result)


if __name__ == "__main__":
    main()
