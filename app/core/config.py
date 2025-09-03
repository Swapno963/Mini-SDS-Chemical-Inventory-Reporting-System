from pydantic import PostgresDsn, BaseSettings


class Settings(BaseSettings):
    # Api settings
    API_PREFIX: str = "/api/v1"
    DEBUG: bool = False
    PROJECT_NAME: str = "Chemical-Inventory-Reporting-System"
    PORT: int = 8000

    # Database settings
    DATABASE_URL: PostgresDsn

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings object
settings = Settings()
