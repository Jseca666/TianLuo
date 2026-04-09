# V4 - 任务导出与 Android 工程生成起步

## 目标

V4 的目标是：

**把已经完成的资源导出链，继续推进到“任务导出链”。**

也就是从：

- 可导出 API
- Android Runtime 模板
- 资源导出链

推进到：

- 任务表示模型
- Kotlin 任务类生成
- 任务注册表生成
- Android Studio 工程收口准备

---

## V4 的边界

### V4 会做什么

- 新增 `task_exporters/` 目录
- 定义任务导出模型
- 建立 Kotlin 任务代码生成器骨架
- 建立任务注册表生成骨架
- 建立 Android 工程导出骨架入口

### V4 不会立刻做什么

- 不追求支持任意 Python 语法
- 不追求一次支持所有旧任务
- 不直接做复杂 DSL / IR 平台
- 不在第一步就导出完整复杂业务任务

---

## V4 的最小目标

V4 第一批提交只需要把下面这条链立住：

1. 受支持脚本 -> 任务表示模型
2. 任务表示模型 -> Kotlin 任务类文本
3. 多个任务 -> 任务注册表文本
4. 资源导出结果 + Kotlin 任务类 -> Android 工程导出入口

---

## 设计原则

### 1. 继续保持低风险演进

- 不破坏旧主链
- 不回头大改 V1/V2/V3
- 先用骨架和最小模型把 V4 起步

### 2. 不做重解释器

V4 不去解释整个 Python 世界，而是只支持“可导出 API 组合”这条受控链路。

### 3. 先输出 Kotlin 类，再考虑复杂任务迁移

V4 第一版关注的是：

- 任务类生成
- 注册表生成
- 工程收口

而不是旧任务自动全量迁移。

---

## V4 的主要目录

```text
task_exporters/
  __init__.py
  export_models.py
  base_task_exporter.py
  kotlin_task_writer.py
  task_registry_writer.py

apk_exporter/
  android_project_exporter.py
```

---

## V4 完成标准

V4 完成时，至少应具备：

- 一个受支持任务模型
- 一个 Kotlin 任务类生成器
- 一个任务注册表生成器
- 一个 Android 工程导出骨架入口

这将成为后续真正导出 Android Studio 工程的起点。
