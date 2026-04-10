from pathlib import Path
from typing import Iterable

from .android_assets_target_layout import AndroidAssetsTargetLayout
from .delivery_ready_compilable_runtime_project_delivery_report_facade import DeliveryReadyCompilableRuntimeProjectDeliveryReportFacade
from .delivery_ready_project_with_assets_result import DeliveryReadyProjectWithAssetsResult
from .export_executor import ExportExecutor


class DeliveryReadyProjectWithAssetsWorkflow:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.delivery_facade = DeliveryReadyCompilableRuntimeProjectDeliveryReportFacade(repo_root)

    def export(self, task_specs: Iterable[dict], output_root: Path, project_name: str = "GeneratedAndroidProject", report_output_dir: Path | None = None) -> DeliveryReadyProjectWithAssetsResult:
        delivery = self.delivery_facade.export(
            task_specs=task_specs,
            output_root=output_root,
            project_name=project_name,
            report_output_dir=report_output_dir,
        )
        export_result = delivery.get("export_result")
        project_root = Path(getattr(export_result, "project_root", ""))
        assets_root = project_root / AndroidAssetsTargetLayout.ASSETS_ROOT
        assets = ExportExecutor(self.repo_root).execute(assets_root)
        return DeliveryReadyProjectWithAssetsResult(
            delivery=delivery,
            assets=assets,
            metadata={
                "repo_root": str(self.repo_root),
                "project_root": str(project_root),
                "assets_root": str(assets_root),
                "project_name": project_name,
            },
        )
