package com.tianluo.runtime.template.runtime.assets

class RuntimeAssetBundleLoader(
    private val textReader: AssetTextReader = AssetTextReader(),
    private val manifestParser: ExportManifestParser = ExportManifestParser(),
    private val locatorParser: LocatorAssetParser = LocatorAssetParser(),
) {
    fun loadManifest(): ExportManifestAsset {
        val json = textReader.read(AssetPaths.EXPORT_MANIFEST)
        return manifestParser.parse(json)
    }

    fun loadLocators(locatorJsonText: String): Map<String, LocatorAsset> {
        return locatorParser.parse(locatorJsonText)
    }
}
