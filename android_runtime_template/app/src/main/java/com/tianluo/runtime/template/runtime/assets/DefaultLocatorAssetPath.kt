package com.tianluo.runtime.template.runtime.assets

object DefaultLocatorAssetPath {
    fun value(): String {
        return LocatorAssetPathResolver().resolve(DefaultLocatorFiles.DEFAULT)
    }
}
