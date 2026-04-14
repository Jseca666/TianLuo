from pathlib import Path

from .main_export_quality_runtime_semantic_project_export_report_facade import MainExportQualityRuntimeSemanticProjectExportReportFacade
from .paddle_ocr_asset_prep_summary import PaddleOcrAssetPrepSummary
from .paddle_ocr_host_prep_script_writer import PaddleOcrHostPrepScriptWriter


class PaddleOcrAssetPrepWorkflow:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.export_facade = MainExportQualityRuntimeSemanticProjectExportReportFacade(repo_root)
        self.script_writer = PaddleOcrHostPrepScriptWriter()

    def run(self, task_specs: list[dict], output_root: Path) -> dict:
        output_root = Path(output_root)
        export_result = self.export_facade.export(
            task_specs=task_specs,
            output_root=output_root / "project",
            project_name="GeneratedAndroidProjectPaddleOcrAssets",
            report_output_dir=output_root / "reports",
        )
        result_obj = export_result.get("result") if isinstance(export_result, dict) else None
        summary_obj = export_result.get("summary") if isinstance(export_result, dict) else None
        project_root = str(getattr(result_obj, "project_root", getattr(summary_obj, "project_root", output_root)))
        host_scripts = self.script_writer.write(Path(project_root))
        expected_assets = {
            "det_model_dir": "app/src/main/assets/models/paddleocr/det",
            "rec_model_dir": "app/src/main/assets/models/paddleocr/rec",
            "cls_model_dir": "app/src/main/assets/models/paddleocr/cls",
            "labels_file": "app/src/main/assets/models/paddleocr/labels/ppocr_keys_v1.txt",
            "official_shell_assets_dir": "PaddleX-Lite-Deploy/ocr/assets",
            "official_shell_demo_dir": "PaddleX-Lite-Deploy/ocr/android/shell/ppocr_demo",
        }
        checks = {
            "host_scripts_written": True,
            "app_asset_layout_declared": True,
            "official_demo_clone_required": True,
            "paddle_lite_download_required": True,
            "ppocr_asset_download_required": True,
        }
        commands = [
            "bash host_tools/paddle_ocr/clone_paddlex_lite_deploy.sh",
            "bash host_tools/paddle_ocr/prepare_paddle_lite_libs.sh",
            "bash host_tools/paddle_ocr/prepare_ppocr_assets.sh PP-OCRv5_mobile",
            "bash host_tools/paddle_ocr/build_ppocr_demo.sh",
            "bash host_tools/paddle_ocr/run_ppocr_demo.sh PP-OCRv5_mobile",
        ]
        notes = [
            "This preparation flow follows the official PaddleOCR Android on-device deployment sequence.",
            "Real PaddleOCR model files are prepared by host-side scripts rather than committed directly to the main repository branch.",
            "PP-OCRv5_mobile is the default model in the generated preparation commands.",
        ]
        summary = PaddleOcrAssetPrepSummary(
            project_root=project_root,
            host_scripts=host_scripts,
            expected_assets=expected_assets,
            checks=checks,
            commands=commands,
            notes=notes,
        )
        return {
            "export_result": export_result,
            "asset_prep": summary,
        }
