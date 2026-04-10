"""V4 main export quality project POC: 导出带更高动作覆盖率的 Android Studio 工程。"""

from pathlib import Path

from apk_exporter.main_export_quality_project_export_facade import MainExportQualityProjectExportFacade
from examples.main_export_quality_poc_task_factory import build_main_export_quality_task_specs


def main():
    repo_root = Path(__file__).resolve().parents[1]
    facade = MainExportQualityProjectExportFacade(repo_root)
    result = facade.export(
        task_specs=build_main_export_quality_task_specs(),
        output_root=repo_root / "generated_output_main_export_quality",
        project_name="GeneratedAndroidProjectMainExportQuality",
    )
    print(result)


if __name__ == "__main__":
    main()
