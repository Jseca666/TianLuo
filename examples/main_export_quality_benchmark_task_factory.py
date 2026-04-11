def build_main_export_quality_benchmark_task_specs():
    return [
        {
            "task_id": "benchmark_exists_wait_tap_locator_back",
            "display_name": "Benchmark Exists Wait Tap Locator Back",
            "api_calls": [
                {"api_name": "exists_image", "params": {"locator_name": "主页庄园图标", "timeout": 1.0}},
                {"api_name": "wait_locator", "params": {"locator_name": "主页庄园图标", "timeout": 5.0}},
                {"api_name": "tap_template", "params": {"locator_name": "主页庄园图标", "timeout": 3.0}},
                {"api_name": "assert_text_contains", "params": {"locator_name": "主页庄园图标", "expected": "庄园"}},
                {"api_name": "sleep", "params": {"seconds": 1}},
                {"api_name": "back", "params": {}},
            ],
        },
        {
            "task_id": "benchmark_swipe_cycle_and_text_equals",
            "display_name": "Benchmark Swipe Cycle And Text Equals",
            "api_calls": [
                {"api_name": "wait_image", "params": {"locator_name": "主页庄园图标", "timeout": 5.0}},
                {"api_name": "swipe_up", "params": {"locator_name": "主页庄园图标", "duration_ms": 280}},
                {"api_name": "swipe_down", "params": {"locator_name": "主页庄园图标", "duration_ms": 280}},
                {"api_name": "swipe_left", "params": {"locator_name": "主页庄园图标", "duration_ms": 280}},
                {"api_name": "swipe_right", "params": {"locator_name": "主页庄园图标", "duration_ms": 280}},
                {"api_name": "assert_text_equals", "params": {"locator_name": "主页庄园图标", "expected": "庄园"}},
            ],
        },
        {
            "task_id": "benchmark_area_tap_and_number_bounds",
            "display_name": "Benchmark Area Tap And Number Bounds",
            "api_calls": [
                {"api_name": "wait_template", "params": {"locator_name": "主页庄园图标", "timeout": 5.0}},
                {"api_name": "tap", "params": {"locator_name": "主页庄园图标"}},
                {"api_name": "ocr_number", "params": {"locator_name": "主页庄园图标"}},
                {"api_name": "assert_number_at_least", "params": {"locator_name": "主页庄园图标", "min_value": 0}},
                {"api_name": "assert_number_at_most", "params": {"locator_name": "主页庄园图标", "max_value": 9999}},
                {"api_name": "back", "params": {}},
            ],
        },
        {
            "task_id": "benchmark_direct_actions_mix",
            "display_name": "Benchmark Direct Actions Mix",
            "api_calls": [
                {"api_name": "exists", "params": {"locator_name": "主页庄园图标", "timeout": 1.0}},
                {"api_name": "tap_area", "params": {"locator_name": "主页庄园图标"}},
                {"api_name": "ocr_text_contains", "params": {"locator_name": "主页庄园图标", "expected": "庄园"}},
                {"api_name": "ocr_int_min", "params": {"locator_name": "主页庄园图标", "min_value": 0}},
                {"api_name": "ocr_int_max", "params": {"locator_name": "主页庄园图标", "max_value": 9999}},
                {"api_name": "sleep", "params": {"seconds": 1}},
            ],
        },
    ]
