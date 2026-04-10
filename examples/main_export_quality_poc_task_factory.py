def build_main_export_quality_task_specs():
    return [
        {
            "task_id": "demo_swipe_and_ocr_asserts",
            "display_name": "Demo Swipe And OCR Asserts",
            "api_calls": [
                {"api_name": "wait_locator", "params": {"locator_name": "主页庄园图标", "timeout": 5.0}},
                {"api_name": "swipe_up", "params": {"locator_name": "主页庄园图标", "duration_ms": 280}},
                {"api_name": "swipe_down", "params": {"locator_name": "主页庄园图标", "duration_ms": 280}},
                {"api_name": "assert_text_equals", "params": {"locator_name": "主页庄园图标", "expected": "庄园"}},
                {"api_name": "assert_number_at_most", "params": {"locator_name": "主页庄园图标", "max_value": 9999}},
                {"api_name": "back", "params": {}},
            ],
        }
    ]
