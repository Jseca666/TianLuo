def build_realistic_demo_task_specs():
    return [
        {
            "task_id": "demo_exists_wait_tap_locator_ocr_back",
            "display_name": "Demo Exists Wait Tap Locator Ocr Back",
            "api_calls": [
                {"api_name": "exists_image", "params": {"locator_name": "主页庄园图标", "timeout": 1.0}},
                {"api_name": "wait_locator", "params": {"locator_name": "主页庄园图标", "timeout": 5.0}},
                {"api_name": "tap_template", "params": {"locator_name": "主页庄园图标", "timeout": 3.0}},
                {"api_name": "ocr_text", "params": {"locator_name": "主页庄园图标"}},
                {"api_name": "sleep", "params": {"seconds": 1}},
                {"api_name": "back", "params": {}},
            ],
        }
    ]
