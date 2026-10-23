import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    APP_NAME = os.getenv("APP_NAME", "School-Connect")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

    DATABASE_URL = os.getenv("DATABASE_URL")

    SECRET_KEY = os.getenv("SECRET_KEY")

    ACCESS_TOKEN_EXPIRE_MINUTES = int(
        os.getenv(
            "ACCESS_TOKEN_EXPIRE_MINUTES",
            "30",
        )
    )

    ALGORITHM = "HS256"


settings = Settings()


if not settings.SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not configured")