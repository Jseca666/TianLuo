from .export_models import ExportedTaskStep


class KotlinStepRenderer:
    def render(self, step: ExportedTaskStep) -> str:
        action = step.action
        params = step.params or {}

        if action == "sleep":
            seconds = params.get("seconds", 1)
            return f"kotlinx.coroutines.delay(({seconds} * 1000).toLong())"

        if action == "tap_locator":
            locator = params.get("locator_name", "")
            return f'// TODO: tap locator: {locator}'

        if action == "back":
            return "// TODO: perform back action"

        return f'// TODO: unsupported action: {action}'
