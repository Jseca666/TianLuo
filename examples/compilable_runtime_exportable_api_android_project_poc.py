"""V4 compilable-runtime POC: 导出更接近可编译代码的 Android Studio 工程骨架。"""

from pathlib import Path

from apk_exporter.compilable_runtime_exportable_api_android_project_facade import CompilableRuntimeExportableApiAndroidProjectFacade
from examples.exportable_api_poc_task_factory import build_demo_task_specs


def main():
    repo_root = Path(__file__).resolve().parents[1]
    facade = CompilableRuntimeExportableApiAndroidProjectFacade(repo_root)
    result = facade.export(
        task_specs=build_demo_task_specs(),
        output_root=repo_root / "generated_output_compilable_runtime",
        project_name="GeneratedAndroidProjectCompilableRuntime",
    )
    print(result)


if __name__ == "__main__":
    main()
