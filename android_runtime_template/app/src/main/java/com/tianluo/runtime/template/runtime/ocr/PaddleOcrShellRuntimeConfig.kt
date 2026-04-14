package com.tianluo.runtime.template.runtime.ocr

import java.io.File

data class PaddleOcrShellRuntimeConfig(
    val executableFile: File,
    val workingDirectory: File,
    val configFile: File,
    val outputImageFileName: String = "ocr_result.jpg",
    val inputImageFileName: String = "ocr_input.jpg",
    val librarySearchPaths: List<File> = emptyList(),
    val clearWorkingDirectoryBeforeRun: Boolean = false,
)
