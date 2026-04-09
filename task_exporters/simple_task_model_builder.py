from typing import Iterable

from .export_models import ExportedTaskModel, ExportedTaskStep


class SimpleTaskModelBuilder:
    def build(self, task_id: str, display_name: str, steps: Iterable[dict]) -> ExportedTaskModel:
        exported_steps = []
        for item in steps:
            exported_steps.append(
                ExportedTaskStep(
                    action=str(item.get("action", "")),
                    params=dict(item.get("params", {})),
                )
            )
        return ExportedTaskModel(
            task_id=task_id,
            display_name=display_name,
            steps=exported_steps,
        )
