from pathlib import Path

from .asset_copy_executor import AssetCopyExecutor
from .asset_manifest_builder import AssetManifestBuilder
from .export_manifest_writer import ExportManifestWriter
from .export_plan_builder import ExportPlanBuilder
from .export_summary import ExportSummary


class ExportExecutor:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)

    def execute(self, target_root: Path) -> dict:
        target_root = Path(target_root)
        manifest = AssetManifestBuilder(self.repo_root).build()
        plan = ExportPlanBuilder(self.repo_root).build()
        copied_files = AssetCopyExecutor().execute(plan, target_root)
        manifest_path = ExportManifestWriter().write(manifest, target_root)
        summary = ExportSummary.build(manifest, plan)
        return {
            "manifest_path": manifest_path,
            "copied_files": copied_files,
            "summary": summary,
        }
