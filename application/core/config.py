import os
from typing import Literal

import dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


# Загружаем основной файл окружения
dotenv.load_dotenv()


class Settings(BaseSettings):
    """
    Класс Settings используется для загрузки конфигураций приложения,
    таких как параметры базы данных, настройки почтового сервера и секретные ключи.
    """

    MODE: Literal["DEV", "TEST"]
    # Параметры подключения к базе данных
    DB_URL: str  # URL для подключения к базе данных
    TEST_DB_URL: str  # URL для подключения в тестовой базе данных

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    REDIS_URL: str

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

    # Используем SettingsConfigDict для указания нужного env-файла
    model_config = SettingsConfigDict(env_file="/.env")


# Создание объекта настроек приложения
settings = Settings()

print(f"Окружение: {settings.MODE}")
