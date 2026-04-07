from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.competitions import router as competitions_router
from app.api.routes.health import router as health_router
from app.api.routes.matches import router as matches_router
from app.api.routes.predictions import router as predictions_router
from app.config.logging_config import setup_logging
from app.config.settings import settings
from app.db.models import create_tables

setup_logging()
create_tables()

app = FastAPI(
    title=f"{settings.APP_NAME} API",
    debug=settings.APP_DEBUG
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(competitions_router)
app.include_router(matches_router)
app.include_router(predictions_router)


@app.get("/")
def root():
    return {"message": f"{settings.APP_NAME} API is running"}