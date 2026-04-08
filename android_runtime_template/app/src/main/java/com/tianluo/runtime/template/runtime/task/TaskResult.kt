package com.tianluo.runtime.template.runtime.task

data class TaskResult(
    val success: Boolean,
    val message: String? = null,
) {
    companion object {
        fun ok(message: String? = null): TaskResult = TaskResult(success = true, message = message)
        fun fail(message: String? = null): TaskResult = TaskResult(success = false, message = message)
    }
}
