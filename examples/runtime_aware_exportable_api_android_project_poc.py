"""V4 runtime-aware POC: 通过代表性 API 调用列表导出 Android Studio 工程骨架。"""

from pathlib import Path

from apk_exporter.runtime_aware_exportable_api_android_project_facade import RuntimeAwareExportableApiAndroidProjectFacade
from examples.exportable_api_poc_task_factory import build_demo_task_specs


def main():
    repo_root = Path(__file__).resolve().parents[1]
    facade = RuntimeAwareExportableApiAndroidProjectFacade(repo_root)
    result = facade.export(
        task_specs=build_demo_task_specs(),
        output_root=repo_root / "generated_output_runtime",
        project_name="GeneratedAndroidProjectRuntimeAware",
    )
    print(result)


if __name__ == "__main__":
    main()
