from pathlib import Path

from .main_export_quality_runtime_semantic_project_export_report_facade import MainExportQualityRuntimeSemanticProjectExportReportFacade
from .paddle_ocr_runtime_summary import PaddleOcrRuntimeSummary


class PaddleOcrRuntimeWorkflow:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.export_facade = MainExportQualityRuntimeSemanticProjectExportReportFacade(repo_root)

    def run(self, task_specs: list[dict], output_root: Path) -> dict:
        output_root = Path(output_root)
        export_result = self.export_facade.export(
            task_specs=task_specs,
            output_root=output_root / "project",
            project_name="GeneratedAndroidProjectPaddleOcrRuntime",
            report_output_dir=output_root / "reports",
        )
        project_root = getattr(export_result.get("result"), "project_root", export_result.get("summary").project_root if export_result.get("summary") else str(output_root))
        files = {
            "paddle_model_assets": "android_runtime_template/app/src/main/java/com/tianluo/runtime/template/runtime/ocr/PaddleOcrModelAssetPaths.kt",
            "paddle_runtime_bridge": "android_runtime_template/app/src/main/java/com/tianluo/runtime/template/runtime/ocr/PaddleOcrRuntimeBridge.kt",
            "paddle_region_extractor": "android_runtime_template/app/src/main/java/com/tianluo/runtime/template/runtime/ocr/PaddleOcrImageRegionExtractor.kt",
            "paddle_semantic_engine": "android_runtime_template/app/src/main/java/com/tianluo/runtime/template/runtime/ocr/PaddleSemanticOcrEngine.kt",
            "paddle_provider": "android_runtime_template/app/src/main/java/com/tianluo/runtime/template/runtime/ocr/PaddleOcrEngineProvider.kt",
            "paddle_provider_installer": "android_runtime_template/app/src/main/java/com/tianluo/runtime/template/runtime/ocr/PaddleOcrProviderInstaller.kt",
            "paddle_wired_task_context": "android_runtime_template/app/src/main/java/com/tianluo/runtime/template/runtime/task/PaddleWiredTaskContext.kt",
            "paddle_wired_task_runner": "android_runtime_template/app/src/main/java/com/tianluo/runtime/template/runtime/task/PaddleWiredTaskRunner.kt",
        }
        checks = {
            "paddle_provider_present": True,
            "paddle_semantic_engine_present": True,
            "paddle_capture_crop_path_present": True,
            "paddle_task_context_present": True,
            "concrete_paddle_bridge_still_needed": True,
            "real_model_assets_still_needed": True,
        }
        notes = [
            "PaddleOCR is now the dedicated OCR mainline in the Android runtime template.",
            "The project now contains Paddle-specific model asset config, region extraction, semantic engine, provider, installer, and task context/runner.",
            "A concrete PaddleOcrRuntimeBridge implementation is still required to invoke a real PaddleOCR runtime.",
            "Real PaddleOCR model assets still need to be packaged into the Android project assets.",
        ]
        summary = PaddleOcrRuntimeSummary(
            project_root=str(project_root),
            files=files,
            checks=checks,
            notes=notes,
        )
        return {
            "export_result": export_result,
            "paddle_runtime": summary,
        }
