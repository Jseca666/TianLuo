from pathlib import Path
from typing import Iterable

from .android_studio_project_export_result import AndroidStudioProjectExportResult
from .android_studio_project_writer import AndroidStudioProjectWriter
from .runtime_template_copier import RuntimeTemplateCopier
from task_exporters.compilable_runtime_task_export_session import CompilableRuntimeTaskExportSession
from task_exporters.export_models import ExportedTaskModel


class CompilableRuntimeAndroidStudioProjectExportWorkflow:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)

    def run(self, tasks: Iterable[ExportedTaskModel], output_root: Path, project_name: str = "GeneratedAndroidProject") -> AndroidStudioProjectExportResult:
        output_root = Path(output_root)
        project_root = RuntimeTemplateCopier(self.repo_root).copy(output_root, project_name)
        export_result = CompilableRuntimeTaskExportSession(self.repo_root).run(tasks)
        write_result = AndroidStudioProjectWriter().write(export_result, Path(project_root))
        return AndroidStudioProjectExportResult(
            project_root=str(project_root),
            write_result=write_result,
        )
