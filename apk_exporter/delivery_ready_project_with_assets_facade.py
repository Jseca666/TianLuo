from pathlib import Path
from typing import Iterable

from .delivery_ready_project_with_assets_workflow import DeliveryReadyProjectWithAssetsWorkflow
from .delivery_ready_project_with_assets_writer import DeliveryReadyProjectWithAssetsWriter


class DeliveryReadyProjectWithAssetsFacade:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.workflow = DeliveryReadyProjectWithAssetsWorkflow(repo_root)

    def export(self, task_specs: Iterable[dict], output_root: Path, project_name: str = "GeneratedAndroidProject", report_output_dir: Path | None = None) -> dict:
        result = self.workflow.export(
            task_specs=task_specs,
            output_root=output_root,
            project_name=project_name,
            report_output_dir=report_output_dir,
        )
        package_report_path = DeliveryReadyProjectWithAssetsWriter().write(
            result,
            Path(report_output_dir or output_root),
        )
        return {
            "result": result,
            "package_report_path": package_report_path,
        }
