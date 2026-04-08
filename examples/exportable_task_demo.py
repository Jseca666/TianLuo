"""V1 可导出 API 最小示例。

使用前请替换：
- adb_path
- device_address
- json_path
- locator 名称
"""

from exportable_api.pc_runtime import ExportablePcTaskApi


def main():
    adb_path = r"E:\\leidian\\LDPlayer9\\adb.exe"
    device_address = "127.0.0.1:5555"
    json_path = "tool/location/Zhuangyuan/Zhuangyuan.json"

    api = ExportablePcTaskApi.from_json(
        adb_path=adb_path,
        device_address=device_address,
        json_path=json_path,
    )

    if api.exists("主页庄园图标", timeout=2.0):
        api.tap_locator("主页庄园图标", threshold=0.9, timeout=5.0)
        api.sleep(1.5)

    frame_a = api.capture()
    api.sleep(1.0)
    frame_b = api.capture()

    same = api.compare(frame_a, frame_b, threshold=0.95)
    print("两次截图是否相似:", same)

    count = api.ocr_int("剩余要求次数", excluded_number=-1)
    print("OCR 数字结果:", count)


if __name__ == "__main__":
    main()
