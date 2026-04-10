# Main Android Project Export Channel

## 当前定位

`main_android_project_export_facade.py` 是当前仓库里更接近长期主入口的导出通道。

它在默认导出通道基础上进一步收口：

- 默认导出 summary
- deep 资源完整性校验
- readiness 视角（TODO / unsupported）
- package 报告
- default 报告
- main 报告

---

## 当前推荐入口

- `apk_exporter/main_android_project_export_facade.py`

如果需要更强类型化返回值，则继续保留：

- `apk_exporter/default_android_project_export_completion_facade.py`

---

## 当前价值

当前 main export 通道可以作为：

- 任务规格输入的统一出口
- Android Studio 工程导出的统一出口
- automation 资源打包的统一出口
- 校验 / readiness / 报告的统一出口

---

## 后续重点

后续不再优先增加新的 façade 名字，而是优先：

1. 提高动作覆盖率
2. 减少 TODO / unsupported
3. 提高导出工程的真实可用性
