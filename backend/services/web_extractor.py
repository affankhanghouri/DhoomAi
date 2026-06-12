import json
import re
from html.parser import HTMLParser
from urllib.parse import urlparse

import httpx

try:
    from bs4 import BeautifulSoup
except ModuleNotFoundError:
    BeautifulSoup = None

from services.source_detector import detect_source_type


class WebsiteExtractionError(Exception):
    pass


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()


class BasicHTMLContextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.meta_description = ""
        self.og_title = ""
        self.og_description = ""
        self.twitter_title = ""
        self.twitter_description = ""
        self.headings: list[str] = []
        self.text_parts: list[str] = []
        self._current_tag = ""
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)

        if tag in {"script", "style", "noscript", "svg", "iframe"}:
            self._skip_depth += 1
            return

        self._current_tag = tag

        if tag != "meta":
            return

        content = attrs_dict.get("content")
        if not content:
            return

        name = attrs_dict.get("name")
        property_name = attrs_dict.get("property")

        if name == "description":
            self.meta_description = clean_text(content)
        elif property_name == "og:title":
            self.og_title = clean_text(content)
        elif property_name == "og:description":
            self.og_description = clean_text(content)
        elif name == "twitter:title":
            self.twitter_title = clean_text(content)
        elif name == "twitter:description":
            self.twitter_description = clean_text(content)

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript", "svg", "iframe"} and self._skip_depth:
            self._skip_depth -= 1

        if self._current_tag == tag:
            self._current_tag = ""

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return

        text = clean_text(data)
        if not text:
            return

        if self._current_tag == "title" and not self.title:
            self.title = text
        elif self._current_tag in {"h1", "h2", "h3"} and len(text) > 2:
            self.headings.append(text)

        self.text_parts.append(text)


def safe_get_meta(soup, *, name: str | None = None, property_name: str | None = None) -> str:
    tag = None

    if name:
        tag = soup.find("meta", attrs={"name": name})

    if property_name and not tag:
        tag = soup.find("meta", attrs={"property": property_name})

    if tag and tag.get("content"):
        return clean_text(str(tag.get("content")))

    return ""


def extract_json_ld(soup: BeautifulSoup) -> list[dict]:
    items: list[dict] = []

    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        raw = script.string or script.get_text()

        if not raw:
            continue

        try:
            parsed = json.loads(raw)

            if isinstance(parsed, list):
                for item in parsed:
                    if isinstance(item, dict):
                        items.append(item)

            elif isinstance(parsed, dict):
                items.append(parsed)

        except Exception:
            continue

    return items[:10]


def get_path_slug(url: str) -> str:
    parsed = urlparse(url)
    parts = [part for part in parsed.path.split("/") if part]

    if not parts:
        return ""

    return parts[0].replace("@", "")


async def fetch_html(url: str) -> str:
    parsed = urlparse(url)

    if parsed.scheme not in ["http", "https"]:
        raise WebsiteExtractionError("Only http and https links are allowed.")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.text
    except Exception as exc:
        raise WebsiteExtractionError(
            "Could not read this public link. Try another public store/profile link."
        ) from exc


def extract_base_context(url: str, html: str, source_type: str) -> dict:
    parsed = urlparse(url)
    domain = parsed.netloc.lower().replace("www.", "")

    if BeautifulSoup is None:
        parser = BasicHTMLContextParser()
        parser.feed(html)

        title = parser.title
        meta_description = parser.meta_description
        og_title = parser.og_title
        og_description = parser.og_description
        twitter_title = parser.twitter_title
        twitter_description = parser.twitter_description
        headings = parser.headings[:25]
        body_text = clean_text(" ".join(parser.text_parts))
        json_ld: list[dict] = []
    else:
        soup = BeautifulSoup(html, "html.parser")

        for tag in soup(["script", "style", "noscript", "svg", "iframe"]):
            tag.decompose()

        title = clean_text(soup.title.string) if soup.title and soup.title.string else ""

        meta_description = safe_get_meta(soup, name="description")
        og_title = safe_get_meta(soup, property_name="og:title")
        og_description = safe_get_meta(soup, property_name="og:description")
        twitter_title = safe_get_meta(soup, name="twitter:title")
        twitter_description = safe_get_meta(soup, name="twitter:description")

        headings = []
        for heading in soup.find_all(["h1", "h2", "h3"]):
            text = clean_text(heading.get_text(" "))
            if text and len(text) > 2:
                headings.append(text)

        body_text = clean_text(soup.get_text(" "))
        json_ld = extract_json_ld(BeautifulSoup(html, "html.parser"))

    best_title = og_title or twitter_title or title or domain
    best_description = og_description or twitter_description or meta_description

    combined = "\n".join(
        [
            f"Source Type: {source_type}",
            f"Domain: {domain}",
            f"Title: {title}",
            f"OG Title: {og_title}",
            f"Twitter Title: {twitter_title}",
            f"Meta Description: {meta_description}",
            f"OG Description: {og_description}",
            f"Twitter Description: {twitter_description}",
            "Headings: " + " | ".join(headings[:25]),
            "Body: " + body_text[:7000],
            "JSON-LD: " + json.dumps(json_ld[:4], ensure_ascii=False)[:3000],
        ]
    )

    return {
        "url": url,
        "source_type": source_type,
        "source_platform": source_type,
        "domain": domain,
        "title": best_title,
        "meta_description": best_description,
        "headings": headings[:25],
        "json_ld": json_ld,
        "text": combined[:10000],
        "raw_source_data": {
            "title": title,
            "og_title": og_title,
            "og_description": og_description,
            "twitter_title": twitter_title,
            "twitter_description": twitter_description,
            "meta_description": meta_description,
            "headings": headings[:25],
            "json_ld_count": len(json_ld),
        },
    }


