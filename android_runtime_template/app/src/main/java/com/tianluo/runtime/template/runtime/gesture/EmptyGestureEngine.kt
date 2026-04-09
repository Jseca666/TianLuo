package com.tianluo.runtime.template.runtime.gesture

import com.tianluo.runtime.template.runtime.assets.PointAsset

class EmptyGestureEngine : GestureEngine {
    override suspend fun tap(point: PointAsset): Boolean = false

    override suspend fun swipe(start: PointAsset, end: PointAsset, durationMs: Long): Boolean = false

    override suspend fun back(): Boolean = false
}
