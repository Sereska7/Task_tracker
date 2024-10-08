from enum import Enum


class TaskStatus(Enum):
    """
    Перечисление для статуса задачи.
    Определяет возможные состояния задачи:
    - PENDING: задача ожидает выполнения.
    - IN_PROGRESS: задача находится в процессе выполнения.
    - COMPLETED: задача завершена.
    """
    PENDING = "Ожидание"          # Задача ожидает выполнения
    IN_PROGRESS = "В работе"      # Задача в процессе выполнения
    COMPLETED = "Выполнено"       # Задача завершена


class TypeTask(Enum):
    """
    Перечисление для типов задач.
    Определяет возможные роли или типы задач:
    - DEVELOPER: задача, связанная с разработкой.
    - MANAGER: задача, связанная с управлением.
    - TESTER: задача, связанная с тестированием.
    """
    DEVELOPER = "Developer"       # Задача для разработчика
    MANAGER = "Manager"           # Задача для менеджера
    TESTER = "Tester"             # Задача для тестировщика


class PositionType(Enum):
    """
    Перечисление для типа должности пользователя.
    Определяет возможные должности пользователя в системе:
    - DEVELOPER: разработчик.
    - MANAGER: менеджер.
    - TESTER: тестировщик.
    """
    DEVELOPER = "Developer"       # Должность разработчика
    MANAGER = "Manager"           # Должность менеджера
    TESTER = "Tester"             # Должность тестировщика
