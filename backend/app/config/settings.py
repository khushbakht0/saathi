from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = ""
    environment: str = "development"
    jwt_secret: str = ""
    openai_api_key: str = ""
    google_client_id: str = ""
    google_client_secret: str = ""
    backend_version: str = "0.2.0"


settings = Settings()
