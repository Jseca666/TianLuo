package com.tianluo.runtime.template.runtime.task

import com.tianluo.runtime.template.runtime.assets.AssetLocatorRepository
import com.tianluo.runtime.template.runtime.assets.EmptyLocatorRepository
import com.tianluo.runtime.template.runtime.capture.CaptureEngine
import com.tianluo.runtime.template.runtime.capture.EmptyCaptureEngine
import com.tianluo.runtime.template.runtime.gesture.EmptyGestureEngine
import com.tianluo.runtime.template.runtime.gesture.GestureEngine
import com.tianluo.runtime.template.runtime.ocr.OcrEngine
import com.tianluo.runtime.template.runtime.ocr.PaddleOcrModelAssetPaths
import com.tianluo.runtime.template.runtime.ocr.PaddleOcrRuntimeBridge
import com.tianluo.runtime.template.runtime.ocr.PaddleSemanticOcrEngine
import com.tianluo.runtime.template.runtime.vision.EmptyImageComparator
import com.tianluo.runtime.template.runtime.vision.EmptyTemplateMatcher
import com.tianluo.runtime.template.runtime.vision.ImageComparator
import com.tianluo.runtime.template.runtime.vision.TemplateMatcher

class PaddleWiredTaskContext(
    private val paddleBridge: PaddleOcrRuntimeBridge,
    private val paddleModelAssets: PaddleOcrModelAssetPaths = PaddleOcrModelAssetPaths(),
    override val locatorRepository: AssetLocatorRepository = EmptyLocatorRepository(),
    override val captureEngine: CaptureEngine = EmptyCaptureEngine(),
    override val gestureEngine: GestureEngine = EmptyGestureEngine(),
    override val templateMatcher: TemplateMatcher = EmptyTemplateMatcher(),
    override val imageComparator: ImageComparator = EmptyImageComparator(),
) : TaskContext {
    override val ocrEngine: OcrEngine = PaddleSemanticOcrEngine(
        captureEngine = captureEngine,
        bridge = paddleBridge,
        modelAssets = paddleModelAssets,
    )
}
