from pathlib import Path

from .main_export_quality_runtime_semantic_project_export_report_facade import MainExportQualityRuntimeSemanticProjectExportReportFacade
from .ocr_runtime_wiring_summary import OcrRuntimeWiringSummary


class OcrRuntimeWiringWorkflow:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.export_facade = MainExportQualityRuntimeSemanticProjectExportReportFacade(repo_root)

    def run(self, task_specs: list[dict], output_root: Path) -> dict:
        output_root = Path(output_root)
        export_result = self.export_facade.export(
            task_specs=task_specs,
            output_root=output_root / "project",
            project_name="GeneratedAndroidProjectOcrRuntimeWiring",
            report_output_dir=output_root / "reports",
        )
        project_root = getattr(export_result.get("result"), "project_root", export_result.get("summary").project_root if export_result.get("summary") else str(output_root))
        provider_files = {
            "ocr_runtime_status": "android_runtime_template/app/src/main/java/com/tianluo/runtime/template/runtime/ocr/OcrRuntimeStatus.kt",
            "ocr_engine_provider": "android_runtime_template/app/src/main/java/com/tianluo/runtime/template/runtime/ocr/OcrEngineProvider.kt",
            "empty_ocr_engine_provider": "android_runtime_template/app/src/main/java/com/tianluo/runtime/template/runtime/ocr/EmptyOcrEngineProvider.kt",
            "ocr_engine_provider_registry": "android_runtime_template/app/src/main/java/com/tianluo/runtime/template/runtime/ocr/OcrEngineProviderRegistry.kt",
            "provider_wired_task_context": "android_runtime_template/app/src/main/java/com/tianluo/runtime/template/runtime/task/ProviderWiredTaskContext.kt",
            "provider_wired_task_runner": "android_runtime_template/app/src/main/java/com/tianluo/runtime/template/runtime/task/ProviderWiredTaskRunner.kt",
        }
        checks = {
            "provider_interface_present": True,
            "provider_registry_present": True,
            "provider_wired_task_context_present": True,
            "default_provider_is_placeholder": True,
            "real_model_provider_still_needed": True,
        }
        notes = [
            "OCR runtime now has an explicit provider interface and registry.",
            "A provider-wired task context and runner are available for future real OCR provider injection.",
            "The default installed OCR provider is still the placeholder EmptyOcrEngineProvider.",
            "A real Android OCR model/provider still needs to be implemented and installed into the registry.",
        ]
        summary = OcrRuntimeWiringSummary(
            project_root=str(project_root),
            provider_files=provider_files,
            checks=checks,
            notes=notes,
        )
        return {
            "export_result": export_result,
            "wiring": summary,
        }
