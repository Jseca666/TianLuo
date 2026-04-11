def build_main_export_quality_semantic_task_specs():
    return [
        {
            "task_id": "semantic_wait_with_threshold_mask_color",
            "display_name": "Semantic Wait With Threshold Mask Color",
            "api_calls": [
                {
                    "api_name": "wait_locator",
                    "params": {
                        "locator_name": "主页庄园图标",
                        "timeout": 6.0,
                        "threshold": 0.92,
                        "mask_name": "主页庄园图标掩码",
                        "use_color": True,
                    },
                },
                {
                    "api_name": "tap_template",
                    "params": {
                        "locator_name": "主页庄园图标",
                        "timeout": 3.0,
                        "threshold": 0.9,
                        "mask": "主页庄园图标掩码",
                        "useColor": True,
                    },
                },
            ],
        },
        {
            "task_id": "semantic_exists_and_ocr_masked",
            "display_name": "Semantic Exists And Ocr Masked",
            "api_calls": [
                {
                    "api_name": "exists_image",
                    "params": {
                        "image_name": "主页庄园图标",
                        "timeout_seconds": 1.5,
                        "similarity_threshold": 0.88,
                        "mask_name": "主页庄园图标掩码",
                    },
                },
                {
                    "api_name": "ocr_text",
                    "params": {
                        "locator_name": "主页庄园图标",
                        "mask_name": "主页庄园图标掩码",
                        "kernel_size": 3,
                    },
                },
                {
                    "api_name": "assert_text_contains",
                    "params": {
                        "locator_name": "主页庄园图标",
                        "expected": "庄园",
                        "mask_name": "主页庄园图标掩码",
                    },
                },
            ],
        },
        {
            "task_id": "semantic_number_bounds_and_swipe",
            "display_name": "Semantic Number Bounds And Swipe",
            "api_calls": [
                {
                    "api_name": "ocr_number",
                    "params": {
                        "locator_name": "主页庄园图标",
                        "mask": "主页庄园图标掩码",
                        "excluded_number": -1,
                    },
                },
                {
                    "api_name": "assert_number_at_least",
                    "params": {
                        "locator_name": "主页庄园图标",
                        "min_value": 0,
                        "mask_name": "主页庄园图标掩码",
                    },
                },
                {
                    "api_name": "assert_number_at_most",
                    "params": {
                        "locator_name": "主页庄园图标",
                        "max_value": 9999,
                        "mask_name": "主页庄园图标掩码",
                    },
                },
                {
                    "api_name": "scroll_down",
                    "params": {
                        "locator_name": "主页庄园图标",
                        "duration": 0.35,
                    },
                },
                {
                    "api_name": "back",
                    "params": {},
                },
            ],
        },
    ]
