package com.tianluo.runtime.template.runtime.ocr

data class PaddleOcrAssetReadiness(
    val modelName: String,
    val expectedAssetPaths: Map<String, String>,
    val missingAssetPaths: List<String>,
    val notes: List<String> = emptyList(),
) {
    val isReady: Boolean
        get() = missingAssetPaths.isEmpty()
}

object PaddleOcrOfficialAssetReadiness {
    fun forModel(
        modelName: String = "PP-OCRv5_mobile",
        detectionModelDir: String = "models/paddleocr/det",
        recognitionModelDir: String = "models/paddleocr/rec",
        classificationModelDir: String? = "models/paddleocr/cls",
        labelsDir: String = "models/paddleocr/labels",
        existingAssetPaths: Set<String> = emptySet(),
    ): PaddleOcrAssetReadiness {
        val labelsFileName = when (modelName) {
            "PP-OCRv5_mobile" -> "ppocr_keys_ocrv5.txt"
            else -> "ppocr_keys_v1.txt"
        }
        val expected = linkedMapOf(
            "detection_model" to joinAssetPath(detectionModelDir, "${modelName}_det.nb"),
            "recognition_model" to joinAssetPath(recognitionModelDir, "${modelName}_rec.nb"),
            "labels" to joinAssetPath(labelsDir, labelsFileName),
        )
        if (classificationModelDir != null) {
            expected["classification_model"] = joinAssetPath(classificationModelDir, "ch_ppocr_mobile_v2.0_cls_slim_opt.nb")
        }
        val missing = expected.values.filterNot { path -> existingAssetPaths.contains(path) }
        return PaddleOcrAssetReadiness(
            modelName = modelName,
            expectedAssetPaths = expected,
            missingAssetPaths = missing,
            notes = listOf(
                "Official PaddleOCR Android on-device flow expects detection, recognition, and optional classification .nb assets.",
                "PP-OCRv5_mobile uses the ppocr_keys_ocrv5.txt label dictionary in the official demo.",
            ),
        )
    }
}

private fun joinAssetPath(directory: String, fileName: String): String {
    val normalizedDirectory = directory.trimEnd('/').takeIf { it.isNotEmpty() } ?: return fileName
    return "$normalizedDirectory/$fileName"
}
