from pathlib import Path
import json

from .runtime_behavior_decision_runner_v2 import RuntimeBehaviorDecisionRunnerV2
from .runtime_behavior_release_gate_builder_v2 import RuntimeBehaviorReleaseGateBuilderV2


class RuntimeBehaviorReleaseGateRunnerV2:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.decision_runner = RuntimeBehaviorDecisionRunnerV2(repo_root)
        self.gate_builder = RuntimeBehaviorReleaseGateBuilderV2()

    def run(self, task_specs: list[dict], output_root: Path, report_output_dir: Path | None = None) -> dict:
        output_root = Path(output_root)
        decision_result = self.decision_runner.run(
            task_specs=task_specs,
            output_root=output_root,
            report_output_dir=report_output_dir,
        )
        release_gate = self.gate_builder.build(decision_result)
        report_dir = Path(report_output_dir or output_root)
        report_dir.mkdir(parents=True, exist_ok=True)
        report_path = report_dir / "runtime_behavior_release_gate.json"
        report_path.write_text(
            json.dumps({"decision_result": decision_result, "release_gate": release_gate}, ensure_ascii=False, indent=2, default=str),
            encoding="utf-8",
        )
        return {
            "decision_result": decision_result,
            "release_gate": release_gate,
            "release_gate_report_path": str(report_path),
        }
