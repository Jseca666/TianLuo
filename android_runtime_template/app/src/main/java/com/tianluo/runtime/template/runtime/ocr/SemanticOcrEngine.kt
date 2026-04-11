package com.tianluo.runtime.template.runtime.ocr

import com.tianluo.runtime.template.runtime.assets.LocatorAsset

interface SemanticOcrEngine : OcrEngine {
    suspend fun readText(locator: LocatorAsset, options: OcrReadOptions = OcrReadOptions()): List<String>
    suspend fun readNumber(locator: LocatorAsset, options: OcrReadOptions = OcrReadOptions()): Int?
}
