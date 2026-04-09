from pathlib import Path

from .android_studio_project_export_result import AndroidStudioProjectExportResult
from .improved_compilable_runtime_project_validation import ImprovedCompilableRuntimeProjectValidation


class ImprovedCompilableRuntimeProjectValidator:
    def validate(self, export_result: AndroidStudioProjectExportResult) -> ImprovedCompilableRuntimeProjectValidation:
        missing_files = []
        warnings = []

        project_root = Path(export_result.project_root)
        if not project_root.exists():
            missing_files.append(str(project_root))

        write_result = export_result.write_result
        registry_file = Path(write_result.registry_file)
        if not registry_file.exists():
            missing_files.append(str(registry_file))

        if not write_result.task_files:
            warnings.append("No generated task files found")

        for _, file_path in write_result.task_files.items():
            path = Path(file_path)
            if not path.exists():
                missing_files.append(str(path))

        return ImprovedCompilableRuntimeProjectValidation(
            is_valid=len(missing_files) == 0,
            missing_files=missing_files,
            warnings=warnings,
        )
