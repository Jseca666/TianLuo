from .export_manifest_serializer import ExportManifestSerializer
from .export_plan_serializer import ExportPlanSerializer


class ExportReportSerializer:
    @staticmethod
    def to_dict(report: dict) -> dict:
        manifest = report.get("manifest")
        plan = report.get("plan")
        summary = report.get("summary", {})
        return {
            "manifest": ExportManifestSerializer.to_dict(manifest),
            "plan": ExportPlanSerializer.to_dict(plan),
            "summary": summary,
        }
