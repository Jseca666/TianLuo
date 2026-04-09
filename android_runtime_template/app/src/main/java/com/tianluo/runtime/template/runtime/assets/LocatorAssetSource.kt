package com.tianluo.runtime.template.runtime.assets

class LocatorAssetSource(
    private val textReader: AssetTextReader = AssetTextReader(),
) {
    fun read(path: String): String {
        return textReader.read(path)
    }
}
