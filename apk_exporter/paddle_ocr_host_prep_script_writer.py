from pathlib import Path


class PaddleOcrHostPrepScriptWriter:
    def write(self, project_root: Path) -> dict:
        project_root = Path(project_root)
        scripts_root = project_root / "host_tools" / "paddle_ocr"
        scripts_root.mkdir(parents=True, exist_ok=True)

        clone_path = scripts_root / "clone_paddlex_lite_deploy.sh"
        prepare_libs_path = scripts_root / "prepare_paddle_lite_libs.sh"
        prepare_assets_path = scripts_root / "prepare_ppocr_assets.sh"
        build_demo_path = scripts_root / "build_ppocr_demo.sh"
        run_demo_path = scripts_root / "run_ppocr_demo.sh"
        readme_path = scripts_root / "README.md"

        clone_path.write_text(
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n"
            "ROOT_DIR=\"$(cd \"$(dirname \"$0\")/../../..\" && pwd)\"\n"
            "cd \"${ROOT_DIR}\"\n"
            "if [ ! -d PaddleX-Lite-Deploy ]; then\n"
            "  git clone -b feature/paddle-x https://github.com/PaddlePaddle/Paddle-Lite-Demo.git PaddleX-Lite-Deploy\n"
            "else\n"
            "  echo 'PaddleX-Lite-Deploy already exists; skip clone.'\n"
            "fi\n",
            encoding="utf-8",
        )
        prepare_libs_path.write_text(
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n"
            "ROOT_DIR=\"$(cd \"$(dirname \"$0\")/../../..\" && pwd)\"\n"
            "cd \"${ROOT_DIR}/PaddleX-Lite-Deploy/libs\"\n"
            "sh download.sh\n",
            encoding="utf-8",
        )
        prepare_assets_path.write_text(
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n"
            "MODEL_NAME=\"${1:-PP-OCRv5_mobile}\"\n"
            "ROOT_DIR=\"$(cd \"$(dirname \"$0\")/../../..\" && pwd)\"\n"
            "cd \"${ROOT_DIR}/PaddleX-Lite-Deploy/ocr/assets\"\n"
            "sh download.sh \"${MODEL_NAME}\"\n",
            encoding="utf-8",
        )
        build_demo_path.write_text(
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n"
            "ROOT_DIR=\"$(cd \"$(dirname \"$0\")/../../..\" && pwd)\"\n"
            "cd \"${ROOT_DIR}/PaddleX-Lite-Deploy/ocr/android/shell/ppocr_demo\"\n"
            "sh build.sh\n",
            encoding="utf-8",
        )
        run_demo_path.write_text(
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n"
            "MODEL_NAME=\"${1:-PP-OCRv5_mobile}\"\n"
            "ROOT_DIR=\"$(cd \"$(dirname \"$0\")/../../..\" && pwd)\"\n"
            "cd \"${ROOT_DIR}/PaddleX-Lite-Deploy/ocr/android/shell/ppocr_demo\"\n"
            "sh run.sh \"${MODEL_NAME}\"\n",
            encoding="utf-8",
        )
        readme_path.write_text(
            "# PaddleOCR Host Preparation Scripts\n\n"
            "These scripts follow the official PaddleOCR Android on-device deployment flow:\n\n"
            "1. Clone `PaddleX-Lite-Deploy` from `Paddle-Lite-Demo` feature/paddle-x branch.\n"
            "2. Download Paddle Lite prediction libraries.\n"
            "3. Download `PP-OCRv5_mobile` assets by default.\n"
            "4. Build the official Android shell OCR demo.\n"
            "5. Run the demo on a connected Android device.\n",
            encoding="utf-8",
        )

        return {
            "scripts_root": str(scripts_root),
            "clone_repo": str(clone_path),
            "prepare_paddle_lite_libs": str(prepare_libs_path),
            "prepare_ppocr_assets": str(prepare_assets_path),
            "build_ppocr_demo": str(build_demo_path),
            "run_ppocr_demo": str(run_demo_path),
            "readme": str(readme_path),
        }
