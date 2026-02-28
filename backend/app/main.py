import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import health, metrics, query, review, upload


app = FastAPI(
    title="Veredicta AI",
    version="0.1.0",
    description="Enterprise Generative AI Platform for Legal Document Intelligence",
)

frontend_origins = os.getenv(
    "FRONTEND_ORIGINS",
    (
        "http://localhost:5173,"
        "http://127.0.0.1:5173,"
        "http://localhost:5174,"
        "http://127.0.0.1:5174,"
        "http://localhost:4173,"
        "http://127.0.0.1:4173"
    ),
)
allow_origins = [origin.strip() for origin in frontend_origins.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(metrics.router)
app.include_router(upload.router)
app.include_router(query.router)
app.include_router(review.router)
