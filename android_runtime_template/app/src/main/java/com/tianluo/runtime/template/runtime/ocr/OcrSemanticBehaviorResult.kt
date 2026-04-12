package com.tianluo.runtime.template.runtime.ocr

data class OcrSemanticTextBehaviorResult(
    val texts: List<String>,
    val usedSemanticEngine: Boolean,
    val kernelSizeHintApplied: Boolean,
)

data class OcrSemanticNumberBehaviorResult(
    val number: Int?,
    val usedSemanticEngine: Boolean,
    val kernelSizeHintApplied: Boolean,
    val excludedNumberFiltered: Boolean,
)
