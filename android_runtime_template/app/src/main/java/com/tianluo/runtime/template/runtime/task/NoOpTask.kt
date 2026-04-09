package com.tianluo.runtime.template.runtime.task

class NoOpTask : RuntimeTask {
    override val taskId: String = "noop"
    override val displayName: String = "No Op Task"

    override suspend fun run(context: TaskContext): TaskResult {
        return TaskResult.ok("No-op task executed")
    }
}
