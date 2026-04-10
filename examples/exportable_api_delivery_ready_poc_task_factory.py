def build_delivery_ready_demo_task_specs():
    return [
        {
            "task_id": "demo_wait_ocr_assert_back",
            "display_name": "Demo Wait OCR Assert Back",
            "api_calls": [
                {"api_name": "wait_locator", "params": {"locator_name": "主页庄园图标", "timeout": 5.0}},
                {"api_name": "assert_text_contains", "params": {"locator_name": "主页庄园图标", "expected": "庄园"}},
                {"api_name": "assert_number_at_least", "params": {"locator_name": "主页庄园图标", "min_value": 1}},
                {"api_name": "sleep", "params": {"seconds": 1}},
                {"api_name": "back", "params": {}},
            ],
        }
    ]
