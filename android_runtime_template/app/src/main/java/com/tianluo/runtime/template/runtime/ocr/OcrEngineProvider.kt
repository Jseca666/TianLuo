package com.tianluo.runtime.template.runtime.ocr

interface OcrEngineProvider {
    val providerName: String

    fun createEngine(): OcrEngine

    fun describe(): OcrRuntimeStatus
}
