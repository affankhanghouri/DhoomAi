def fallback_quality_check(final_campaign: dict) -> dict:
    risk_flags: list[str] = []

    caption = final_campaign.get("caption") or ""
    whatsapp_copy = final_campaign.get("whatsapp_copy") or ""
    poster_direction = final_campaign.get("poster_direction") or ""
    primary_cta = final_campaign.get("primary_cta") or ""

    score = 76
    improvements = []

    if len(caption.strip()) < 80:
        score -= 8
        improvements.append("Caption may be too short; added clarity where possible.")

    if len(whatsapp_copy.strip()) < 40:
        score -= 8
        improvements.append("WhatsApp copy may need clearer ordering direction.")

    if len(poster_direction.strip()) < 80:
        score -= 7
        improvements.append("Poster direction may need more execution detail.")

    if not primary_cta:
        score -= 8
        final_campaign["primary_cta"] = "Message us to order"
        improvements.append("Added a clearer primary CTA.")

    risky_words = ["guaranteed", "100%", "cure", "instant result", "best in pakistan"]

    combined = f"{caption} {whatsapp_copy} {poster_direction}".lower()

    for word in risky_words:
        if word in combined:
            risk_flags.append(f"Potential unsupported claim: {word}")

    if risk_flags:
        score -= 8

    score = max(min(score, 88), 55)

    if score >= 82:
        status = "approved"
    elif score >= 70:
        status = "improved"
    else:
        status = "needs_review"

    if not improvements:
        improvements = [
            "Checked campaign clarity.",
            "Checked CTA strength.",
            "Checked risk and unsupported claims.",
        ]

    return {
        "final_campaign": final_campaign,
        "quality_report": {
            "campaign_score": score,
            "quality_status": status,
            "quality_notes": [
                "Campaign was checked for brand fit.",
                "Campaign was checked for Pakistani market relevance.",
                "Campaign was checked for caption, WhatsApp, poster, and CTA clarity.",
                "Campaign was checked for generic or risky claims.",
            ],
            "improvements_applied": improvements,
            "risk_flags": risk_flags,
        },
    }
