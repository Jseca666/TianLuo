package com.tianluo.runtime.template.runtime.assets

class FileNameLocatorRepositoryProvider(
    private val pathResolver: LocatorAssetPathResolver = LocatorAssetPathResolver(),
    private val factory: AssetLocatorRepositoryFactory = AssetLocatorRepositoryFactory(),
) {
    fun provide(fileName: String): AssetLocatorRepository {
        val assetPath = pathResolver.resolve(fileName)
        return factory.create(assetPath)
    }
}
