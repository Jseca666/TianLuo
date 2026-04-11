from pathlib import Path
from typing import Iterable

from .main_export_quality_semantic_project_export_report_facade import MainExportQualitySemanticProjectExportReportFacade
from .main_export_quality_runtime_semantic_project_export_report_facade import MainExportQualityRuntimeSemanticProjectExportReportFacade
from .runtime_semantic_readiness_analyzer import RuntimeSemanticReadinessAnalyzer


class RuntimeSemanticComparisonWorkflow:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.semantic_facade = MainExportQualitySemanticProjectExportReportFacade(repo_root)
        self.runtime_semantic_facade = MainExportQualityRuntimeSemanticProjectExportReportFacade(repo_root)
        self.readiness_analyzer = RuntimeSemanticReadinessAnalyzer()

    def compare(self, task_specs: Iterable[dict], output_root: Path) -> dict:
        task_specs = list(task_specs)
        output_root = Path(output_root)
        semantic_quality = self.semantic_facade.export(
            task_specs=task_specs,
            output_root=output_root / "semantic_quality",
            project_name="GeneratedAndroidProjectSemanticQuality",
            report_output_dir=output_root / "semantic_quality_reports",
        )
        runtime_semantic_quality = self.runtime_semantic_facade.export(
            task_specs=task_specs,
            output_root=output_root / "runtime_semantic_quality",
            project_name="GeneratedAndroidProjectRuntimeSemanticQuality",
            report_output_dir=output_root / "runtime_semantic_quality_reports",
        )
        semantic_runtime = self.readiness_analyzer.analyze(task_specs, semantic_quality)
        runtime_semantic_runtime = self.readiness_analyzer.analyze(task_specs, runtime_semantic_quality)

        notes = []
        if runtime_semantic_runtime.ocr_read_options_count > semantic_runtime.ocr_read_options_count:
            notes.append("Runtime-semantic export adds OCR read options to generated code")
        if runtime_semantic_runtime.kernel_size_option_count > semantic_runtime.kernel_size_option_count:
            notes.append("Runtime-semantic export carries kernel_size deeper into generated code")
        if runtime_semantic_runtime.excluded_number_option_count > semantic_runtime.excluded_number_option_count:
            notes.append("Runtime-semantic export carries excluded_number deeper into generated code")
        if runtime_semantic_runtime.read_text_semantic_count > semantic_runtime.read_text_semantic_count:
            notes.append("Runtime-semantic export adds readTextSemantic helper calls")
        if runtime_semantic_runtime.read_number_semantic_count > semantic_runtime.read_number_semantic_count:
            notes.append("Runtime-semantic export adds readNumberSemantic helper calls")

        return {
            "semantic_quality": semantic_quality,
            "runtime_semantic_quality": runtime_semantic_quality,
            "semantic_runtime": semantic_runtime,
            "runtime_semantic_runtime": runtime_semantic_runtime,
            "notes": notes,
        }
