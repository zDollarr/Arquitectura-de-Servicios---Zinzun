from fastapi import APIRouter, Request
from app.models.auth_model import LoginRequest
from app.services.auth_service import login_service
from app.core.rate_limit import limiter


router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login")
@limiter.limit("5/minute")
def login(request: Request, datos: LoginRequest):
    return login_service(datos)