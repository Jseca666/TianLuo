from pathlib import Path
from typing import Iterable

from .main_android_project_export_facade import MainAndroidProjectExportFacade
from .main_export_quality_semantic_project_export_report_facade import MainExportQualitySemanticProjectExportReportFacade
from .semantic_parameter_readiness_analyzer import SemanticParameterReadinessAnalyzer


class SemanticParameterComparisonWorkflow:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.main_facade = MainAndroidProjectExportFacade(repo_root)
        self.semantic_facade = MainExportQualitySemanticProjectExportReportFacade(repo_root)
        self.readiness_analyzer = SemanticParameterReadinessAnalyzer()

    def compare(self, task_specs: Iterable[dict], output_root: Path) -> dict:
        task_specs = list(task_specs)
        output_root = Path(output_root)
        baseline = self.main_facade.export(
            task_specs=task_specs,
            output_root=output_root / "baseline",
            project_name="GeneratedAndroidProjectBaseline",
            report_output_dir=output_root / "baseline_reports",
        )
        semantic_quality = self.semantic_facade.export(
            task_specs=task_specs,
            output_root=output_root / "semantic_quality",
            project_name="GeneratedAndroidProjectSemanticQuality",
            report_output_dir=output_root / "semantic_quality_reports",
        )
        baseline_semantic = self.readiness_analyzer.analyze(task_specs, baseline)
        quality_semantic = self.readiness_analyzer.analyze(task_specs, semantic_quality)

        notes = []
        if quality_semantic.propagated_threshold_count > baseline_semantic.propagated_threshold_count:
            notes.append("Semantic quality export propagates more threshold parameters than baseline")
        if quality_semantic.propagated_mask_name_count > baseline_semantic.propagated_mask_name_count:
            notes.append("Semantic quality export propagates more mask_name parameters than baseline")
        if quality_semantic.propagated_use_color_count > baseline_semantic.propagated_use_color_count:
            notes.append("Semantic quality export propagates more use_color parameters than baseline")
        if quality_semantic.semantic_kernel_note_count >= baseline_semantic.semantic_kernel_note_count and quality_semantic.expected_kernel_size_steps > 0:
            notes.append("Semantic quality export preserves kernel_size semantic gap visibility")
        if quality_semantic.semantic_excluded_number_note_count >= baseline_semantic.semantic_excluded_number_note_count and quality_semantic.expected_excluded_number_steps > 0:
            notes.append("Semantic quality export preserves excluded_number semantic gap visibility")

        return {
            "baseline": baseline,
            "semantic_quality": semantic_quality,
            "baseline_semantic": baseline_semantic,
            "quality_semantic": quality_semantic,
            "notes": notes,
        }
