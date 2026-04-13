package com.tianluo.runtime.template.runtime.task

import com.tianluo.runtime.template.runtime.ocr.PaddleOcrModelAssetPaths
import com.tianluo.runtime.template.runtime.ocr.PaddleOcrRuntimeBridge

class PaddleWiredTaskRunner(
    paddleBridge: PaddleOcrRuntimeBridge,
    paddleModelAssets: PaddleOcrModelAssetPaths = PaddleOcrModelAssetPaths(),
    private val context: TaskContext = PaddleWiredTaskContext(
        paddleBridge = paddleBridge,
        paddleModelAssets = paddleModelAssets,
    ),
) {
    suspend fun run(task: RuntimeTask): TaskResult {
        return task.run(context)
    }
}
