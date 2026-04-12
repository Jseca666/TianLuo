from pathlib import Path

from .semantic_quality_stage_status_runner import SemanticQualityStageStatusRunner
from .semantic_quality_work_item_plan_builder import SemanticQualityWorkItemPlanBuilder
from .semantic_quality_work_item_plan_writer import SemanticQualityWorkItemPlanWriter


class SemanticQualityWorkItemPlanRunner:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.stage_status_runner = SemanticQualityStageStatusRunner(repo_root)
        self.plan_builder = SemanticQualityWorkItemPlanBuilder()
        self.plan_writer = SemanticQualityWorkItemPlanWriter()

    def run(self, task_specs: list[dict], output_root: Path, report_output_dir: Path | None = None) -> dict:
        output_root = Path(output_root)
        stage_status_result = self.stage_status_runner.run(
            task_specs=task_specs,
            output_root=output_root,
            report_output_dir=report_output_dir,
        )
        plan = self.plan_builder.build(stage_status_result)
        report_path = self.plan_writer.write(
            {"stage_status_result": stage_status_result, "plan": plan},
            Path(report_output_dir or output_root),
        )
        return {
            "stage_status_result": stage_status_result,
            "plan": plan,
            "plan_report_path": report_path,
        }
