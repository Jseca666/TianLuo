package com.tianluo.runtime.template.runtime.ocr

import com.tianluo.runtime.template.runtime.assets.LocatorAsset
import com.tianluo.runtime.template.runtime.capture.CaptureEngine

class PaddleSemanticOcrEngine(
    private val captureEngine: CaptureEngine,
    private val bridge: PaddleOcrRuntimeBridge,
    private val modelAssets: PaddleOcrModelAssetPaths = PaddleOcrModelAssetPaths(),
) : SemanticOcrEngine {
    override suspend fun readText(locator: LocatorAsset, maskName: String?): List<String> {
        return readText(locator, OcrReadOptions(maskName = maskName))
    }

    override suspend fun readNumber(locator: LocatorAsset, maskName: String?): Int? {
        return readNumber(locator, OcrReadOptions(maskName = maskName))
    }

    override suspend fun readText(locator: LocatorAsset, options: OcrReadOptions): List<String> {
        val capturedBytes = captureEngine.captureToBytes()
        val croppedBytes = PaddleOcrImageRegionExtractor.cropToLocator(capturedBytes, locator) ?: return emptyList()
        return bridge.recognizeText(croppedBytes, modelAssets, options)
    }

    override suspend fun readNumber(locator: LocatorAsset, options: OcrReadOptions): Int? {
        val texts = readText(locator, options)
        val parsed = texts.asSequence()
            .mapNotNull { parseFirstInteger(it) }
            .firstOrNull()
        return if (parsed != null && options.excludedNumber != null && parsed == options.excludedNumber) {
            null
        } else {
            parsed
        }
    }

    private fun parseFirstInteger(text: String): Int? {
        val digits = buildString {
            for (char in text) {
                if (char.isDigit() || (length == 0 && char == '-')) {
                    append(char)
                } else if (isNotEmpty()) {
                    break
                }
            }
        }
        if (digits.isEmpty() || digits == "-") return null
        return digits.toIntOrNull()
    }
}
