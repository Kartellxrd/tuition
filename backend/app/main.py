from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.core.config import settings

app=FastAPI(title=settings.APP_NAME,version="0.1.0")
if settings.CORS_ORIGINS:
    app.add_middleware(CORSMiddleware,allow_origins=settings.CORS_ORIGINS,allow_credentials=False,allow_methods=["GET","POST","PATCH","DELETE"],allow_headers=["Authorization","Content-Type"])
app.include_router(api_router,prefix=settings.API_V1_PREFIX)

@app.get("/")
def root():
    return {"name":settings.APP_NAME,"status":"running"}
