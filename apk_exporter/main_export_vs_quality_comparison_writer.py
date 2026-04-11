from pathlib import Path
import json

from .main_export_vs_quality_comparison_serializer import MainExportVsQualityComparisonSerializer


class MainExportVsQualityComparisonWriter:
    def write(self, summary, output_dir: Path) -> str:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / 'main_export_vs_quality_comparison.json'
        path.write_text(
            json.dumps(
                MainExportVsQualityComparisonSerializer.to_dict(summary),
                ensure_ascii=False,
                indent=2,
            ),
            encoding='utf-8',
        )
        return str(path)
