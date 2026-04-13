package com.tianluo.runtime.template.runtime.ocr

data class PaddleOcrModelAssetPaths(
    val detectionModelDir: String = "models/paddleocr/det",
    val recognitionModelDir: String = "models/paddleocr/rec",
    val classificationModelDir: String? = "models/paddleocr/cls",
    val labelsPath: String = "models/paddleocr/labels/ppocr_keys_v1.txt",
)
