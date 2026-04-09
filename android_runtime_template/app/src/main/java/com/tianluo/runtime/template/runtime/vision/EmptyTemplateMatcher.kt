package com.tianluo.runtime.template.runtime.vision

import com.tianluo.runtime.template.runtime.assets.LocatorAsset

class EmptyTemplateMatcher : TemplateMatcher {
    override suspend fun waitFor(
        locator: LocatorAsset,
        threshold: Double,
        timeoutMs: Long,
        maskName: String?,
        useColor: Boolean,
    ): TemplateMatch? = null
}
