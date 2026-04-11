from .export_models import ExportedTaskStep


class MainExportQualitySemanticStepMapper:
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
            "check_exists": "exists",
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
        normalized_params = self._normalize_params(normalized, dict(params))
        return ExportedTaskStep(action=normalized, params=normalized_params)

    def _normalize_params(self, action: str, params: dict) -> dict:
        result = dict(params)

        locator_name = (
            result.get("locator_name")
            or result.get("template_name")
            or result.get("image_name")
            or result.get("locator")
            or result.get("template")
            or result.get("image")
            or result.get("target")
        )
        if locator_name is not None:
            result["locator_name"] = locator_name

        timeout = (
            result.get("timeout")
            or result.get("timeout_seconds")
            or result.get("wait_seconds")
            or result.get("wait_timeout")
        )
        if timeout is not None:
            result["timeout"] = timeout

        threshold = (
            result.get("threshold")
            or result.get("similarity_threshold")
            or result.get("match_threshold")
        )
        if threshold is not None:
            result["threshold"] = threshold

        mask_name = (
            result.get("mask_name")
            or result.get("maskName")
            or result.get("mask")
        )
        if mask_name is not None:
            result["mask_name"] = mask_name

        use_color = result.get("use_color")
        if use_color is None and result.get("useColor") is not None:
            use_color = result.get("useColor")
        if use_color is not None:
            result["use_color"] = bool(use_color)

        expected = (
            result.get("expected")
            or result.get("text")
            or result.get("target_text")
            or result.get("value")
        )
        if action in {"ocr_text_contains", "ocr_text_equals"} and expected is not None:
            result["expected"] = expected

        if result.get("min_value") is None and result.get("min") is not None:
            result["min_value"] = result.get("min")
        if result.get("max_value") is None and result.get("max") is not None:
            result["max_value"] = result.get("max")

        if result.get("duration_ms") is None and result.get("duration") is not None:
            try:
                duration_value = float(result.get("duration"))
                result["duration_ms"] = int(duration_value if duration_value >= 20 else duration_value * 1000)
            except (TypeError, ValueError):
                pass

        return result
