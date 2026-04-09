# V3 - 资源导出链

## 目标

V3 的目标是：

**把当前仓库里的 locator JSON、模板图、mask 配置，稳定整理成 Android Runtime 可直接消费的资源输出。**

这一版不做 Kotlin 任务生成，也不做 APK 编译，只聚焦资源链。

---

## V3 会做什么

- 新增 `apk_exporter/` 目录
- 建立资源收集模块
- 建立路径规范化模块
- 建立资源清单输出模块
- 约定 Android assets 目标目录结构

---

## V3 不做什么

- 不翻译旧任务脚本
- 不生成 Kotlin 任务类
- 不导出完整 Android Studio 工程
- 不实现 Android Runtime 具体能力

---

## 输入资源来源

主要来自当前仓库：

- `tool/location/**/*.json`
- 模板图文件
- `tool/masks.json`

---

## 输出目标

目标输出结构建议为：

```text
app/src/main/assets/automation/
  locators/
  templates/
  masks.json
  export_manifest.json
```

---

## V3 核心模块

### path_normalizer.py

负责：

- 统一路径分隔符
- 统一大小写策略
- 把 Windows 风格路径转成 Android assets 风格路径

### asset_collector.py

负责：

- 收集 locator JSON
- 扫描 locator 引用到的模板图
- 收集 masks.json

### export_manifest.py

负责：

- 生成导出资源清单
- 为后续 Kotlin 任务生成器提供资源索引

---

## V3 完成标准

完成 V3 后，给定一组 locator JSON 和模板图，应该能够得到一份稳定的 Android assets 目录输出。

V4 会在这个基础上继续生成 Kotlin 任务类和 Android Studio 工程。
