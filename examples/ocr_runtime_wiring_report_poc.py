from pathlib import Path

from apk_exporter.ocr_runtime_wiring_workflow import OcrRuntimeWiringWorkflow
from apk_exporter.ocr_runtime_wiring_writer import OcrRuntimeWiringWriter
from examples.main_export_quality_semantic_task_factory import build_main_export_quality_semantic_task_specs


def main():
    repo_root = Path(__file__).resolve().parents[1]
    task_specs = build_main_export_quality_semantic_task_specs()
    workflow = OcrRuntimeWiringWorkflow(repo_root)
    result = workflow.run(
        task_specs=task_specs,
        output_root=repo_root / "generated_output_ocr_runtime_wiring",
    )
    report_path = OcrRuntimeWiringWriter().write(
        result,
        repo_root / "generated_output_ocr_runtime_wiring_reports",
    )
    print({"result": result, "wiring_report_path": report_path})


if __name__ == "__main__":
    main()
