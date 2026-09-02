"""HTTP API for generation jobs and audio delivery."""

from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from redis.exceptions import RedisError
from rq.exceptions import NoSuchJobError
from rq.job import Job

from .config import get_settings
from .queue import get_generation_queue, get_redis
from .schemas import GenerationCreate, GenerationStatus, HealthStatus
from .tasks import generate_music

settings = get_settings()
app = FastAPI(title=settings.app_name, version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


def _fetch_job(generation_id: str) -> Job:
    try:
        return Job.fetch(generation_id, connection=get_redis())
    except NoSuchJobError as error:
        raise HTTPException(status_code=404, detail="Generation not found") from error
    except RedisError as error:
        raise HTTPException(status_code=503, detail="Queue is unavailable") from error


def _job_status(job: Job) -> GenerationStatus:
    job.refresh()
    job_status = job.get_status(refresh=False)
    output_url = f"/v1/generations/{job.id}/audio" if job_status == "finished" else None
    return GenerationStatus(
        id=job.id,
        status=job_status,
        output_url=output_url,
        error=job.exc_info if job_status == "failed" else None,
    )


@app.get("/health", response_model=HealthStatus)
def health() -> HealthStatus:
    try:
        get_redis().ping()
    except RedisError:
        return HealthStatus(status="degraded", redis="unavailable")
    return HealthStatus(status="ok", redis="ok")


@app.post(
    "/v1/generations",
    response_model=GenerationStatus,
    status_code=status.HTTP_202_ACCEPTED,
)
def create_generation(request: GenerationCreate) -> GenerationStatus:
    generation_id = uuid4().hex
    try:
        job = get_generation_queue().enqueue(
            generate_music,
            generation_id,
            request.model_dump(),
            job_id=generation_id,
            job_timeout="30m",
            result_ttl=86_400,
            failure_ttl=604_800,
        )
    except RedisError as error:
        raise HTTPException(status_code=503, detail="Queue is unavailable") from error
    return _job_status(job)


@app.get("/v1/generations/{generation_id}", response_model=GenerationStatus)
def get_generation(generation_id: str) -> GenerationStatus:
    return _job_status(_fetch_job(generation_id))


@app.get("/v1/generations/{generation_id}/audio")
def get_generated_audio(generation_id: str) -> FileResponse:
    job = _fetch_job(generation_id)
    if job.get_status(refresh=True) != "finished" or not isinstance(job.result, dict):
        raise HTTPException(status_code=409, detail="Generation is not complete")

    output_path = Path(job.result["output_path"]).resolve()
    output_dir = settings.output_dir.resolve()
    if not output_path.is_relative_to(output_dir) or not output_path.is_file():
        raise HTTPException(status_code=404, detail="Generated audio not found")
    return FileResponse(output_path, media_type="audio/mpeg", filename=output_path.name)
