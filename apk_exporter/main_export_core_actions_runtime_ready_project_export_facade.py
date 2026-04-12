from pathlib import Path
from typing import Iterable

from .delivery_ready_project_with_assets_deep_validator import DeliveryReadyProjectWithAssetsDeepValidator
from .main_export_core_actions_runtime_ready_project_export_workflow import MainExportCoreActionsRuntimeReadyProjectExportWorkflow
from .main_export_quality_project_export_summary import MainExportQualityProjectExportSummary


class MainExportCoreActionsRuntimeReadyProjectExportFacade:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.workflow = MainExportCoreActionsRuntimeReadyProjectExportWorkflow(repo_root)

    def export(self, task_specs: Iterable[dict], output_root: Path, project_name: str = "GeneratedAndroidProject") -> dict:
        result = self.workflow.export(
            task_specs=task_specs,
            output_root=output_root,
            project_name=project_name,
        )
        deep_validation = DeliveryReadyProjectWithAssetsDeepValidator().validate(result)
        write_result = result.write_result
        summary = MainExportQualityProjectExportSummary(
            project_root=result.project_root,
            assets_root=result.metadata.get("assets_root", ""),
            task_count=len(write_result.task_files),
            task_ids=list(write_result.task_files.keys()),
            asset_file_count=len(result.assets.get("copied_files", [])),
            todo_count=getattr(result.readiness, "todo_count", 0),
            unsupported_count=getattr(result.readiness, "unsupported_count", 0),
            files={**write_result.task_files, "registry": write_result.registry_file, "asset_manifest": result.assets.get("manifest_path", "")},
        )
        return {
            "result": result,
            "summary": summary,
            "deep_validation": deep_validation,
        }
