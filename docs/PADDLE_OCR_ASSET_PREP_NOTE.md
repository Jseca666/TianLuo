# Paddle OCR Asset Preparation Note

## 当前目的

这一轮的目标，不是继续讨论 OCR 选型，而是把已经确定的 `PaddleOCR` 主线推进到“仓库内可直接准备官方模型与依赖”的阶段。

因此本次新增的重点是：

- 固定 app 内 PaddleOCR 资产目录约定
- 为导出工程自动写入主机侧准备脚本
- 把官方 Android 端 Paddle 流程收口成仓库里的 workflow 和报告入口

---

## 参考的官方流程

当前仓库里的主机侧准备链，遵循的是 PaddleOCR 官方 Android 端侧部署流程：

1. 克隆 `PaddleX-Lite-Deploy`（来自 `Paddle-Lite-Demo` 的 `feature/paddle-x` 分支）
2. 在 `libs/` 下执行 `download.sh` 下载 Paddle Lite 预测库
3. 在 `ocr/assets/` 下执行 `download.sh PP-OCRv5_mobile` 下载 OCR 资产
4. 在 `ocr/android/shell/ppocr_demo` 下执行 `build.sh`
5. 在 `ocr/android/shell/ppocr_demo` 下执行 `run.sh PP-OCRv5_mobile`

这条链现在已经被收口进仓库里的 host-side 脚本生成器。citeturn458495search0turn458495search1

---

## 当前新增内容

本次新增：

- `android_runtime_template/app/src/main/assets/models/paddleocr/README.md`
- `apk_exporter/paddle_ocr_host_prep_script_writer.py`
- `apk_exporter/paddle_ocr_asset_prep_summary.py`
- `apk_exporter/paddle_ocr_asset_prep_workflow.py`
- `apk_exporter/paddle_ocr_asset_prep_writer.py`
- `examples/paddle_ocr_asset_prep_poc.py`

---

## 当前 app 内资产目录约定

当前仓库里已经明确了 app 内 PaddleOCR 资产目录约定：

- `app/src/main/assets/models/paddleocr/det`
- `app/src/main/assets/models/paddleocr/rec`
- `app/src/main/assets/models/paddleocr/cls`
- `app/src/main/assets/models/paddleocr/labels/ppocr_keys_v1.txt`

这意味着后续把真实 Paddle 模型打进 Android 工程时，已经有了固定落点，而不是继续临时决定目录结构。

---

## 当前会生成哪些主机侧脚本

在导出的项目根目录下，当前会生成：

- `host_tools/paddle_ocr/clone_paddlex_lite_deploy.sh`
- `host_tools/paddle_ocr/prepare_paddle_lite_libs.sh`
- `host_tools/paddle_ocr/prepare_ppocr_assets.sh`
- `host_tools/paddle_ocr/build_ppocr_demo.sh`
- `host_tools/paddle_ocr/run_ppocr_demo.sh`

其中：

- 默认模型是 `PP-OCRv5_mobile`
- 准备链与官方 Android 端侧部署步骤一一对应citeturn458495search0turn458495search1

---

## 为什么当前不把大模型直接提交到 main

当前没有把官方 PaddleOCR 大模型和 Paddle Lite 预测库直接提交进仓库 `main`，原因不是不准备，而是：

- 官方流程本身就是按外部下载准备组织的citeturn458495search0turn458495search1
- 模型和预测库体积较大，不适合作为普通源码直接进主分支
- 当前更合理的方式，是把“如何准备它们”的脚本和固定目录先做进仓库

这会让仓库本身保持更稳定，同时又不影响后续本地一键准备模型。

---

## 当前推荐入口

当前推荐直接运行：

- `python examples/paddle_ocr_asset_prep_poc.py`

它会：

1. 导出一个带 Paddle 主线的 Android 工程
2. 自动写入 Paddle 主机侧准备脚本
3. 生成一份 `paddle_ocr_asset_prep.json`

这样当前仓库里关于 PaddleOCR 的模型和依赖准备链，就已经不再只是口头计划，而是有可直接运行的入口。

---

## 当前结论

这一轮的核心意义是：

> PaddleOCR 这条主线已经不只是“有 provider 骨架”，而是开始具备“官方模型与依赖如何准备”的仓库内落地链路。

这会让后续继续推进真实 `PaddleOcrRuntimeBridge` 实现时，不再卡在模型和依赖准备这一层。 
