from pathlib import Path

from .export_executor import ExportExecutor
from .export_preview_facade import ExportPreviewFacade


class ExportWorkflow:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)

    def preview(self, output_dir: Path) -> dict:
        return ExportPreviewFacade(self.repo_root).build(output_dir)

    def execute(self, target_root: Path) -> dict:
        return ExportExecutor(self.repo_root).execute(target_root)
