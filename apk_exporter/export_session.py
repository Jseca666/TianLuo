from pathlib import Path

from .export_preview_facade import ExportPreviewFacade
from .export_session_result import ExportSessionResult
from .validated_export_executor import ValidatedExportExecutor


class ExportSession:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)

    def run(self, preview_output_dir: Path, target_root: Path) -> ExportSessionResult:
        preview = ExportPreviewFacade(self.repo_root).build(preview_output_dir)
        execution = ValidatedExportExecutor(self.repo_root).execute(target_root)
        return ExportSessionResult(
            preview=preview,
            execution=execution,
        )
