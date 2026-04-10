"""V4 main export quality POC: 生成支持 swipe 与更严格 OCR 断言的 Kotlin 任务文本。"""

from pathlib import Path

from task_exporters.main_export_quality_task_builder import MainExportQualityTaskBuilder
from task_exporters.main_export_quality_task_export_session import MainExportQualityTaskExportSession
from examples.main_export_quality_poc_task_factory import build_main_export_quality_task_specs


def main():
    repo_root = Path(__file__).resolve().parents[1]
    builder = MainExportQualityTaskBuilder()
    tasks = [
        builder.build(
            task_id=spec["task_id"],
            display_name=spec["display_name"],
            api_calls=spec["api_calls"],
        )
        for spec in build_main_export_quality_task_specs()
    ]
    result = MainExportQualityTaskExportSession(repo_root).run(tasks)
    print(result)


if __name__ == "__main__":
    main()
