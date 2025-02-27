from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
import httpx
from pydantic import BaseModel
from app.scraping.ScraperFactory import ScraperFactory


# url = "https://www.linkedin.com/jobs/view/4148231334"
DB_API_URL = "http://db-service:80"


class JobPayload(BaseModel):
    id: str
    url: str
    site: str


app = FastAPI()


@app.post("/jobs/scrape")
async def scrape_job(payload: JobPayload):
    scraper = ScraperFactory.get_scraper(payload.site)
    if not scraper:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Invalid site"}
        )
    soup = scraper.scrape(payload.url)
    job = scraper.extract_info(soup)
    job["url"] = payload.url
    job["id"] = payload.id

    async with httpx.AsyncClient() as client:
        try:
            db_response = await client.post(f"{DB_API_URL}/jobs/create", json=job)
        except httpx.ConnectError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )

    return JSONResponse(status_code=db_response.status_code, content=db_response.json())
