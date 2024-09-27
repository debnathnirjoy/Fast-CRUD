from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    ALLOWED_HOSTS: list[str]
    ENV: str
    LOG_PATH: str
    PAPERTRAIL_PORT: int
    PAPERTRAIL_HOST: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


config = Settings()
