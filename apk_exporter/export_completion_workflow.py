from pathlib import Path

from .export_acceptance_workflow import ExportAcceptanceWorkflow
from .export_completion_result import ExportCompletionResult


class ExportCompletionWorkflow:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)

    def run(self, preview_output_dir: Path, target_root: Path, report_output_dir: Path | None = None) -> ExportCompletionResult:
        result = ExportAcceptanceWorkflow(self.repo_root).run(
            preview_output_dir=preview_output_dir,
            target_root=target_root,
            report_output_dir=report_output_dir,
        )
        return ExportCompletionResult(
            acceptance=result["report"],
            report_path=result["report_path"],
            metadata={
                "repo_root": str(self.repo_root),
                "preview_output_dir": str(preview_output_dir),
                "target_root": str(target_root),
            },
        )
