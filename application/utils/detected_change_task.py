from typing import Dict, Any

from application.core.schemas.task import SBaseTask, SChangeTask


def detect_changes(current_task: SBaseTask, new_data: SChangeTask) -> Dict[str, Any]:
    """
    Сравнение текущих данных задачи с новыми данными для выявления изменений.

    :param current_task: Текущие данные задачи, представленные как SBaseTask.
    :param new_data: Новые данные задачи, которые нужно сравнить, представлены как SChangeTask.
    :return: Словарь с полями, которые были изменены, и их новыми значениями.
    """
    changes = {}

    # Сравнение описания задачи
    if current_task.description != new_data.description:
        changes["description"] = new_data.description

    # Сравнение даты начала задачи
    if current_task.date_from != new_data.date_from:
        changes["date_from"] = new_data.date_from

    # Сравнение даты окончания задачи
    if current_task.date_to != new_data.date_to:
        changes["date_to"] = new_data.date_to

    return changes
