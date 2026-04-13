package com.tianluo.runtime.template.runtime.ocr

import com.tianluo.runtime.template.runtime.capture.CaptureEngine

object PaddleOcrProviderInstaller {
    fun install(
        captureEngine: CaptureEngine,
        bridge: PaddleOcrRuntimeBridge,
        modelAssets: PaddleOcrModelAssetPaths = PaddleOcrModelAssetPaths(),
    ) {
        OcrEngineProviderRegistry.install(
            PaddleOcrEngineProvider(
                captureEngine = captureEngine,
                bridge = bridge,
                modelAssets = modelAssets,
            )
        )
    }
}
