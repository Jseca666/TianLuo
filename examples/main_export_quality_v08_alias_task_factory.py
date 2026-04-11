def build_main_export_quality_v08_alias_task_specs():
    return [
        {
            "task_id": "v08_alias_wait_click_read_back",
            "display_name": "V08 Alias Wait Click Read Back",
            "api_calls": [
                {"api_name": "assert_exists", "params": {"locator_name": "主页庄园图标", "timeout": 1.0}},
                {"api_name": "wait_for_locator", "params": {"locator_name": "主页庄园图标", "timeout": 5.0}},
                {"api_name": "click_template", "params": {"locator_name": "主页庄园图标", "timeout": 3.0}},
                {"api_name": "read_text", "params": {"locator_name": "主页庄园图标"}},
                {"api_name": "assert_text_contains", "params": {"locator_name": "主页庄园图标", "expected": "庄园"}},
                {"api_name": "back", "params": {}},
            ],
        },
        {
            "task_id": "v08_alias_scroll_and_number_bounds",
            "display_name": "V08 Alias Scroll And Number Bounds",
            "api_calls": [
                {"api_name": "wait_for_image", "params": {"locator_name": "主页庄园图标", "timeout": 5.0}},
                {"api_name": "click", "params": {"locator_name": "主页庄园图标"}},
                {"api_name": "scroll_down", "params": {"locator_name": "主页庄园图标", "duration_ms": 280}},
                {"api_name": "scroll_up", "params": {"locator_name": "主页庄园图标", "duration_ms": 280}},
                {"api_name": "read_number", "params": {"locator_name": "主页庄园图标"}},
                {"api_name": "assert_number_min", "params": {"locator_name": "主页庄园图标", "min_value": 0}},
                {"api_name": "assert_number_max", "params": {"locator_name": "主页庄园图标", "max_value": 9999}},
            ],
        },
        {
            "task_id": "v08_alias_direct_click_area_mix",
            "display_name": "V08 Alias Direct Click Area Mix",
            "api_calls": [
                {"api_name": "exists_locator", "params": {"locator_name": "主页庄园图标", "timeout": 1.0}},
                {"api_name": "click_area", "params": {"locator_name": "主页庄园图标"}},
                {"api_name": "check_text_equals", "params": {"locator_name": "主页庄园图标", "expected": "庄园"}},
                {"api_name": "sleep", "params": {"seconds": 1}},
            ],
        },
    ]
