from .asset_export_plan import AssetExportPlan
from .export_manifest import ExportManifest


class ExportSummary:
    @staticmethod
    def build(manifest: ExportManifest, plan: AssetExportPlan) -> dict:
        return {
            'locator_count': len(manifest.locator_files),
            'template_count': len(manifest.template_files),
            'mask_count': len(manifest.mask_files),
            'copy_item_count': len(plan.items),
        }
