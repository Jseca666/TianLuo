package com.tianluo.runtime.template.runtime.ocr

import com.tianluo.runtime.template.runtime.capture.CaptureEngine

class PaddleOcrEngineProvider(
    private val captureEngine: CaptureEngine,
    private val bridge: PaddleOcrRuntimeBridge,
    private val modelAssets: PaddleOcrModelAssetPaths = PaddleOcrModelAssetPaths(),
) : OcrEngineProvider {
    override val providerName: String = "paddleocr"

    override fun createEngine(): OcrEngine {
        return PaddleSemanticOcrEngine(
            captureEngine = captureEngine,
            bridge = bridge,
            modelAssets = modelAssets,
        )
    }

    override fun describe(): OcrRuntimeStatus {
        return OcrRuntimeStatus(
            providerName = providerName,
            engineClassName = PaddleSemanticOcrEngine::class.java.simpleName,
            supportsSemanticOptions = true,
            isPlaceholder = false,
            requiresExternalModelSetup = true,
            notes = listOf(
                "PaddleOCR provider wiring is installed.",
                "A concrete PaddleOcrRuntimeBridge implementation and model assets are still required.",
            ),
        )
    }
}
