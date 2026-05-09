import uuid
import secrets
from fastapi import APIRouter, HTTPException, status, Depends, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import timedelta

from app.db.database import get_db
from app.core.config import settings
from app.core.security import create_access_token
from app.services.github_service import github_service
from app.models.user import User
from app.schemas.user import TokenResponse, OAuthCallbackRequest

router = APIRouter()

# Store OAuth states temporarily (in production, use Redis)  
oauth_states = {}



@router.get("/login")
async def github_login():
    """Initiate GitHub OAuth login"""
    state = secrets.token_urlsafe(32)
    oauth_states[state] = True  # Store state validation
    
    oauth_url = await github_service.get_oauth_url(state)
    return RedirectResponse(url=oauth_url)


@router.get("/callback")
async def github_callback(
    code: str = Query(...),
    state: str = Query(...),
    db: Session = Depends(get_db),
):
    """Handle GitHub OAuth callback"""
    
    # Validate state  
    if state not in oauth_states:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid state parameter",
        )
    
    del oauth_states[state]
    
    # Exchange code for access token  
    token_response = await github_service.exchange_code_for_token(code)
    if not token_response or "access_token" not in token_response:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to obtain access token",
        )
    
    access_token = token_response.get("access_token")
    
    # Fetch user profile from GitHub  
    user_profile = await github_service.get_user_profile(access_token)
    if not user_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to fetch user profile",
        )
    
    github_id = user_profile.get("id")
    github_username = user_profile.get("login")
    
    # Check if user exists
    existing_user = db.query(User).filter(User.github_id == github_id).first()
    
    if existing_user:
        # Update existing user  
        existing_user.access_token = access_token
        existing_user.avatar_url = user_profile.get("avatar_url")
        existing_user.profile_url = user_profile.get("html_url")
        existing_user.bio = user_profile.get("bio")
        existing_user.location = user_profile.get("location")
        existing_user.email = user_profile.get("email")
        db.commit()
        user = existing_user
    else:
        # Create new user
        # Generate unique portfolio username
        portfolio_username = github_username
        counter = 1
        while db.query(User).filter(User.portfolio_username == portfolio_username).first():
            portfolio_username = f"{github_username}{counter}"
            counter += 1
        
        user = User(
            github_id=github_id,
            github_username=github_username,
            portfolio_username=portfolio_username,
            access_token=access_token,
            avatar_url=user_profile.get("avatar_url"),
            profile_url=user_profile.get("html_url"),
            bio=user_profile.get("bio"),
            location=user_profile.get("location"),
            email=user_profile.get("email"),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # Create JWT token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    jwt_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )
    
    # Redirect to frontend callback page with token in URL
    callback_url = settings.FRONTEND_CALLBACK_URL
    separator = "&" if "?" in callback_url else "?"
    redirect_url = (
        f"{callback_url}{separator}token={jwt_token}"
        f"&user_id={user.id}&username={user.portfolio_username}"
    )
    return RedirectResponse(url=redirect_url)


@router.post("/logout")
async def logout():
    """Logout endpoint (clear client-side token)"""
    return {"message": "Logged out successfully"}
