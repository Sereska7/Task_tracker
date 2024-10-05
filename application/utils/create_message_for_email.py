from email.message import EmailMessage

from pydantic import EmailStr

from application.core.config import settings
from application.core.schemas.task import SMyTask


def create_message_confirmation_code(email_to: EmailStr, code: int):
    email = EmailMessage()

    email["Subject"] = "Ваш код подтверждения регистрации"
    email["From"] = settings.SMTP_USERNAME
    email["To"] = email_to

    email.set_content(f"Здравствуйте, вот ваш код подтверждения: {code}")
    return email


def create_message_add_new_task(email_to: EmailStr, data_task: SMyTask):
    email = EmailMessage()

    email["Subject"] = "Вам назначена новая задача!!!"
    email["From"] = settings.SMTP_USERNAME
    email["To"] = email_to

    email.set_content(
        f"Здравствуйте, вот ваша новая задача!\nПожалуйста ознакомьтесь:\n"
        f"Название: {data_task.name}\n"
        f"Проект: {data_task.project_name}\n"
        f"Описание: {data_task.description}\n"
        f"Дата начала: {data_task.date_from}\n"
        f"Дата окончания: {data_task.date_to}\n"
        f"Статус: {data_task.status}\n"
    )
    return email


def create_message_change_task(email_to: EmailStr, data_task: dict):
    email = EmailMessage()

    email["Subject"] = "Ваша задача изменилась!!!"
    email["From"] = settings.SMTP_USERNAME
    email["To"] = email_to

    text = "\n".join([f"{key}: {value}" for key, value in data_task.items()])

    email.set_content(
        f"Здравствуйте, ваша задача изменилась!\nПожалуйста ознакомьтесь:\n"
        f"{"\n".join([f"{key}: {value}" for key, value in data_task.items()])}"
    )
    return email


def create_message_accept_task(email_to: EmailStr, data_task: SMyTask):
    email = EmailMessage()

    email["Subject"] = "Вы приняли задачу в работу!"
    email["From"] = settings.SMTP_USERNAME
    email["To"] = email_to

    email.set_content(
        f"Здравствуйте, вы приняли задачу {data_task.name}\nПожалуйста ознакомьтесь:\n"
        f"Название: {data_task.name}\n"
        f"Описание: {data_task.description}\n"
        f"Сроки: с {data_task.date_from} по {data_task.date_to}"
    )
    return email
