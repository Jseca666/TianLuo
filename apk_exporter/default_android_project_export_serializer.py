class DefaultAndroidProjectExportSerializer:
    @staticmethod
    def to_dict(result: dict) -> dict:
        summary = result.get("summary")
        deep_validation = result.get("deep_validation")
        package_report_path = result.get("package_report_path")
        return {
            "summary": {
                "project_root": getattr(summary, "project_root", "") if summary else "",
                "assets_root": getattr(summary, "assets_root", "") if summary else "",
                "task_count": getattr(summary, "task_count", 0) if summary else 0,
                "task_ids": getattr(summary, "task_ids", []) if summary else [],
                "asset_file_count": getattr(summary, "asset_file_count", 0) if summary else 0,
                "validation_ok": getattr(summary, "validation_ok", False) if summary else False,
                "files": getattr(summary, "files", {}) if summary else {},
            },
            "deep_validation": {
                "is_valid": getattr(deep_validation, "is_valid", False),
                "missing_paths": getattr(deep_validation, "missing_paths", []),
                "warnings": getattr(deep_validation, "warnings", []),
            },
            "package_report_path": package_report_path,
        }
