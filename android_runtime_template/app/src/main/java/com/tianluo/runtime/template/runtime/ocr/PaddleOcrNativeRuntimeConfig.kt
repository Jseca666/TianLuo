package com.tianluo.runtime.template.runtime.ocr

data class PaddleOcrNativeRuntimeConfig(
    val cpuThreadCount: Int = 4,
    val cpuPowerMode: String = "LITE_POWER_HIGH",
    val enableFp16: Boolean = false,
    val enableVerboseLog: Boolean = false,
)
