"""V4 main export quality report POC: 导出更高动作覆盖率工程并写 quality 报告。"""

from pathlib import Path

from apk_exporter.main_export_quality_project_export_report_facade import MainExportQualityProjectExportReportFacade
from examples.main_export_quality_poc_task_factory import build_main_export_quality_task_specs


def main():
    repo_root = Path(__file__).resolve().parents[1]
    facade = MainExportQualityProjectExportReportFacade(repo_root)
    result = facade.export(
        task_specs=build_main_export_quality_task_specs(),
        output_root=repo_root / "generated_output_main_export_quality_report",
        project_name="GeneratedAndroidProjectMainExportQualityReport",
        report_output_dir=repo_root / "generated_output_main_export_quality_report_reports",
    )
    print(result)


if __name__ == "__main__":
    main()
