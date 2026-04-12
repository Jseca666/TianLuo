package com.tianluo.runtime.template.runtime.ocr

data class OcrRuntimeStatus(
    val providerName: String,
    val engineClassName: String,
    val supportsSemanticOptions: Boolean,
    val isPlaceholder: Boolean,
    val requiresExternalModelSetup: Boolean,
    val notes: List<String> = emptyList(),
)
