from pathlib import Path
from typing import Iterable

from .export_models import ExportedTaskModel
from .main_export_core_actions_kotlin_step_renderer import MainExportCoreActionsKotlinStepRenderer
from .task_export_result import TaskExportResult
from .task_registry_writer import TaskRegistryWriter


class MainExportCoreActionsTaskExportSession:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.step_renderer = MainExportCoreActionsKotlinStepRenderer()

    def run(self, tasks: Iterable[ExportedTaskModel]) -> TaskExportResult:
        task_list = list(tasks)
        rendered_tasks = {}
        for task in task_list:
            rendered_tasks[task.task_id] = self._render_task(task)
        registry_text = TaskRegistryWriter().render(task_list)
        models = {task.task_id: task for task in task_list}
        return TaskExportResult(tasks=rendered_tasks, registry=registry_text, models=models)

    def _render_task(self, task: ExportedTaskModel) -> str:
        class_name = self._class_name(task.task_id)
        step_lines = []
        for index, step in enumerate(task.steps):
            rendered = self.step_renderer.render(index, step)
            for line in rendered.splitlines():
                step_lines.append(f"        {line}")
        steps_block = "\n".join(step_lines) if step_lines else "        // TODO: no steps exported"
        return f'''package com.tianluo.generated.tasks

import com.tianluo.runtime.template.runtime.task.RuntimeTask
import com.tianluo.runtime.template.runtime.task.TaskContext
import com.tianluo.runtime.template.runtime.task.TaskResult

class {class_name} : RuntimeTask {{
    override val taskId: String = "{task.task_id}"
    override val displayName: String = "{task.display_name}"

    override suspend fun run(context: TaskContext): TaskResult {{
{steps_block}
        return TaskResult.ok("Main export core actions task generated")
    }}
}}
'''

    def _class_name(self, task_id: str) -> str:
        parts = [part for part in task_id.replace('-', '_').split('_') if part]
        if not parts:
            return "GeneratedTask"
        return ''.join(p[:1].upper() + p[1:] for p in parts) + "Task"
