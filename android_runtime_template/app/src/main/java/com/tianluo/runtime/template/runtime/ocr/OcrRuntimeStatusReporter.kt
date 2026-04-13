package com.tianluo.runtime.template.runtime.ocr

object OcrRuntimeStatusReporter {
    fun asText(status: OcrRuntimeStatus = OcrRuntimeBootstrap.currentStatus()): String {
        val notesText = if (status.notes.isEmpty()) {
            ""
        } else {
            status.notes.joinToString(separator = " | ", prefix = " notes=")
        }
        return "provider=${status.providerName}, engine=${status.engineClassName}, semantic=${status.supportsSemanticOptions}, placeholder=${status.isPlaceholder}, externalSetup=${status.requiresExternalModelSetup}${notesText}"
    }
}
