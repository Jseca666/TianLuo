"""V4 improved delivery POC: 导出工程、校验结果并分析就绪度。"""

from pathlib import Path

from apk_exporter.improved_compilable_runtime_project_delivery_facade import ImprovedCompilableRuntimeProjectDeliveryFacade
from examples.exportable_api_realistic_poc_task_factory import build_realistic_demo_task_specs


def main():
    repo_root = Path(__file__).resolve().parents[1]
    facade = ImprovedCompilableRuntimeProjectDeliveryFacade(repo_root)
    result = facade.export(
        task_specs=build_realistic_demo_task_specs(),
        output_root=repo_root / "generated_output_delivery",
        project_name="GeneratedAndroidProjectDelivery",
        report_output_dir=repo_root / "generated_output_delivery_reports",
    )
    print(result)


if __name__ == "__main__":
    main()
