from pathlib import Path

from .asset_export_plan import AssetCopyItem, AssetExportPlan
from .asset_layout import AssetLayout
from .asset_manifest_builder import AssetManifestBuilder
from .mask_file_resolver import MaskFileResolver
from .path_normalizer import PathNormalizer


class ExportPlanBuilder:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)

    def build(self) -> AssetExportPlan:
        plan = AssetExportPlan()
        manifest = AssetManifestBuilder(self.repo_root).build()

        for locator_file in manifest.locator_files:
            source = Path(locator_file)
            target = f"{AssetLayout.LOCATORS_DIR}/{source.name}"
            plan.items.append(AssetCopyItem(source_path=str(source), target_path=target))

        for template_file in manifest.template_files:
            normalized = PathNormalizer.normalize_asset_path(template_file)
            source = self.repo_root / 'tool' / normalized
            target = f"{AssetLayout.TEMPLATES_DIR}/{normalized}"
            plan.items.append(AssetCopyItem(source_path=str(source), target_path=target))

        masks_file = MaskFileResolver(self.repo_root).resolve()
        if masks_file is not None:
            plan.items.append(
                AssetCopyItem(source_path=str(masks_file), target_path=AssetLayout.MASKS_FILE)
            )

        return plan
