from pathlib import Path

from .asset_export_plan import AssetExportPlan
from .export_validation import ExportValidationResult


class ExportValidator:
    def validate(self, plan: AssetExportPlan) -> ExportValidationResult:
        missing_sources = []
        warnings = []

        for item in plan.items:
            source = Path(item.source_path)
            if not source.exists():
                missing_sources.append(str(source))

        if not plan.items:
            warnings.append("Export plan is empty")

        return ExportValidationResult(
            is_valid=len(missing_sources) == 0,
            missing_sources=missing_sources,
            warnings=warnings,
        )
