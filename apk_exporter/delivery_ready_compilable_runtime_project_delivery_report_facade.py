from pathlib import Path
from typing import Iterable

from .delivery_ready_compilable_runtime_project_delivery_facade import DeliveryReadyCompilableRuntimeProjectDeliveryFacade
from .delivery_ready_compilable_runtime_project_delivery_writer import DeliveryReadyCompilableRuntimeProjectDeliveryWriter


class DeliveryReadyCompilableRuntimeProjectDeliveryReportFacade:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.facade = DeliveryReadyCompilableRuntimeProjectDeliveryFacade(repo_root)

    def export(self, task_specs: Iterable[dict], output_root: Path, project_name: str = "GeneratedAndroidProject", report_output_dir: Path | None = None) -> dict:
        result = self.facade.export(
            task_specs=task_specs,
            output_root=output_root,
            project_name=project_name,
            report_output_dir=report_output_dir,
        )
        delivery_report_path = DeliveryReadyCompilableRuntimeProjectDeliveryWriter().write(
            result,
            Path(report_output_dir or output_root),
        )
        result["delivery_report_path"] = delivery_report_path
        return result
