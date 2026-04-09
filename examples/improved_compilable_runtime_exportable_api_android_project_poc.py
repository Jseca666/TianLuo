"""V4 improved-compilable-runtime POC: 导出更接近真实任务语义的 Android Studio 工程骨架。"""

from pathlib import Path

from apk_exporter.improved_compilable_runtime_exportable_api_android_project_facade import ImprovedCompilableRuntimeExportableApiAndroidProjectFacade
from examples.exportable_api_advanced_poc_task_factory import build_advanced_demo_task_specs


def main():
    repo_root = Path(__file__).resolve().parents[1]
    facade = ImprovedCompilableRuntimeExportableApiAndroidProjectFacade(repo_root)
    result = facade.export(
        task_specs=build_advanced_demo_task_specs(),
        output_root=repo_root / "generated_output_improved_compilable_runtime",
        project_name="GeneratedAndroidProjectImprovedCompilableRuntime",
    )
    print(result)


if __name__ == "__main__":
    main()
