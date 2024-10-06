from typing import Optional

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse, RedirectResponse

from application.core.models import User
from application.pages.router_admin import templates_admin
from application.utils.dependencies import get_current_user

# Роутер для страниц авторизации и базовых страниц интерфейса
router = APIRouter(tags=["Pages"], prefix="/pages")

# Шаблоны для обычных страниц
templates = Jinja2Templates(directory="application/template")


# Страница базы, доступная только авторизованным пользователям
@router.get("/base", response_class=HTMLResponse)
async def base_page(
    request: Request,
    current_user: Optional[User] = Depends(
        get_current_user
    ),  # Зависимость для получения текущего пользователя
):
    """
    Страница базы для отображения интерфейса.
    Страница отображается даже для неавторизованных пользователей.
    В зависимости от прав пользователя (директор или нет) загружается соответствующий шаблон.
    """
    # Если пользователь авторизован и является директором, используется админский шаблон
    if current_user and current_user.is_director:
        return templates_admin.TemplateResponse("base_admin.html", {"request": request})
    else:
        # Используем общий шаблон для неавторизованных или обычных пользователей
        return templates.TemplateResponse("base.html", {"request": request})


# Страница регистрации нового пользователя
@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """
    Отображение страницы регистрации.
    """
    return templates.TemplateResponse("register.html", {"request": request})


# Страница подтверждения регистрации
@router.get("/verify", response_class=HTMLResponse)
async def verify_page(request: Request):
    """
    Отображение страницы подтверждения (верификации) пользователя.
    """
    return templates.TemplateResponse("verify.html", {"request": request})


# Страница входа в систему
@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """
    Отображение страницы входа.
    """
    return templates.TemplateResponse("login.html", {"request": request})


# Страница выхода из системы
@router.get("/logout", response_class=HTMLResponse)
async def logout_page(request: Request):
    """
    Страница выхода из системы.
    """
    return templates.TemplateResponse("logout.html", {"request": request})
