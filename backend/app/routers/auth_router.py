from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.services.auth import (
    create_access_token,
    decode_access_token,
    get_password_hash,
    verify_password
)
from app.services.user_store import UserStore

router = APIRouter(prefix="/api/auth", tags=["Authentication"])
security = HTTPBearer()


# Pydantic models
class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    created_at: str


# Dependency to get current user from token
async def get_current_user(authorization: Optional[str] = Header(None)) -> dict:
    """Get current user from JWT token"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        # Extract token from "Bearer <token>"
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")

        payload = decode_access_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        user = UserStore.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header")


@router.post("/register", response_model=Token)
async def register(user_data: UserRegister):
    """
    Register a new user

    - **email**: User's email address
    - **username**: Unique username
    - **password**: Password (minimum 6 characters recommended)
    """
    # Check if user already exists
    if UserStore.get_user_by_email(user_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    if UserStore.get_user_by_username(user_data.username):
        raise HTTPException(status_code=400, detail="Username already taken")

    # Validate password
    if len(user_data.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

    # Create user
    hashed_password = get_password_hash(user_data.password)
    user = UserStore.create_user(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password
    )

    # Create access token
    access_token = create_access_token(data={"sub": user["id"]})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/login", response_model=Token)
async def login(user_data: UserLogin):
    """
    Login with email and password

    Returns a JWT access token that expires in 7 days
    """
    # Get user by email
    user = UserStore.get_user_by_email(user_data.email)

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    # Verify password
    if not verify_password(user_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    # Create access token
    access_token = create_access_token(data={"sub": user["id"]})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    Get current user information

    Requires: Bearer token in Authorization header
    """
    return {
        "id": current_user["id"],
        "email": current_user["email"],
        "username": current_user["username"],
        "created_at": current_user["created_at"]
    }


@router.post("/logout")
async def logout():
    """
    Logout (client should delete the token)

    Note: JWT tokens are stateless, so logout is handled client-side
    """
    return {"message": "Logged out successfully"}
