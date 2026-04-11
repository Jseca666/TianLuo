from pathlib import Path
import json


class MainExportComparisonBenchmarkWriter:
    def write(self, enriched_result: dict, output_dir: Path) -> str:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / "main_export_benchmark_comparison_enriched.json"
        path.write_text(
            json.dumps(enriched_result, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return str(path)
