from pathlib import Path

from .runtime_behavior_comparison_workflow import RuntimeBehaviorComparisonWorkflow
from .runtime_behavior_gap_backlog_builder import RuntimeBehaviorGapBacklogBuilder


class RuntimeBehaviorGapBacklogWorkflow:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.comparison_workflow = RuntimeBehaviorComparisonWorkflow(repo_root)
        self.backlog_builder = RuntimeBehaviorGapBacklogBuilder()

    def build(self, task_specs: list[dict], output_root: Path) -> dict:
        comparison_result = self.comparison_workflow.compare(task_specs=task_specs, output_root=output_root)
        backlog = self.backlog_builder.build(comparison_result)
        return {
            "comparison_result": comparison_result,
            "backlog": backlog,
        }
