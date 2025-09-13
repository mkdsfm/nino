from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.api.endpoints import users, results
from app.config import settings
from app.init_db import init_db

# Initialize database
init_db()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  # In production, this should be restricted to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(results.router, prefix=f"{settings.API_V1_STR}/results", tags=["results"])


@app.get("/")
def root():
    """
    Root endpoint - redirects to API documentation
    """
    return {"message": "Welcome to Medical Personal Account API. Go to /docs for API documentation."}


@app.get("/health")
def health_check():
    """
    Health check endpoint
    """
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
