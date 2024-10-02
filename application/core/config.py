import dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

dotenv.load_dotenv()


class Settings(BaseSettings):

    DB_URL: str

    db_echo: bool = False
    db_echo_pool: bool = False
    db_pool_size: int = 50
    db_max_overflow: int = 10

    ADMIN_EMAIL: str

    SECRET_KEY: str
    ALGORITHM: str

    model_config = SettingsConfigDict(env_file="/.env")


settings = Settings()
