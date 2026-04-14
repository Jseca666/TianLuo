package com.tianluo.runtime.template.runtime.ocr

interface PaddleOcrRuntimeExecutor {
    suspend fun recognize(
        imageBytes: ByteArray,
        preparedAssets: PaddleOcrPreparedAssetPaths,
        options: OcrReadOptions = OcrReadOptions(),
        runtimeConfig: PaddleOcrNativeRuntimeConfig = PaddleOcrNativeRuntimeConfig(),
        modelProfile: PaddleOcrOfficialModelProfile = PaddleOcrOfficialModelProfile.PpOcrV5Mobile,
    ): PaddleOcrStructuredResult
}
