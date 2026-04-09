package com.tianluo.runtime.template.runtime.ocr

import com.tianluo.runtime.template.runtime.assets.LocatorAsset

class EmptyOcrEngine : OcrEngine {
    override suspend fun readText(locator: LocatorAsset, maskName: String?): List<String> = emptyList()

    override suspend fun readNumber(locator: LocatorAsset, maskName: String?): Int? = null
}
