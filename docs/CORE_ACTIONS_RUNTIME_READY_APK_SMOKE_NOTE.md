# Core Actions Runtime Ready APK Smoke Note

## 当前目的

这一轮继续沿着更贴最终目标的 `core-actions runtime-ready` 主线推进，但重点不再只是：

- 导出 Android 工程
- 做代码级覆盖检查

而是继续往前补一层更接近最终验收的主机侧闭环工具：

- `build`
- `install`
- `launch`
- `smoke`

也就是为导出的 Android 工程，自动生成一组可在本地 Gradle + adb 环境里直接使用的主机侧脚本。

---

## 当前新增内容

本次新增：

- `apk_exporter/core_actions_runtime_ready_host_script_writer.py`
- `apk_exporter/core_actions_runtime_ready_apk_smoke_summary.py`
- `apk_exporter/core_actions_runtime_ready_apk_smoke_workflow.py`
- `apk_exporter/core_actions_runtime_ready_apk_smoke_writer.py`
- `examples/core_actions_runtime_ready_apk_smoke_poc.py`

---

## 当前已确认的模板启动信息

当前 Android runtime template 中：

- `applicationId = com.tianluo.runtime.template`
- 主入口 Activity 为 `com.tianluo.runtime.template.MainActivity`

因此当前主机侧脚本会围绕这组固定入口生成：

- `adb install -r app/build/outputs/apk/debug/app-debug.apk`
- `adb shell am start -n com.tianluo.runtime.template/com.tianluo.runtime.template.MainActivity`

---

## 当前生成的主机侧脚本

当前会在导出的项目根目录下新增：

- `host_tools/build_debug.sh`
- `host_tools/install_debug.sh`
- `host_tools/launch_main_activity.sh`
- `host_tools/smoke_core_actions_debug.sh`

它们对应：

1. Gradle debug 构建
2. adb 安装 debug APK
3. adb 启动主 Activity
4. 一次串行的基础 smoke 操作

---

## 当前 smoke workflow 会做什么

当前 `CoreActionsRuntimeReadyApkSmokeWorkflow` 会统一完成：

1. 导出 `core-actions runtime-ready` 工程
2. 执行代码级 readiness 分析
3. 为导出工程写入主机侧脚本
4. 输出一份 smoke summary，包含：
   - `project_root`
   - `package_name`
   - `main_activity`
   - `apk_relative_path`
   - `host_scripts`
   - `checks`
   - `commands`
   - `notes`

这意味着这条更贴目标的线，现在已经不只是“能导出 + 能自检”，还开始具备：

> 导出后如何在本地 Android 构建和 adb 环境里继续往下执行 smoke 的明确路径。

---

## 推荐入口

当前推荐直接运行：

- `python examples/core_actions_runtime_ready_apk_smoke_poc.py`

它会：

1. 导出项目
2. 输出代码级 readiness
3. 写入 host_tools 脚本
4. 生成一份 JSON smoke 报告

---

## 当前结论

这一轮的核心意义是：

> `core-actions runtime-ready` 线已经开始补齐导出后的主机侧 build / install / launch / smoke 路径。

这仍然不是最终的真机 APK 验收闭环，但已经比单纯导出工程更进一步，明显更接近：

- 真实构建
- 真实安装
- 真实启动
- 真实 smoke

这一最终目标链路。
