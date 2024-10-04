import smtplib

from celery import Celery
from pydantic import EmailStr

from application.core.config import settings
from application.core.schemas.task import SMyTask
from application.utils.create_message_for_email import (
    create_message_add_new_task,
    create_message_confirmation_of_registration,
)

celery = Celery("task", broker="redis://localhost:6379")


@celery.task()
def send_email_confirmation_code(email_to: EmailStr, data_task: SMyTask):
    msg_content = create_message_add_new_task(email_to, data_task)
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        server.send_message(msg_content)


@celery.task()
def send_email_add_new_task_for_you(email_to: EmailStr, code: int):
    msg_content = create_message_confirmation_of_registration(email_to, code)
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        server.send_message(msg_content)
