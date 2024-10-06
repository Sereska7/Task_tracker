from typing import Annotated, List, Dict

from fastapi import APIRouter, Depends, Request, HTTPException, Form
from sqlalchemy.ext.asyncio import AsyncSession

from application.background_tasks.send_message import (
    send_email_add_new_task_for_you,
    send_email_change_task_for_you,
    send_email_accept_task,
)
from application.core.models import User
from application.core.models.db_helper import db_helper
from application.core.models.task import TypeTask, TaskStatus
from application.core.schemas.task import (
    STask,
    SChangeTask,
    SBaseTask,
    SMyTask,
    STaskCreateForm,
)
from application.crud.projects import get_all_projects
from application.crud.tasks import (
    add_task,
    get_all_tasks,
    get_task,
    change_status_task,
    update_task,
    get_my_tasks,
    get_task_by_id,
    remove_task,
    get_tasks_by_project,
)
from application.crud.users import get_users
from application.pages.router_base import templates
from application.pages.router_admin import templates_admin as templates_admin
from application.utils.dependencies import get_current_user
from application.utils.detected_change_task import detect_changes

# Маршрутизатор для управления задачами
router = APIRouter(tags=["Task"], prefix="/task")


# Роутер для создания задачи
@router.post("/create")
async def create_task(
    request: Request,  # Объект запроса
    task_data: Annotated[
        STaskCreateForm, Depends(STaskCreateForm.as_form)
    ],  # Форма создания задачи
    session: Annotated[
        AsyncSession, Depends(db_helper.session_getter)
    ],  # Сессия базы данных
    current_user: User = Depends(
        get_current_user
    ),  # Текущий авторизованный пользователь
):
    """
    Создание новой задачи:
    - Проверяет, является ли пользователь директором, и добавляет задачу.
    - Возвращает страницу с новой задачей или сообщение об отсутствии прав.
    """
    if current_user.is_director:
        # Создание новой задачи
        new_task = await add_task(task_data, session)
        task = await get_task_by_id(new_task.id, session)

        # Получение списков проектов и пользователей для формы
        projects = await get_all_projects(session)
        users = await get_users(session)

        # Отправка email о новой задаче
        send_email_add_new_task_for_you(task.contractor_email, task)

        # Возвращаем шаблон с созданной задачей
        return templates_admin.TemplateResponse(
            "new_task.html", {"request": request, "task": task}
        )
    else:
        projects = await get_all_projects(session)
        users = await get_users(session)
        return templates_admin.TemplateResponse(
            "create_task_admin.html",
            {
                "request": request,
                "message": "У вас нет прав для создания задач",
                "projects": projects,
                "users": users,
            },
        )


# Роутер для получения всех задач
@router.get("/get_all")
async def get_tasks(
    request: Request,  # Объект запроса
    session: Annotated[
        AsyncSession, Depends(db_helper.session_getter)
    ],  # Сессия базы данных
    current_user: User = Depends(
        get_current_user
    ),  # Текущий авторизованный пользователь
) -> List[SBaseTask]:
    """
    Получение всех задач:
    - Если пользователь является директором, возвращает админскую версию страницы задач.
    """
    tasks = await get_all_tasks(session)
    if current_user.is_director:
        return templates_admin.TemplateResponse(
            "task_admin.html", {"request": request, "tasks": tasks}
        )


# Роутер для получения задач текущего пользователя
@router.get("/my_tasks")
async def view_my_tasks(
    request: Request,  # Объект запроса
    session: Annotated[
        AsyncSession, Depends(db_helper.session_getter)
    ],  # Сессия базы данных
    current_user: User = Depends(
        get_current_user
    ),  # Текущий авторизованный пользователь
) -> List[SMyTask]:
    """
    Просмотр задач текущего пользователя:
    - Возвращает страницу с задачами, назначенными текущему пользователю.
    """
    user_id = current_user.id
    tasks = await get_my_tasks(user_id, session)
    return templates.TemplateResponse(
        "my_tasks.html", {"request": request, "tasks": tasks}
    )


