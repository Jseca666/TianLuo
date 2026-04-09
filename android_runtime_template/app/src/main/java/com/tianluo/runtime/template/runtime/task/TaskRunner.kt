package com.tianluo.runtime.template.runtime.task

class TaskRunner(
    private val context: TaskContext = DefaultTaskContext(),
) {
    suspend fun run(task: RuntimeTask): TaskResult {
        return task.run(context)
    }
}
