package com.tianluo.runtime.template.runtime.assets

class RuntimeAssetBundleFacade(
    private val loader: RuntimeAssetBundleLoader = RuntimeAssetBundleLoader(),
) {
    fun load(locatorJsonText: String): RuntimeAssetBundle {
        val manifest = loader.loadManifest()
        val locators = loader.loadLocators(locatorJsonText)
        return RuntimeAssetBundle(
            manifest = manifest,
            locators = locators,
        )
    }
}
