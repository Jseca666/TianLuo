from pathlib import Path

from apk_exporter.semantic_quality_dashboard_runner import SemanticQualityDashboardRunner
from examples.main_export_quality_semantic_task_factory import build_main_export_quality_semantic_task_specs


def main():
    repo_root = Path(__file__).resolve().parents[1]
    task_specs = build_main_export_quality_semantic_task_specs()
    runner = SemanticQualityDashboardRunner(repo_root)
    result = runner.run(
        task_specs=task_specs,
        output_root=repo_root / "generated_output_semantic_quality_dashboard",
        report_output_dir=repo_root / "generated_output_semantic_quality_dashboard_reports",
    )
    print(result)


if __name__ == "__main__":
    main()
