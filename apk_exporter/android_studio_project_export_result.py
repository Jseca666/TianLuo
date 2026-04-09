from dataclasses import dataclass

from .android_project_write_result import AndroidProjectWriteResult


@dataclass
class AndroidStudioProjectExportResult:
    project_root: str
    write_result: AndroidProjectWriteResult
