def build_demo_task_specs():
    return [
        {
            "task_id": "demo_wait_tap_back",
            "display_name": "Demo Wait Tap Back",
            "api_calls": [
                {"api_name": "wait_image", "params": {"locator_name": "主页庄园图标", "timeout": 5.0}},
                {"api_name": "tap_locator", "params": {"locator_name": "主页庄园图标", "timeout": 3.0}},
                {"api_name": "sleep", "params": {"seconds": 1}},
                {"api_name": "back", "params": {}},
            ],
        }
    ]
