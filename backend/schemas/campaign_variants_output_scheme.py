CAMPAIGN_VARIANTS_JSON_SCHEMA = {
    "name": "campaign_variants_output",
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "required": ["variants"],
        "properties": {
            "variants": {
                "type": "array",
                "minItems": 3,
                "maxItems": 3,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": [
                        "variant_id",
                        "name",
                        "description",
                        "visual_direction",
                        "caption_style",
                        "whatsapp_style",
                        "poster_layout",
                        "why_it_fits",
                        "confidence",
                    ],
                    "properties": {
                        "variant_id": {
                            "type": "string",
                            "description": "kebab-case unique id",
                        },
                        "name": {"type": "string"},
                        "description": {"type": "string"},
                        "visual_direction": {"type": "string"},
                        "caption_style": {"type": "string"},
                        "whatsapp_style": {"type": "string"},
                        "poster_layout": {"type": "string"},
                        "why_it_fits": {"type": "string"},
                        "confidence": {"type": "number"},
                    },
                },
            }
        },
    },
    "strict": True,
}


REFINED_VARIANT_JSON_SCHEMA = {
    "name": "refined_campaign_variant_output",
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "variant_id",
            "name",
            "description",
            "visual_direction",
            "caption_style",
            "whatsapp_style",
            "poster_layout",
            "why_it_fits",
            "confidence",
        ],
        "properties": {
            "variant_id": {"type": "string"},
            "name": {"type": "string"},
            "description": {"type": "string"},
            "visual_direction": {"type": "string"},
            "caption_style": {"type": "string"},
            "whatsapp_style": {"type": "string"},
            "poster_layout": {"type": "string"},
            "why_it_fits": {"type": "string"},
            "confidence": {"type": "number"},
        },
    },
    "strict": True,
}