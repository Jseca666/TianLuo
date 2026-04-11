from pathlib import Path
from typing import Iterable

from .main_android_project_export_facade import MainAndroidProjectExportFacade
from .main_export_quality_project_export_report_facade import MainExportQualityProjectExportReportFacade
from .main_export_vs_quality_comparison_summary import MainExportVsQualityComparisonSummary
from .main_export_vs_quality_comparison_writer import MainExportVsQualityComparisonWriter


class MainExportVsQualityComparisonFacade:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.main_facade = MainAndroidProjectExportFacade(repo_root)
        self.quality_facade = MainExportQualityProjectExportReportFacade(repo_root)

    def export(self, task_specs: Iterable[dict], output_root: Path, project_name: str = "GeneratedAndroidProject", report_output_dir: Path | None = None) -> dict:
        output_root = Path(output_root)
        main_result = self.main_facade.export(
            task_specs=task_specs,
            output_root=output_root / "main_export",
            project_name=project_name + "Main",
            report_output_dir=Path(report_output_dir or output_root) / "main_export_reports",
        )
        quality_result = self.quality_facade.export(
            task_specs=task_specs,
            output_root=output_root / "quality_export",
            project_name=project_name + "Quality",
            report_output_dir=Path(report_output_dir or output_root) / "quality_export_reports",
        )

        main_summary = main_result.get("summary")
        quality_summary = quality_result.get("summary")
        main_validation = main_result.get("deep_validation")
        quality_validation = quality_result.get("deep_validation")

        summary = MainExportVsQualityComparisonSummary(
            project_roots={
                "main": getattr(main_summary, "project_root", "") if main_summary else "",
                "quality": getattr(quality_summary, "project_root", "") if quality_summary else "",
            },
            task_counts={
                "main": getattr(main_summary, "task_count", 0) if main_summary else 0,
                "quality": getattr(quality_summary, "task_count", 0) if quality_summary else 0,
            },
            asset_file_counts={
                "main": getattr(main_summary, "asset_file_count", 0) if main_summary else 0,
                "quality": getattr(quality_summary, "asset_file_count", 0) if quality_summary else 0,
            },
            todo_counts={
                "main": getattr(main_summary, "todo_count", 0) if main_summary else 0,
                "quality": getattr(quality_summary, "todo_count", 0) if quality_summary else 0,
            },
            unsupported_counts={
                "main": getattr(main_summary, "unsupported_count", 0) if main_summary else 0,
                "quality": getattr(quality_summary, "unsupported_count", 0) if quality_summary else 0,
            },
            validation_ok={
                "main": getattr(main_validation, "is_valid", False),
                "quality": getattr(quality_validation, "is_valid", False),
            },
            report_paths={
                "main_package": main_result.get("package_report_path", ""),
                "main_default": main_result.get("default_report_path", ""),
                "main_main": main_result.get("main_report_path", ""),
                "quality": quality_result.get("quality_report_path", ""),
            },
            task_ids=list(getattr(main_summary, "task_ids", []) if main_summary else []),
        )
        comparison_report_path = MainExportVsQualityComparisonWriter().write(
            summary,
            Path(report_output_dir or output_root),
        )
        return {
            "main_result": main_result,
            "quality_result": quality_result,
            "summary": summary,
            "comparison_report_path": comparison_report_path,
        }
