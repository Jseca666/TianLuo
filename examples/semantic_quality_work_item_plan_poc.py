from pathlib import Path

from apk_exporter.semantic_quality_work_item_plan_runner import SemanticQualityWorkItemPlanRunner
from examples.main_export_quality_semantic_task_factory import build_main_export_quality_semantic_task_specs


def main():
    repo_root = Path(__file__).resolve().parents[1]
    task_specs = build_main_export_quality_semantic_task_specs()
    runner = SemanticQualityWorkItemPlanRunner(repo_root)
    result = runner.run(
        task_specs=task_specs,
        output_root=repo_root / "generated_output_semantic_quality_work_item_plan",
        report_output_dir=repo_root / "generated_output_semantic_quality_work_item_plan_reports",
    )
    print(result)


if __name__ == "__main__":
    main()
