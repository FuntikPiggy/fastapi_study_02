from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../../.env")

    db_path: str = "default_value"
    mode: str = "default_value"
