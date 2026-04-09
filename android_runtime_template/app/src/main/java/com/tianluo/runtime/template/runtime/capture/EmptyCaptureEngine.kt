package com.tianluo.runtime.template.runtime.capture

class EmptyCaptureEngine : CaptureEngine {
    override suspend fun captureToBytes(): ByteArray {
        return ByteArray(0)
    }
}
