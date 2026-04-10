from pathlib import Path
import json

from .default_android_project_export_serializer import DefaultAndroidProjectExportSerializer


class DefaultAndroidProjectExportWriter:
    def write(self, result: dict, output_dir: Path) -> str:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / 'default_android_project_export.json'
        path.write_text(
            json.dumps(
                DefaultAndroidProjectExportSerializer.to_dict(result),
                ensure_ascii=False,
                indent=2,
            ),
            encoding='utf-8',
        )
        return str(path)
