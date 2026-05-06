from fastapi import FastAPI, HTTPException

from article_assurance.api import AssuranceService

app = FastAPI(
    title="Article Assurance Engine",
    version="1.0.0"
)

service = AssuranceService()


@app.post("/assess")
async def assess(payload: dict):

    try:
        result = service.assess(payload)
        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )