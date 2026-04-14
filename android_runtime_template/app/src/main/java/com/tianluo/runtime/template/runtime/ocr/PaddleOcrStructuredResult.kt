package com.tianluo.runtime.template.runtime.ocr

data class PaddleOcrPoint(
    val x: Int,
    val y: Int,
)

data class PaddleOcrPolygon(
    val points: List<PaddleOcrPoint>,
)

data class PaddleOcrLineResult(
    val text: String,
    val confidence: Float? = null,
    val polygon: PaddleOcrPolygon? = null,
    val angleClassificationLabel: String? = null,
)

data class PaddleOcrStructuredResult(
    val lines: List<PaddleOcrLineResult>,
    val elapsedMs: Long? = null,
    val sourceWidth: Int? = null,
    val sourceHeight: Int? = null,
    val modelProfileName: String? = null,
    val notes: List<String> = emptyList(),
) {
    fun mergedTextLines(): List<String> {
        return lines.mapNotNull { line ->
            line.text.trim().takeIf { text -> text.isNotEmpty() }
        }
    }

    fun mergedText(separator: String = "\n"): String {
        return mergedTextLines().joinToString(separator)
    }

    fun bestInteger(excludedNumber: Int? = null): Int? {
        val parsed = mergedTextLines().asSequence()
            .mapNotNull(::parseFirstInteger)
            .firstOrNull()
        return if (parsed != null && excludedNumber != null && parsed == excludedNumber) {
            null
        } else {
            parsed
        }
    }
}

private fun parseFirstInteger(text: String): Int? {
    val digits = buildString {
        for (char in text) {
            if (char.isDigit() || (length == 0 && char == '-')) {
                append(char)
            } else if (isNotEmpty()) {
                break
            }
        }
    }
    if (digits.isEmpty() || digits == "-") return null
    return digits.toIntOrNull()
}
