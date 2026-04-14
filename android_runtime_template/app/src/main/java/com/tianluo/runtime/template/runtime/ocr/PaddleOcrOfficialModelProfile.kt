package com.tianluo.runtime.template.runtime.ocr

data class PaddleOcrOfficialModelProfile(
    val modelName: String = "PP-OCRv5_mobile",
    val detectionModelFileName: String = "PP-OCRv5_mobile_det.nb",
    val recognitionModelFileName: String = "PP-OCRv5_mobile_rec.nb",
    val classificationModelFileName: String = "ch_ppocr_mobile_v2.0_cls_slim_opt.nb",
    val labelsFileName: String = "ppocr_keys_v1.txt",
) {
    fun detectionModelAssetPath(paths: PaddleOcrModelAssetPaths = PaddleOcrModelAssetPaths()): String {
        return joinAssetPath(paths.detectionModelDir, detectionModelFileName)
    }

    fun recognitionModelAssetPath(paths: PaddleOcrModelAssetPaths = PaddleOcrModelAssetPaths()): String {
        return joinAssetPath(paths.recognitionModelDir, recognitionModelFileName)
    }

    fun classificationModelAssetPath(paths: PaddleOcrModelAssetPaths = PaddleOcrModelAssetPaths()): String? {
        val dir = paths.classificationModelDir ?: return null
        return joinAssetPath(dir, classificationModelFileName)
    }

    fun labelsAssetPath(paths: PaddleOcrModelAssetPaths = PaddleOcrModelAssetPaths()): String {
        return joinAssetPath(paths.labelsPath.substringBeforeLast('/', missingDelimiterValue = ""), labelsFileName)
    }

    fun expectedAssetPaths(paths: PaddleOcrModelAssetPaths = PaddleOcrModelAssetPaths()): Map<String, String> {
        val values = linkedMapOf(
            "detection_model" to detectionModelAssetPath(paths),
            "recognition_model" to recognitionModelAssetPath(paths),
            "labels" to labelsAssetPath(paths),
        )
        val classification = classificationModelAssetPath(paths)
        if (classification != null) {
            values["classification_model"] = classification
        }
        return values
    }

    companion object {
        val PpOcrV5Mobile: PaddleOcrOfficialModelProfile = PaddleOcrOfficialModelProfile()
    }
}

private fun joinAssetPath(directory: String, fileName: String): String {
    val normalizedDirectory = directory.trimEnd('/').takeIf { it.isNotEmpty() } ?: return fileName
    return "$normalizedDirectory/$fileName"
}
