package com.tianluo.runtime.template.runtime.ocr

import com.tianluo.runtime.template.runtime.capture.CaptureEngine

object StructuredPaddleOcrProviderInstaller {
    fun install(
        captureEngine: CaptureEngine,
        bridge: StructuredPaddleOcrRuntimeBridge,
        modelAssets: PaddleOcrModelAssetPaths = PaddleOcrModelAssetPaths(),
        modelProfile: PaddleOcrOfficialModelProfile = PaddleOcrOfficialModelProfile.PpOcrV5Mobile,
    ) {
        OcrEngineProviderRegistry.install(
            StructuredPaddleOcrEngineProvider(
                captureEngine = captureEngine,
                bridge = bridge,
                modelAssets = modelAssets,
                modelProfile = modelProfile,
            )
        )
    }
}
