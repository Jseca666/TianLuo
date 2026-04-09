from pathlib import Path

from .export_preview_writer import ExportPreviewWriter
from .export_report_writer import ExportReportWriter
from .export_summary import ExportSummary
from .asset_manifest_builder import AssetManifestBuilder
from .export_plan_builder import ExportPlanBuilder


class ExportPreviewFacade:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)

    def build(self, output_dir: Path) -> dict:
        output_dir = Path(output_dir)
        manifest = AssetManifestBuilder(self.repo_root).build()
        plan = ExportPlanBuilder(self.repo_root).build()
        summary = ExportSummary.build(manifest, plan)
        preview_paths = ExportPreviewWriter(self.repo_root).write(output_dir)
        report_path = ExportReportWriter(self.repo_root).write(output_dir)
        return {
            'summary': summary,
            'preview_paths': preview_paths,
            'report_path': report_path,
        }
