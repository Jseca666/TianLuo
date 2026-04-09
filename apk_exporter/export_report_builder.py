from pathlib import Path

from .asset_manifest_builder import AssetManifestBuilder
from .export_plan_builder import ExportPlanBuilder
from .export_summary import ExportSummary


class ExportReportBuilder:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)

    def build(self) -> dict:
        manifest = AssetManifestBuilder(self.repo_root).build()
        plan = ExportPlanBuilder(self.repo_root).build()
        summary = ExportSummary.build(manifest, plan)
        return {
            "manifest": manifest,
            "plan": plan,
            "summary": summary,
        }
