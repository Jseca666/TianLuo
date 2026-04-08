package com.tianluo.runtime.template.runtime.ocr

import com.tianluo.runtime.template.runtime.assets.LocatorAsset

interface OcrEngine {
    suspend fun readText(locator: LocatorAsset, maskName: String? = null): List<String>
    suspend fun readNumber(locator: LocatorAsset, maskName: String? = null): Int?
}
