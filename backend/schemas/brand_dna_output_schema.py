BRAND_DNA_JSON_SCHEMA = {
    "name": "brand_dna_output",
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "brand_name",
            "business_type",
            "category",
            "summary",
            "target_audience",
            "tone",
            "visual_style",
            "price_positioning",
            "pakistani_market_context",
            "selling_points",
            "trust_signals",
            "weaknesses",
            "campaign_rules",
            "angle_strategy",
            "content_language_strategy",
            "confidence",
        ],
        "properties": {
            "brand_name": {"type": "string"},
            "business_type": {"type": "string"},
            "category": {"type": "string"},
            "summary": {"type": "string"},
            "target_audience": {"type": "string"},
            "tone": {"type": "string"},
            "visual_style": {"type": "string"},
            "price_positioning": {"type": "string"},

            "pakistani_market_context": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "buyer_mindset",
                    "trust_barriers",
                    "purchase_triggers",
                    "seasonal_relevance",
                    "platform_behavior",
                ],
                "properties": {
                    "buyer_mindset": {"type": "string"},
                    "trust_barriers": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "purchase_triggers": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "seasonal_relevance": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "platform_behavior": {"type": "string"},
                },
            },

            "selling_points": {
                "type": "array",
                "items": {"type": "string"},
            },

            "trust_signals": {
                "type": "array",
                "items": {"type": "string"},
            },

            "weaknesses": {
                "type": "array",
                "items": {"type": "string"},
            },

            "campaign_rules": {
                "type": "object",
                "additionalProperties": False,
                "required": ["do", "avoid", "poster_rules", "caption_rules"],
                "properties": {
                    "do": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "avoid": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "poster_rules": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "caption_rules": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
            },

            "angle_strategy": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "best_angles",
                    "bad_angles",
                    "default_campaign_direction",
                ],
                "properties": {
                    "best_angles": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "additionalProperties": False,
                            "required": ["title", "why_it_works", "when_to_use"],
                            "properties": {
                                "title": {"type": "string"},
                                "why_it_works": {"type": "string"},
                                "when_to_use": {"type": "string"},
                            },
                        },
                    },
                    "bad_angles": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "default_campaign_direction": {"type": "string"},
                },
            },

            "content_language_strategy": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "primary_language",
                    "roman_urdu_usage",
                    "english_usage",
                    "tone_warning",
                ],
                "properties": {
                    "primary_language": {"type": "string"},
                    "roman_urdu_usage": {"type": "string"},
                    "english_usage": {"type": "string"},
                    "tone_warning": {"type": "string"},
                },
            },

            "confidence": {"type": "number"},
        },
    },
    "strict": True,
}