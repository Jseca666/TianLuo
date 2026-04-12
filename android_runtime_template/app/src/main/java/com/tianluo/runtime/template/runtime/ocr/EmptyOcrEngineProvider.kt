package com.tianluo.runtime.template.runtime.ocr

class EmptyOcrEngineProvider : OcrEngineProvider {
    override val providerName: String = "empty"

    override fun createEngine(): OcrEngine = EmptyOcrEngine()

    override fun describe(): OcrRuntimeStatus {
        return OcrRuntimeStatus(
            providerName = providerName,
            engineClassName = EmptyOcrEngine::class.java.simpleName,
            supportsSemanticOptions = false,
            isPlaceholder = true,
            requiresExternalModelSetup = true,
            notes = listOf(
                "Current OCR engine is a placeholder implementation.",
                "A real Android OCR provider still needs to be wired in.",
            ),
        )
    }
}
