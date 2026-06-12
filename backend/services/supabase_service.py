"""Supabase client helpers."""

from fastapi import HTTPException

from core.config import settings


def get_supabase():
    if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_ROLE_KEY:
        raise HTTPException(
            status_code=500,
            detail=(
                "Missing backend Supabase settings. Add SUPABASE_URL and "
                "SUPABASE_SERVICE_ROLE_KEY to backend/.env."
            ),
        )

    try:
        from supabase  import create_client
    except ModuleNotFoundError as exc:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail="Supabase Python package is not installed. Run `pip install supabase`.",
        ) from exc

    return create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)
