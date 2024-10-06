import smtplib

from celery import Celery
from pydantic import EmailStr

from application.core.config import settings
from application.core.schemas.task import SMyTask
from application.utils.create_message_for_email import (
    create_message_add_new_task,
    create_message_change_task,
    create_message_confirmation_code,
    create_message_accept_task,
)

# Инициализация объекта Celery с брокером Redis
celery = Celery("task", broker=settings.REDIS_URL)


# Задача Celery для отправки email с кодом подтверждения
@celery.task()
def send_email_confirmation_code(email_to: EmailStr, code: int):
    """
    Отправляет письмо с кодом подтверждения на указанный email.

    :param email_to: Email-адрес получателя.
    :param code: Код подтверждения, который будет отправлен.
    """
    # Формируем содержимое письма
    msg_content = create_message_confirmation_code(email_to, code)

    # Настраиваем SMTP-соединение и отправляем письмо
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        # Авторизация на SMTP-сервере
        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        # Отправка письма
        server.send_message(msg_content)


# Задача Celery для отправки email с информацией о новой задаче
@celery.task()
def send_email_add_new_task_for_you(email_to: EmailStr, data_task: SMyTask):
    """
    Отправляет уведомление о создании новой задачи на email пользователя.

    :param email_to: Email-адрес получателя.
    :param data_task: Объект задачи с информацией о новой задаче.
    """
    # Формируем содержимое письма
    msg_content = create_message_add_new_task(email_to, data_task)

    # Настраиваем SMTP-соединение и отправляем письмо
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        # Авторизация на SMTP-сервере
        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        # Отправка письма
        server.send_message(msg_content)


# Задача Celery для отправки email при изменении задачи
@celery.task()
def send_email_change_task_for_you(email_to: EmailStr, data_task: dict):
    """
    Отправляет уведомление об изменении задачи на email пользователя.

    :param email_to: Email-адрес получателя.
    :param data_task: Словарь с информацией о изменениях в задаче.
    """
    # Формируем содержимое письма
    msg_content = create_message_change_task(email_to, data_task)

    # Настраиваем SMTP-соединение и отправляем письмо
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        # Авторизация на SMTP-сервере
        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        # Отправка письма
        server.send_message(msg_content)


# Задача Celery для отправки email при принятии задачи в работу
@celery.task()
def send_email_accept_task(email_to: EmailStr, data_task: dict):
    """
    Отправляет уведомление о принятии задачи в работу на email пользователя.

    :param email_to: Email-адрес получателя.
    :param data_task: Словарь с информацией о принятой задаче.
    """
    # Формируем содержимое письма
    msg_content = create_message_accept_task(email_to, data_task)

    # Настраиваем SMTP-соединение и отправляем письмо
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        # Авторизация на SMTP-сервере
        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        # Отправка письма
        server.send_message(msg_content)
