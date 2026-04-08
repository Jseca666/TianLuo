package com.tianluo.runtime.template.runtime.task

interface RuntimeTask {
    val taskId: String
    val displayName: String

    suspend fun run(context: TaskContext): TaskResult
}
