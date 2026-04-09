package com.tianluo.runtime.template.runtime.assets

class DirectDefaultLocatorRepository(
    private val factory: AssetLocatorRepositoryFactory = AssetLocatorRepositoryFactory(),
) {
    fun get(): AssetLocatorRepository {
        return factory.create(DefaultLocatorAssetPath.value())
    }
}
