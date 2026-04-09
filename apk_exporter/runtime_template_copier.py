from pathlib import Path
import shutil


class RuntimeTemplateCopier:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)

    def copy(self, output_root: Path, project_name: str = "GeneratedAndroidProject") -> str:
        output_root = Path(output_root)
        source = self.repo_root / "android_runtime_template"
        target = output_root / project_name

        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(source, target)
        return str(target)
