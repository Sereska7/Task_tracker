from typing import Optional

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse, RedirectResponse

from application.core.models import User
from application.utils.dependencies import get_current_user

# Роутер для страниц авторизации и базовых страниц интерфейса
router = APIRouter(tags=["Pages"], prefix="/pages")

# Шаблоны для обычных страниц
templates = Jinja2Templates(directory="template")


# Страница базы, доступная только авторизованным пользователям
@router.get("/base", response_class=HTMLResponse)
async def base_page(
    request: Request,
    current_user: Optional[User] = Depends(get_current_user)  # Зависимость для получения текущего пользователя
):
    """
    Страница базы для отображения интерфейса.
    Если пользователь не авторизован, он перенаправляется на страницу логина.
    В зависимости от прав пользователя (директор или нет) загружается соответствующий шаблон.
    """
    if current_user is None:
        # Если пользователь не авторизован, перенаправляем на страницу входа
        return RedirectResponse(url="/pages/login", status_code=303)

    # Если пользователь — директор, используется админский шаблон, иначе обычный
    template = "admin/base_admin.html" if current_user.is_director else "base.html"

    # Возвращаем шаблон с данными пользователя
    return templates.TemplateResponse(
        template, {"request": request, "user": current_user}
    )


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
