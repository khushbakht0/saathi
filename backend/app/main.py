from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.timetable import router as timetable_router
from app.core.logger import logger
from app.database import check_database_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    if check_database_connection():
        logger.info("Database startup health check succeeded")
    else:
        logger.error("Database startup health check failed")
    yield


app = FastAPI(title="AI Student Assistant API", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)
app.include_router(timetable_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
