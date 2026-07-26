from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://user:password@localhost:5432/ai_student_assistant"
    openai_api_key: str = ""
    google_client_id: str = ""
    google_client_secret: str = ""
    jwt_secret: str = "change-me"
    next_public_api_url: str = "http://localhost:8000"

    class Config:
        env_file = ".env"


settings = Settings()
