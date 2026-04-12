from pathlib import Path
from typing import Iterable

from .main_export_quality_project_export_writer import MainExportQualityProjectExportWriter
from .main_export_quality_runtime_behavior_project_export_facade import MainExportQualityRuntimeBehaviorProjectExportFacade


class MainExportQualityRuntimeBehaviorProjectExportReportFacade:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.facade = MainExportQualityRuntimeBehaviorProjectExportFacade(repo_root)

    def export(self, task_specs: Iterable[dict], output_root: Path, project_name: str = "GeneratedAndroidProject", report_output_dir: Path | None = None) -> dict:
        result = self.facade.export(
            task_specs=task_specs,
            output_root=output_root,
            project_name=project_name,
        )
        quality_report_path = MainExportQualityProjectExportWriter().write(
            result,
            Path(report_output_dir or output_root),
        )
        result["quality_report_path"] = quality_report_path
        return result
