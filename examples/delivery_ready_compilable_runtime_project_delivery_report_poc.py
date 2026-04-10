"""V4 delivery-ready report POC: 导出工程并写出 delivery-ready 完整报告。"""

from pathlib import Path

from apk_exporter.delivery_ready_compilable_runtime_project_delivery_report_facade import DeliveryReadyCompilableRuntimeProjectDeliveryReportFacade
from examples.exportable_api_delivery_ready_poc_task_factory import build_delivery_ready_demo_task_specs


def main():
    repo_root = Path(__file__).resolve().parents[1]
    facade = DeliveryReadyCompilableRuntimeProjectDeliveryReportFacade(repo_root)
    result = facade.export(
        task_specs=build_delivery_ready_demo_task_specs(),
        output_root=repo_root / "generated_output_delivery_ready",
        project_name="GeneratedAndroidProjectDeliveryReady",
        report_output_dir=repo_root / "generated_output_delivery_ready_reports",
    )
    print(result)


if __name__ == "__main__":
    main()
