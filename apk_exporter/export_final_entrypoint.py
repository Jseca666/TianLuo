from pathlib import Path

from .export_completion_workflow import ExportCompletionWorkflow


class ExportFinalEntrypoint:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)

    def run(self, preview_output_dir: Path, target_root: Path, report_output_dir: Path | None = None):
        return ExportCompletionWorkflow(self.repo_root).run(
            preview_output_dir=preview_output_dir,
            target_root=target_root,
            report_output_dir=report_output_dir,
        )
