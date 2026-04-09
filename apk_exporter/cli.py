from pathlib import Path

from .asset_manifest_builder import AssetManifestBuilder
from .export_manifest_serializer import ExportManifestSerializer
from .export_plan_builder import ExportPlanBuilder
from .export_plan_serializer import ExportPlanSerializer


def preview_export(repo_root: str) -> dict:
    root = Path(repo_root)
    manifest = AssetManifestBuilder(root).build()
    plan = ExportPlanBuilder(root).build()
    return {
        "manifest": ExportManifestSerializer.to_dict(manifest),
        "plan": ExportPlanSerializer.to_dict(plan),
    }
