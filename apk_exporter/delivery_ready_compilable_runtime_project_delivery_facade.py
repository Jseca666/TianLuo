from pathlib import Path
from typing import Iterable

from .android_studio_project_summary import AndroidStudioProjectSummary
from .improved_compilable_runtime_project_completion_writer import ImprovedCompilableRuntimeProjectCompletionWriter
from .improved_compilable_runtime_project_readiness_analyzer import ImprovedCompilableRuntimeProjectReadinessAnalyzer
from .improved_compilable_runtime_project_validator import ImprovedCompilableRuntimeProjectValidator
from .runtime_template_copier import RuntimeTemplateCopier
from .android_studio_project_writer import AndroidStudioProjectWriter
from task_exporters.delivery_ready_compilable_runtime_task_export_session import DeliveryReadyCompilableRuntimeTaskExportSession
from task_exporters.delivery_ready_runtime_exportable_api_task_builder import DeliveryReadyRuntimeExportableApiTaskBuilder


class DeliveryReadyCompilableRuntimeProjectDeliveryFacade:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.task_builder = DeliveryReadyRuntimeExportableApiTaskBuilder()

    def export(self, task_specs: Iterable[dict], output_root: Path, project_name: str = "GeneratedAndroidProject", report_output_dir: Path | None = None) -> dict:
        tasks = []
        for spec in task_specs:
            tasks.append(
                self.task_builder.build(
                    task_id=str(spec.get("task_id", "generated_task")),
                    display_name=str(spec.get("display_name", "Generated Task")),
                    api_calls=spec.get("api_calls", []),
                )
            )

        output_root = Path(output_root)
        project_root = RuntimeTemplateCopier(self.repo_root).copy(output_root, project_name)
        export_result = DeliveryReadyCompilableRuntimeTaskExportSession(self.repo_root).run(tasks)
        write_result = AndroidStudioProjectWriter().write(export_result, Path(project_root))

        class _ExportResult:
            def __init__(self, project_root, write_result):
                self.project_root = project_root
                self.write_result = write_result

        export_wrapper = _ExportResult(str(project_root), write_result)
        validation = ImprovedCompilableRuntimeProjectValidator().validate(export_wrapper)
        readiness = ImprovedCompilableRuntimeProjectReadinessAnalyzer().analyze(export_wrapper)

        class _Completion:
            def __init__(self, export_result, validation, metadata):
                self.export_result = export_result
                self.validation = validation
                self.metadata = metadata

        completion = _Completion(
            export_wrapper,
            validation,
            {
                "repo_root": str(self.repo_root),
                "output_root": str(output_root),
                "project_name": project_name,
            },
        )

        report_path = ImprovedCompilableRuntimeProjectCompletionWriter().write(
            completion,
            Path(report_output_dir or output_root),
        )

        summary = AndroidStudioProjectSummary(
            project_root=str(project_root),
            task_count=len(write_result.task_files),
            task_ids=list(write_result.task_files.keys()),
            files={**write_result.task_files, "registry": write_result.registry_file, "completion_report": report_path},
        )

        return {
            "export_result": export_wrapper,
            "validation": validation,
            "readiness": readiness,
            "summary": summary,
            "report_path": report_path,
        }
