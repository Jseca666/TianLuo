from pathlib import Path
import json

from .runtime_behavior_decision_builder_v2 import RuntimeBehaviorDecisionBuilderV2
from .runtime_behavior_work_item_plan_runner_v2 import RuntimeBehaviorWorkItemPlanRunnerV2


class RuntimeBehaviorDecisionRunnerV2:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.plan_runner = RuntimeBehaviorWorkItemPlanRunnerV2(repo_root)
        self.decision_builder = RuntimeBehaviorDecisionBuilderV2()

    def run(self, task_specs: list[dict], output_root: Path, report_output_dir: Path | None = None) -> dict:
        output_root = Path(output_root)
        plan_result = self.plan_runner.run(
            task_specs=task_specs,
            output_root=output_root,
            report_output_dir=report_output_dir,
        )
        decision = self.decision_builder.build(plan_result)
        report_dir = Path(report_output_dir or output_root)
        report_dir.mkdir(parents=True, exist_ok=True)
        report_path = report_dir / "runtime_behavior_decision.json"
        report_path.write_text(
            json.dumps({"plan_result": plan_result, "decision": decision}, ensure_ascii=False, indent=2, default=str),
            encoding="utf-8",
        )
        return {
            "plan_result": plan_result,
            "decision": decision,
            "decision_report_path": str(report_path),
        }
