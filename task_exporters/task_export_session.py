from pathlib import Path
from typing import Iterable

from .export_models import ExportedTaskModel
from .task_export_result import TaskExportResult
from task_exporters.kotlin_task_writer import KotlinTaskWriter
from task_exporters.task_registry_writer import TaskRegistryWriter


class TaskExportSession:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)

    def run(self, tasks: Iterable[ExportedTaskModel]) -> TaskExportResult:
        task_list = list(tasks)
        task_writer = KotlinTaskWriter()
        registry_writer = TaskRegistryWriter()

        rendered_tasks = {
            task.task_id: task_writer.render(task)
            for task in task_list
        }
        registry_text = registry_writer.render(task_list)
        models = {task.task_id: task for task in task_list}

        return TaskExportResult(
            tasks=rendered_tasks,
            registry=registry_text,
            models=models,
        )
