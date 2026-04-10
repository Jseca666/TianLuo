# Default Android Project Export Channel

## 当前定位

当前仓库已经形成一条更接近长期主入口的默认导出通道：

- 任务规格输入
- 生成 Kotlin 任务与注册表
- 复制 Android Runtime 模板工程
- 写入任务代码
- 打入 automation 资源到 `app/src/main/assets`
- 做 deep 资源完整性校验
- 输出默认导出 summary 与默认导出报告

---

## 当前主入口

当前推荐使用：

- `apk_exporter/default_android_project_export_facade.py`
- `apk_exporter/default_android_project_export_completion_facade.py`

其中：

- `DefaultAndroidProjectExportFacade` 适合返回默认导出结果字典与报告路径
- `DefaultAndroidProjectExportCompletionFacade` 适合返回更稳定的完成态结果对象

---

## 当前能力边界

当前默认导出通道已经能做到：

1. 导出 Android Studio 工程骨架
2. 生成任务 Kotlin 文件与注册表
3. 打入 automation 资源
4. 校验 `export_manifest.json`、`locators`、`templates`、`masks.json`
5. 输出默认导出报告

但当前仍有边界：

- 不是所有任务动作都已经落到 Runtime 现有接口
- 仍然存在部分 TODO / unsupported fallback
- 仍然需要继续向真实通用任务组合扩展

---

## 后续重点

默认导出通道后续重点不是再铺很多平行链，而是：

- 继续扩动作覆盖率
- 继续减少 fallback / TODO
- 继续提升默认导出通道的稳定性
