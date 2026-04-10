from .export_models import ExportedTaskStep


class DeliveryReadyExportableApiStepMapper:
    def map(self, api_name: str, **params) -> ExportedTaskStep:
        name = str(api_name).strip()

        aliases = {
            "tap": "tap_area",
            "tap_template": "tap_locator",
            "tap_image": "tap_locator",
            "wait_locator": "wait_image",
            "wait_template": "wait_image",
            "exists_image": "exists",
            "ocr_number": "ocr_int",
            "ocr_digit": "ocr_int",
            "check_text_contains": "ocr_text_contains",
            "assert_text_contains": "ocr_text_contains",
            "check_number_min": "ocr_int_min",
            "assert_number_at_least": "ocr_int_min",
        }
        normalized = aliases.get(name, name)

        return ExportedTaskStep(action=normalized, params=dict(params))
