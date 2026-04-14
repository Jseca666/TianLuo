package com.tianluo.runtime.template.runtime.ocr

interface PaddleOcrAssetLoader {
    fun exists(assetPath: String): Boolean

    fun loadBytes(assetPath: String): ByteArray
}
