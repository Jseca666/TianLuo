package com.tianluo.runtime.template.runtime.assets

class LocatorAssetPathResolver {
    fun resolve(fileName: String): String {
        return "${AssetPaths.LOCATORS_DIR}/$fileName"
    }
}
