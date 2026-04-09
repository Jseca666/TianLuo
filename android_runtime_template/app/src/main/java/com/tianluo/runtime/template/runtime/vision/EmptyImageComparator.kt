package com.tianluo.runtime.template.runtime.vision

class EmptyImageComparator : ImageComparator {
    override suspend fun compare(
        frameA: ByteArray,
        frameB: ByteArray,
        threshold: Double,
        maskName: String?,
        useColor: Boolean,
    ): Boolean = false
}
