package com.tianluo.runtime.template.runtime.ocr

object OcrEngineProviderRegistry {
    private var currentProvider: OcrEngineProvider = EmptyOcrEngineProvider()

    fun current(): OcrEngineProvider = currentProvider

    fun install(provider: OcrEngineProvider) {
        currentProvider = provider
    }

    fun resetToDefault() {
        currentProvider = EmptyOcrEngineProvider()
    }
}
