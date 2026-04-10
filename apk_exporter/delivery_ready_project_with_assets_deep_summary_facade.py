from pathlib import Path
from typing import Iterable

from .delivery_ready_project_with_assets_deep_validator import DeliveryReadyProjectWithAssetsDeepValidator
from .delivery_ready_project_with_assets_summary import DeliveryReadyProjectWithAssetsSummary
from .delivery_ready_project_with_assets_summary_facade import DeliveryReadyProjectWithAssetsSummaryFacade


class DeliveryReadyProjectWithAssetsDeepSummaryFacade:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.facade = DeliveryReadyProjectWithAssetsSummaryFacade(repo_root)

    def export(self, task_specs: Iterable[dict], output_root: Path, project_name: str = "GeneratedAndroidProject", report_output_dir: Path | None = None) -> dict:
        result = self.facade.export(
            task_specs=task_specs,
            output_root=output_root,
            project_name=project_name,
            report_output_dir=report_output_dir,
        )
        package_result = result.get("result")
        deep_validation = DeliveryReadyProjectWithAssetsDeepValidator().validate(package_result)
        summary = result.get("summary")

        deep_summary = DeliveryReadyProjectWithAssetsSummary(
            project_root=getattr(summary, "project_root", "") if summary else "",
            assets_root=getattr(summary, "assets_root", "") if summary else "",
            task_count=getattr(summary, "task_count", 0) if summary else 0,
            task_ids=getattr(summary, "task_ids", []) if summary else [],
            asset_file_count=getattr(summary, "asset_file_count", 0) if summary else 0,
            validation_ok=deep_validation.is_valid,
            files=getattr(summary, "files", {}) if summary else {},
        )
        result["deep_validation"] = deep_validation
        result["deep_summary"] = deep_summary
        return result
