"""V0.8 main export quality project export report POC: 使用 alias-friendly quality 线导出真实 Android 工程并输出报告。"""

from pathlib import Path

from apk_exporter.main_export_quality_v08_project_export_report_facade import MainExportQualityV08ProjectExportReportFacade
from examples.main_export_quality_v08_alias_task_factory import build_main_export_quality_v08_alias_task_specs


def main():
    repo_root = Path(__file__).resolve().parents[1]
    facade = MainExportQualityV08ProjectExportReportFacade(repo_root)
    result = facade.export(
        task_specs=build_main_export_quality_v08_alias_task_specs(),
        output_root=repo_root / "generated_output_main_export_quality_v08_project",
        project_name="GeneratedAndroidProjectQualityV08",
        report_output_dir=repo_root / "generated_output_main_export_quality_v08_reports",
    )
    print(result)


if __name__ == "__main__":
    main()
