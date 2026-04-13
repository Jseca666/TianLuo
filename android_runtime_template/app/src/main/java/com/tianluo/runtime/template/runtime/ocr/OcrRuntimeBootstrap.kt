package com.tianluo.runtime.template.runtime.ocr

object OcrRuntimeBootstrap {
    fun installProvider(provider: OcrEngineProvider) {
        OcrEngineProviderRegistry.install(provider)
    }

    fun resetToDefault() {
        OcrEngineProviderRegistry.resetToDefault()
    }

    fun currentStatus(): OcrRuntimeStatus {
        return OcrEngineProviderRegistry.current().describe()
    }
}
