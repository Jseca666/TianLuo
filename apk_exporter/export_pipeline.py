from pathlib import Path

from .export_preview_facade import ExportPreviewFacade


class ExportPipeline:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)

    def preview(self, output_dir: Path) -> dict:
        return ExportPreviewFacade(self.repo_root).build(output_dir)
