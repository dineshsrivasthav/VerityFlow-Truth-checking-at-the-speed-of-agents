# from fastapi import FastAPI, HTTPException

# from article_assurance.api import AssuranceService

# app = FastAPI(
#     title="Article Assurance Engine",
#     version="1.0.0"
# )

# service = AssuranceService()


# @app.post("/assess")
# async def assess(payload: dict):

#     try:
#         result = service.assess(payload)
#         return result

#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=str(e)
#         )


from fastapi import FastAPI, HTTPException
from article_assurance.api import AssuranceService
import asyncio
import concurrent.futures

app = FastAPI()
service = AssuranceService()

# Create a thread pool executor
executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)

@app.post("/assess")
async def assess(payload: dict):
    try:
        # Run the synchronous assess method in a thread
        result = await asyncio.get_event_loop().run_in_executor(
            executor, 
            service.assess, 
            payload
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Optional: Clean up executor on shutdown
@app.on_event("shutdown")
async def shutdown_event():
    executor.shutdown(wait=True)