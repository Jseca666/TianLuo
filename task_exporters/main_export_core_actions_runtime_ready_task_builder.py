from typing import Iterable

from .export_models import ExportedTaskModel
from .main_export_core_actions_runtime_ready_step_mapper import MainExportCoreActionsRuntimeReadyStepMapper


class MainExportCoreActionsRuntimeReadyTaskBuilder:
    def __init__(self):
        self.step_mapper = MainExportCoreActionsRuntimeReadyStepMapper()

    def build(self, task_id: str, display_name: str, api_calls: Iterable[dict]) -> ExportedTaskModel:
        steps = []
        for call in api_calls:
            api_name = str(call.get("api_name", ""))
            params = dict(call.get("params", {}))
            steps.append(self.step_mapper.map(api_name, **params))
        return ExportedTaskModel(
            task_id=task_id,
            display_name=display_name,
            steps=steps,
        )
