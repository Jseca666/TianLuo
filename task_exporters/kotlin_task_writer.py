from .export_models import ExportedTaskModel


class KotlinTaskWriter:
    def render(self, task: ExportedTaskModel, package_name: str = "com.tianluo.generated.tasks") -> str:
        class_name = self._class_name(task.task_id)
        return f'''package {package_name}

import com.tianluo.runtime.template.runtime.task.RuntimeTask
import com.tianluo.runtime.template.runtime.task.TaskContext
import com.tianluo.runtime.template.runtime.task.TaskResult

class {class_name} : RuntimeTask {{
    override val taskId: String = "{task.task_id}"
    override val displayName: String = "{task.display_name}"

    override suspend fun run(context: TaskContext): TaskResult {{
        return TaskResult.ok("Task skeleton generated")
    }}
}}
'''

    def _class_name(self, task_id: str) -> str:
        parts = [part for part in task_id.replace('-', '_').split('_') if part]
        if not parts:
            return "GeneratedTask"
        return ''.join(p[:1].upper() + p[1:] for p in parts) + "Task"
