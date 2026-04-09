from pathlib import Path
from typing import Iterable

from task_exporters.export_models import ExportedTaskModel
from task_exporters.kotlin_task_writer import KotlinTaskWriter
from task_exporters.task_registry_writer import TaskRegistryWriter


class AndroidProjectExporter:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)

    def export_tasks(self, tasks: Iterable[ExportedTaskModel]) -> dict:
        task_list = list(tasks)
        task_writer = KotlinTaskWriter()
        registry_writer = TaskRegistryWriter()

        rendered_tasks = {
            task.task_id: task_writer.render(task)
            for task in task_list
        }
        registry_text = registry_writer.render(task_list)

        return {
            "tasks": rendered_tasks,
            "registry": registry_text,
        }
