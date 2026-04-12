from pathlib import Path

from .semantic_quality_decision_runner import SemanticQualityDecisionRunner
from .semantic_quality_release_gate_builder import SemanticQualityReleaseGateBuilder
from .semantic_quality_release_gate_writer import SemanticQualityReleaseGateWriter


class SemanticQualityReleaseGateRunner:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.decision_runner = SemanticQualityDecisionRunner(repo_root)
        self.gate_builder = SemanticQualityReleaseGateBuilder()
        self.gate_writer = SemanticQualityReleaseGateWriter()

    def run(self, task_specs: list[dict], output_root: Path, report_output_dir: Path | None = None) -> dict:
        output_root = Path(output_root)
        decision_result = self.decision_runner.run(
            task_specs=task_specs,
            output_root=output_root,
            report_output_dir=report_output_dir,
        )
        release_gate = self.gate_builder.build(decision_result)
        report_path = self.gate_writer.write(
            {"decision_result": decision_result, "release_gate": release_gate},
            Path(report_output_dir or output_root),
        )
        return {
            "decision_result": decision_result,
            "release_gate": release_gate,
            "release_gate_report_path": report_path,
        }
