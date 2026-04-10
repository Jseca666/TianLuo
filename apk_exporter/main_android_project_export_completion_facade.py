from pathlib import Path
from typing import Iterable

from .main_android_project_export_facade import MainAndroidProjectExportFacade
from .main_android_project_export_result import MainAndroidProjectExportResult


class MainAndroidProjectExportCompletionFacade:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.facade = MainAndroidProjectExportFacade(repo_root)

    def export(self, task_specs: Iterable[dict], output_root: Path, project_name: str = "GeneratedAndroidProject", report_output_dir: Path | None = None):
        result = self.facade.export(
            task_specs=task_specs,
            output_root=output_root,
            project_name=project_name,
            report_output_dir=report_output_dir,
        )
        return MainAndroidProjectExportResult(
            summary=result.get("summary"),
            deep_validation=result.get("deep_validation"),
            readiness=result.get("readiness"),
            package_report_path=result.get("package_report_path", ""),
            default_report_path=result.get("default_report_path", ""),
            main_report_path=result.get("main_report_path", ""),
            metadata={
                "repo_root": str(self.repo_root),
                "output_root": str(output_root),
                "project_name": project_name,
            },
        )
