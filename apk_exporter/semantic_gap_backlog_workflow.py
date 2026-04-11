from pathlib import Path

from .semantic_gap_backlog_builder import SemanticGapBacklogBuilder
from .semantic_parameter_comparison_workflow import SemanticParameterComparisonWorkflow


class SemanticGapBacklogWorkflow:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.comparison_workflow = SemanticParameterComparisonWorkflow(repo_root)
        self.backlog_builder = SemanticGapBacklogBuilder()

    def build(self, task_specs: list[dict], output_root: Path) -> dict:
        comparison_result = self.comparison_workflow.compare(task_specs=task_specs, output_root=output_root)
        backlog = self.backlog_builder.build(comparison_result)
        return {
            "comparison_result": comparison_result,
            "backlog": backlog,
        }
