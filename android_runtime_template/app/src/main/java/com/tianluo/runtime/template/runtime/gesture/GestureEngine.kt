package com.tianluo.runtime.template.runtime.gesture

import com.tianluo.runtime.template.runtime.assets.PointAsset

interface GestureEngine {
    suspend fun tap(point: PointAsset): Boolean
    suspend fun swipe(start: PointAsset, end: PointAsset, durationMs: Long = 300L): Boolean
    suspend fun back(): Boolean
}
