from .export_models import ExportedTaskStep


class MainExportQualityStepMapper:
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
            "assert_text_equals": "ocr_text_equals",
            "check_number_min": "ocr_int_min",
            "assert_number_at_least": "ocr_int_min",
            "check_number_max": "ocr_int_max",
            "assert_number_at_most": "ocr_int_max",
            "swipe_up": "swipe_up_area",
            "swipe_down": "swipe_down_area",
            "swipe_left": "swipe_left_area",
            "swipe_right": "swipe_right_area",
        }
        normalized = aliases.get(name, name)
        return ExportedTaskStep(action=normalized, params=dict(params))
