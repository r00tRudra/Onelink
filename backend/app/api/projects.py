from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from app.db.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.project import Project
from app.schemas.project import 
(
    ProjectResponse, ProjectUpdate, ProjectPublicResponse, 
    ProjectSyncRequest, ProjectListResponse
)
from app.services.github_service import github_service

router = APIRouter()


async def sync_user_projects(user: User, db: Session):
    """Sync projects from GitHub for a user"""
    if not user.access_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No GitHub access token available",
        )
    
    # Fetch repositories from GitHub
    repos = await github_service.get_user_repos(
        user.access_token, 
        user.github_username
    )
    
    synced_projects = []
    
    for repo in repos:
        # Check if project already exists
        existing_project = db.query(Project).filter(
            Project.github_id == repo["id"],
            Project.user_id == user.id
        ).first()
        
        # Fetch languages
        languages = await github_service.get_repo_languages(
            user.access_token,
            repo["owner"]["login"],
            repo["name"]
        )
        
        # Fetch README
        readme = await github_service.get_readme_content(
            user.access_token,
            repo["owner"]["login"],
            repo["name"]
        )
        
        # Detect demo URL
        deployed_url = github_service.detect_demo_url(
            repo.get("homepage"),
            readme
        )
        
        # Classify project
        status_type = github_service.classify_project(
            deployed_url,
            bool(repo.get("homepage")),
            repo.get("description")
        )
        
        if existing_project:
            # Update existing project
            existing_project.name = repo["name"]
            existing_project.description = repo.get("description")
            existing_project.url = repo["html_url"]
            existing_project.homepage = repo.get("homepage")
            existing_project.readme_content = readme
            existing_project.languages = languages
            existing_project.stars = repo.get("stargazers_count", 0)
            existing_project.forks = repo.get("forks_count", 0)
            existing_project.watchers = repo.get("watchers_count", 0)
            existing_project.is_deployed = deployed_url is not None
            existing_project.deployed_url = deployed_url
            existing_project.status = status_type
            existing_project.is_archived = repo.get("archived", False)
            existing_project.is_fork = repo.get("fork", False)
            existing_project.github_updated_at = datetime.utcnow()
            existing_project.updated_at = datetime.utcnow()
            db.commit()
            synced_projects.append(existing_project)
        else:
            # Create new project
            new_project = Project(
                user_id=user.id,
                github_id=repo["id"],
                name=repo["name"],
                description=repo.get("description"),
                url=repo["html_url"],
                homepage=repo.get("homepage"),
                readme_content=readme,
                languages=languages,
                stars=repo.get("stargazers_count", 0),
                forks=repo.get("forks_count", 0),
                watchers=repo.get("watchers_count", 0),
                is_deployed=deployed_url is not None,
                deployed_url=deployed_url,
                status=status_type,
                is_archived=repo.get("archived", False),
                is_fork=repo.get("fork", False),
                github_updated_at=datetime.utcnow(),
            )
            db.add(new_project)
            db.commit()
            db.refresh(new_project)
            synced_projects.append(new_project)
    
    # Update last sync time
    user.last_sync = datetime.utcnow()
    db.commit()
    
    return synced_projects


@router.post("/sync")
async def sync_projects(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Manually sync projects from GitHub"""
    synced = await sync_user_projects(current_user, db)
    return {
        "message": f"Synced {len(synced)} projects",
        "synced_count": len(synced)
    }


@router.get("", response_model=ProjectListResponse)
async def get_user_projects(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status_filter: Optional[str] = Query(None),
):
    """Get user's projects"""
    query = db.query(Project).filter(Project.user_id == current_user.id)
    
    if status_filter:
        query = query.filter(Project.status == status_filter)
    
    total = query.count()
    projects = query.offset(skip).limit(limit).all()
    
    return {
        "items": projects,
        "total": total,
        "page": skip // limit,
        "page_size": limit,
    }


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a specific project"""
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    return project


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update project (e.g., visibility)"""
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    if project_update.is_visible is not None:
        project.is_visible = project_update.is_visible
    
    project.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(project)
    return project


@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete project"""
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    db.delete(project)
    db.commit()
    return {"message": "Project deleted"}
