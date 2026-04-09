from .export_models import ExportedTaskStep


class RuntimeAwareKotlinStepRenderer:
    def render(self, step: ExportedTaskStep) -> str:
        action = step.action
        params = step.params or {}

        if action == "sleep":
            seconds = params.get("seconds", 1)
            return f"kotlinx.coroutines.delay(({seconds} * 1000).toLong())"

        if action == "tap_locator":
            locator = params.get("locator_name", "")
            return f'// TODO runtime: tap locator using exported asset: {locator}'

        if action == "tap_area":
            locator = params.get("locator_name", "")
            return f'// TODO runtime: tap area for locator: {locator}'

        if action == "wait_image":
            locator = params.get("locator_name", "")
            return f'// TODO runtime: wait image for locator: {locator}'

        if action == "exists":
            locator = params.get("locator_name", "")
            return f'// TODO runtime: exists check for locator: {locator}'

        if action == "back":
            return "// TODO runtime: perform back action"

        return f'// TODO runtime: unsupported action: {action}'
