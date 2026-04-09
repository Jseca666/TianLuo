"""V4 POC: 通过最小 API 调用列表导出 Android Studio 工程骨架。"""

from pathlib import Path

from apk_exporter.exportable_api_android_project_exporter import ExportableApiAndroidProjectExporter


def main():
    repo_root = Path(__file__).resolve().parents[1]
    exporter = ExportableApiAndroidProjectExporter(repo_root)

    task_specs = [
        {
            "task_id": "demo_sleep_and_back",
            "display_name": "Demo Sleep And Back",
            "api_calls": [
                {"api_name": "sleep", "params": {"seconds": 1}},
                {"api_name": "back", "params": {}},
            ],
        }
    ]

    result = exporter.export(
        task_specs=task_specs,
        output_root=repo_root / "generated_output",
        project_name="GeneratedAndroidProjectDemo",
    )

    print(result)


if __name__ == "__main__":
    main()
