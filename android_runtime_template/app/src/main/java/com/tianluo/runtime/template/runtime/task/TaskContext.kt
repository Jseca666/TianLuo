package com.tianluo.runtime.template.runtime.task

import com.tianluo.runtime.template.runtime.assets.AssetLocatorRepository
import com.tianluo.runtime.template.runtime.capture.CaptureEngine
import com.tianluo.runtime.template.runtime.gesture.GestureEngine
import com.tianluo.runtime.template.runtime.ocr.OcrEngine
import com.tianluo.runtime.template.runtime.vision.ImageComparator
import com.tianluo.runtime.template.runtime.vision.TemplateMatcher

interface TaskContext {
    val locatorRepository: AssetLocatorRepository
    val captureEngine: CaptureEngine
    val gestureEngine: GestureEngine
    val templateMatcher: TemplateMatcher
    val ocrEngine: OcrEngine
    val imageComparator: ImageComparator
}
