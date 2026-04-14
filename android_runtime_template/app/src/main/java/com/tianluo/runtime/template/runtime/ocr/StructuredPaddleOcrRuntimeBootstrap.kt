package com.tianluo.runtime.template.runtime.ocr

import com.tianluo.runtime.template.runtime.capture.CaptureEngine

object StructuredPaddleOcrRuntimeBootstrap {
    fun installProvider(
        captureEngine: CaptureEngine,
        bridge: StructuredPaddleOcrRuntimeBridge,
        modelAssets: PaddleOcrModelAssetPaths = PaddleOcrModelAssetPaths(),
        modelProfile: PaddleOcrOfficialModelProfile = PaddleOcrOfficialModelProfile.PpOcrV5Mobile,
    ) {
        StructuredPaddleOcrProviderInstaller.install(
            captureEngine = captureEngine,
            bridge = bridge,
            modelAssets = modelAssets,
            modelProfile = modelProfile,
        )
    }

    fun currentAssetReadiness(existingAssetPaths: Set<String> = emptySet()): PaddleOcrAssetReadiness {
        return PaddleOcrOfficialAssetReadiness.forModel(
            modelName = "PP-OCRv5_mobile",
            detectionModelDir = "models/paddleocr/det",
            recognitionModelDir = "models/paddleocr/rec",
            classificationModelDir = "models/paddleocr/cls",
            labelsDir = "models/paddleocr/labels",
            existingAssetPaths = existingAssetPaths,
        )
    }

    fun currentStatus(existingAssetPaths: Set<String> = emptySet()): OcrRuntimeStatus {
        val providerStatus = OcrRuntimeBootstrap.currentStatus()
        val assetReadiness = currentAssetReadiness(existingAssetPaths)
        val assetNotes = buildList {
            addAll(providerStatus.notes)
            add("Target model profile defaults to PP-OCRv5_mobile.")
            if (assetReadiness.isReady) {
                add("Official PaddleOCR assets are present for the structured runtime path.")
            } else {
                add("Missing official PaddleOCR assets: ${assetReadiness.missingAssetPaths.joinToString()}")
            }
        }
        return providerStatus.copy(
            requiresExternalModelSetup = !assetReadiness.isReady,
            notes = assetNotes,
        )
    }
}
