package com.tianluo.runtime.template.runtime.ocr

import java.io.File

data class PaddleOcrPreparedAssetPaths(
    val detectionModelFile: File,
    val recognitionModelFile: File,
    val classificationModelFile: File? = null,
    val labelsFile: File,
) {
    fun allFiles(): List<File> {
        return buildList {
            add(detectionModelFile)
            add(recognitionModelFile)
            if (classificationModelFile != null) add(classificationModelFile)
            add(labelsFile)
        }
    }
}
