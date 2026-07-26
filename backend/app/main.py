from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.timetable import router as timetable_router
from app.core.database import check_database_connection
from app.core.health import get_health_payload
from app.core.logger import logger


@asynccontextmanager
async def lifespan(_: FastAPI):
    if check_database_connection():
        logger.info("Database connectivity check successful at startup.")
    else:
        logger.warning("Database connectivity check failed at startup.")
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
async def health_check() -> dict[str, str]:
    return await get_health_payload()
