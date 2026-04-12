from pathlib import Path

from apk_exporter.runtime_behavior_dashboard_runner_v2 import RuntimeBehaviorDashboardRunnerV2
from examples.main_export_quality_semantic_task_factory import build_main_export_quality_semantic_task_specs


def main():
    repo_root = Path(__file__).resolve().parents[1]
    task_specs = build_main_export_quality_semantic_task_specs()
    runner = RuntimeBehaviorDashboardRunnerV2(repo_root)
    result = runner.run(
        task_specs=task_specs,
        output_root=repo_root / "generated_output_runtime_behavior_dashboard",
        report_output_dir=repo_root / "generated_output_runtime_behavior_dashboard_reports",
    )
    print(result)


if __name__ == "__main__":
    main()
