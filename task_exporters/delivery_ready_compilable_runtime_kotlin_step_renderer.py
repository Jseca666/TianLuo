from .export_models import ExportedTaskStep


class DeliveryReadyCompilableRuntimeKotlinStepRenderer:
    def render(self, index: int, step: ExportedTaskStep) -> str:
        action = step.action
        params = step.params or {}

        if action == "sleep":
            seconds = params.get("seconds", 1)
            return f"kotlinx.coroutines.delay(({seconds} * 1000).toLong())"

        if action == "back":
            return "context.gestureEngine.back()"

        if action == "tap_locator":
            locator = params.get("locator_name", "")
            timeout = float(params.get("timeout", 3.0))
            timeout_ms = int(timeout * 1000)
            return f'''val locator{index} = context.locatorRepository.get("{locator}")
        val match{index} = context.templateMatcher.waitFor(locator{index}, timeoutMs = {timeout_ms}L)
        if (match{index} == null) {{
            return TaskResult.fail("Locator not found: {locator}")
        }}
        context.gestureEngine.tap(match{index}.center)'''

        if action == "tap_area":
            locator = params.get("locator_name", "")
            return f'''val locator{index} = context.locatorRepository.get("{locator}")
        val centerPoint{index} = com.tianluo.runtime.template.runtime.assets.PointAsset(
            (locator{index}.rect.topLeft.x + locator{index}.rect.bottomRight.x) / 2,
            (locator{index}.rect.topLeft.y + locator{index}.rect.bottomRight.y) / 2,
        )
        context.gestureEngine.tap(centerPoint{index})'''

        if action == "wait_image":
            locator = params.get("locator_name", "")
            timeout = float(params.get("timeout", 5.0))
            timeout_ms = int(timeout * 1000)
            return f'''val locator{index} = context.locatorRepository.get("{locator}")
        val match{index} = context.templateMatcher.waitFor(locator{index}, timeoutMs = {timeout_ms}L)
        if (match{index} == null) {{
            return TaskResult.fail("Wait image timeout: {locator}")
        }}'''

        if action == "exists":
            locator = params.get("locator_name", "")
            timeout = float(params.get("timeout", 1.0))
            timeout_ms = int(timeout * 1000)
            return f'''val locator{index} = context.locatorRepository.get("{locator}")
        val exists{index} = context.templateMatcher.waitFor(locator{index}, timeoutMs = {timeout_ms}L) != null
        if (!exists{index}) {{
            return TaskResult.fail("Locator does not exist: {locator}")
        }}'''

        if action == "ocr_text":
            locator = params.get("locator_name", "")
            return f'''val locator{index} = context.locatorRepository.get("{locator}")
        context.ocrEngine.readText(locator{index})'''

        if action == "ocr_int":
            locator = params.get("locator_name", "")
            return f'''val locator{index} = context.locatorRepository.get("{locator}")
        context.ocrEngine.readNumber(locator{index})'''

        if action == "ocr_text_contains":
            locator = params.get("locator_name", "")
            expected = str(params.get("expected", ""))
            return f'''val locator{index} = context.locatorRepository.get("{locator}")
        val texts{index} = context.ocrEngine.readText(locator{index})
        val found{index} = texts{index}.any {{ it.contains("{expected}") }}
        if (!found{index}) {{
            return TaskResult.fail("OCR text does not contain expected text: {expected}")
        }}'''

        if action == "ocr_int_min":
            locator = params.get("locator_name", "")
            min_value = int(params.get("min_value", 0))
            return f'''val locator{index} = context.locatorRepository.get("{locator}")
        val number{index} = context.ocrEngine.readNumber(locator{index})
        if (number{index} == null || number{index} < {min_value}) {{
            return TaskResult.fail("OCR number is lower than expected minimum: {min_value}")
        }}'''

        return f'// TODO delivery-ready compilable runtime: unsupported action: {action}'
