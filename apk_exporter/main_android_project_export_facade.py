from pathlib import Path
from typing import Iterable

from .default_android_project_export_delivery_facade import DefaultAndroidProjectExportDeliveryFacade
from .main_android_project_export_writer import MainAndroidProjectExportWriter


class MainAndroidProjectExportFacade:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.facade = DefaultAndroidProjectExportDeliveryFacade(repo_root)

    def export(self, task_specs: Iterable[dict], output_root: Path, project_name: str = "GeneratedAndroidProject", report_output_dir: Path | None = None) -> dict:
        result = self.facade.export(
            task_specs=task_specs,
            output_root=output_root,
            project_name=project_name,
            report_output_dir=report_output_dir,
        )
        main_report_path = MainAndroidProjectExportWriter().write(
            result,
            Path(report_output_dir or output_root),
        )
        result["main_report_path"] = main_report_path
        return result
