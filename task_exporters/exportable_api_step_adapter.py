from .export_models import ExportedTaskStep


class ExportableApiStepAdapter:
    def adapt(self, api_name: str, **params) -> ExportedTaskStep:
        return ExportedTaskStep(
            action=str(api_name),
            params=dict(params),
        )
