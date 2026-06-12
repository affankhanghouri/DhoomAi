BRAND_DNA_ENRICHMENT_JSON_SCHEMA = {
    "name": "brand_dna_enrichment_output",
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
                    "buyer_behavior",
                    "trust_barriers",
                    "selling_channels",
                    "seasonal_moments",
                    "price_sensitivity",
                ],
                "properties": {
                    "buyer_behavior": {"type": "string"},
                    "trust_barriers": {"type": "string"},
                    "selling_channels": {"type": "string"},
                    "seasonal_moments": {"type": "string"},
                    "price_sensitivity": {"type": "string"},
                },
            },

            "selling_points": {
                "type": "array",
                "minItems": 3,
                "maxItems": 8,
                "items": {"type": "string"},
            },
            "trust_signals": {
                "type": "array",
                "minItems": 3,
                "maxItems": 8,
                "items": {"type": "string"},
            },
            "weaknesses": {
                "type": "array",
                "minItems": 3,
                "maxItems": 8,
                "items": {"type": "string"},
            },

            "campaign_rules": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "do",
                    "avoid",
                    "best_campaign_angles",
                    "poster_rules",
                    "caption_rules",
                ],
                "properties": {
                    "do": {
                        "type": "array",
                        "minItems": 3,
                        "maxItems": 8,
                        "items": {"type": "string"},
                    },
                    "avoid": {
                        "type": "array",
                        "minItems": 3,
                        "maxItems": 8,
                        "items": {"type": "string"},
                    },
                    "best_campaign_angles": {
                        "type": "array",
                        "minItems": 3,
                        "maxItems": 8,
                        "items": {"type": "string"},
                    },
                    "poster_rules": {
                        "type": "array",
                        "minItems": 3,
                        "maxItems": 8,
                        "items": {"type": "string"},
                    },
                    "caption_rules": {
                        "type": "array",
                        "minItems": 3,
                        "maxItems": 8,
                        "items": {"type": "string"},
                    },
                },
            },

            "angle_strategy": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "strongest_angles",
                    "avoid_angles",
                    "positioning_notes",
                ],
                "properties": {
                    "strongest_angles": {
                        "type": "array",
                        "minItems": 3,
                        "maxItems": 8,
                        "items": {"type": "string"},
                    },
                    "avoid_angles": {
                        "type": "array",
                        "minItems": 2,
                        "maxItems": 6,
                        "items": {"type": "string"},
                    },
                    "positioning_notes": {"type": "string"},
                },
            },

            "content_language_strategy": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "primary_language",
                    "roman_urdu_usage",
                    "emoji_usage",
                    "tone_notes",
                ],
                "properties": {
                    "primary_language": {"type": "string"},
                    "roman_urdu_usage": {"type": "string"},
                    "emoji_usage": {"type": "string"},
                    "tone_notes": {"type": "string"},
                },
            },

            "confidence": {"type": "number"},
        },
    },
    "strict": True,
}