FINAL_CAMPAIGN_JSON_SCHEMA = {
    "name": "final_campaign_output",
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "campaign_headline",
            "campaign_angle",
            "buyer_insight",
            "caption",
            "whatsapp_copy",
            "offer_idea",
            "story_flow",
            "poster_direction",
            "reel_direction",
            "primary_cta",
            "do_rules",
            "avoid_rules",
            "confidence",
        ],
        "properties": {
            "campaign_headline": {
                "type": "string",
                "description": "Short powerful campaign headline",
            },
            "campaign_angle": {
                "type": "string",
                "description": "Final strategic campaign angle",
            },
            "buyer_insight": {
                "type": "string",
                "description": "The buyer psychology behind the campaign",
            },
            "caption": {
                "type": "string",
                "description": "Instagram/Facebook caption ready to use",
            },
            "whatsapp_copy": {
                "type": "string",
                "description": "WhatsApp message copy ready to use",
            },
            "offer_idea": {
                "type": "string",
                "description": "Practical offer idea for the seller",
            },
            "story_flow": {
                "type": "array",
                "minItems": 4,
                "maxItems": 5,
                "items": {"type": "string"},
            },
            "poster_direction": {
                "type": "string",
                "description": "Detailed poster creative direction",
            },
            "reel_direction": {
                "type": "string",
                "description": "Short reel/video creative direction",
            },
            "primary_cta": {
                "type": "string",
                "description": "Main call to action",
            },
            "do_rules": {
                "type": "array",
                "minItems": 3,
                "maxItems": 6,
                "items": {"type": "string"},
            },
            "avoid_rules": {
                "type": "array",
                "minItems": 3,
                "maxItems": 6,
                "items": {"type": "string"},
            },
            "confidence": {
                "type": "number",
                "description": "0 to 1 final campaign confidence",
            },
        },
    },
    "strict": True,
}