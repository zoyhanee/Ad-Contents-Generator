from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.config import settings
from app.crud.user import (
    create_oauth_user,
    create_user,
    get_user_by_email,
    get_user_by_provider,
    link_oauth_provider,
)
from app.db.database import get_db
from app.schemas.user import OAuthLoginUrlResponse, UserCreate, UserResponse
from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token
from app.schemas.user import TokenResponse, UserLogin
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def signup(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = get_user_by_email(db, user.email)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists.",
        )

    password_hash = hash_password(user.password)

    created_user = create_user(
        db=db,
        user=user,
        password_hash=password_hash,
    )

    return created_user


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    user: UserLogin,
    db: Session = Depends(get_db),
):
    db_user = get_user_by_email(db, user.email)

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    if not db_user.password_hash or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    access_token = create_access_token(db_user.id)

    return TokenResponse(
        access_token=access_token,
        user=db_user,
    )


@router.get(
    "/google/login-url",
    response_model=OAuthLoginUrlResponse,
)
def get_google_login_url():
    if not settings.GOOGLE_CLIENT_ID:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Google OAuth client ID is not configured.",
        )

    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "select_account",
    }

    return OAuthLoginUrlResponse(
        login_url=(
            "https://accounts.google.com/o/oauth2/v2/auth?"
            + urlencode(params)
        )
    )


@router.get(
    "/google/callback",
)
def google_callback(
    code: str = Query(...),
    db: Session = Depends(get_db),
):
    if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Google OAuth credentials are not configured.",
        )

    token_data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    try:
        with httpx.Client(timeout=15) as client:
            token_response = client.post(
                "https://oauth2.googleapis.com/token",
                data=token_data,
            )
            token_response.raise_for_status()
            google_token = token_response.json()

            user_response = client.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={
                    "Authorization": f"Bearer {google_token['access_token']}",
                },
            )
            user_response.raise_for_status()
            google_user = user_response.json()

    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to authenticate with Google.",
        ) from exc

    google_user_id = google_user.get("id")
    email = google_user.get("email")

    if not google_user_id or not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google account information is incomplete.",
        )

    db_user = get_user_by_provider(
        db=db,
        provider="google",
        provider_user_id=google_user_id,
    )

    if db_user is None:
        db_user = get_user_by_email(db, email)

        if db_user is None:
            db_user = create_oauth_user(
                db=db,
                email=email,
                provider="google",
                provider_user_id=google_user_id,
                store_name=google_user.get("name"),
            )

        elif db_user.provider_user_id is None:
            db_user = link_oauth_provider(
                db=db,
                user=db_user,
                provider_user_id=google_user_id,
            )

    access_token = create_access_token(db_user.id)

    redirect_params = urlencode(
        {
            "page": "oauth_callback",
            "access_token": access_token,
        }
    )

    return RedirectResponse(
        url=f"{settings.FRONTEND_BASE_URL}/?{redirect_params}",
        status_code=status.HTTP_302_FOUND,
    )
    
@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user
