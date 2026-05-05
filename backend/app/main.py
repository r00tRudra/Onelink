from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
import logging

from app.core.config import settings
from app.db.database import engine, get_db
from app.db.init_db import init_db
from app.api import auth, users, projects, portfolio, resume

# Import models to create tables
import app.models.user
import app.models.project
import app.models.experience
import app.models.education
import app.models.skill
import app.models.media

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="OneLink Portfolio API",
    description="Portfolio builder using GitHub data",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup
@app.on_event("startup")
async def startup():
    """Initialize database on startup"""
    try:
        # Create all tables
        from app.models import User, Project, Experience, Education, Skill, Media
        from app.db.database import Base
        Base.metadata.create_all(bind=engine)
        
        # Enable foreign keys for SQLite
        with engine.connect() as connection:
            connection.execute(text("PRAGMA foreign_keys=ON"))
            connection.commit()
        
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error during startup: {e}")

# Include API routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(projects.router, prefix="/projects", tags=["projects"])
app.include_router(portfolio.router, prefix="/portfolio", tags=["portfolio"])
app.include_router(resume.router, prefix="/resume", tags=["resume"])

@app.get("/")
async def read_root():
    """Root endpoint"""
    return {
        "message": "OneLink Portfolio API",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "database": "sqlite"}
