class DeliveryReadyCompilableRuntimeProjectDeliverySerializer:
    @staticmethod
    def to_dict(result: dict) -> dict:
        export_result = result.get("export_result")
        validation = result.get("validation")
        readiness = result.get("readiness")
        summary = result.get("summary")
        report_path = result.get("report_path")

        write_result = getattr(export_result, "write_result", None)
        return {
            "export_result": {
                "project_root": getattr(export_result, "project_root", ""),
                "write_result": {
                    "root_dir": getattr(write_result, "root_dir", "") if write_result else "",
                    "task_files": getattr(write_result, "task_files", {}) if write_result else {},
                    "registry_file": getattr(write_result, "registry_file", "") if write_result else "",
                },
            },
            "validation": {
                "is_valid": getattr(validation, "is_valid", False),
                "missing_files": getattr(validation, "missing_files", []),
                "warnings": getattr(validation, "warnings", []),
            },
            "readiness": {
                "todo_count": getattr(readiness, "todo_count", 0),
                "unsupported_count": getattr(readiness, "unsupported_count", 0),
                "task_file_todo_counts": getattr(readiness, "task_file_todo_counts", {}),
                "task_file_unsupported_counts": getattr(readiness, "task_file_unsupported_counts", {}),
                "warnings": getattr(readiness, "warnings", []),
            },
            "summary": {
                "project_root": getattr(summary, "project_root", "") if summary else "",
                "task_count": getattr(summary, "task_count", 0) if summary else 0,
                "task_ids": getattr(summary, "task_ids", []) if summary else [],
                "files": getattr(summary, "files", {}) if summary else {},
            },
            "report_path": report_path,
        }
