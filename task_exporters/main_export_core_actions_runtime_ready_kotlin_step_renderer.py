from .export_models import ExportedTaskStep


class MainExportCoreActionsRuntimeReadyKotlinStepRenderer:
    def render(self, index: int, step: ExportedTaskStep) -> str:
        action = step.action
        params = step.params or {}

        if action == "sleep":
            milliseconds = int(params.get("milliseconds", 1000))
            return f"kotlinx.coroutines.delay({milliseconds}L)"

        if action == "back":
            return f'''val backed{index} = context.gestureEngine.back()
        if (!backed{index}) {{
            return TaskResult.fail("Back gesture failed for exported core action step {index}")
        }}'''

        if action == "tap_point":
            x = int(params.get("x", 0))
            y = int(params.get("y", 0))
            return f'''val point{index} = com.tianluo.runtime.template.runtime.assets.PointAsset({x}, {y})
        val tapped{index} = context.gestureEngine.tap(point{index})
        if (!tapped{index}) {{
            return TaskResult.fail("Tap gesture failed at ({x}, {y})")
        }}'''

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
            return TaskResult.fail("Swipe gesture failed from ({start_x}, {start_y}) to ({end_x}, {end_y})")
        }}'''

        return f'// TODO main-export-core-actions-runtime-ready: unsupported action: {action}'
