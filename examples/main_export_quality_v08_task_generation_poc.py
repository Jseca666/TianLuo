"""V0.8 main export quality alias-friendly POC: 使用增强别名映射生成更贴近 PC 端叫法的 Kotlin 任务文本。"""

from pathlib import Path

from examples.main_export_quality_v08_alias_task_factory import build_main_export_quality_v08_alias_task_specs
from task_exporters.main_export_quality_v08_task_builder import MainExportQualityV08TaskBuilder
from task_exporters.main_export_quality_v08_task_export_session import MainExportQualityV08TaskExportSession


def main():
    repo_root = Path(__file__).resolve().parents[1]
    builder = MainExportQualityV08TaskBuilder()
    tasks = [
        builder.build(
            task_id=spec["task_id"],
            display_name=spec["display_name"],
            api_calls=spec["api_calls"],
        )
        for spec in build_main_export_quality_v08_alias_task_specs()
    ]
    result = MainExportQualityV08TaskExportSession(repo_root).run(tasks)
    print(result)


if __name__ == "__main__":
    main()
