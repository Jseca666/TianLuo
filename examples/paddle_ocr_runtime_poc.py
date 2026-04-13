from pathlib import Path

from apk_exporter.paddle_ocr_runtime_workflow import PaddleOcrRuntimeWorkflow
from apk_exporter.paddle_ocr_runtime_writer import PaddleOcrRuntimeWriter
from examples.main_export_quality_semantic_task_factory import build_main_export_quality_semantic_task_specs


def main():
    repo_root = Path(__file__).resolve().parents[1]
    task_specs = build_main_export_quality_semantic_task_specs()
    workflow = PaddleOcrRuntimeWorkflow(repo_root)
    result = workflow.run(
        task_specs=task_specs,
        output_root=repo_root / "generated_output_paddle_ocr_runtime",
    )
    report_path = PaddleOcrRuntimeWriter().write(
        result,
        repo_root / "generated_output_paddle_ocr_runtime_reports",
    )
    print({"result": result, "paddle_runtime_report_path": report_path})


if __name__ == "__main__":
    main()
