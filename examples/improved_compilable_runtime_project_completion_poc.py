"""V4 improved completion POC: 导出工程并写出 completion 报告。"""

from pathlib import Path

from apk_exporter.improved_compilable_runtime_project_completion_facade import ImprovedCompilableRuntimeProjectCompletionFacade
from examples.exportable_api_realistic_poc_task_factory import build_realistic_demo_task_specs


def main():
    repo_root = Path(__file__).resolve().parents[1]
    facade = ImprovedCompilableRuntimeProjectCompletionFacade(repo_root)
    result = facade.export(
        task_specs=build_realistic_demo_task_specs(),
        output_root=repo_root / "generated_output_completion",
        project_name="GeneratedAndroidProjectCompletion",
        report_output_dir=repo_root / "generated_output_completion_reports",
    )
    print(result)


if __name__ == "__main__":
    main()
