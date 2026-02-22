from fastapi import FastAPI

from app.routers import health, metrics, query, review, upload


app = FastAPI(
    title="Veredicta AI",
    version="0.1.0",
    description="Enterprise Generative AI Platform for Legal Document Intelligence",
)

app.include_router(health.router)
app.include_router(metrics.router)
app.include_router(upload.router)
app.include_router(query.router)
app.include_router(review.router)
