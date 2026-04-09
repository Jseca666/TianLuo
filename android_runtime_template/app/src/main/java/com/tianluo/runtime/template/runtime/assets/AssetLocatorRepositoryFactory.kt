package com.tianluo.runtime.template.runtime.assets

class AssetLocatorRepositoryFactory(
    private val source: LocatorAssetSource = LocatorAssetSource(),
    private val provider: DefaultLocatorRepositoryProvider = DefaultLocatorRepositoryProvider(),
) {
    fun create(locatorAssetPath: String): AssetLocatorRepository {
        val locatorJsonText = source.read(locatorAssetPath)
        return provider.provide(locatorJsonText)
    }
}
