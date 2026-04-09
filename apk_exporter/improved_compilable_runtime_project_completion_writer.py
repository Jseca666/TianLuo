from pathlib import Path
import json

from .improved_compilable_runtime_project_completion_serializer import ImprovedCompilableRuntimeProjectCompletionSerializer


class ImprovedCompilableRuntimeProjectCompletionWriter:
    def write(self, result, output_dir: Path) -> str:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / 'improved_compilable_runtime_completion.json'
        path.write_text(
            json.dumps(
                ImprovedCompilableRuntimeProjectCompletionSerializer.to_dict(result),
                ensure_ascii=False,
                indent=2,
            ),
            encoding='utf-8',
        )
        return str(path)
