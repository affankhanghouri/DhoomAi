CAMPAIGN_ASSET_BRIEF_JSON_SCHEMA = {
    "name": "campaign_asset_brief_output",
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "creative_brief_title",
            "poster_prompt",
            "image_generation_prompt",
            "poster_layout_direction",
            "poster_text_hierarchy",
            "poster_design_rules",
            "reel_prompt",
            "video_generation_prompt",
            "reel_shot_list",
            "reel_sound_direction",
            "reel_editing_style",
            "designer_notes",
            "asset_risks",
            "confidence",
        ],
        "properties": {
            "creative_brief_title": {"type": "string"},

            "poster_prompt": {"type": "string"},
            "image_generation_prompt": {"type": "string"},
            "poster_layout_direction": {"type": "string"},

            "poster_text_hierarchy": {
                "type": "array",
                "minItems": 3,
                "maxItems": 6,
                "items": {"type": "string"},
            },

            "poster_design_rules": {
                "type": "array",
                "minItems": 3,
                "maxItems": 8,
                "items": {"type": "string"},
            },

            "reel_prompt": {"type": "string"},
            "video_generation_prompt": {"type": "string"},

            "reel_shot_list": {
                "type": "array",
                "minItems": 4,
                "maxItems": 7,
                "items": {"type": "string"},
            },

            "reel_sound_direction": {"type": "string"},
            "reel_editing_style": {"type": "string"},

            "designer_notes": {
                "type": "array",
                "minItems": 3,
                "maxItems": 8,
                "items": {"type": "string"},
            },

            "asset_risks": {
                "type": "array",
                "minItems": 0,
                "maxItems": 6,
                "items": {"type": "string"},
            },

            "confidence": {"type": "number"},
        },
    },
    "strict": True,
}