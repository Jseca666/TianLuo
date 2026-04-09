package com.tianluo.runtime.template.runtime.assets

class RuntimeAssetBundle(
    val manifest: ExportManifestAsset,
    val locators: Map<String, LocatorAsset> = emptyMap(),
)
