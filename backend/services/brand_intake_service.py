import asyncio
from datetime import datetime, timezone

from services.brand_dna_pipeline import analyze_and_save_brand_dna
from services.supabase_service import get_supabase


INTAKE_STEPS = [
    {
        "id": "source_reader",
        "label": "Reading public brand source",
        "description": "Dhoom is scanning the link and collecting visible brand signals.",
    },
    {
        "id": "category_detector",
        "label": "Detecting business category",
        "description": "Finding what the seller offers and how the store should be positioned.",
    },
    {
        "id": "buyer_mapper",
        "label": "Mapping Pakistani buyer context",
        "description": "Understanding likely buyers, trust barriers, and social-commerce behavior.",
    },
    {
        "id": "tone_extractor",
        "label": "Extracting brand tone and trust signals",
        "description": "Finding the right campaign voice, visual style, and credibility points.",
    },
    {
        "id": "campaign_brain",
        "label": "Building campaign operating rules",
        "description": "Preparing Brand DNA rules for captions, posters, WhatsApp, and offers.",
    },
    {
        "id": "workspace_ready",
        "label": "Brand workspace ready",
        "description": "Your Dhoom campaign engine is ready for this brand.",
    },
]


def build_initial_steps() -> list[dict]:
    return [
        {
            **step,
            "status": "pending",
        }
        for step in INTAKE_STEPS
    ]


def update_job(
    job_id: str,
    *,
    status: str,
    current_step: str,
    progress: int,
    steps: list[dict],
    brand_profile_id: str | None = None,
    error_message: str | None = None,
    completed: bool = False,
):
    payload = {
        "status": status,
        "current_step": current_step,
        "progress": progress,
        "steps": steps,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }

    if brand_profile_id:
        payload["brand_profile_id"] = brand_profile_id

    if error_message:
        payload["error_message"] = error_message

    if completed:
        payload["completed_at"] = datetime.now(timezone.utc).isoformat()

    supabase = get_supabase()
    supabase.table("brand_intake_jobs").update(payload).eq("id", job_id).execute()


def mark_step(steps: list[dict], active_index: int) -> list[dict]:
    next_steps = []

    for index, step in enumerate(steps):
        if index < active_index:
            status = "completed"
        elif index == active_index:
            status = "processing"
        else:
            status = "pending"

        next_steps.append(
            {
                **step,
                "status": status,
            }
        )

    return next_steps


async def run_brand_intake_job(job_id: str, source_url: str, source_type: str):
    steps = build_initial_steps()

    try:
        for index, step in enumerate(INTAKE_STEPS[:-1]):
            progress = min(12 + index * 15, 82)
            active_steps = mark_step(steps, index)

            update_job(
                job_id,
                status="processing",
                current_step=step["id"],
                progress=progress,
                steps=active_steps,
            )

            await asyncio.sleep(0.7)

        result = await analyze_and_save_brand_dna(
            source_url=source_url,
            source_type=source_type,
        )

        final_steps = [
            {
                **step,
                "status": "completed",
            }
            for step in steps
        ]

        update_job(
            job_id,
            status="completed",
            current_step="workspace_ready",
            progress=100,
            steps=final_steps,
            brand_profile_id=result["id"],
            completed=True,
        )

    except Exception as exc:
        failed_steps = []

        for step in steps:
            failed_steps.append(
                {
                    **step,
                    "status": "failed" if step.get("status") == "processing" else step["status"],
                }
            )

        update_job(
            job_id,
            status="failed",
            current_step="failed",
            progress=0,
            steps=failed_steps,
            error_message=str(exc),
        )
