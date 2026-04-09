package com.tianluo.runtime.template.runtime.assets

class BundleLocatorRepository(
    private val bundle: RuntimeAssetBundle,
) : AssetLocatorRepository {
    override fun get(locatorName: String): LocatorAsset {
        return bundle.locators[locatorName]
            ?: throw IllegalArgumentException("Locator not found: $locatorName")
    }
}
