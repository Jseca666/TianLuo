package com.tianluo.runtime.template.runtime.ocr

import android.graphics.Bitmap
import android.graphics.BitmapFactory
import com.tianluo.runtime.template.runtime.assets.LocatorAsset
import java.io.ByteArrayOutputStream
import kotlin.math.max
import kotlin.math.min

object PaddleOcrImageRegionExtractor {
    fun cropToLocator(capturedBytes: ByteArray, locator: LocatorAsset): ByteArray? {
        if (capturedBytes.isEmpty()) return null
        val bitmap = BitmapFactory.decodeByteArray(capturedBytes, 0, capturedBytes.size) ?: return null
        val left = locator.rect.topLeft.x
        val top = locator.rect.topLeft.y
        val right = locator.rect.bottomRight.x
        val bottom = locator.rect.bottomRight.y
        val safeLeft = max(0, min(left, bitmap.width - 1))
        val safeTop = max(0, min(top, bitmap.height - 1))
        val safeRight = max(safeLeft + 1, min(right, bitmap.width))
        val safeBottom = max(safeTop + 1, min(bottom, bitmap.height))
        val width = safeRight - safeLeft
        val height = safeBottom - safeTop
        val cropped = Bitmap.createBitmap(bitmap, safeLeft, safeTop, width, height)
        val output = ByteArrayOutputStream()
        cropped.compress(Bitmap.CompressFormat.PNG, 100, output)
        cropped.recycle()
        bitmap.recycle()
        return output.toByteArray()
    }
}
