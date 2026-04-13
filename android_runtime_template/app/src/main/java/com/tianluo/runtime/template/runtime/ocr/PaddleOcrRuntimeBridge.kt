package com.tianluo.runtime.template.runtime.ocr

interface PaddleOcrRuntimeBridge {
    suspend fun recognizeText(
        imageBytes: ByteArray,
        modelAssets: PaddleOcrModelAssetPaths,
        options: OcrReadOptions = OcrReadOptions(),
    ): List<String>
}
