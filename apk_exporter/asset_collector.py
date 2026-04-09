from pathlib import Path
from typing import Iterable, List

from .export_manifest import ExportManifest


class AssetCollector:
    """V3 资源收集器骨架。"""

    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)

    def collect(self, locator_files: Iterable[str]) -> ExportManifest:
        manifest = ExportManifest()
        manifest.locator_files.extend([str(x) for x in locator_files])
        return manifest
