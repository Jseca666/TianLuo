from pathlib import Path
from typing import Iterable

from .main_export_quality_runtime_semantic_project_export_report_facade import MainExportQualityRuntimeSemanticProjectExportReportFacade
from .main_export_quality_runtime_behavior_project_export_report_facade import MainExportQualityRuntimeBehaviorProjectExportReportFacade
from .runtime_behavior_readiness_analyzer import RuntimeBehaviorReadinessAnalyzer


class RuntimeBehaviorComparisonWorkflow:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.runtime_semantic_facade = MainExportQualityRuntimeSemanticProjectExportReportFacade(repo_root)
        self.runtime_behavior_facade = MainExportQualityRuntimeBehaviorProjectExportReportFacade(repo_root)
        self.readiness_analyzer = RuntimeBehaviorReadinessAnalyzer()

    def compare(self, task_specs: Iterable[dict], output_root: Path) -> dict:
        task_specs = list(task_specs)
        output_root = Path(output_root)
        runtime_semantic_quality = self.runtime_semantic_facade.export(
            task_specs=task_specs,
            output_root=output_root / "runtime_semantic_quality",
            project_name="GeneratedAndroidProjectRuntimeSemanticQuality",
            report_output_dir=output_root / "runtime_semantic_quality_reports",
        )
        runtime_behavior_quality = self.runtime_behavior_facade.export(
            task_specs=task_specs,
            output_root=output_root / "runtime_behavior_quality",
            project_name="GeneratedAndroidProjectRuntimeBehaviorQuality",
            report_output_dir=output_root / "runtime_behavior_quality_reports",
        )
        runtime_semantic_behavior = self.readiness_analyzer.analyze(task_specs, runtime_semantic_quality)
        runtime_behavior = self.readiness_analyzer.analyze(task_specs, runtime_behavior_quality)

        notes = []
        if runtime_behavior.read_text_behavior_count > runtime_semantic_behavior.read_text_behavior_count:
            notes.append("Runtime-behavior export adds text behavior helper calls")
        if runtime_behavior.read_number_behavior_count > runtime_semantic_behavior.read_number_behavior_count:
            notes.append("Runtime-behavior export adds number behavior helper calls")
        if runtime_behavior.used_semantic_engine_flag_count > runtime_semantic_behavior.used_semantic_engine_flag_count:
            notes.append("Runtime-behavior export exposes usedSemanticEngine flags")
        if runtime_behavior.kernel_hint_flag_count > runtime_semantic_behavior.kernel_hint_flag_count:
            notes.append("Runtime-behavior export exposes kernelSizeHintApplied flags")
        if runtime_behavior.excluded_filtered_flag_count > runtime_semantic_behavior.excluded_filtered_flag_count:
            notes.append("Runtime-behavior export exposes excludedNumberFiltered flags")

        return {
            "runtime_semantic_quality": runtime_semantic_quality,
            "runtime_behavior_quality": runtime_behavior_quality,
            "runtime_semantic_behavior": runtime_semantic_behavior,
            "runtime_behavior": runtime_behavior,
            "notes": notes,
        }
