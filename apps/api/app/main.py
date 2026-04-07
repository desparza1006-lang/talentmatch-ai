"""Main FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import analysis, cv, matching


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    print(f"🚀 Starting {settings.project_name} v{settings.version}")
    yield
    # Shutdown
    print("👋 Shutting down application")


app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    description="AI-powered CV analysis and job matching API",
    openapi_url=f"{settings.api_v1_str}/openapi.json",
    docs_url=f"{settings.api_v1_str}/docs",
    redoc_url=f"{settings.api_v1_str}/redoc",
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(cv.router, prefix=settings.api_v1_str, tags=["CV Processing"])
app.include_router(
    matching.router, prefix=settings.api_v1_str, tags=["Matching"]
)
app.include_router(
    analysis.router, prefix=settings.api_v1_str, tags=["Analysis"]
)


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.version,
        "debug": settings.debug,
    }


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.project_name,
        "version": settings.version,
        "docs": f"{settings.api_v1_str}/docs",
    }