# Роутер для просмотра задачи по ID
@router.get("/get_task")
async def view_task(
    task_id: int,  # Идентификатор задачи
    request: Request,  # Объект запроса
    session: Annotated[
        AsyncSession, Depends(db_helper.session_getter)
    ],  # Сессия базы данных
    current_user: User = Depends(
        get_current_user
    ),  # Текущий авторизованный пользователь
) -> SMyTask:
    """
    Просмотр конкретной задачи по ID:
    - Возвращает страницу с деталями задачи.
    """
    task = await get_task_by_id(task_id, session)
    return templates.TemplateResponse(
        "task_details.html", {"request": request, "task": task}
    )


# Роутер для просмотра задач по проекту
@router.get("/by_project")
async def view_task_by_project(
    project_id: int,  # Идентификатор проекта
    request: Request,  # Объект запроса
    session: Annotated[
        AsyncSession, Depends(db_helper.session_getter)
    ],  # Сессия базы данных
    current_user: User = Depends(
        get_current_user
    ),  # Текущий авторизованный пользователь
) -> List[SBaseTask]:
    """
    Просмотр задач по проекту:
    - Возвращает задачи, связанные с выбранным проектом.
    """
    tasks = await get_tasks_by_project(project_id, session)
    return templates.TemplateResponse(
        "task_by_project.html", {"request": request, "tasks": tasks}
    )


# Роутер для принятия задачи в работу
@router.post("/accepted_for_work")
async def accepted_task(
    request: Request,  # Объект запроса
    session: Annotated[
        AsyncSession, Depends(db_helper.session_getter)
    ],  # Сессия базы данных
    current_user: User = Depends(
        get_current_user
    ),  # Текущий авторизованный пользователь
):
    """
    Принятие задачи в работу:
    - Если текущий пользователь является исполнителем задачи, статус изменяется на 'В работе'.
    - Возвращает обновленный список задач пользователя.
    """
    form_data = await request.form()
    task_id = int(form_data.get("task_id"))  # Получение ID задачи из формы

    task = await get_task(session, id=task_id)
    if task.contractor == current_user.id:
        up_task = await change_status_task(
            task_id, current_user.id, session, status=TaskStatus.IN_PROGRESS
        )
        task = await get_task_by_id(up_task.id, session)
        send_email_accept_task(task.contractor_email, task)
        tasks = await get_my_tasks(current_user.id, session)
        return templates.TemplateResponse(
            "my_tasks.html", {"request": request, "tasks": tasks}
        )
    return {"message": "Вы не являетесь исполнителем этой задачи"}


# Роутер для изменения задачи
@router.patch("/change")
async def change_task(
    task_id: int,  # Идентификатор задачи
    data_task: SChangeTask,  # Данные для изменения задачи
    session: Annotated[
        AsyncSession, Depends(db_helper.session_getter)
    ],  # Сессия базы данных
    current_user: User = Depends(
        get_current_user
    ),  # Текущий авторизованный пользователь
) -> SBaseTask | dict:
    """
    Изменение существующей задачи:
    - Если пользователь является директором, задача обновляется.
    - Если поля изменены, отправляется email уведомление исполнителю.
    """
    if current_user.is_director:
        current_task = await get_task_by_id(task_id, session)
        changed_fields = detect_changes(current_task, data_task)
        up_task = await update_task(task_id, data_task, session)
        if changed_fields:
            send_email_change_task_for_you(
                current_task.contractor_email, changed_fields
            )
        return up_task
    else:
        return {"message": "У пользователя нет прав доступа"}


# Роутер для удаления задачи
@router.post("/delete")
async def del_task(
    request: Request,  # Объект запроса
    session: Annotated[
        AsyncSession, Depends(db_helper.session_getter)
    ],  # Сессия базы данных
    task_id: int = Form(...),  # Идентификатор задачи для удаления
):
    """
    Удаление задачи:
    - Удаляет задачу и возвращает обновленный список задач с сообщением об удалении.
    """
    task = await get_task_by_id(task_id, session)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await remove_task(task_id, session)
    tasks = await get_all_tasks(session)

    # После удаления возвращаем шаблон с сообщением об успехе
    return templates_admin.TemplateResponse(
        "task_admin.html",
        {"request": request, "tasks": tasks, "message": "Задача была успешно удалена"},
    )
