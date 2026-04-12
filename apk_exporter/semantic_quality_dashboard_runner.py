from pathlib import Path

from .semantic_quality_release_gate_runner import SemanticQualityReleaseGateRunner
from .semantic_quality_dashboard_writer import SemanticQualityDashboardWriter


class SemanticQualityDashboardRunner:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.release_gate_runner = SemanticQualityReleaseGateRunner(repo_root)
        self.dashboard_writer = SemanticQualityDashboardWriter()

    def run(self, task_specs: list[dict], output_root: Path, report_output_dir: Path | None = None) -> dict:
        output_root = Path(output_root)
        release_gate_result = self.release_gate_runner.run(
            task_specs=task_specs,
            output_root=output_root,
            report_output_dir=report_output_dir,
        )
        report_path = self.dashboard_writer.write(release_gate_result, Path(report_output_dir or output_root))
        return {
            **release_gate_result,
            "dashboard_report_path": report_path,
        }