def enrich_instagram_context(context: dict) -> dict:
    username = get_path_slug(context["url"])

    extra = f"""
Instagram source notes:
- Username/page slug: {username or "unknown"}
- Treat this as an Instagram-first seller unless the page text proves otherwise.
- Focus on social-commerce behavior: profile trust, visual identity, DMs/WhatsApp ordering, comments, highlights, reels, and product showcase style.
- If public page data is limited, confidence should be lower and weaknesses should mention limited public profile data.
"""

    context["text"] = f"{extra}\n\n{context['text']}"
    context["raw_source_data"]["profile_slug"] = username
    return context


def enrich_facebook_context(context: dict) -> dict:
    page_slug = get_path_slug(context["url"])

    extra = f"""
Facebook source notes:
- Page slug: {page_slug or "unknown"}
- Treat this as a Facebook/social-commerce seller unless the page text proves otherwise.
- Focus on trust signals, reviews, page activity, local buyer behavior, Messenger/WhatsApp ordering, delivery clarity, and offer posts.
- If public page data is limited, confidence should be lower and weaknesses should mention limited public page data.
"""

    context["text"] = f"{extra}\n\n{context['text']}"
    context["raw_source_data"]["page_slug"] = page_slug
    return context


def enrich_shopify_context(context: dict) -> dict:
    extra = """
Shopify source notes:
- Treat this as an ecommerce store.
- Look for product category, brand style, pricing, shipping/return trust, catalog clarity, and conversion signals.
- Campaigns should work for product pages, Instagram posts, and WhatsApp follow-up.
"""

    context["text"] = f"{extra}\n\n{context['text']}"
    return context


def enrich_daraz_context(context: dict) -> dict:
    extra = """
Daraz source notes:
- Treat this as a marketplace/store/product source.
- Focus on marketplace buyer behavior: price comparison, ratings/reviews, delivery trust, product title clarity, discount hooks, and feature clarity.
- Campaigns should translate marketplace product value into Instagram/WhatsApp-style campaign assets.
"""

    context["text"] = f"{extra}\n\n{context['text']}"
    return context


async def extract_website_context(url: str, source_type: str = "auto") -> dict:
    detected_source_type = detect_source_type(url, source_type)

    try:
        html = await fetch_html(url)
    except WebsiteExtractionError:
        if detected_source_type in ["facebook", "instagram", "daraz"]:
            return build_limited_social_context(url, detected_source_type)

        raise

    context = extract_base_context(url, html, detected_source_type)

    if detected_source_type == "instagram":
        return enrich_instagram_context(context)

    if detected_source_type == "facebook":
        return enrich_facebook_context(context)

    if detected_source_type == "shopify":
        return enrich_shopify_context(context)

    if detected_source_type == "daraz":
        return enrich_daraz_context(context)

    return context

def build_limited_social_context(url: str, source_type: str) -> dict:
    parsed = urlparse(url)
    domain = parsed.netloc.lower().replace("www.", "")
    slug = get_path_slug(url)

    platform_label = source_type.title()

    if source_type == "facebook":
        source_notes = f"""
Facebook limited-access source notes:
- Facebook did not return readable public page HTML to the backend.
- Page slug/name from URL: {slug or "unknown"}
- Treat this as a Facebook/social-commerce seller profile.
- Analyze carefully using only the page URL, slug, platform behavior, and Pakistani market context.
- Confidence should be lower because public page content was limited.
- Weaknesses must mention that public Facebook data was limited.
- Focus on trust, Messenger/WhatsApp ordering, social proof, page credibility, delivery clarity, and offer-style campaigns.
"""

    elif source_type == "instagram":
        source_notes = f"""
Instagram limited-access source notes:
- Instagram returned limited public data to the backend.
- Profile slug/username from URL: {slug or "unknown"}
- Treat this as an Instagram-first social-commerce seller.
- Confidence should be lower because public profile content was limited.
- Weaknesses must mention that public Instagram data was limited.
- Focus on profile trust, visual identity, DMs/WhatsApp ordering, highlights, reels, and product showcase style.
"""

    elif source_type == "daraz":
        source_notes = f"""
Daraz limited-access source notes:
- Daraz did not return enough readable public HTML to the backend.
- Source slug from URL: {slug or "unknown"}
- Treat this as a marketplace/store/product source.
- Confidence should be lower because public marketplace data was limited.
- Focus on price comparison, ratings/reviews if visible later, delivery trust, product clarity, discounts, and marketplace buyer behavior.
"""

    else:
        source_notes = f"""
Limited-access source notes:
- The source did not return enough readable public HTML to the backend.
- Source slug from URL: {slug or "unknown"}
- Confidence should be lower because public data was limited.
"""

    text = f"""
Source Type: {source_type}
Source Platform: {platform_label}
Domain: {domain}
Source URL: {url}
Detected slug/name: {slug or "unknown"}

{source_notes}

Instruction:
Create Brand DNA using this limited source context. Do not invent exact products, prices, reviews, followers, or claims. Use cautious language. Mention limited public source data in weaknesses.
"""

    return {
        "url": url,
        "source_type": source_type,
        "source_platform": source_type,
        "domain": domain,
        "title": slug or domain,
        "meta_description": "",
        "headings": [slug] if slug else [],
        "json_ld": [],
        "text": text.strip(),
        "raw_source_data": {
            "access_status": "limited",
            "profile_slug": slug,
            "reason": "source did not return readable public HTML",
        },
    }