from pathlib import Path
from typing import Iterable

from .default_android_project_export_summary import DefaultAndroidProjectExportSummary
from .default_android_project_export_writer import DefaultAndroidProjectExportWriter
from .delivery_ready_project_with_assets_deep_summary_facade import DeliveryReadyProjectWithAssetsDeepSummaryFacade


class DefaultAndroidProjectExportFacade:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.facade = DeliveryReadyProjectWithAssetsDeepSummaryFacade(repo_root)

    def export(self, task_specs: Iterable[dict], output_root: Path, project_name: str = "GeneratedAndroidProject", report_output_dir: Path | None = None) -> dict:
        result = self.facade.export(
            task_specs=task_specs,
            output_root=output_root,
            project_name=project_name,
            report_output_dir=report_output_dir,
        )
        summary = result.get("deep_summary")
        default_summary = DefaultAndroidProjectExportSummary(
            project_root=getattr(summary, "project_root", "") if summary else "",
            assets_root=getattr(summary, "assets_root", "") if summary else "",
            task_count=getattr(summary, "task_count", 0) if summary else 0,
            task_ids=getattr(summary, "task_ids", []) if summary else [],
            asset_file_count=getattr(summary, "asset_file_count", 0) if summary else 0,
            validation_ok=getattr(summary, "validation_ok", False) if summary else False,
            files=getattr(summary, "files", {}) if summary else {},
        )
        final_result = {
            "summary": default_summary,
            "deep_validation": result.get("deep_validation"),
            "package_report_path": result.get("package_report_path"),
        }
        default_report_path = DefaultAndroidProjectExportWriter().write(
            final_result,
            Path(report_output_dir or output_root),
        )
        final_result["default_report_path"] = default_report_path
        return final_result
