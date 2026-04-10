from pathlib import Path
import json

from .main_export_quality_project_export_serializer import MainExportQualityProjectExportSerializer


class MainExportQualityProjectExportWriter:
    def write(self, result: dict, output_dir: Path) -> str:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / 'main_export_quality_project_export.json'
        path.write_text(
            json.dumps(
                MainExportQualityProjectExportSerializer.to_dict(result),
                ensure_ascii=False,
                indent=2,
            ),
            encoding='utf-8',
        )
        return str(path)
