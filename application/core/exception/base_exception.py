class CustomError(Exception):
    """Базовый класс для общих кастомных ошибок."""


class DataBaseError(CustomError):
    """Ошибка для случаев, связанных с базой данных."""

    pass
