package com.tianluo.runtime.template.runtime.ocr

interface PaddleOcrAssetMaterializer {
    suspend fun prepare(
        modelAssets: PaddleOcrModelAssetPaths = PaddleOcrModelAssetPaths(),
        modelProfile: PaddleOcrOfficialModelProfile = PaddleOcrOfficialModelProfile.PpOcrV5Mobile,
    ): PaddleOcrPreparedAssetPaths
}
