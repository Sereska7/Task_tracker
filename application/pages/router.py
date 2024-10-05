from typing import Optional

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse

from application.api.view_auth import register_user
from application.core.models import User
from application.utils.dependencies import get_current_user

router = APIRouter(tags=["Pages"], prefix="/pages")

templates = Jinja2Templates(directory="template")


@router.get("/base", response_class=HTMLResponse)
async def base_page(request: Request, current_user: Optional[User] = Depends(get_current_user)):
    # Если пользователь не авторизован, current_user будет None
    return templates.TemplateResponse("base.html", {"request": request, "user": current_user})


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.get("/verify", response_class=HTMLResponse)
async def verify_page(request: Request):
    return templates.TemplateResponse("verify.html", {"request": request})


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/logout", response_class=HTMLResponse)
async def logout_page(request: Request):
    return templates.TemplateResponse("logout.html", {"request": request})
