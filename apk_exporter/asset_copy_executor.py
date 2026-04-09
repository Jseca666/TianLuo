import shutil
from pathlib import Path

from .asset_export_plan import AssetExportPlan


class AssetCopyExecutor:
    def execute(self, plan: AssetExportPlan, target_root: Path) -> list[str]:
        target_root = Path(target_root)
        copied: list[str] = []

        for item in plan.items:
            source = Path(item.source_path)
            target = target_root / item.target_path
            target.parent.mkdir(parents=True, exist_ok=True)
            if source.exists():
                shutil.copy2(source, target)
                copied.append(str(target))
        return copied
