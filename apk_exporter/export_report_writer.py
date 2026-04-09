from pathlib import Path

from .export_report_builder import ExportReportBuilder
from .export_report_serializer import ExportReportSerializer


class ExportReportWriter:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)

    def write(self, output_dir: Path) -> str:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        report = ExportReportBuilder(self.repo_root).build()
        report_path = output_dir / 'export_report.preview.json'
        report_path.write_text(
            str(ExportReportSerializer.to_dict(report)),
            encoding='utf-8',
        )
        return str(report_path)
