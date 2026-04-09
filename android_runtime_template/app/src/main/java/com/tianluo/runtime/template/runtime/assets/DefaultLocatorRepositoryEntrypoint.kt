package com.tianluo.runtime.template.runtime.assets

class DefaultLocatorRepositoryEntrypoint(
    private val provider: DefaultFileNameLocatorProvider = DefaultFileNameLocatorProvider(),
) {
    fun get(): AssetLocatorRepository {
        return provider.provideDefault()
    }
}
