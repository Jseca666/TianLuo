package com.tianluo.runtime.template.runtime.assets

class DefaultRuntimeAssetBundleProvider(
    private val facade: RuntimeAssetBundleFacade = RuntimeAssetBundleFacade(),
) {
    fun provide(locatorJsonText: String): RuntimeAssetBundle {
        return facade.load(locatorJsonText)
    }
}
