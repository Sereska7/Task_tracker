from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from application.core.models import User
from application.core.models.user import PositionType
from application.core.schemas.user import SUserCreate, SUser
from application.utils.auth_user import get_password_hash


# Добавление нового пользователя в базу данных
async def add_user(
    name: str, position: str, email: str, password: str, session: AsyncSession
) -> SUserCreate:
    """
    Добавляет нового пользователя в базу данных, хэширует пароль перед сохранением.

    :param name: Имя пользователя.
    :param position: Должность пользователя.
    :param email: Электронная почта пользователя.
    :param password: Пароль пользователя.
    :param session: Асинхронная сессия базы данных.
    :return: Возвращает созданного пользователя.
    """
    # Хэшируем пароль перед сохранением
    hash_password = get_password_hash(password)

    # Создаем объект пользователя
    user = User(
        name=name,
        email=email,
        hash_password=hash_password,
        position=position,
    )

    # Добавляем пользователя в сессию и фиксируем изменения в базе данных
    session.add(user)
    await session.commit()

    return user


# Получение пользователя по заданным фильтрам (например, по email)
async def get_user(session: AsyncSession, **data: dict):
    """
    Возвращает одного пользователя на основе заданных фильтров (например, email).

    :param session: Асинхронная сессия базы данных.
    :param data: Фильтры для поиска пользователя.
    :return: Найденный пользователь или None.
    """
    stmt = select(User.__table__.columns).filter_by(**data)
    user = await session.execute(stmt)
    return user.mappings().one_or_none()


# Получение профиля текущего пользователя по его ID
async def get_my_profile(user_id: int, session: AsyncSession):
    """
    Возвращает профиль текущего пользователя по его ID.

    :param user_id: ID пользователя.
    :param session: Асинхронная сессия базы данных.
    :return: Профиль пользователя.
    """
    stmt = select(User).where(User.id == user_id)
    user = await session.execute(stmt)
    return user.scalar()


# Получение всех пользователей, которые не являются директорами
async def get_users(session: AsyncSession):
    """
    Возвращает список всех пользователей, которые не являются директорами.

    :param session: Асинхронная сессия базы данных.
    :return: Список пользователей.
    """
    stmt = select(User).where(User.is_director == False)
    user = await session.execute(stmt)
    return user.scalars().all()
