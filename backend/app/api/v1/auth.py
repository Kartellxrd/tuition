from datetime import datetime, timedelta, timezone
import hashlib
import secrets
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.dependencies import get_current_user
from app.core.database import get_db
from app.core.security import create_access_token, hash_password, verify_password
from app.models.email_verification import EmailVerificationToken
from app.models.user import User, UserRole\nfrom app.models.password_reset import PasswordResetToken
from app.services.email import send_verification_code, send_password_reset_code
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserResponse, VerifyEmailRequest, ResendVerificationRequest, ForgotPasswordRequest, ResetPasswordRequest

router = APIRouter()

def serialize_user(user: User) -> UserResponse:
    return UserResponse(id=str(user.id), name=user.name, email=user.email, role=user.role.value, email_verified=user.email_verified, active=user.active)

def code_hash(code: str) -> str:
    return hashlib.sha256(code.encode()).hexdigest()

def issue_verification(user: User, db: Session) -> str:
    code = f"{secrets.randbelow(1_000_000):06d}"
    db.add(EmailVerificationToken(user_id=user.id, code_hash=code_hash(code), expires_at=datetime.now(timezone.utc) + timedelta(minutes=15)))
    return code

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    email = payload.email.lower().strip()
    if db.scalar(select(User).where(User.email == email)):
        raise HTTPException(status_code=409, detail="An account with this email already exists.")
    user = User(name=payload.name.strip(), email=email, password_hash=hash_password(payload.password), role=UserRole.STUDENT)
    db.add(user); db.flush()
    code=issue_verification(user, db)
    db.commit(); db.refresh(user)
    send_verification_code(user.email, code)
    return serialize_user(user)

@router.post("/verify-email", response_model=UserResponse)
def verify_email(payload: VerifyEmailRequest, db: Session = Depends(get_db)):
    email = payload.email.lower().strip()
    user = db.scalar(select(User).where(User.email == email))
    if not user: raise HTTPException(status_code=400, detail="Invalid verification request.")
    token = db.scalar(select(EmailVerificationToken).where(EmailVerificationToken.user_id == user.id, EmailVerificationToken.used_at.is_(None)).order_by(EmailVerificationToken.created_at.desc()))
    now = datetime.now(timezone.utc)
    if not token or token.expires_at < now or not secrets.compare_digest(token.code_hash, code_hash(payload.code)):
        raise HTTPException(status_code=400, detail="Invalid or expired verification code.")
    token.used_at = now; user.email_verified = True
    db.commit(); db.refresh(user)
    return serialize_user(user)

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    email = payload.email.lower().strip()
    user = db.scalar(select(User).where(User.email == email))
    if not user or not verify_password(payload.password, user.password_hash): raise HTTPException(status_code=401, detail="Invalid email or password.")
    if not user.active: raise HTTPException(status_code=403, detail="Account is inactive.")
    token = create_access_token(str(user.id), user.role.value)
    return TokenResponse(access_token=token, user=serialize_user(user))

@router.get("/me", response_model=UserResponse)
def me(user: User = Depends(get_current_user)):
    return serialize_user(user)

@router.post("/resend-verification")
def resend_verification(payload:ResendVerificationRequest,db:Session=Depends(get_db)):
    user=db.scalar(select(User).where(User.email==payload.email.lower().strip()))
    if not user or user.email_verified: return {"message":"If verification is required, a new code will be sent."}
    latest=db.scalar(select(EmailVerificationToken).where(EmailVerificationToken.user_id==user.id).order_by(EmailVerificationToken.created_at.desc()))
    now=datetime.now(timezone.utc)
    if latest and latest.created_at and (now-latest.created_at).total_seconds()<60: raise HTTPException(429,"Please wait before requesting another code.")
    for token in db.scalars(select(EmailVerificationToken).where(EmailVerificationToken.user_id==user.id,EmailVerificationToken.used_at.is_(None))): token.used_at=now
    code=issue_verification(user,db);db.commit();send_verification_code(user.email,code)
    return {"message":"If verification is required, a new code will be sent."}

@router.post("/forgot-password")
def forgot_password(payload:ForgotPasswordRequest,db:Session=Depends(get_db)):
    user=db.scalar(select(User).where(User.email==payload.email.lower().strip()))
    if user and user.active:
        now=datetime.now(timezone.utc)
        for token in db.scalars(select(PasswordResetToken).where(PasswordResetToken.user_id==user.id,PasswordResetToken.used_at.is_(None))): token.used_at=now
        code=f"{secrets.randbelow(1_000_000):06d}"
        db.add(PasswordResetToken(user_id=user.id,token_hash=code_hash(code),expires_at=now+timedelta(minutes=15)));db.commit();send_password_reset_code(user.email,code)
    return {"message":"If the account exists, password reset instructions will be sent."}

@router.post("/reset-password")
def reset_password(payload:ResetPasswordRequest,db:Session=Depends(get_db)):
    user=db.scalar(select(User).where(User.email==payload.email.lower().strip()))
    if not user: raise HTTPException(400,"Invalid or expired reset code.")
    token=db.scalar(select(PasswordResetToken).where(PasswordResetToken.user_id==user.id,PasswordResetToken.used_at.is_(None)).order_by(PasswordResetToken.created_at.desc()))
    now=datetime.now(timezone.utc)
    if not token or token.expires_at<now or not secrets.compare_digest(token.token_hash,code_hash(payload.code)): raise HTTPException(400,"Invalid or expired reset code.")
    user.password_hash=hash_password(payload.new_password);token.used_at=now;db.commit()
    return {"message":"Password updated successfully."}
