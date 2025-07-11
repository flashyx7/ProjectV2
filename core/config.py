
import os
from typing import Optional

class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production-123456789")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./recruitment_tracker.db")
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")
    OFFER_LETTERS_DIR: str = os.getenv("OFFER_LETTERS_DIR", "./offer_letters")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()
import os
from typing import Optional

class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()
