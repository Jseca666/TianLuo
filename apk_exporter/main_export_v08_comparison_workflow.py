from pathlib import Path
from typing import Iterable

from .main_android_project_export_facade import MainAndroidProjectExportFacade
from .main_export_comparison_summary import MainExportComparisonSummary
from .main_export_quality_v08_project_export_report_facade import MainExportQualityV08ProjectExportReportFacade


class MainExportV08ComparisonWorkflow:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.main_facade = MainAndroidProjectExportFacade(repo_root)
        self.quality_v08_facade = MainExportQualityV08ProjectExportReportFacade(repo_root)

    def compare(self, task_specs: Iterable[dict], output_root: Path) -> dict:
        output_root = Path(output_root)
        baseline = self.main_facade.export(
            task_specs=task_specs,
            output_root=output_root / "baseline",
            project_name="GeneratedAndroidProjectBaseline",
            report_output_dir=output_root / "baseline_reports",
        )
        quality = self.quality_v08_facade.export(
            task_specs=task_specs,
            output_root=output_root / "quality_v08",
            project_name="GeneratedAndroidProjectQualityV08",
            report_output_dir=output_root / "quality_v08_reports",
        )

        baseline_summary = baseline.get("summary")
        quality_summary = quality.get("summary")
        baseline_validation = baseline.get("deep_validation")
        quality_validation = quality.get("deep_validation")

        summary = MainExportComparisonSummary(
            baseline_project_root=getattr(baseline_summary, "project_root", "") if baseline_summary else "",
            quality_project_root=getattr(quality_summary, "project_root", "") if quality_summary else "",
            baseline_todo_count=getattr(baseline_summary, "todo_count", 0) if baseline_summary else 0,
            quality_todo_count=getattr(quality_summary, "todo_count", 0) if quality_summary else 0,
            baseline_unsupported_count=getattr(baseline_summary, "unsupported_count", 0) if baseline_summary else 0,
            quality_unsupported_count=getattr(quality_summary, "unsupported_count", 0) if quality_summary else 0,
            baseline_asset_file_count=getattr(baseline_summary, "asset_file_count", 0) if baseline_summary else 0,
            quality_asset_file_count=getattr(quality_summary, "asset_file_count", 0) if quality_summary else 0,
            baseline_validation_ok=getattr(baseline_validation, "is_valid", False),
            quality_validation_ok=getattr(quality_validation, "is_valid", False),
            files={
                "baseline_default_report": baseline.get("default_report_path", ""),
                "baseline_main_report": baseline.get("main_report_path", ""),
                "quality_v08_report": quality.get("quality_report_path", ""),
            },
            notes=[],
        )
        if summary.quality_todo_count < summary.baseline_todo_count:
            summary.notes.append("Quality v0.8 export reduces TODO count")
        if summary.quality_unsupported_count < summary.baseline_unsupported_count:
            summary.notes.append("Quality v0.8 export reduces unsupported count")
        if summary.quality_asset_file_count == summary.baseline_asset_file_count:
            summary.notes.append("Quality v0.8 export keeps asset file count aligned with baseline")

        return {
            "baseline": baseline,
            "quality": quality,
            "summary": summary,
        }
