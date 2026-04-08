package com.tianluo.runtime.template.runtime.vision

interface ImageComparator {
    suspend fun compare(
        frameA: ByteArray,
        frameB: ByteArray,
        threshold: Double = 0.85,
        maskName: String? = null,
        useColor: Boolean = false,
    ): Boolean
}
