package com.tianluo.runtime.template.runtime.ocr

import com.tianluo.runtime.template.runtime.capture.CaptureEngine

class StructuredPaddleOcrEngineProvider(
    private val captureEngine: CaptureEngine,
    private val bridge: StructuredPaddleOcrRuntimeBridge,
    private val modelAssets: PaddleOcrModelAssetPaths = PaddleOcrModelAssetPaths(),
    private val modelProfile: PaddleOcrOfficialModelProfile = PaddleOcrOfficialModelProfile.PpOcrV5Mobile,
) : OcrEngineProvider {
    override val providerName: String = "paddleocr-structured"

    override fun createEngine(): OcrEngine {
        return StructuredPaddleSemanticOcrEngine(
            captureEngine = captureEngine,
            bridge = bridge,
            modelAssets = modelAssets,
            modelProfile = modelProfile,
        )
    }

    override fun describe(): OcrRuntimeStatus {
        return OcrRuntimeStatus(
            providerName = providerName,
            engineClassName = StructuredPaddleSemanticOcrEngine::class.java.simpleName,
            supportsSemanticOptions = true,
            isPlaceholder = false,
            requiresExternalModelSetup = true,
            notes = listOf(
                "Structured PaddleOCR provider wiring is installed.",
                "Target model profile defaults to ${modelProfile.modelName}.",
                "A concrete StructuredPaddleOcrRuntimeBridge implementation is still required.",
                "Official .nb model assets still need to be packaged into the Android project assets.",
            ),
        )
    }
}
