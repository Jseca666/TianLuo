package com.tianluo.runtime.template.runtime.ocr

class ExecutorBackedStructuredPaddleOcrRuntimeBridge(
    private val assetMaterializer: PaddleOcrAssetMaterializer,
    private val runtimeExecutor: PaddleOcrRuntimeExecutor,
    private val runtimeConfig: PaddleOcrNativeRuntimeConfig = PaddleOcrNativeRuntimeConfig(),
    private val modelProfile: PaddleOcrOfficialModelProfile = PaddleOcrOfficialModelProfile.PpOcrV5Mobile,
) : StructuredPaddleOcrRuntimeBridge {
    override suspend fun recognizeStructured(
        imageBytes: ByteArray,
        modelAssets: PaddleOcrModelAssetPaths,
        options: OcrReadOptions,
    ): PaddleOcrStructuredResult {
        val preparedAssets = assetMaterializer.prepare(
            modelAssets = modelAssets,
            modelProfile = modelProfile,
        )
        val result = runtimeExecutor.recognize(
            imageBytes = imageBytes,
            preparedAssets = preparedAssets,
            options = options,
            runtimeConfig = runtimeConfig,
            modelProfile = modelProfile,
        )
        return if (result.modelProfileName != null) {
            result
        } else {
            result.copy(modelProfileName = modelProfile.modelName)
        }
    }
}
