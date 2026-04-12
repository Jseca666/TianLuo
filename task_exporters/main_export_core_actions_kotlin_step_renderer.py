from .export_models import ExportedTaskStep


class MainExportCoreActionsKotlinStepRenderer:
    def render(self, index: int, step: ExportedTaskStep) -> str:
        action = step.action
        params = step.params or {}

        if action == "sleep":
            seconds = float(params.get("seconds", 1))
            return f"kotlinx.coroutines.delay(({seconds} * 1000).toLong())"

        if action == "back":
            return "context.gestureEngine.back()"

        if action == "tap_point":
            x = int(params.get("x", 0))
            y = int(params.get("y", 0))
            return f'''val point{index} = com.tianluo.runtime.template.runtime.assets.PointAsset({x}, {y})
        context.gestureEngine.tap(point{index})'''

        if action == "swipe_points":
            start_x = int(params.get("start_x", 0))
            start_y = int(params.get("start_y", 0))
            end_x = int(params.get("end_x", 0))
            end_y = int(params.get("end_y", 0))
            duration_ms = int(params.get("duration_ms", 300))
            return f'''val startPoint{index} = com.tianluo.runtime.template.runtime.assets.PointAsset({start_x}, {start_y})
        val endPoint{index} = com.tianluo.runtime.template.runtime.assets.PointAsset({end_x}, {end_y})
        val swiped{index} = context.gestureEngine.swipe(startPoint{index}, endPoint{index}, durationMs = {duration_ms}L)
        if (!swiped{index}) {{
            return TaskResult.fail("Swipe gesture failed for exported core action step {index}")
        }}'''

        return f'// TODO main-export-core-actions: unsupported action: {action}'
