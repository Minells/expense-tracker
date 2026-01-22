from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth_router, categories_router, expenses_router, reports_router
from app.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="A professional REST API for tracking personal expenses with authentication, categories, and reporting features.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(categories_router)
app.include_router(expenses_router)
app.include_router(reports_router)


@app.get("/", tags=["Health Check"])
def root():
    """
    Root endpoint for health check.
    """
    return {
        "message": "Expense Tracker API is running",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", tags=["Health Check"])
def health_check():
    """
    Health check endpoint for monitoring.
    """
    return {"status": "healthy"}
