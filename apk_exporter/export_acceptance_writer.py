from pathlib import Path
import json

from .export_acceptance_serializer import ExportAcceptanceSerializer


class ExportAcceptanceWriter:
    def write(self, report, output_dir: Path) -> str:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / 'export_acceptance.preview.json'
        path.write_text(
            json.dumps(ExportAcceptanceSerializer.to_dict(report), ensure_ascii=False, indent=2),
            encoding='utf-8',
        )
        return str(path)
