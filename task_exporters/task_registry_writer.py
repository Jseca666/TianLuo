from typing import Iterable

from .export_models import ExportedTaskModel


class TaskRegistryWriter:
    def render(self, tasks: Iterable[ExportedTaskModel], package_name: str = "com.tianluo.generated") -> str:
        task_list = list(tasks)
        imports = []
        entries = []
        for task in task_list:
            class_name = self._class_name(task.task_id)
            imports.append(f"import com.tianluo.generated.tasks.{class_name}")
            entries.append(f'        "{task.task_id}" to {class_name}()')

        imports_text = "\n".join(imports)
        entries_text = ",\n".join(entries) if entries else ""
        return f'''package {package_name}

{imports_text}

object GeneratedTaskRegistry {{
    fun all(): Map<String, Any> = mapOf(
{entries_text}
    )
}}
'''

    def _class_name(self, task_id: str) -> str:
        parts = [part for part in task_id.replace('-', '_').split('_') if part]
        if not parts:
            return "GeneratedTask"
        return ''.join(p[:1].upper() + p[1:] for p in parts) + "Task"
