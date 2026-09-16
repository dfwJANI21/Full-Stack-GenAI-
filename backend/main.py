import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from routers import story, job
from db.database import create_tables

create_tables()  # Create tables if they don't exist

app = FastAPI(
    title="my API",
    description="to gen story",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Robust CORS configuration for local development and Vercel deployments
configured_origins = [o.strip() for o in settings.ALLOWED_ORIGINS if o.strip()]

# If wildcard is requested or no origins are set, allow all HTTP/HTTPS origins safely
if "*" in configured_origins or not configured_origins:
    cors_origins = []
    cors_regex = r"^https?://.*"
else:
    cors_origins = configured_origins
    # Automatically permit any Vercel domain in addition to explicitly configured origins
    cors_regex = r"^https://.*\.vercel\.app$"

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_origin_regex=cors_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Interactive Story API is running"}

app.include_router(story.router, prefix=settings.API_PREFIX)
app.include_router(job.router, prefix=settings.API_PREFIX)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
