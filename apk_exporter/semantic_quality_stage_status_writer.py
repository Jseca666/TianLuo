from dataclasses import asdict, is_dataclass
from pathlib import Path
import json


class SemanticQualityStageStatusWriter:
    def write(self, result: dict, output_dir: Path) -> str:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / "semantic_quality_stage_status.json"
        payload = {}
        for key, value in result.items():
            if is_dataclass(value):
                payload[key] = asdict(value)
            elif isinstance(value, dict):
                payload[key] = value
            else:
                payload[key] = value
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
        return str(path)
