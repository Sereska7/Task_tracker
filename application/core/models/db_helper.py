from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
)

from application.core.config import settings


# Класс помощника для управления соединениями с базой данных и сессиями.
class DatabaseHelper:
    def __init__(
        self,
        url: str,  # URL подключения к базе данных
        echo: bool = False,  # Логгирование SQL-запросов
        echo_pool: bool = False,  # Логгирование операций пула
        pool_size: int = 5,  # Размер пула подключений
        max_overflow: int = 10,  # Максимальное количество дополнительных подключений
    ) -> None:
        """
        Инициализирует экземпляр DatabaseHelper, создавая асинхронный движок базы данных
        и фабрику сессий с настраиваемыми параметрами.
        """
        # Создание асинхронного движка для подключения к базе данных
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )

        # Создание фабрики для сессий базы данных
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False
        )

    async def dispose(self) -> None:
        """
        Закрывает все подключения движка к базе данных, очищая пул.
        """
        await self.engine.dispose()

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Асинхронный генератор для получения сессии базы данных.
        Используйте его в зависимостях FastAPI для работы с базой данных.
        """
        async with self.session_factory() as session:
            yield session


if settings.MODE == "TEST":
    DB_URL = settings.TEST_DB_URL
else:
    DB_URL = settings.DB_URL

print(f"DB_URL: {DB_URL}")

# Создание экземпляра DatabaseHelper с настройками из переменных окружения
db_helper = DatabaseHelper(
    url=str(DB_URL),
    echo=settings.db_echo,
    echo_pool=settings.db_echo_pool,
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
)
