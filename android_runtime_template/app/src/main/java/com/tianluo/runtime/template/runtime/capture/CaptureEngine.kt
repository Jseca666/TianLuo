package com.tianluo.runtime.template.runtime.capture

interface CaptureEngine {
    suspend fun captureToBytes(): ByteArray
}
