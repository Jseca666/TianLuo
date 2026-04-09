from .export_models import ExportedTaskStep


class ExportableApiStepMapper:
    def map(self, api_name: str, **params) -> ExportedTaskStep:
        name = str(api_name)
        if name in {"tap_locator", "sleep", "back", "tap_area", "tap"}:
            return ExportedTaskStep(action=name, params=dict(params))
        if name in {"wait_image", "exists", "ocr_text", "ocr_int"}:
            return ExportedTaskStep(action=name, params=dict(params))
        return ExportedTaskStep(action=name, params=dict(params))
