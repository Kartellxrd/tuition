import json
from urllib import request,error
from app.core.config import settings

class EmailDeliveryError(RuntimeError): pass

def _send(to:str,subject:str,html:str)->None:
    if not settings.EMAIL_ENABLED: return
    if not settings.RESEND_API_KEY or not settings.EMAIL_FROM:
        raise EmailDeliveryError("Email delivery is enabled but not configured.")
    payload=json.dumps({"from":settings.EMAIL_FROM,"to":[to],"subject":subject,"html":html}).encode()
    req=request.Request("https://api.resend.com/emails",data=payload,method="POST",headers={"Authorization":f"Bearer {settings.RESEND_API_KEY}","Content-Type":"application/json"})
    try:
        with request.urlopen(req,timeout=10) as response:
            if response.status>=300: raise EmailDeliveryError("Email provider rejected the message.")
    except (error.URLError,error.HTTPError,TimeoutError) as exc:
        raise EmailDeliveryError("Email could not be delivered.") from exc

def send_verification_code(to:str,code:str)->None:
    _send(to,"Verify your CODE READY TUTORS account",f"<h2>Verify your email</h2><p>Your verification code is <strong>{code}</strong>.</p><p>It expires in 15 minutes.</p>")

def send_password_reset_code(to:str,code:str)->None:
    _send(to,"Reset your CODE READY TUTORS password",f"<h2>Password reset</h2><p>Your reset code is <strong>{code}</strong>.</p><p>It expires in 15 minutes. If you did not request this, ignore this email.</p>")
