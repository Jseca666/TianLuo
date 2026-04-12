from .export_models import ExportedTaskStep


class MainExportQualityRuntimeBehaviorKotlinStepRenderer:
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
            timeout_ms = int(float(params.get("timeout", 3.0)) * 1000)
            threshold = float(params.get("threshold", 0.8))
            mask_name = self._string_or_null(params.get("mask_name"))
            use_color = self._bool_literal(params.get("use_color", False))
            return f'''val locator{index} = context.locatorRepository.get("{locator}")
        val match{index} = context.templateMatcher.waitFor(
            locator{index},
            threshold = {threshold},
            timeoutMs = {timeout_ms}L,
            maskName = {mask_name},
            useColor = {use_color},
        )
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
            timeout_ms = int(float(params.get("timeout", 5.0)) * 1000)
            threshold = float(params.get("threshold", 0.8))
            mask_name = self._string_or_null(params.get("mask_name"))
            use_color = self._bool_literal(params.get("use_color", False))
            return f'''val locator{index} = context.locatorRepository.get("{locator}")
        val match{index} = context.templateMatcher.waitFor(
            locator{index},
            threshold = {threshold},
            timeoutMs = {timeout_ms}L,
            maskName = {mask_name},
            useColor = {use_color},
        )
        if (match{index} == null) {{
            return TaskResult.fail("Wait image timeout: {locator}")
        }}'''

        if action == "exists":
            locator = params.get("locator_name", "")
            timeout_ms = int(float(params.get("timeout", 1.0)) * 1000)
            threshold = float(params.get("threshold", 0.8))
            mask_name = self._string_or_null(params.get("mask_name"))
            use_color = self._bool_literal(params.get("use_color", False))
            return f'''val locator{index} = context.locatorRepository.get("{locator}")
        val exists{index} = context.templateMatcher.waitFor(
            locator{index},
            threshold = {threshold},
            timeoutMs = {timeout_ms}L,
            maskName = {mask_name},
            useColor = {use_color},
        ) != null
        if (!exists{index}) {{
            return TaskResult.fail("Locator does not exist: {locator}")
        }}'''

        if action == "ocr_text":
            locator = params.get("locator_name", "")
            options = self._ocr_options(params)
            return f'''val locator{index} = context.locatorRepository.get("{locator}")
        val textBehavior{index} = com.tianluo.runtime.template.runtime.ocr.readTextSemanticBehavior(
            context.ocrEngine,
            locator{index},
            {options},
        )
        val texts{index} = textBehavior{index}.texts
        val usedSemanticEngine{index} = textBehavior{index}.usedSemanticEngine
        val kernelSizeHintApplied{index} = textBehavior{index}.kernelSizeHintApplied'''

        if action == "ocr_int":
            locator = params.get("locator_name", "")
            options = self._ocr_options(params)
            return f'''val locator{index} = context.locatorRepository.get("{locator}")
        val numberBehavior{index} = com.tianluo.runtime.template.runtime.ocr.readNumberSemanticBehavior(
            context.ocrEngine,
            locator{index},
            {options},
        )
        val number{index} = numberBehavior{index}.number
        val usedSemanticEngine{index} = numberBehavior{index}.usedSemanticEngine
        val kernelSizeHintApplied{index} = numberBehavior{index}.kernelSizeHintApplied
        val excludedNumberFiltered{index} = numberBehavior{index}.excludedNumberFiltered'''

        if action == "ocr_text_contains":
            locator = params.get("locator_name", "")
            expected = str(params.get("expected", ""))
            options = self._ocr_options(params)
            return f'''val locator{index} = context.locatorRepository.get("{locator}")
        val textBehavior{index} = com.tianluo.runtime.template.runtime.ocr.readTextSemanticBehavior(
            context.ocrEngine,
            locator{index},
            {options},
        )
        val texts{index} = textBehavior{index}.texts
        val usedSemanticEngine{index} = textBehavior{index}.usedSemanticEngine
        val kernelSizeHintApplied{index} = textBehavior{index}.kernelSizeHintApplied
        val found{index} = texts{index}.any {{ it.contains("{expected}") }}
        if (!found{index}) {{
            return TaskResult.fail("OCR text does not contain expected text: {expected}")
        }}'''

        if action == "ocr_text_equals":
            locator = params.get("locator_name", "")
            expected = str(params.get("expected", ""))
            options = self._ocr_options(params)
            return f'''val locator{index} = context.locatorRepository.get("{locator}")
        val textBehavior{index} = com.tianluo.runtime.template.runtime.ocr.readTextSemanticBehavior(
            context.ocrEngine,
            locator{index},
            {options},
        )
        val texts{index} = textBehavior{index}.texts
        val usedSemanticEngine{index} = textBehavior{index}.usedSemanticEngine
        val kernelSizeHintApplied{index} = textBehavior{index}.kernelSizeHintApplied
        val found{index} = texts{index}.any {{ it == "{expected}" }}
        if (!found{index}) {{
            return TaskResult.fail("OCR text does not equal expected text: {expected}")
        }}'''

        if action == "ocr_int_min":
            locator = params.get("locator_name", "")
            min_value = int(params.get("min_value", 0))
            options = self._ocr_options(params)
            return f'''val locator{index} = context.locatorRepository.get("{locator}")
        val numberBehavior{index} = com.tianluo.runtime.template.runtime.ocr.readNumberSemanticBehavior(
            context.ocrEngine,
            locator{index},
            {options},
        )
        val number{index} = numberBehavior{index}.number
        val usedSemanticEngine{index} = numberBehavior{index}.usedSemanticEngine
        val kernelSizeHintApplied{index} = numberBehavior{index}.kernelSizeHintApplied
        val excludedNumberFiltered{index} = numberBehavior{index}.excludedNumberFiltered
        if (number{index} == null || number{index} < {min_value}) {{
            return TaskResult.fail("OCR number is lower than expected minimum: {min_value}")
        }}'''

        if action == "ocr_int_max":
            locator = params.get("locator_name", "")
            max_value = int(params.get("max_value", 0))
            options = self._ocr_options(params)
            return f'''val locator{index} = context.locatorRepository.get("{locator}")
        val numberBehavior{index} = com.tianluo.runtime.template.runtime.ocr.readNumberSemanticBehavior(
            context.ocrEngine,
            locator{index},
            {options},
        )
        val number{index} = numberBehavior{index}.number
        val usedSemanticEngine{index} = numberBehavior{index}.usedSemanticEngine
        val kernelSizeHintApplied{index} = numberBehavior{index}.kernelSizeHintApplied
        val excludedNumberFiltered{index} = numberBehavior{index}.excludedNumberFiltered
        if (number{index} == null || number{index} > {max_value}) {{
            return TaskResult.fail("OCR number is greater than expected maximum: {max_value}")
        }}'''

        if action in {"swipe_up_area", "swipe_down_area", "swipe_left_area", "swipe_right_area"}:
            locator = params.get("locator_name", "")
            duration_ms = int(params.get("duration_ms", 300))
            return self._render_swipe(index=index, locator=locator, duration_ms=duration_ms, action=action)

        return f'// TODO main-export-quality-runtime-behavior: unsupported action: {action}'

    def _render_swipe(self, index: int, locator: str, duration_ms: int, action: str) -> str:
        if action == "swipe_up_area":
            start_expr = "com.tianluo.runtime.template.runtime.assets.PointAsset(centerX{0}, top{0} + (height{0} * 3 / 4))".format(index)
            end_expr = "com.tianluo.runtime.template.runtime.assets.PointAsset(centerX{0}, top{0} + (height{0} / 4))".format(index)
        elif action == "swipe_down_area":
            start_expr = "com.tianluo.runtime.template.runtime.assets.PointAsset(centerX{0}, top{0} + (height{0} / 4))".format(index)
            end_expr = "com.tianluo.runtime.template.runtime.assets.PointAsset(centerX{0}, top{0} + (height{0} * 3 / 4))".format(index)
        elif action == "swipe_left_area":
            start_expr = "com.tianluo.runtime.template.runtime.assets.PointAsset(left{0} + (width{0} * 3 / 4), centerY{0})".format(index)
            end_expr = "com.tianluo.runtime.template.runtime.assets.PointAsset(left{0} + (width{0} / 4), centerY{0})".format(index)
        else:
            start_expr = "com.tianluo.runtime.template.runtime.assets.PointAsset(left{0} + (width{0} / 4), centerY{0})".format(index)
            end_expr = "com.tianluo.runtime.template.runtime.assets.PointAsset(left{0} + (width{0} * 3 / 4), centerY{0})".format(index)
        return f'''val locator{index} = context.locatorRepository.get("{locator}")
        val left{index} = locator{index}.rect.topLeft.x
        val top{index} = locator{index}.rect.topLeft.y
        val right{index} = locator{index}.rect.bottomRight.x
        val bottom{index} = locator{index}.rect.bottomRight.y
        val width{index} = right{index} - left{index}
        val height{index} = bottom{index} - top{index}
        val centerX{index} = (left{index} + right{index}) / 2
        val centerY{index} = (top{index} + bottom{index}) / 2
        val startPoint{index} = {start_expr}
        val endPoint{index} = {end_expr}
        val swiped{index} = context.gestureEngine.swipe(startPoint{index}, endPoint{index}, durationMs = {duration_ms}L)
        if (!swiped{index}) {{
            return TaskResult.fail("Swipe gesture failed for locator: {locator}")
        }}'''

    def _ocr_options(self, params: dict) -> str:
        mask_name = self._string_or_null(params.get("mask_name"))
        kernel_size = self._int_or_null(params.get("kernel_size"))
        excluded_number = self._int_or_null(params.get("excluded_number"))
        return f"com.tianluo.runtime.template.runtime.ocr.OcrReadOptions(maskName = {mask_name}, kernelSize = {kernel_size}, excludedNumber = {excluded_number})"

    def _string_or_null(self, value) -> str:
        if value is None or value == "":
            return "null"
        return f'"{value}"'

    def _bool_literal(self, value) -> str:
        return "true" if bool(value) else "false"

    def _int_or_null(self, value) -> str:
        if value is None or value == "":
            return "null"
        return str(int(value))
