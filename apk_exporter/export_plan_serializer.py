import json
from dataclasses import asdict

from .asset_export_plan import AssetExportPlan


class ExportPlanSerializer:
    @staticmethod
    def to_dict(plan: AssetExportPlan) -> dict:
        return {
            "items": [asdict(item) for item in plan.items],
        }

    @staticmethod
    def to_json(plan: AssetExportPlan, ensure_ascii: bool = False, indent: int = 2) -> str:
        return json.dumps(
            ExportPlanSerializer.to_dict(plan),
            ensure_ascii=ensure_ascii,
            indent=indent,
        )
