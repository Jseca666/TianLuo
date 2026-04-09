package com.tianluo.runtime.template.runtime.assets

class DefaultLocatorRepositoryProvider(
    private val bundleProvider: DefaultRuntimeAssetBundleProvider = DefaultRuntimeAssetBundleProvider(),
) {
    fun provide(locatorJsonText: String): AssetLocatorRepository {
        val bundle = bundleProvider.provide(locatorJsonText)
        return BundleLocatorRepository(bundle)
    }
}
