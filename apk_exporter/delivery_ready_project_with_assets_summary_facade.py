from pathlib import Path
from typing import Iterable

from .delivery_ready_project_with_assets_facade import DeliveryReadyProjectWithAssetsFacade
from .delivery_ready_project_with_assets_summary import DeliveryReadyProjectWithAssetsSummary
from .delivery_ready_project_with_assets_validator import DeliveryReadyProjectWithAssetsValidator


class DeliveryReadyProjectWithAssetsSummaryFacade:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.facade = DeliveryReadyProjectWithAssetsFacade(repo_root)

    def export(self, task_specs: Iterable[dict], output_root: Path, project_name: str = "GeneratedAndroidProject", report_output_dir: Path | None = None) -> dict:
        facade_result = self.facade.export(
            task_specs=task_specs,
            output_root=output_root,
            project_name=project_name,
            report_output_dir=report_output_dir,
        )
        result = facade_result.get("result")
        validation = DeliveryReadyProjectWithAssetsValidator().validate(result)

        delivery = getattr(result, "delivery", {}) or {}
        delivery_summary = delivery.get("summary")
        metadata = getattr(result, "metadata", {}) or {}
        assets = getattr(result, "assets", {}) or {}

        summary = DeliveryReadyProjectWithAssetsSummary(
            project_root=metadata.get("project_root", ""),
            assets_root=metadata.get("assets_root", ""),
            task_count=getattr(delivery_summary, "task_count", 0) if delivery_summary else 0,
            task_ids=getattr(delivery_summary, "task_ids", []) if delivery_summary else [],
            asset_file_count=len(assets.get("copied_files", [])),
            validation_ok=validation.is_valid,
            files={
                **(getattr(delivery_summary, "files", {}) if delivery_summary else {}),
                "package_report": facade_result.get("package_report_path", ""),
                "asset_manifest": assets.get("manifest_path", ""),
            },
        )
        return {
            "result": result,
            "validation": validation,
            "summary": summary,
            "package_report_path": facade_result.get("package_report_path"),
        }
