def build_advanced_demo_task_specs():
    return [
        {
            "task_id": "demo_exists_wait_tap_area_back",
            "display_name": "Demo Exists Wait Tap Area Back",
            "api_calls": [
                {"api_name": "exists", "params": {"locator_name": "主页庄园图标", "timeout": 1.0}},
                {"api_name": "wait_image", "params": {"locator_name": "主页庄园图标", "timeout": 5.0}},
                {"api_name": "tap_area", "params": {"locator_name": "主页庄园图标"}},
                {"api_name": "sleep", "params": {"seconds": 1}},
                {"api_name": "back", "params": {}},
            ],
        }
    ]
