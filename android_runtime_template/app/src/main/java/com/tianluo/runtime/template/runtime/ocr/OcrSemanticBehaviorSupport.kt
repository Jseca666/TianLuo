package com.tianluo.runtime.template.runtime.ocr

import com.tianluo.runtime.template.runtime.assets.LocatorAsset

suspend fun readTextSemanticBehavior(
    engine: OcrEngine,
    locator: LocatorAsset,
    options: OcrReadOptions = OcrReadOptions(),
): OcrSemanticTextBehaviorResult {
    return if (engine is SemanticOcrEngine) {
        val texts = engine.readText(locator, options)
        OcrSemanticTextBehaviorResult(
            texts = texts,
            usedSemanticEngine = true,
            kernelSizeHintApplied = options.kernelSize != null,
        )
    } else {
        val texts = engine.readText(locator, maskName = options.maskName)
        OcrSemanticTextBehaviorResult(
            texts = texts,
            usedSemanticEngine = false,
            kernelSizeHintApplied = false,
        )
    }
}

suspend fun readNumberSemanticBehavior(
    engine: OcrEngine,
    locator: LocatorAsset,
    options: OcrReadOptions = OcrReadOptions(),
): OcrSemanticNumberBehaviorResult {
    val usedSemanticEngine = engine is SemanticOcrEngine
    val value = if (engine is SemanticOcrEngine) {
        engine.readNumber(locator, options)
    } else {
        engine.readNumber(locator, maskName = options.maskName)
    }
    val filtered = value != null && options.excludedNumber != null && value == options.excludedNumber
    return OcrSemanticNumberBehaviorResult(
        number = if (filtered) null else value,
        usedSemanticEngine = usedSemanticEngine,
        kernelSizeHintApplied = usedSemanticEngine && options.kernelSize != null,
        excludedNumberFiltered = filtered,
    )
}
