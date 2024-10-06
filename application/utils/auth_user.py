from jose import jwt
from passlib.context import CryptContext

from application.core.config import settings

# Используемый контекст для хеширования паролей с bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """
    Возвращает хеш пароля с использованием bcrypt.

    :param password: Открытый пароль в виде строки.
    :return: Хешированный пароль.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет соответствие открытого пароля и хешированного пароля.

    :param plain_password: Открытый пароль.
    :param hashed_password: Хешированный пароль.
    :return: True, если пароль совпадает, иначе False.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    """
    Создание JWT токена для авторизации пользователя.

    :param data: Данные, которые будут зашифрованы в токене.
    :return: Строка с закодированным JWT токеном.
    """
    # Создаем копию переданных данных для дальнейшего кодирования
    to_encode = data.copy()

    # Кодируем данные в JWT токен, используя секретный ключ и алгоритм
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    # Возвращаем закодированный JWT токен
    return encoded_jwt
