"""V4 delivery-ready advanced POC: 导出工程并输出更清晰的 report summary。"""

from pathlib import Path

from apk_exporter.delivery_ready_compilable_runtime_project_report_summary_facade import DeliveryReadyCompilableRuntimeProjectReportSummaryFacade
from examples.exportable_api_delivery_ready_advanced_poc_task_factory import build_delivery_ready_advanced_task_specs


def main():
    repo_root = Path(__file__).resolve().parents[1]
    facade = DeliveryReadyCompilableRuntimeProjectReportSummaryFacade(repo_root)
    result = facade.export(
        task_specs=build_delivery_ready_advanced_task_specs(),
        output_root=repo_root / "generated_output_delivery_ready_advanced",
        project_name="GeneratedAndroidProjectDeliveryReadyAdvanced",
        report_output_dir=repo_root / "generated_output_delivery_ready_advanced_reports",
    )
    print(result)


if __name__ == "__main__":
    main()
