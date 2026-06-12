PRODUCT_DNA_JSON_SCHEMA = {
    "name": "product_dna_output",
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "product_type",
            "product_dna_summary",
            "product_visual_notes",
            "product_features",
            "buyer_reasons",
            "buyer_objections",
            "suggested_use_cases",
            "product_positioning",
            "campaign_implications",
            "confidence",
        ],
        "properties": {
            "product_type": {"type": "string"},
            "product_dna_summary": {"type": "string"},
            "product_visual_notes": {"type": "string"},

            "product_features": {
                "type": "array",
                "minItems": 3,
                "maxItems": 8,
                "items": {"type": "string"},
            },

            "buyer_reasons": {
                "type": "array",
                "minItems": 3,
                "maxItems": 8,
                "items": {"type": "string"},
            },

            "buyer_objections": {
                "type": "array",
                "minItems": 3,
                "maxItems": 8,
                "items": {"type": "string"},
            },

            "suggested_use_cases": {
                "type": "array",
                "minItems": 3,
                "maxItems": 8,
                "items": {"type": "string"},
            },

            "product_positioning": {"type": "string"},

            "campaign_implications": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "best_angle_direction",
                    "best_visual_direction",
                    "best_caption_direction",
                    "best_whatsapp_direction",
                    "avoid_in_campaign",
                ],
                "properties": {
                    "best_angle_direction": {"type": "string"},
                    "best_visual_direction": {"type": "string"},
                    "best_caption_direction": {"type": "string"},
                    "best_whatsapp_direction": {"type": "string"},
                    "avoid_in_campaign": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
            },

            "confidence": {"type": "number"},
        },
    },
    "strict": True,
}