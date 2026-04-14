package com.tianluo.runtime.template.runtime.ocr

interface StructuredPaddleOcrRuntimeBridge : PaddleOcrRuntimeBridge {
    suspend fun recognizeStructured(
        imageBytes: ByteArray,
        modelAssets: PaddleOcrModelAssetPaths,
        options: OcrReadOptions = OcrReadOptions(),
    ): PaddleOcrStructuredResult

    override suspend fun recognizeText(
        imageBytes: ByteArray,
        modelAssets: PaddleOcrModelAssetPaths,
        options: OcrReadOptions,
    ): List<String> {
        return recognizeStructured(
            imageBytes = imageBytes,
            modelAssets = modelAssets,
            options = options,
        ).mergedTextLines()
    }
}
