package com.tianluo.runtime.template.runtime.ocr

import java.io.File

class AssetLoaderBackedPaddleOcrAssetMaterializer(
    private val assetLoader: PaddleOcrAssetLoader,
    private val outputRoot: File,
) : PaddleOcrAssetMaterializer {
    override suspend fun prepare(
        modelAssets: PaddleOcrModelAssetPaths,
        modelProfile: PaddleOcrOfficialModelProfile,
    ): PaddleOcrPreparedAssetPaths {
        outputRoot.mkdirs()
        val expected = modelProfile.expectedAssetPaths(modelAssets)
        val detectionModel = materialize(expected.getValue("detection_model"))
        val recognitionModel = materialize(expected.getValue("recognition_model"))
        val classificationModel = expected["classification_model"]?.let(::materialize)
        val labelsFile = materialize(expected.getValue("labels"))
        return PaddleOcrPreparedAssetPaths(
            detectionModelFile = detectionModel,
            recognitionModelFile = recognitionModel,
            classificationModelFile = classificationModel,
            labelsFile = labelsFile,
        )
    }

    private fun materialize(assetPath: String): File {
        require(assetLoader.exists(assetPath)) { "Missing PaddleOCR asset: $assetPath" }
        val file = File(outputRoot, assetPath.substringAfterLast('/'))
        if (file.exists() && file.length() > 0L) {
            return file
        }
        file.parentFile?.mkdirs()
        file.writeBytes(assetLoader.loadBytes(assetPath))
        return file
    }
}
