package com.tianluo.runtime.template.runtime.vision

import com.tianluo.runtime.template.runtime.assets.LocatorAsset
import com.tianluo.runtime.template.runtime.assets.PointAsset

data class TemplateMatch(
    val center: PointAsset,
    val score: Double,
)

interface TemplateMatcher {
    suspend fun waitFor(
        locator: LocatorAsset,
        threshold: Double = 0.8,
        timeoutMs: Long = 10_000L,
        maskName: String? = null,
        useColor: Boolean = false,
    ): TemplateMatch?
}
