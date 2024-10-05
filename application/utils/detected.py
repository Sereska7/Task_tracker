from typing import Dict, Any

from application.core.schemas.task import SBaseTask, SChangeTask


def detect_changes(
    current_task: SBaseTask, new_data: SChangeTask
) -> Dict[str, Any]:
    """
    Сравнение текущих данных задачи с новыми данными для выявления изменений
    """
    changes = {}

    # Пример сравнения полей задачи
    if current_task.description != new_data.description:
        changes["description"] = new_data.description
    if current_task.date_from != new_data.date_from:
        changes["date_from"] = new_data.date_from
    if current_task.date_to != new_data.date_to:
        changes["date_to"] = new_data.date_to

    return changes
