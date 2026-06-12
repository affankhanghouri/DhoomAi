import base64
import mimetypes
import os
import tempfile
from datetime import datetime, timezone

import httpx
from openai import OpenAI

from core.config import settings
from services.supabase_service import get_supabase


client = OpenAI(api_key=settings.OPENAI_API_KEY)


class PosterGenerationError(Exception):
    pass


def build_safe_poster_prompt(asset: dict, draft: dict) -> str:
    product_name = draft.get("product_name") or "the product"
    category = draft.get("category") or "product"

    return f"""
Create a premium social-commerce poster visual for a Pakistani online seller.

Product:
- Name: {product_name}
- Category: {category}

Creative direction:
{asset.get("generation_prompt")}

Source prompt:
{asset.get("source_prompt")}

Execution rules:
- Use the attached product image as the main product reference.
- Preserve product shape, color, style, and identity as much as possible.
- Keep product as the hero.
- Create a premium Instagram/Facebook ad composition.
- Keep background clean, polished, modern, and conversion-focused.
- Leave clean negative space for headline, buyer benefit, and CTA overlay.
- Do not add fake reviews.
- Do not add fake discounts.
- Do not add fake badges.
- Do not add unsupported claims.
- Avoid tiny unreadable text.
- Avoid clutter.
- Avoid watermarks.
- Avoid logos unless visible in the provided product image.
"""


async def download_reference_image(image_url: str) -> tuple[str, str]:
    try:
        async with httpx.AsyncClient(timeout=30, follow_redirects=True) as http:
            response = await http.get(image_url)
            response.raise_for_status()
    except Exception as exc:
        raise PosterGenerationError("Could not download product reference image.") from exc

    content_type = response.headers.get("content-type", "image/png").split(";")[0]
    extension = mimetypes.guess_extension(content_type) or ".png"

    if extension not in [".png", ".jpg", ".jpeg", ".webp"]:
        extension = ".png"
        content_type = "image/png"

    temp = tempfile.NamedTemporaryFile(delete=False, suffix=extension)
    temp.write(response.content)
    temp.close()

    return temp.name, content_type


def upload_generated_image_to_supabase(
    image_bytes: bytes,
    generated_asset_id: str,
) -> tuple[str, str]:
    file_path = f"posters/{generated_asset_id}-{int(datetime.now().timestamp())}.png"
    supabase = get_supabase()

    try:
        supabase.storage.from_(settings.GENERATED_ASSETS_BUCKET).upload(
            path=file_path,
            file=image_bytes,
            file_options={
                "content-type": "image/png",
                "upsert": "true",
            },
        )
    except Exception as exc:
        raise PosterGenerationError("Could not upload generated poster.") from exc

    public_url = supabase.storage.from_(
        settings.GENERATED_ASSETS_BUCKET,
    ).get_public_url(file_path)

    return file_path, public_url


async def generate_poster_image(asset: dict, draft: dict) -> tuple[bytes, dict]:
    prompt = build_safe_poster_prompt(asset=asset, draft=draft)
    product_image_url = draft.get("product_image_url")

    try:
        if product_image_url:
            reference_path, _content_type = await download_reference_image(
                product_image_url,
            )

            try:
                with open(reference_path, "rb") as image_file:
                    result = client.images.edit(
                        model=settings.OPENAI_IMAGE_MODEL,
                        image=image_file,
                        prompt=prompt,
                        size=settings.OPENAI_IMAGE_SIZE,
                        quality=settings.OPENAI_IMAGE_QUALITY,
                    )
            finally:
                if os.path.exists(reference_path):
                    os.remove(reference_path)
        else:
            result = client.images.generate(
                model=settings.OPENAI_IMAGE_MODEL,
                prompt=prompt,
                size=settings.OPENAI_IMAGE_SIZE,
                quality=settings.OPENAI_IMAGE_QUALITY,
            )

        image_base64 = result.data[0].b64_json

        if not image_base64:
            raise PosterGenerationError("Image model returned empty image data.")

        image_bytes = base64.b64decode(image_base64)

        metadata = {
            "model": settings.OPENAI_IMAGE_MODEL,
            "size": settings.OPENAI_IMAGE_SIZE,
            "quality": settings.OPENAI_IMAGE_QUALITY,
            "used_reference_image": bool(product_image_url),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

        return image_bytes, metadata

    except PosterGenerationError:
        raise
    except Exception as exc:
        raise PosterGenerationError("Poster generation failed.") from exc


def map_generated_asset(row: dict) -> dict:
    return {
        "id": row["id"],
        "asset_brief_id": row["asset_brief_id"],
        "output_id": row["output_id"],
        "draft_id": row["draft_id"],
        "asset_type": row["asset_type"],
        "asset_slot": row["asset_slot"],
        "title": row["title"],
        "description": row.get("description"),
        "source_prompt": row["source_prompt"],
        "generation_prompt": row["generation_prompt"],
        "asset_url": row.get("asset_url"),
        "asset_path": row.get("asset_path"),
        "thumbnail_url": row.get("thumbnail_url"),
        "status": row["status"],
        "provider": row.get("provider"),
        "generation_metadata": row.get("generation_metadata") or {},
    }
