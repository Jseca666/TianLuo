from pathlib import Path

from apk_exporter.semantic_gap_backlog_workflow import SemanticGapBacklogWorkflow
from apk_exporter.semantic_gap_backlog_writer import SemanticGapBacklogWriter
from examples.main_export_quality_semantic_task_factory import build_main_export_quality_semantic_task_specs


def main():
    repo_root = Path(__file__).resolve().parents[1]
    task_specs = build_main_export_quality_semantic_task_specs()
    workflow = SemanticGapBacklogWorkflow(repo_root)
    result = workflow.build(
        task_specs=task_specs,
        output_root=repo_root / "generated_output_semantic_gap_backlog",
    )
    report_path = SemanticGapBacklogWriter().write(
        result,
        repo_root / "generated_output_semantic_gap_backlog_reports",
    )
    print({"result": result, "backlog_report_path": report_path})


if __name__ == "__main__":
    main()
