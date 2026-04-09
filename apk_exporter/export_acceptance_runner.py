from pathlib import Path

from .export_acceptance_report import ExportAcceptanceReport
from .export_session import ExportSession


class ExportAcceptanceRunner:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)

    def run(self, preview_output_dir: Path, target_root: Path) -> ExportAcceptanceReport:
        session = ExportSession(self.repo_root).run(preview_output_dir, target_root)
        execution = session.execution

        checks = {
            "has_preview": bool(session.preview),
            "has_execution": execution is not None,
            "has_manifest_path": bool(execution and execution.manifest_path),
            "validation_ok": bool(execution and execution.validation and execution.validation.is_valid),
            "has_copied_files": bool(execution and execution.copied_files),
        }

        notes = []
        if execution and execution.validation and execution.validation.missing_sources:
            notes.extend(execution.validation.missing_sources)
        if execution and execution.validation and execution.validation.warnings:
            notes.extend(execution.validation.warnings)

        return ExportAcceptanceReport(
            passed=all(checks.values()),
            checks=checks,
            notes=notes,
            preview=session.preview,
            execution=execution,
        )
