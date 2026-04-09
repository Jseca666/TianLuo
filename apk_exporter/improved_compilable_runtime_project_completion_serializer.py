class ImprovedCompilableRuntimeProjectCompletionSerializer:
    @staticmethod
    def to_dict(result) -> dict:
        export_result = result.export_result
        write_result = export_result.write_result
        validation = result.validation
        return {
            "export_result": {
                "project_root": export_result.project_root,
                "write_result": {
                    "root_dir": write_result.root_dir,
                    "task_files": write_result.task_files,
                    "registry_file": write_result.registry_file,
                },
            },
            "validation": {
                "is_valid": validation.is_valid,
                "missing_files": validation.missing_files,
                "warnings": validation.warnings,
            },
            "metadata": result.metadata,
        }
