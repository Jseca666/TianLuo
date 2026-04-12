from pathlib import Path
import json

from .runtime_behavior_release_gate_runner_v2 import RuntimeBehaviorReleaseGateRunnerV2


class RuntimeBehaviorDashboardRunnerV2:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.release_gate_runner = RuntimeBehaviorReleaseGateRunnerV2(repo_root)

    def run(self, task_specs: list[dict], output_root: Path, report_output_dir: Path | None = None) -> dict:
        output_root = Path(output_root)
        release_gate_result = self.release_gate_runner.run(
            task_specs=task_specs,
            output_root=output_root,
            report_output_dir=report_output_dir,
        )
        report_dir = Path(report_output_dir or output_root)
        report_dir.mkdir(parents=True, exist_ok=True)
        report_path = report_dir / "runtime_behavior_dashboard.json"
        report_path.write_text(json.dumps(release_gate_result, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
        return {
            **release_gate_result,
            "dashboard_report_path": str(report_path),
        }
