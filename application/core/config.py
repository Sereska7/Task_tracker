import dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Загружаем переменные окружения из файла .env
dotenv.load_dotenv()


class Settings(BaseSettings):
    """
    Класс Settings используется для загрузки конфигураций приложения,
    таких как параметры базы данных, настройки почтового сервера и секретные ключи.
    """

    # Параметры подключения к базе данных
    DB_URL: str  # URL для подключения к базе данных

    # Параметры пула соединений базы данных
    db_echo: bool = False  # Логирование SQL-запросов
    db_echo_pool: bool = False  # Логирование действий с пулом соединений
    db_pool_size: int = 50  # Размер пула соединений
    db_max_overflow: int = 10  # Максимальное количество дополнительных соединений

    # Параметры администратора
    ADMIN_EMAIL: str  # Email администратора системы

    # Параметры безопасности
    SECRET_KEY: str  # Секретный ключ для генерации токенов
    ALGORITHM: str  # Алгоритм шифрования для токенов

    # Параметры SMTP (почтового сервера)
    SMTP_USERNAME: str  # Логин для подключения к SMTP-серверу
    SMTP_PASSWORD: str  # Пароль для подключения к SMTP-серверу
    SMTP_HOST: str  # Адрес SMTP-сервера
    SMTP_PORT: int  # Порт SMTP-сервера

    # Конфигурация модели Pydantic для загрузки переменных окружения
    model_config = {
        "env_file": ".env"  # Путь к файлу окружения
    }


# Создание объекта настроек приложения
settings = Settings()
