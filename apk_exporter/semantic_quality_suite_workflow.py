from pathlib import Path

from .semantic_parameter_comparison_workflow import SemanticParameterComparisonWorkflow
from .semantic_gap_backlog_workflow import SemanticGapBacklogWorkflow
from .runtime_semantic_comparison_workflow import RuntimeSemanticComparisonWorkflow
from .runtime_semantic_gap_backlog_workflow import RuntimeSemanticGapBacklogWorkflow


class SemanticQualitySuiteWorkflow:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.semantic_parameter_comparison = SemanticParameterComparisonWorkflow(repo_root)
        self.semantic_gap_backlog = SemanticGapBacklogWorkflow(repo_root)
        self.runtime_semantic_comparison = RuntimeSemanticComparisonWorkflow(repo_root)
        self.runtime_semantic_gap_backlog = RuntimeSemanticGapBacklogWorkflow(repo_root)

    def run(self, task_specs: list[dict], output_root: Path) -> dict:
        output_root = Path(output_root)
        parameter_comparison = self.semantic_parameter_comparison.compare(
            task_specs=task_specs,
            output_root=output_root / "parameter_comparison",
        )
        semantic_gap = self.semantic_gap_backlog.build(
            task_specs=task_specs,
            output_root=output_root / "semantic_gap_backlog",
        )
        runtime_comparison = self.runtime_semantic_comparison.compare(
            task_specs=task_specs,
            output_root=output_root / "runtime_semantic_comparison",
        )
        runtime_gap = self.runtime_semantic_gap_backlog.build(
            task_specs=task_specs,
            output_root=output_root / "runtime_semantic_gap_backlog",
        )

        notes = []
        notes.extend(parameter_comparison.get("notes", []))
        notes.extend(runtime_comparison.get("notes", []))

        semantic_backlog = semantic_gap.get("backlog")
        runtime_backlog = runtime_gap.get("backlog")
        if semantic_backlog is not None and runtime_backlog is not None:
            if getattr(runtime_backlog, "total_unresolved_gap_count", 0) <= getattr(semantic_backlog, "total_unresolved_gap_count", 0):
                notes.append("Runtime-semantic backlog is no worse than semantic backlog on current benchmark scope")
            if getattr(runtime_backlog, "total_unresolved_gap_count", 0) < getattr(semantic_backlog, "total_unresolved_gap_count", 0):
                notes.append("Runtime-semantic backlog reduces unresolved gap count compared with semantic backlog")

        return {
            "parameter_comparison": parameter_comparison,
            "semantic_gap_backlog": semantic_gap,
            "runtime_semantic_comparison": runtime_comparison,
            "runtime_semantic_gap_backlog": runtime_gap,
            "notes": notes,
        }
