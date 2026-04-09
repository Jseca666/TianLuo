package com.tianluo.runtime.template.runtime.assets

class JsonAssetLocatorRepository : AssetLocatorRepository {
    override fun get(locatorName: String): LocatorAsset {
        throw UnsupportedOperationException("JSON asset loading is not implemented yet")
    }
}
