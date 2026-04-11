class MainExportComparisonSerializer:
    @staticmethod
    def to_dict(result: dict) -> dict:
        summary = result.get("summary")
        return {
            "summary": {
                "baseline_project_root": getattr(summary, "baseline_project_root", "") if summary else "",
                "quality_project_root": getattr(summary, "quality_project_root", "") if summary else "",
                "baseline_todo_count": getattr(summary, "baseline_todo_count", 0) if summary else 0,
                "quality_todo_count": getattr(summary, "quality_todo_count", 0) if summary else 0,
                "baseline_unsupported_count": getattr(summary, "baseline_unsupported_count", 0) if summary else 0,
                "quality_unsupported_count": getattr(summary, "quality_unsupported_count", 0) if summary else 0,
                "baseline_asset_file_count": getattr(summary, "baseline_asset_file_count", 0) if summary else 0,
                "quality_asset_file_count": getattr(summary, "quality_asset_file_count", 0) if summary else 0,
                "baseline_validation_ok": getattr(summary, "baseline_validation_ok", False) if summary else False,
                "quality_validation_ok": getattr(summary, "quality_validation_ok", False) if summary else False,
                "files": getattr(summary, "files", {}) if summary else {},
                "notes": getattr(summary, "notes", []) if summary else [],
            }
        }
