package com.tianluo.runtime.template.runtime.assets

class DefaultFileNameLocatorProvider(
    private val provider: FileNameLocatorRepositoryProvider = FileNameLocatorRepositoryProvider(),
) {
    fun provideDefault(): AssetLocatorRepository {
        return provider.provide(DefaultLocatorFiles.DEFAULT)
    }
}
