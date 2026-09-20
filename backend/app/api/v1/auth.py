from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User, UserRole
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserResponse

router = APIRouter()

def serialize_user(user: User) -> UserResponse:
    return UserResponse(id=str(user.id), name=user.name, email=user.email, role=user.role.value, email_verified=user.email_verified, active=user.active)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    email = payload.email.lower().strip()
    if db.scalar(select(User).where(User.email == email)):
        raise HTTPException(status_code=409, detail="An account with this email already exists.")
    user = User(name=payload.name.strip(), email=email, password_hash=hash_password(payload.password), role=UserRole.STUDENT)
    db.add(user)
    db.commit()
    db.refresh(user)
    return serialize_user(user)

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    email = payload.email.lower().strip()
    user = db.scalar(select(User).where(User.email == email))
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    if not user.active:
        raise HTTPException(status_code=403, detail="Account is inactive.")
    token = create_access_token(str(user.id), user.role.value)
    return TokenResponse(access_token=token, user=serialize_user(user))
