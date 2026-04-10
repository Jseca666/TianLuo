class MainExportVsQualityComparisonSerializer:
    @staticmethod
    def to_dict(summary) -> dict:
        return {
            "project_roots": getattr(summary, "project_roots", {}),
            "task_counts": getattr(summary, "task_counts", {}),
            "asset_file_counts": getattr(summary, "asset_file_counts", {}),
            "todo_counts": getattr(summary, "todo_counts", {}),
            "unsupported_counts": getattr(summary, "unsupported_counts", {}),
            "validation_ok": getattr(summary, "validation_ok", {}),
            "report_paths": getattr(summary, "report_paths", {}),
            "task_ids": getattr(summary, "task_ids", []),
        }
