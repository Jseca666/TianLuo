from pathlib import Path

from .semantic_quality_decision_builder import SemanticQualityDecisionBuilder
from .semantic_quality_decision_writer import SemanticQualityDecisionWriter
from .semantic_quality_work_item_plan_runner import SemanticQualityWorkItemPlanRunner


class SemanticQualityDecisionRunner:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.plan_runner = SemanticQualityWorkItemPlanRunner(repo_root)
        self.decision_builder = SemanticQualityDecisionBuilder()
        self.decision_writer = SemanticQualityDecisionWriter()

    def run(self, task_specs: list[dict], output_root: Path, report_output_dir: Path | None = None) -> dict:
        output_root = Path(output_root)
        plan_result = self.plan_runner.run(
            task_specs=task_specs,
            output_root=output_root,
            report_output_dir=report_output_dir,
        )
        decision = self.decision_builder.build(plan_result)
        report_path = self.decision_writer.write(
            {"plan_result": plan_result, "decision": decision},
            Path(report_output_dir or output_root),
        )
        return {
            "plan_result": plan_result,
            "decision": decision,
            "decision_report_path": report_path,
        }
