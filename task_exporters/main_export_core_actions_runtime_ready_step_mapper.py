from .export_models import ExportedTaskStep


class MainExportCoreActionsRuntimeReadyStepMapper:
    def map(self, api_name: str, **params) -> ExportedTaskStep:
        name = str(api_name).strip()
        aliases = {
            "tap": "tap_point",
            "tap_xy": "tap_point",
            "tap_coordinate": "tap_point",
            "click_point": "tap_point",
            "click_xy": "tap_point",
            "swipe": "swipe_points",
            "swipe_xy": "swipe_points",
            "swipe_points_xy": "swipe_points",
            "back_key": "back",
            "press_back": "back",
            "go_back": "back",
            "sleep_seconds": "sleep",
            "wait_seconds": "sleep",
            "sleep_ms": "sleep",
            "wait_ms": "sleep",
            "delay_ms": "sleep",
        }
        normalized = aliases.get(name, name)
        normalized_params = self._normalize_params(normalized, dict(params))
        return ExportedTaskStep(action=normalized, params=normalized_params)

    def _normalize_params(self, action: str, params: dict) -> dict:
        result = dict(params)

        x = result.get("x")
        if x is None and result.get("point_x") is not None:
            x = result.get("point_x")
        if x is None and result.get("target_x") is not None:
            x = result.get("target_x")
        if x is not None:
            result["x"] = x

        y = result.get("y")
        if y is None and result.get("point_y") is not None:
            y = result.get("point_y")
        if y is None and result.get("target_y") is not None:
            y = result.get("target_y")
        if y is not None:
            result["y"] = y

        start_x = result.get("start_x")
        if start_x is None and result.get("x1") is not None:
            start_x = result.get("x1")
        if start_x is not None:
            result["start_x"] = start_x

        start_y = result.get("start_y")
        if start_y is None and result.get("y1") is not None:
            start_y = result.get("y1")
        if start_y is not None:
            result["start_y"] = start_y

        end_x = result.get("end_x")
        if end_x is None and result.get("x2") is not None:
            end_x = result.get("x2")
        if end_x is not None:
            result["end_x"] = end_x

        end_y = result.get("end_y")
        if end_y is None and result.get("y2") is not None:
            end_y = result.get("y2")
        if end_y is not None:
            result["end_y"] = end_y

        if action == "sleep":
            milliseconds = result.get("milliseconds")
            if milliseconds is None and result.get("ms") is not None:
                milliseconds = result.get("ms")
            if milliseconds is None and result.get("duration_ms") is not None:
                milliseconds = result.get("duration_ms")
            if milliseconds is None and result.get("wait_ms") is not None:
                milliseconds = result.get("wait_ms")
            if milliseconds is None and result.get("delay_ms") is not None:
                milliseconds = result.get("delay_ms")
            if milliseconds is None:
                seconds = result.get("seconds")
                if seconds is None and result.get("duration_seconds") is not None:
                    seconds = result.get("duration_seconds")
                if seconds is None and result.get("wait_seconds") is not None:
                    seconds = result.get("wait_seconds")
                if seconds is not None:
                    try:
                        milliseconds = int(float(seconds) * 1000)
                    except (TypeError, ValueError):
                        pass
            if milliseconds is not None:
                try:
                    result["milliseconds"] = int(float(milliseconds))
                except (TypeError, ValueError):
                    pass

        if action == "swipe_points" and result.get("duration_ms") is None and result.get("duration") is not None:
            try:
                duration_value = float(result.get("duration"))
                result["duration_ms"] = int(duration_value if duration_value >= 20 else duration_value * 1000)
            except (TypeError, ValueError):
                pass

        return result
