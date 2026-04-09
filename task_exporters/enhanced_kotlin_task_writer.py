from .export_models import ExportedTaskModel
from .kotlin_step_renderer import KotlinStepRenderer


class EnhancedKotlinTaskWriter:
    def __init__(self):
        self.step_renderer = KotlinStepRenderer()

    def render(self, task: ExportedTaskModel, package_name: str = "com.tianluo.generated.tasks") -> str:
        class_name = self._class_name(task.task_id)
        step_lines = []
        for step in task.steps:
            rendered = self.step_renderer.render(step)
            step_lines.append(f"        {rendered}")
        steps_block = "\n".join(step_lines) if step_lines else "        // TODO: no steps exported"

        return f'''package {package_name}

import com.tianluo.runtime.template.runtime.task.RuntimeTask
import com.tianluo.runtime.template.runtime.task.TaskContext
import com.tianluo.runtime.template.runtime.task.TaskResult

class {class_name} : RuntimeTask {{
    override val taskId: String = "{task.task_id}"
    override val displayName: String = "{task.display_name}"

    override suspend fun run(context: TaskContext): TaskResult {{
{steps_block}
        return TaskResult.ok("Task generated from exported steps")
    }}
}}
'''

    def _class_name(self, task_id: str) -> str:
        parts = [part for part in task_id.replace('-', '_').split('_') if part]
        if not parts:
            return "GeneratedTask"
        return ''.join(p[:1].upper() + p[1:] for p in parts) + "Task"
