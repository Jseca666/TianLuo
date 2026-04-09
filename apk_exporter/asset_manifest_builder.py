from pathlib import Path

from .export_manifest import ExportManifest
from .locator_indexer import LocatorIndexer


class AssetManifestBuilder:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)

    def build(self) -> ExportManifest:
        manifest = ExportManifest()
        index = LocatorIndexer(self.repo_root).scan()
        manifest.locator_files.extend(index.files)

        template_paths = []
        for record in index.records:
            if record.image_path not in template_paths:
                template_paths.append(record.image_path)
        manifest.template_files.extend(template_paths)

        masks_file = self.repo_root / 'tool' / 'masks.json'
        if masks_file.exists():
            manifest.mask_files.append(str(masks_file))

        return manifest
