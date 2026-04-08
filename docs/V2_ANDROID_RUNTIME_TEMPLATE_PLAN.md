# V2 - Android Runtime 模板最小底座

## 目标

V2 的目标是：

**在仓库里建立一份固定的 Android Runtime 模板工程骨架。**

这一版只解决两件事：

1. 让后续导出器有固定的 Android 工程宿主
2. 让 V1 冻结下来的可导出 API，在 Android 侧拥有同语义接口位置

---

## V2 边界

### V2 会做什么

- 新增 `android_runtime_template/` 目录
- 建立最小 Android Studio 工程骨架
- 建立 Runtime 的核心接口目录
- 建立任务执行模型接口
- 建立 Accessibility / MediaProjection / OCR / 资源加载的占位入口

### V2 不做什么

- 不打通完整自动化能力
- 不实现全部模板匹配细节
- 不导出 APK
- 不把旧任务翻译成 Kotlin
- 不改现有 Python 主链

---

## V2 后的预期结果

完成 V2 后，仓库里会第一次出现：

- 固定 Android Runtime 工程模板
- Runtime 任务模型
- 资源加载模型
- AccessibilityService 与前台服务入口骨架

这样 V3 才能继续做资源导出，V4 才能做真正的工程生成。

---

## 模板目录目标

```text
android_runtime_template/
  settings.gradle.kts
  build.gradle.kts
  gradle.properties
  app/
    build.gradle.kts
    src/main/
      AndroidManifest.xml
      java/com/tianluo/runtime/template/
      res/xml/
```

---

## V2 里的核心 Kotlin 接口

### task

- `RuntimeTask`
- `TaskContext`
- `TaskResult`

### capture

- `CaptureEngine`

### gesture

- `GestureEngine`

### vision

- `TemplateMatcher`
- `ImageComparator`

### ocr

- `OcrEngine`

### assets

- `LocatorAsset`
- `AssetLocatorRepository`

### service

- `RuntimeAccessibilityService`
- `RuntimeForegroundService`

---

## 和 V1 的衔接关系

V1 在 Python 侧冻结了这些通用能力：

- 截图
- 点击
- 滑动
- 返回
- 等待图片
- OCR
- 图像对比
- locator 读取

V2 不是在 Android 侧直接复刻 Python 实现，而是先把这些能力的接口位置固定下来。

也就是说：

- V1 解决“脚本调用面”
- V2 解决“Android 宿主位置”

---

## V3 之后的衔接

V2 完成后，接下来最自然的是：

- V3：把现有 `tool/location/**/*.json`、模板图、`tool/masks.json` 导入 Android assets
- V4：根据受支持脚本生成 Kotlin 任务类并输出 Android Studio 工程

因此，V2 的价值是把 Android 侧的模板底座定住。
