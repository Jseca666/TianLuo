from pathlib import Path

from .delivery_ready_project_with_assets_validation import DeliveryReadyProjectWithAssetsValidation


class DeliveryReadyProjectWithAssetsValidator:
    def validate(self, result) -> DeliveryReadyProjectWithAssetsValidation:
        missing_paths = []
        warnings = []

        metadata = getattr(result, "metadata", {})
        assets_root = Path(metadata.get("assets_root", ""))
        project_root = Path(metadata.get("project_root", ""))

        if not project_root.exists():
            missing_paths.append(str(project_root))

        if not assets_root.exists():
            missing_paths.append(str(assets_root))

        manifest_path = assets_root / "automation/export_manifest.json"
        locators_dir = assets_root / "automation/locators"
        if not manifest_path.exists():
            missing_paths.append(str(manifest_path))
        if not locators_dir.exists():
            missing_paths.append(str(locators_dir))

        assets = getattr(result, "assets", {}) or {}
        copied_files = assets.get("copied_files", [])
        if not copied_files:
            warnings.append("No copied asset files recorded")

        delivery = getattr(result, "delivery", {}) or {}
        delivery_report_path = delivery.get("delivery_report_path")
        if delivery_report_path and not Path(delivery_report_path).exists():
            missing_paths.append(str(delivery_report_path))

        return DeliveryReadyProjectWithAssetsValidation(
            is_valid=len(missing_paths) == 0,
            missing_paths=missing_paths,
            warnings=warnings,
        )
