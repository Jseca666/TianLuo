from .export_models import ExportedTaskStep


class MainExportQualityV08StepMapper:
    def map(self, api_name: str, **params) -> ExportedTaskStep:
        name = str(api_name).strip()
        aliases = {
            "tap": "tap_area",
            "tap_template": "tap_locator",
            "tap_image": "tap_locator",
            "click": "tap_area",
            "click_area": "tap_area",
            "click_template": "tap_locator",
            "click_image": "tap_locator",
            "click_locator": "tap_locator",
            "wait_locator": "wait_image",
            "wait_template": "wait_image",
            "wait_for_locator": "wait_image",
            "wait_for_template": "wait_image",
            "wait_for_image": "wait_image",
            "exists_image": "exists",
            "exists_locator": "exists",
            "assert_exists": "exists",
            "ocr_number": "ocr_int",
            "ocr_digit": "ocr_int",
            "read_number": "ocr_int",
            "read_text": "ocr_text",
            "check_text_contains": "ocr_text_contains",
            "assert_text_contains": "ocr_text_contains",
            "check_text_equals": "ocr_text_equals",
            "assert_text_equals": "ocr_text_equals",
            "check_number_min": "ocr_int_min",
            "assert_number_at_least": "ocr_int_min",
            "assert_number_min": "ocr_int_min",
            "check_number_max": "ocr_int_max",
            "assert_number_at_most": "ocr_int_max",
            "assert_number_max": "ocr_int_max",
            "swipe_up": "swipe_up_area",
            "swipe_down": "swipe_down_area",
            "swipe_left": "swipe_left_area",
            "swipe_right": "swipe_right_area",
            "scroll_up": "swipe_up_area",
            "scroll_down": "swipe_down_area",
            "scroll_left": "swipe_left_area",
            "scroll_right": "swipe_right_area",
        }
        normalized = aliases.get(name, name)
        return ExportedTaskStep(action=normalized, params=dict(params))
