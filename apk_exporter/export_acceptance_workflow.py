from pathlib import Path

from .export_acceptance_runner import ExportAcceptanceRunner
from .export_acceptance_writer import ExportAcceptanceWriter


class ExportAcceptanceWorkflow:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)

    def run(self, preview_output_dir: Path, target_root: Path, report_output_dir: Path | None = None) -> dict:
        report_output_dir = Path(report_output_dir or preview_output_dir)
        report = ExportAcceptanceRunner(self.repo_root).run(preview_output_dir, target_root)
        report_path = ExportAcceptanceWriter().write(report, report_output_dir)
        return {
            "report": report,
            "report_path": report_path,
        }
