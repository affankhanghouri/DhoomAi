from fastapi import APIRouter, BackgroundTasks, HTTPException

from schemas.brand_intake import (
    GetBrandIntakeResponse,
    StartBrandIntakeRequest,
    StartBrandIntakeResponse,
)
from services.brand_intake_service import build_initial_steps, run_brand_intake_job
from services.supabase_service import get_supabase


router = APIRouter(prefix="/brand-dna/intake", tags=["Brand DNA Intake"])


def map_job(row: dict) -> dict:
    return {
        "id": row["id"],
        "source_url": row["source_url"],
        "source_type": row["source_type"],
        "status": row["status"],
        "current_step": row.get("current_step"),
        "progress": int(row.get("progress") or 0),
        "steps": row.get("steps") or [],
        "brand_profile_id": row.get("brand_profile_id"),
        "error_message": row.get("error_message"),
    }


@router.post("/start", response_model=StartBrandIntakeResponse)
async def start_brand_intake_route(
    payload: StartBrandIntakeRequest,
    background_tasks: BackgroundTasks,
):
    steps = build_initial_steps()
    supabase = get_supabase()

    insert_result = (
        supabase.table("brand_intake_jobs")
        .insert(
            {
                "source_url": str(payload.source_url),
                "source_type": payload.source_type,
                "status": "queued",
                "current_step": "queued",
                "progress": 3,
                "steps": steps,
            }
        )
        .execute()
    )

    if not insert_result.data:
        raise HTTPException(status_code=500, detail="Could not start brand intake.")

    job = insert_result.data[0]

    background_tasks.add_task(
        run_brand_intake_job,
        job["id"],
        str(payload.source_url),
        payload.source_type,
    )

    return {"job": map_job(job)}


@router.get("/{job_id}", response_model=GetBrandIntakeResponse)
async def get_brand_intake_route(job_id: str):
    supabase = get_supabase()

    result = (
        supabase.table("brand_intake_jobs")
        .select("*")
        .eq("id", job_id)
        .single()
        .execute()
    )

    if not result.data:
        raise HTTPException(status_code=404, detail="Brand intake job not found.")

    return {"job": map_job(result.data)}
