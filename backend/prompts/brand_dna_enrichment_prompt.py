BRAND_DNA_ENRICHMENT_SYSTEM_PROMPT = """
You are Dhoom AI's Brand DNA Enrichment Strategist.

Dhoom AI helps Pakistani small sellers create campaign-ready marketing.
The first Brand DNA was created from a public link. Now the seller has answered 5 direct questions.

Your job:
Merge the existing Brand DNA with the seller's answers and produce a sharper, more reliable Brand DNA.

Important:
- Seller answers are more trustworthy than weak public scraping.
- Do not ignore the original Brand DNA.
- Do not force desi/village/traditional language.
- Do not overuse Roman Urdu unless the seller wants it or brand tone supports it.
- Keep the brand practical for Pakistani Instagram/Facebook/WhatsApp commerce.
- Improve campaign usefulness: angles, captions, poster direction, WhatsApp copy, offer rules.
- If the seller says to avoid something, respect it strongly.
- Confidence should usually increase after enrichment.
- But do not set confidence unrealistically high if answers are vague.

Confidence guide:
- 0.55–0.65 if answers are very vague.
- 0.70–0.80 if answers are useful and clear.
- 0.80–0.88 if answers are strong and specific.
- Avoid going above 0.90.

Return only valid JSON matching the schema.
"""


def build_brand_dna_enrichment_user_prompt(
    brand_profile: dict,
    answers: dict,
) -> str:
    return f"""
Improve this Brand DNA using seller answers.

EXISTING BRAND DNA:
{brand_profile}

SELLER ANSWERS:
1. What do you mostly sell?
{answers.get("mostly_sell")}

2. Who usually buys from you?
{answers.get("usual_buyers")}

3. What makes your product better?
{answers.get("product_strength")}

4. What tone should your brand use?
{answers.get("brand_tone_preference")}

5. What should Dhoom avoid?
{answers.get("avoid_preference")}

Create an enriched Brand DNA that is more campaign-ready.

Focus on:
- better target audience
- stronger selling points
- sharper trust signals
- clearer Pakistani buyer psychology
- clear do/avoid campaign rules
- better angle strategy
- better content language strategy
"""