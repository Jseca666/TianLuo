from pathlib import Path

from .asset_layout import AssetLayout
from .export_manifest import ExportManifest
from .export_manifest_serializer import ExportManifestSerializer


class ExportManifestWriter:
    def write(self, manifest: ExportManifest, target_root: Path) -> str:
        target_root = Path(target_root)
        manifest_path = target_root / AssetLayout.EXPORT_MANIFEST
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(
            ExportManifestSerializer.to_json(manifest),
            encoding='utf-8',
        )
        return str(manifest_path)
