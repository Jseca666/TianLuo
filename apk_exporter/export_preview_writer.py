from pathlib import Path

from .asset_manifest_builder import AssetManifestBuilder
from .export_manifest_serializer import ExportManifestSerializer
from .export_plan_builder import ExportPlanBuilder
from .export_plan_serializer import ExportPlanSerializer


class ExportPreviewWriter:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)

    def write(self, output_dir: Path) -> dict:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        manifest = AssetManifestBuilder(self.repo_root).build()
        plan = ExportPlanBuilder(self.repo_root).build()

        manifest_path = output_dir / 'export_manifest.preview.json'
        plan_path = output_dir / 'export_plan.preview.json'

        manifest_path.write_text(
            ExportManifestSerializer.to_json(manifest),
            encoding='utf-8',
        )
        plan_path.write_text(
            ExportPlanSerializer.to_json(plan),
            encoding='utf-8',
        )

        return {
            'manifest_path': str(manifest_path),
            'plan_path': str(plan_path),
        }
