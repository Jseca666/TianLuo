"""V4 realistic improved-compilable-runtime POC: 使用更接近现有脚本命名的 API 组合导出工程。"""

from pathlib import Path

from apk_exporter.improved_builder_compilable_runtime_exportable_api_android_project_facade import ImprovedBuilderCompilableRuntimeExportableApiAndroidProjectFacade
from examples.exportable_api_realistic_poc_task_factory import build_realistic_demo_task_specs


def main():
    repo_root = Path(__file__).resolve().parents[1]
    facade = ImprovedBuilderCompilableRuntimeExportableApiAndroidProjectFacade(repo_root)
    result = facade.export(
        task_specs=build_realistic_demo_task_specs(),
        output_root=repo_root / "generated_output_realistic_improved",
        project_name="GeneratedAndroidProjectRealisticImproved",
    )
    print(result)


if __name__ == "__main__":
    main()
