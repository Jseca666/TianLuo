package com.tianluo.runtime.template.runtime.assets

class EmptyLocatorRepository : AssetLocatorRepository {
    override fun get(locatorName: String): LocatorAsset {
        throw UnsupportedOperationException("Locator repository not initialized")
    }
}
