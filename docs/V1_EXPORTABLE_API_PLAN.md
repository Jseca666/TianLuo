# V1 - 可导出通用 API 冻结计划

## 目标

V1 的目标不是导出 APK，也不是引入 Android Runtime。
V1 只做一件事：

**把当前仓库中已经成熟的通用能力，冻结成一套可导出的脚本 API。**

后续所有希望导出为 Android 独立运行工程的脚本，都必须只依赖这套 API。

---

## 为什么先做这一版

当前仓库已经具备很丰富的通用能力，但这些能力的宿主仍然是：

- PC + Python
- ADB + subprocess
- PyQt 调度

典型来源：

- `RC_ui.py`：桌面端调度入口
- `base_tool/AndroidDevice.py`：设备、截图、找图、OCR、点击、滑动、对比
- `base_tool/read_json.py`：locator 资源读取

现阶段真正缺少的不是能力，而是：

1. 一套稳定的、可翻译的、可导出的 API 白名单
2. 新脚本写法与旧底层实现解耦
3. 为后续 Android Runtime 和 APK 导出器提供固定接口

---

## V1 的边界

### V1 会做什么

- 新增 `exportable_api/` 包
- 定义 `ExportableTaskApi` 抽象接口
- 定义 locator / match / capture 等通用数据结构
- 新增一个 PC 侧适配器，把旧 `AndroidDevice` 封装进新 API
- 提供一个最小示例脚本
- 补充迁移与使用文档

### V1 不做什么

- 不导出 Android Studio 工程
- 不生成 APK
- 不引入 Android Runtime
- 不自动迁移全部旧任务
- 不修改现有 `assignment/*` 主链

---

## V1 冻结后的可导出 API

V1 约定未来可导出脚本只能使用以下能力：

### 设备与应用

- `launch_app(package_name, activity=None)`
- `stop_app(package_name)`
- `tap(point)`
- `tap_locator(locator_name, threshold=0.8, timeout=10.0, mask=None, use_color=False)`
- `tap_area(locator_name)`
- `swipe(start, end, duration_ms=3000)`
- `back()`
- `sleep(seconds)`

### 视觉

- `capture()`
- `wait_image(locator_name, threshold=0.8, timeout=10.0, mask=None, use_color=False)`
- `exists(locator_name, threshold=0.8, timeout=1.0, mask=None, use_color=False)`
- `compare(frame_a, frame_b, threshold=0.85, mask=None, use_color=False)`

### OCR

- `ocr_text(locator_name, mask=None, kernel_size=None)`
- `ocr_int(locator_name, mask=None, excluded_number=None, kernel_size=None)`

### 资源

- `locator(locator_name)`
- `center(locator_name)`

---

## 资源规范

V1 沿用现有资源组织方式，不做格式推倒重来。

继续保留：

- `tool/location/**/*.json`
- `tool/masks.json`

其中 locator JSON 仍然保持当前结构：

- `image_path`
- `coordinates.top_left`
- `coordinates.bottom_right`

这意味着 V1 之后，旧资源仍然可以直接继续使用。

---

## 现有能力到 V1 API 的映射

| 现有实现 | V1 API |
| --- | --- |
| `AndroidDevice.launch_app()` | `launch_app()` |
| `AndroidDevice.stop_app()` | `stop_app()` |
| `AndroidDevice.tap_on_screen()` | `tap()` |
| `AndroidDevice.swipe_on_screen()` | `swipe()` |
| `AndroidDevice.press_back_button()` | `back()` |
| `AndroidDevice.capture_screenshot()` | `capture()` |
| `AndroidDevice.wait_for_image()` | `wait_image()` |
| `AndroidDevice.get_text_from_screen()` | `ocr_text()` |
| `number_get.extract_numbers()` 的常见用法 | `ocr_int()` |
| `AndroidDevice.compare_images()` | `compare()` |
| `json_reader.img_path()` + `img_areas()` | `locator()` |

---

## 新旧脚本的迁移规则

### 旧风格

```python
self.device.tap_on_screen(self.device.wait_for_image(self.json.img_path('开始按钮'))[0])
num = int(self.numberget.extract_numbers('剩余次数', excluded_number=-1)[0])
```

### V1 推荐风格

```python
api.tap_locator('开始按钮')
num = api.ocr_int('剩余次数', excluded_number=-1)
```

### 旧风格

```python
loc = self.device.get_centra(self.json.img_areas('确认按钮')[0], self.json.img_areas('确认按钮')[1])
self.device.tap_on_screen(loc)
```

### V1 推荐风格

```python
api.tap_area('确认按钮')
```

---

## 对旧项目主链的要求

V1 不破坏现有入口与任务体系：

- `RC_ui.py` 保持不动
- `assignment/*` 保持不动
- `base_tool/*` 保持不动

V1 只新增一层可导出 API 和一个 PC 侧适配器，供新脚本或迁移脚本使用。

---

## V1 完成后的结果

完成 V1 后，仓库会同时存在两套体系：

### 旧体系

- 继续运行当前项目
- 继续支持现有任务

### 新体系

- 为未来导出 Android Runtime 做接口准备
- 为未来 APK 导出器提供可翻译的脚本调用面
- 为旧任务迁移提供收敛方向

---

## V2 之后的自然演进

V1 完成后，后续版本可以按下面的顺序推进：

- V2：Android Runtime 最小底座
- V3：资源导出链
- V4：单脚本导出 Android 工程

因此，V1 是后续所有导出工作的接口基线。
