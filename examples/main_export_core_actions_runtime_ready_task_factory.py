def build_main_export_core_actions_runtime_ready_task_specs():
    return [
        {
            "task_id": "core_actions_runtime_ready_tap_back_wait",
            "display_name": "Core Actions Runtime Ready Tap Back Wait",
            "api_calls": [
                {"api_name": "tap_point", "params": {"x": 540, "y": 1200}},
                {"api_name": "sleep_ms", "params": {"milliseconds": 800}},
                {"api_name": "press_back", "params": {}},
            ],
        },
        {
            "task_id": "core_actions_runtime_ready_swipe_aliases",
            "display_name": "Core Actions Runtime Ready Swipe Aliases",
            "api_calls": [
                {
                    "api_name": "swipe_xy",
                    "params": {"x1": 540, "y1": 1600, "x2": 540, "y2": 700, "duration": 0.35},
                },
                {
                    "api_name": "wait_ms",
                    "params": {"ms": 500},
                },
                {
                    "api_name": "click_xy",
                    "params": {"point_x": 420, "point_y": 980},
                },
                {
                    "api_name": "go_back",
                    "params": {},
                },
            ],
        },
    ]
