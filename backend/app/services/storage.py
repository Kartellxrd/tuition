from pathlib import Path
from uuid import uuid4
from fastapi import HTTPException, UploadFile
from supabase import create_client
from app.core.config import settings

PAYMENT_BUCKET = "payment-proofs"
ALLOWED_PAYMENT_TYPES = {"image/jpeg", "image/png", "image/webp", "application/pdf"}
MAX_PAYMENT_SIZE = 5 * 1024 * 1024

def _client():
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)

async def upload_payment_proof(file: UploadFile, student_id: str) -> str:
    if file.content_type not in ALLOWED_PAYMENT_TYPES:
        raise HTTPException(status_code=400, detail="Payment proof must be JPG, PNG, WEBP or PDF.")
    data = await file.read(MAX_PAYMENT_SIZE + 1)
    if not data or len(data) > MAX_PAYMENT_SIZE:
        raise HTTPException(status_code=400, detail="Payment proof must be between 1 byte and 5 MB.")
    ext = Path(file.filename or "").suffix.lower()
    safe_ext = ext if ext in {".jpg", ".jpeg", ".png", ".webp", ".pdf"} else ""
    path = f"{student_id}/{uuid4()}{safe_ext}"
    try:
        _client().storage.from_(PAYMENT_BUCKET).upload(path, data, {"content-type": file.content_type, "upsert": "false"})
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Could not securely store payment proof.") from exc
    return path

def signed_payment_proof_url(path: str, expires_in: int = 300) -> str:
    try:
        result = _client().storage.from_(PAYMENT_BUCKET).create_signed_url(path, expires_in)
        return result.get("signedURL") or result.get("signedUrl")
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Could not open payment proof.") from exc

COURSE_BUCKET = "course-materials"
ALLOWED_MATERIAL_TYPES = {"application/pdf", "image/jpeg", "image/png"}
MAX_MATERIAL_SIZE = 25 * 1024 * 1024

async def upload_course_material(file: UploadFile, module_id: str) -> tuple[str, str]:
    if file.content_type not in ALLOWED_MATERIAL_TYPES:
        raise HTTPException(status_code=400, detail="Material must be PDF, JPG or PNG.")
    data = await file.read(MAX_MATERIAL_SIZE + 1)
    if not data or len(data) > MAX_MATERIAL_SIZE:
        raise HTTPException(status_code=400, detail="Material must be between 1 byte and 25 MB.")
    original = Path(file.filename or "material").name
    ext = Path(original).suffix.lower()
    safe_ext = ext if ext in {".pdf", ".jpg", ".jpeg", ".png"} else ""
    path = f"{module_id}/{uuid4()}{safe_ext}"
    try:
        _client().storage.from_(COURSE_BUCKET).upload(path, data, {"content-type": file.content_type, "upsert": "false"})
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Could not securely store material.") from exc
    return path, original

def signed_course_material_url(path: str, expires_in: int = 300) -> str:
    try:
        result = _client().storage.from_(COURSE_BUCKET).create_signed_url(path, expires_in)
        return result.get("signedURL") or result.get("signedUrl")
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Could not open material.") from exc

def delete_course_material(path: str) -> None:
    try:
        _client().storage.from_(COURSE_BUCKET).remove([path])
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Could not remove material file.") from exc


PROFILE_BUCKET = "profile-images"
ALLOWED_PROFILE_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_PROFILE_SIZE = 5 * 1024 * 1024

async def upload_profile_image(file: UploadFile, user_id: str) -> str:
    if file.content_type not in ALLOWED_PROFILE_TYPES:
        raise HTTPException(status_code=400, detail="Profile image must be JPG, PNG or WEBP.")
    data = await file.read(MAX_PROFILE_SIZE + 1)
    if not data or len(data) > MAX_PROFILE_SIZE:
        raise HTTPException(status_code=400, detail="Profile image must be between 1 byte and 5 MB.")
    ext = Path(file.filename or "").suffix.lower()
    safe_ext = ext if ext in {".jpg", ".jpeg", ".png", ".webp"} else ".jpg"
    path = f"{user_id}/{uuid4()}{safe_ext}"
    try:
        _client().storage.from_(PROFILE_BUCKET).upload(path, data, {"content-type": file.content_type, "upsert": "false"})
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Could not store profile image.") from exc
    return path

def signed_profile_image_url(path: str, expires_in: int = 3600) -> str:
    try:
        result = _client().storage.from_(PROFILE_BUCKET).create_signed_url(path, expires_in)
        return result.get("signedURL") or result.get("signedUrl")
    except Exception:
        return None

def delete_profile_image(path: str) -> None:
    try:
        _client().storage.from_(PROFILE_BUCKET).remove([path])
    except Exception:
        pass
