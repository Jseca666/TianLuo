from pathlib import Path
from typing import Iterable

from .android_assets_target_layout import AndroidAssetsTargetLayout
from .android_studio_project_writer import AndroidStudioProjectWriter
from .export_executor import ExportExecutor
from .runtime_template_copier import RuntimeTemplateCopier
from .main_export_quality_project_export_result import MainExportQualityProjectExportResult
from .improved_compilable_runtime_project_readiness_analyzer import ImprovedCompilableRuntimeProjectReadinessAnalyzer
from task_exporters.main_export_quality_semantic_task_builder import MainExportQualitySemanticTaskBuilder
from task_exporters.main_export_quality_semantic_task_export_session import MainExportQualitySemanticTaskExportSession


class MainExportQualitySemanticProjectExportWorkflow:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.task_builder = MainExportQualitySemanticTaskBuilder()

    def export(self, task_specs: Iterable[dict], output_root: Path, project_name: str = "GeneratedAndroidProject") -> MainExportQualityProjectExportResult:
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
        export_result = MainExportQualitySemanticTaskExportSession(self.repo_root).run(tasks)
        write_result = AndroidStudioProjectWriter().write(export_result, Path(project_root))

        class _ExportResult:
            def __init__(self, project_root: str, write_result):
                self.project_root = project_root
                self.write_result = write_result

        export_wrapper = _ExportResult(str(project_root), write_result)
        readiness = ImprovedCompilableRuntimeProjectReadinessAnalyzer().analyze(export_wrapper)
        assets_root = Path(project_root) / AndroidAssetsTargetLayout.ASSETS_ROOT
        assets = ExportExecutor(self.repo_root).execute(assets_root)

        return MainExportQualityProjectExportResult(
            project_root=str(project_root),
            write_result=write_result,
            readiness=readiness,
            assets=assets,
            metadata={
                "repo_root": str(self.repo_root),
                "project_root": str(project_root),
                "assets_root": str(assets_root),
                "project_name": project_name,
                "quality_line": "semantic_parameter_aware",
            },
        )
