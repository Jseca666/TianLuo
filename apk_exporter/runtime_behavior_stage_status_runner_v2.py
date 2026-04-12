from pathlib import Path

from .runtime_behavior_stage_status_builder_v2 import RuntimeBehaviorStageStatusBuilderV2
from .runtime_behavior_stage_status_writer_v2 import RuntimeBehaviorStageStatusWriterV2
from .runtime_behavior_suite_workflow import RuntimeBehaviorSuiteWorkflow


class RuntimeBehaviorStageStatusRunnerV2:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.suite_workflow = RuntimeBehaviorSuiteWorkflow(repo_root)
        self.status_builder = RuntimeBehaviorStageStatusBuilderV2()
        self.status_writer = RuntimeBehaviorStageStatusWriterV2()

    def run(self, task_specs: list[dict], output_root: Path, report_output_dir: Path | None = None) -> dict:
        output_root = Path(output_root)
        suite_result = self.suite_workflow.run(task_specs=task_specs, output_root=output_root)
        stage_status = self.status_builder.build(suite_result)
        report_path = self.status_writer.write(
            {"suite_result": suite_result, "stage_status": stage_status},
            Path(report_output_dir or output_root),
        )
        return {
            "suite_result": suite_result,
            "stage_status": stage_status,
            "stage_status_report_path": report_path,
        }
