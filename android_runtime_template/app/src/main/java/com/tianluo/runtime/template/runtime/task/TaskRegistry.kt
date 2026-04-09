package com.tianluo.runtime.template.runtime.task

class TaskRegistry(
    private val tasks: Map<String, RuntimeTask> = emptyMap(),
) {
    fun get(taskId: String): RuntimeTask? = tasks[taskId]

    fun all(): List<RuntimeTask> = tasks.values.toList()
}
