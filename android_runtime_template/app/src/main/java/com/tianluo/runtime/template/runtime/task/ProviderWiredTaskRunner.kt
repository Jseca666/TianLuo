package com.tianluo.runtime.template.runtime.task

class ProviderWiredTaskRunner(
    private val context: TaskContext = ProviderWiredTaskContext(),
) {
    suspend fun run(task: RuntimeTask): TaskResult {
        return task.run(context)
    }
}
