from pathlib import Path
from typing import Iterable

from .delivery_ready_compilable_runtime_project_delivery_report_facade import DeliveryReadyCompilableRuntimeProjectDeliveryReportFacade
from .delivery_ready_compilable_runtime_project_report_summary import DeliveryReadyCompilableRuntimeProjectReportSummary


class DeliveryReadyCompilableRuntimeProjectReportSummaryFacade:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.facade = DeliveryReadyCompilableRuntimeProjectDeliveryReportFacade(repo_root)

    def export(self, task_specs: Iterable[dict], output_root: Path, project_name: str = "GeneratedAndroidProject", report_output_dir: Path | None = None) -> dict:
        result = self.facade.export(
            task_specs=task_specs,
            output_root=output_root,
            project_name=project_name,
            report_output_dir=report_output_dir,
        )
        export_result = result.get("export_result")
        validation = result.get("validation")
        readiness = result.get("readiness")
        summary = result.get("summary")
        delivery_report_path = result.get("delivery_report_path")

        report_summary = DeliveryReadyCompilableRuntimeProjectReportSummary(
            project_root=getattr(export_result, "project_root", ""),
            task_count=getattr(summary, "task_count", 0) if summary else 0,
            task_ids=getattr(summary, "task_ids", []) if summary else [],
            validation_ok=getattr(validation, "is_valid", False),
            todo_count=getattr(readiness, "todo_count", 0),
            unsupported_count=getattr(readiness, "unsupported_count", 0),
            files={**(getattr(summary, "files", {}) if summary else {}), "delivery_report": delivery_report_path},
        )
        result["report_summary"] = report_summary
        return result
