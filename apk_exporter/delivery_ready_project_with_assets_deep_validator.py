from pathlib import Path

from .delivery_ready_project_with_assets_deep_validation import DeliveryReadyProjectWithAssetsDeepValidation


class DeliveryReadyProjectWithAssetsDeepValidator:
    def validate(self, result) -> DeliveryReadyProjectWithAssetsDeepValidation:
        missing_paths = []
        warnings = []

        metadata = getattr(result, "metadata", {}) or {}
        assets_root = Path(metadata.get("assets_root", ""))
        project_root = Path(metadata.get("project_root", ""))

        expected_paths = [
            project_root,
            assets_root,
            assets_root / "automation/export_manifest.json",
            assets_root / "automation/locators",
            assets_root / "automation/templates",
            assets_root / "automation/masks.json",
        ]
        for path in expected_paths:
            if not path.exists():
                missing_paths.append(str(path))

        assets = getattr(result, "assets", {}) or {}
        copied_files = assets.get("copied_files", [])
        if len(copied_files) < 2:
            warnings.append("Copied asset files look too few for a realistic package")

        delivery = getattr(result, "delivery", {}) or {}
        summary = delivery.get("summary")
        if summary is not None and getattr(summary, "task_count", 0) == 0:
            warnings.append("No generated tasks found in delivery summary")

        return DeliveryReadyProjectWithAssetsDeepValidation(
            is_valid=len(missing_paths) == 0,
            missing_paths=missing_paths,
            warnings=warnings,
        )
