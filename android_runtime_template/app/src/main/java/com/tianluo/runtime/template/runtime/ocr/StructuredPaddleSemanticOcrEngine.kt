package com.tianluo.runtime.template.runtime.ocr

import com.tianluo.runtime.template.runtime.assets.LocatorAsset
import com.tianluo.runtime.template.runtime.capture.CaptureEngine

class StructuredPaddleSemanticOcrEngine(
    private val captureEngine: CaptureEngine,
    private val bridge: StructuredPaddleOcrRuntimeBridge,
    private val modelAssets: PaddleOcrModelAssetPaths = PaddleOcrModelAssetPaths(),
    private val modelProfile: PaddleOcrOfficialModelProfile = PaddleOcrOfficialModelProfile.PpOcrV5Mobile,
) : SemanticOcrEngine {
    override suspend fun readText(locator: LocatorAsset, maskName: String?): List<String> {
        return readText(locator, OcrReadOptions(maskName = maskName))
    }

    override suspend fun readNumber(locator: LocatorAsset, maskName: String?): Int? {
        return readNumber(locator, OcrReadOptions(maskName = maskName))
    }

    override suspend fun readText(locator: LocatorAsset, options: OcrReadOptions): List<String> {
        return readStructured(locator, options).mergedTextLines()
    }

    override suspend fun readNumber(locator: LocatorAsset, options: OcrReadOptions): Int? {
        return readStructured(locator, options).bestInteger(options.excludedNumber)
    }

    suspend fun readStructured(
        locator: LocatorAsset,
        options: OcrReadOptions = OcrReadOptions(),
    ): PaddleOcrStructuredResult {
        val capturedBytes = captureEngine.captureToBytes()
        val croppedBytes = PaddleOcrImageRegionExtractor.cropToLocator(capturedBytes, locator)
            ?: return PaddleOcrStructuredResult(
                lines = emptyList(),
                modelProfileName = modelProfile.modelName,
                notes = listOf("Image crop for OCR returned null."),
            )
        return bridge.recognizeStructured(
            imageBytes = croppedBytes,
            modelAssets = modelAssets,
            options = options,
        )
    }
}
