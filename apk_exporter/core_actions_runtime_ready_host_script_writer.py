from pathlib import Path


class CoreActionsRuntimeReadyHostScriptWriter:
    PACKAGE_NAME = "com.tianluo.runtime.template"
    MAIN_ACTIVITY = "com.tianluo.runtime.template.MainActivity"
    APK_RELATIVE_PATH = "app/build/outputs/apk/debug/app-debug.apk"

    def write(self, project_root: Path) -> dict:
        project_root = Path(project_root)
        scripts_root = project_root / "host_tools"
        scripts_root.mkdir(parents=True, exist_ok=True)

        build_path = scripts_root / "build_debug.sh"
        install_path = scripts_root / "install_debug.sh"
        launch_path = scripts_root / "launch_main_activity.sh"
        smoke_path = scripts_root / "smoke_core_actions_debug.sh"

        build_path.write_text(
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n"
            "cd \"$(dirname \"$0\")/..\"\n"
            "./gradlew assembleDebug\n",
            encoding="utf-8",
        )
        install_path.write_text(
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n"
            "cd \"$(dirname \"$0\")/..\"\n"
            f"adb install -r {self.APK_RELATIVE_PATH}\n",
            encoding="utf-8",
        )
        launch_path.write_text(
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n"
            f"adb shell am start -n {self.PACKAGE_NAME}/{self.MAIN_ACTIVITY}\n",
            encoding="utf-8",
        )
        smoke_path.write_text(
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n"
            "cd \"$(dirname \"$0\")\"\n"
            "bash ./build_debug.sh\n"
            "bash ./install_debug.sh\n"
            f"adb shell am force-stop {self.PACKAGE_NAME}\n"
            "bash ./launch_main_activity.sh\n"
            "adb shell sleep 2\n"
            f"adb logcat -d -s ActivityTaskManager:{self.PACKAGE_NAME} AndroidRuntime *:S || true\n",
            encoding="utf-8",
        )

        return {
            "scripts_root": str(scripts_root),
            "build_debug": str(build_path),
            "install_debug": str(install_path),
            "launch_main_activity": str(launch_path),
            "smoke_core_actions_debug": str(smoke_path),
            "package_name": self.PACKAGE_NAME,
            "main_activity": self.MAIN_ACTIVITY,
            "apk_relative_path": self.APK_RELATIVE_PATH,
        }
