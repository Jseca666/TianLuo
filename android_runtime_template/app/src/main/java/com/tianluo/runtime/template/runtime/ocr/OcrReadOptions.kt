package com.tianluo.runtime.template.runtime.ocr

data class OcrReadOptions(
    val maskName: String? = null,
    val kernelSize: Int? = null,
    val excludedNumber: Int? = null,
)
