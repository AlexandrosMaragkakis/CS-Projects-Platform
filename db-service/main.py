from fastapi import FastAPI, HTTPException, status, Depends
from contextlib import asynccontextmanager
from pydantic import BaseModel, HttpUrl, Field
from uuid import uuid4
from neo4j import AsyncSession

from dependencies import get_db_session, close_db_connection

# TODO: add more models (f.e. response models)


class JobTemporary(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    status: str = "processing"
    company_id: str


class Job(BaseModel):
    id: str
    title: str
    company: str
    description: str
    seniority_level: str
    employment_type: str
    job_function: str
    industries: str
    url: HttpUrl


class JobResponse(BaseModel):
    message: str
    job_id: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield
    finally:
        close_db_connection()


app = FastAPI(
    lifespan=lifespan,
    title="Data Access Layer API",
    version="0.1",
    description="API for interacting with the database",
)


@app.get(
    "/jobs/{company_id}",
)
async def get_jobs(company_id: str, db: AsyncSession = Depends(get_db_session)):
    query = """
            MATCH (c:Company {uid: $company_id})-[:POSTED]->(j:Job)
            RETURN j.title as title, j.url as url, j.status as status
            """

    params = {"company_id": company_id}

    try:
        result = await db.run(query, **params)
        records = await result.data()
        jobs = [
            {"title": record["title"], "url": record["url"], "status": record["status"]}
            for record in records
        ]
        return {"jobs": jobs}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"A database error occurred (): {str(e)}",
        )


@app.post(
    "/jobs/create_tmp", response_model=JobResponse, status_code=status.HTTP_201_CREATED
)
async def create_tmp_job(
    tmp_job: JobTemporary, db: AsyncSession = Depends(get_db_session)
):
    query = """
            MERGE (c:Company {uid: $company_id})
            CREATE (j:Job
                {
                    id: $id,
                    status: $status
                }
            )
            CREATE (c)-[:POSTED]->(j)
            """

    params = {
        "id": tmp_job.id,
        "company_id": tmp_job.company_id,
        "status": tmp_job.status,
    }

    try:
        async with await db.begin_transaction() as tx:
            await tx.run(query, **params)
            await tx.commit()
        return JobResponse(
            message="Temporary job created successfully", job_id=tmp_job.id
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"A database error occurred: {str(e)}",
        )


@app.post(
    "/jobs/create", response_model=JobResponse, status_code=status.HTTP_201_CREATED
)
async def create_job(job: Job, db: AsyncSession = Depends(get_db_session)):

    query = """
            MATCH (j:Job {id : $id})
            SET j.title = $title,
                j.company = $company,
                j.description = $description,
                j.seniority_level = $seniority_level,
                j.employment_type = $employment_type,
                j.job_function = $job_function,
                j.industries = $industries,
                j.status = $status,
                j.url = $url
            """

    params = {
        "id": job.id,
        "title": job.title,
        "company": job.company,
        "description": job.description,
        "seniority_level": job.seniority_level,
        "employment_type": job.employment_type,
        "job_function": job.job_function,
        "industries": job.industries,
        "status": "submitted",
        "url": str(job.url),
    }

    try:
        async with await db.begin_transaction() as tx:
            await tx.run(query, **params)
            await tx.commit()
        return JobResponse(
            message="Job created successfully", job_id=job.id, status=201
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"A database error occurred: {str(e)}",
        )
