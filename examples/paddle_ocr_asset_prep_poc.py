from pathlib import Path

from apk_exporter.paddle_ocr_asset_prep_workflow import PaddleOcrAssetPrepWorkflow
from apk_exporter.paddle_ocr_asset_prep_writer import PaddleOcrAssetPrepWriter
from examples.main_export_quality_semantic_task_factory import build_main_export_quality_semantic_task_specs


def main():
    repo_root = Path(__file__).resolve().parents[1]
    task_specs = build_main_export_quality_semantic_task_specs()
    workflow = PaddleOcrAssetPrepWorkflow(repo_root)
    result = workflow.run(
        task_specs=task_specs,
        output_root=repo_root / "generated_output_paddle_ocr_asset_prep",
    )
    report_path = PaddleOcrAssetPrepWriter().write(
        result,
        repo_root / "generated_output_paddle_ocr_asset_prep_reports",
    )
    print({"result": result, "asset_prep_report_path": report_path})


if __name__ == "__main__":
    main()
