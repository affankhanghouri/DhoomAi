from urllib.parse import urlparse


SUPPORTED_SOURCE_TYPES = {
    "auto",
    "website",
    "instagram",
    "facebook",
    "shopify",
    "daraz",
}


def normalize_source_type(source_type: str | None) -> str:
    if not source_type:
        return "auto"

    source_type = source_type.lower().strip()

    if source_type not in SUPPORTED_SOURCE_TYPES:
        return "auto"

    return source_type


def detect_source_type(url: str, requested_source_type: str | None = "auto") -> str:
    requested_source_type = normalize_source_type(requested_source_type)

    if requested_source_type != "auto":
        return requested_source_type

    domain = urlparse(url).netloc.lower().replace("www.", "")

    if "instagram.com" in domain:
        return "instagram"

    if "facebook.com" in domain or domain == "fb.com":
        return "facebook"

    if "myshopify.com" in domain:
        return "shopify"

    if "daraz." in domain:
        return "daraz"

    return "website"