from typing import Annotated, List

from fastapi import APIRouter, Depends, Request, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from application.core.models import User
from application.core.models.db_helper import db_helper
from application.core.schemas.project import SProject, SProjectCreateForm
from application.crud.projects import (
    add_project,
    get_project,
    update_project,
    get_all_projects,
    del_project,
)
from application.pages.router_base import templates
from application.pages.router_admin import templates_admin as templates_admit
from application.utils.dependencies import get_current_user

# Маршрутизатор для управления проектами
router = APIRouter(tags=["Project"], prefix="/project")


# Роутер для создания проекта
@router.post("/create")
async def create_project(
    request: Request,  # Объект запроса
    data_project: Annotated[
        SProjectCreateForm, Depends(SProjectCreateForm.as_form)
    ],  # Форма для создания проекта
    session: Annotated[
        AsyncSession, Depends(db_helper.session_getter)
    ],  # Сессия базы данных
    current_user: User = Depends(
        get_current_user
    ),  # Текущий авторизованный пользователь
):
    """
    Создание нового проекта:
    - Если пользователь имеет права директора, создается новый проект и возвращается список проектов с сообщением об успехе.
    - Если нет прав, возвращается сообщение об отсутствии доступа.
    """
    try:
        if current_user.is_director:
            # Добавление нового проекта
            project = await add_project(data_project, session)

            # Получение всех проектов после добавления нового
            projects = await get_all_projects(session)

            # Возврат ответа с обновленным списком проектов и сообщением об успехе
            return templates_admit.TemplateResponse(
                "project_admin.html",
                {
                    "request": request,
                    "projects": projects,
                    "message": "Проект успешно создан.",
                },
            )
        else:
            raise HTTPException(
                status_code=403, detail="У пользователя нет прав доступа"
            )

    except Exception as e:
        # Общая обработка исключений
        raise HTTPException(
            status_code=500, detail=f"Ошибка при создании проекта: {str(e)}"
        )


# Роутер для обновления проекта
@router.patch("/update_{name}")
async def change_project(
    product_id: int,  # Идентификатор проекта для обновления
    date_update: SProject,  # Данные для обновления проекта
    session: Annotated[
        AsyncSession, Depends(db_helper.session_getter)
    ],  # Сессия базы данных
    current_user: User = Depends(
        get_current_user
    ),  # Текущий авторизованный пользователь
) -> SProject | dict:
    """
    Обновление существующего проекта:
    - Если пользователь имеет права директора, проект обновляется.
    - Если проект не найден или нет прав доступа, возвращается сообщение.
    """
    try:
        if current_user.is_director:
            # Поиск проекта по ID
            project = await get_project(session, id=product_id)
            if not project:
                raise HTTPException(
                    status_code=404, detail="Такого проекта не существует"
                )

            # Обновление проекта
            up_project = await update_project(project.name, session, date_update)
            return up_project

        else:
            raise HTTPException(
                status_code=403, detail="У пользователя нет прав доступа"
            )

    except Exception as e:
        # Общая обработка исключений
        raise HTTPException(
            status_code=500, detail=f"Ошибка при обновлении проекта: {str(e)}"
        )


# Роутер для получения всех проектов
@router.get("/get")
async def get_projects(
    request: Request,  # Объект запроса
    session: Annotated[
        AsyncSession, Depends(db_helper.session_getter)
    ],  # Сессия базы данных
    current_user: User = Depends(
        get_current_user
    ),  # Текущий авторизованный пользователь
) -> List[SProject] | dict:
    """
    Получение списка всех проектов:
    - Если пользователь является директором, возвращается административный шаблон.
    - Для обычных пользователей возвращается стандартный шаблон.
    """
    try:
        projects = await get_all_projects(session)

        if current_user.is_director:
            return templates_admit.TemplateResponse(
                "project_admin.html", {"request": request, "projects": projects}
            )
        else:
            return templates.TemplateResponse(
                "project.html", {"request": request, "projects": projects}
            )

    except Exception as e:
        # Общая обработка исключений
        raise HTTPException(
            status_code=500, detail=f"Ошибка при получении проектов: {str(e)}"
        )


# Роутер для удаления проекта
@router.post("/delete")
async def delete_project(
    request: Request,  # Объект запроса
    session: Annotated[
        AsyncSession, Depends(db_helper.session_getter)
    ],  # Сессия базы данных
    current_user: User = Depends(
        get_current_user
    ),  # Текущий авторизованный пользователь
    project_id: int = Form(...),  # Идентификатор проекта для удаления
) -> dict:
    """
    Удаление проекта:
    - Если пользователь имеет права директора, проект удаляется и возвращается список проектов с сообщением об удалении.
    - Если нет прав, возвращается сообщение об отсутствии доступа.
    """
    try:
        if current_user.is_director:
            # Удаление проекта
            project = await del_project(project_id, session)

            # Получение обновленного списка проектов после удаления
            projects = await get_all_projects(session)

            # Возврат ответа с обновленным списком проектов и сообщением об успехе
            return templates_admit.TemplateResponse(
                "project_admin.html",
                {
                    "request": request,
                    "projects": projects,
                    "message": "Проект успешно удален",
                },
            )
        else:
            raise HTTPException(
                status_code=403, detail="У пользователя нет прав доступа"
            )

    except Exception as e:
        # Общая обработка исключений
        raise HTTPException(
            status_code=500, detail=f"Ошибка при удалении проекта: {str(e)}"
        )
