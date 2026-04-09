from .export_report_serializer import ExportReportSerializer


class ExportAcceptanceSerializer:
    @staticmethod
    def to_dict(report) -> dict:
        execution = report.execution
        execution_dict = None
        if execution is not None:
            execution_dict = {
                "manifest_path": execution.manifest_path,
                "copied_files": execution.copied_files,
                "summary": execution.summary,
                "validation": {
                    "is_valid": execution.validation.is_valid if execution.validation else False,
                    "missing_sources": execution.validation.missing_sources if execution.validation else [],
                    "warnings": execution.validation.warnings if execution.validation else [],
                },
            }
        return {
            "passed": report.passed,
            "checks": report.checks,
            "notes": report.notes,
            "preview": report.preview,
            "execution": execution_dict,
        }
