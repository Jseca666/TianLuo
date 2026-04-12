def build_main_export_core_actions_task_specs():
    return [
        {
            "task_id": "core_actions_tap_single_point",
            "display_name": "Core Actions Tap Single Point",
            "api_calls": [
                {
                    "api_name": "tap_point",
                    "params": {"x": 540, "y": 1200},
                },
            ],
        },
        {
            "task_id": "core_actions_tap_wait_back",
            "display_name": "Core Actions Tap Wait Back",
            "api_calls": [
                {
                    "api_name": "click_point",
                    "params": {"point_x": 300, "point_y": 900},
                },
                {
                    "api_name": "sleep_seconds",
                    "params": {"seconds": 1.5},
                },
                {
                    "api_name": "back",
                    "params": {},
                },
            ],
        },
        {
            "task_id": "core_actions_swipe_path",
            "display_name": "Core Actions Swipe Path",
            "api_calls": [
                {
                    "api_name": "swipe_points",
                    "params": {
                        "start_x": 540,
                        "start_y": 1600,
                        "end_x": 540,
                        "end_y": 600,
                        "duration_ms": 350,
                    },
                },
                {
                    "api_name": "swipe_xy",
                    "params": {
                        "x1": 540,
                        "y1": 700,
                        "x2": 540,
                        "y2": 1500,
                        "duration": 0.4,
                    },
                },
            ],
        },
    ]
