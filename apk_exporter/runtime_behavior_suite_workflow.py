from pathlib import Path

from .runtime_behavior_comparison_workflow import RuntimeBehaviorComparisonWorkflow
from .runtime_behavior_gap_backlog_workflow import RuntimeBehaviorGapBacklogWorkflow


class RuntimeBehaviorSuiteWorkflow:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.comparison_workflow = RuntimeBehaviorComparisonWorkflow(repo_root)
        self.backlog_workflow = RuntimeBehaviorGapBacklogWorkflow(repo_root)

    def run(self, task_specs: list[dict], output_root: Path) -> dict:
        output_root = Path(output_root)
        comparison_result = self.comparison_workflow.compare(
            task_specs=task_specs,
            output_root=output_root / "comparison",
        )
        backlog_result = self.backlog_workflow.build(
            task_specs=task_specs,
            output_root=output_root / "backlog",
        )
        notes = []
        notes.extend(comparison_result.get("notes", []))
        backlog = backlog_result.get("backlog")
        if backlog is not None and getattr(backlog, "total_unresolved_gap_count", 0) == 0:
            notes.append("Runtime-behavior suite currently shows no unresolved tracked behavior observability gaps")
        else:
            notes.append("Runtime-behavior suite still shows unresolved tracked behavior observability gaps")
        return {
            "comparison": comparison_result,
            "backlog": backlog_result,
            "notes": notes,
        }
