package com.tianluo.runtime.template.runtime.task

import com.tianluo.runtime.template.runtime.assets.AssetLocatorRepository
import com.tianluo.runtime.template.runtime.assets.EmptyLocatorRepository
import com.tianluo.runtime.template.runtime.capture.CaptureEngine
import com.tianluo.runtime.template.runtime.capture.EmptyCaptureEngine
import com.tianluo.runtime.template.runtime.gesture.EmptyGestureEngine
import com.tianluo.runtime.template.runtime.gesture.GestureEngine
import com.tianluo.runtime.template.runtime.ocr.OcrEngine
import com.tianluo.runtime.template.runtime.ocr.OcrEngineProviderRegistry
import com.tianluo.runtime.template.runtime.vision.EmptyImageComparator
import com.tianluo.runtime.template.runtime.vision.EmptyTemplateMatcher
import com.tianluo.runtime.template.runtime.vision.ImageComparator
import com.tianluo.runtime.template.runtime.vision.TemplateMatcher

class ProviderWiredTaskContext(
    override val locatorRepository: AssetLocatorRepository = EmptyLocatorRepository(),
    override val captureEngine: CaptureEngine = EmptyCaptureEngine(),
    override val gestureEngine: GestureEngine = EmptyGestureEngine(),
    override val templateMatcher: TemplateMatcher = EmptyTemplateMatcher(),
    override val ocrEngine: OcrEngine = OcrEngineProviderRegistry.current().createEngine(),
    override val imageComparator: ImageComparator = EmptyImageComparator(),
) : TaskContext
