package com.tianluo.runtime.template.runtime.ocr

import com.tianluo.runtime.template.runtime.assets.LocatorAsset

suspend fun readTextSemantic(
    engine: OcrEngine,
    locator: LocatorAsset,
    options: OcrReadOptions = OcrReadOptions(),
): List<String> {
    return if (engine is SemanticOcrEngine) {
        engine.readText(locator, options)
    } else {
        engine.readText(locator, maskName = options.maskName)
    }
}

suspend fun readNumberSemantic(
    engine: OcrEngine,
    locator: LocatorAsset,
    options: OcrReadOptions = OcrReadOptions(),
): Int? {
    val value = if (engine is SemanticOcrEngine) {
        engine.readNumber(locator, options)
    } else {
        engine.readNumber(locator, maskName = options.maskName)
    }
    return if (value != null && options.excludedNumber != null && value == options.excludedNumber) {
        null
    } else {
        value
    }
}
