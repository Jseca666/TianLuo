from pathlib import Path

from apk_exporter.main_export_quality_semantic_project_export_report_facade import MainExportQualitySemanticProjectExportReportFacade
from examples.main_export_quality_semantic_task_factory import build_main_export_quality_semantic_task_specs


def main():
    repo_root = Path(__file__).resolve().parents[1]
    facade = MainExportQualitySemanticProjectExportReportFacade(repo_root)
    result = facade.export(
        task_specs=build_main_export_quality_semantic_task_specs(),
        output_root=repo_root / "generated_output_main_export_quality_semantic_project",
        project_name="GeneratedAndroidProjectQualitySemantic",
        report_output_dir=repo_root / "generated_output_main_export_quality_semantic_reports",
    )
    print(result)


if __name__ == "__main__":
    main()
