package com.tianluo.runtime.template.runtime.assets

interface AssetLocatorRepository {
    fun get(locatorName: String): LocatorAsset
}
