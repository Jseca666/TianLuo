from pathlib import Path

from .asset_collector import AssetCollector
from .asset_layout import AssetLayout


def export_assets(repo_root: str, locator_files: list[str]):
    collector = AssetCollector(Path(repo_root))
    manifest = collector.collect(locator_files)
    return {
        "root": AssetLayout.ROOT,
        "locators": manifest.locator_files,
        "templates": manifest.template_files,
        "masks": manifest.mask_files,
    }
