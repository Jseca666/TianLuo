from pathlib import Path

from .android_project_write_result import AndroidProjectWriteResult
from .android_studio_layout import AndroidStudioLayout
from task_exporters.task_export_result import TaskExportResult


class AndroidStudioProjectWriter:
    def write(self, export_result: TaskExportResult, project_root: Path) -> AndroidProjectWriteResult:
        project_root = Path(project_root)
        tasks_dir = project_root / AndroidStudioLayout.TASKS_DIR
        tasks_dir.mkdir(parents=True, exist_ok=True)

        task_files = {}
        for task_id, content in export_result.tasks.items():
            file_name = self._class_name(task_id) + ".kt"
            path = tasks_dir / file_name
            path.write_text(content, encoding="utf-8")
            task_files[task_id] = str(path)

        registry_path = project_root / AndroidStudioLayout.REGISTRY_FILE
        registry_path.parent.mkdir(parents=True, exist_ok=True)
        registry_path.write_text(export_result.registry, encoding="utf-8")

        return AndroidProjectWriteResult(
            root_dir=str(project_root),
            task_files=task_files,
            registry_file=str(registry_path),
        )

    def _class_name(self, task_id: str) -> str:
        parts = [part for part in task_id.replace('-', '_').split('_') if part]
        if not parts:
            return "GeneratedTask"
        return ''.join(p[:1].upper() + p[1:] for p in parts) + "Task"
