import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Literal

class Settings(BaseSettings):
    # 路徑中心化
    PROJECT_ROOT: Path = Path(__file__).resolve().parent
    LOG_DIR: Path = PROJECT_ROOT / "logs"
    
    # 多模型 API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    
    # 預設評估引擎
    DEFAULT_PROVIDER: Literal["openai", "anthropic", "google", "local"] = os.getenv("EVALUATOR_PROVIDER", "openai")
    
    # 服務設定
    APP_NAME: str = "Enterprise AI Evaluator"
    APP_VERSION: str = "1.1.0"

    class Config:
        env_file = ".env"

settings = Settings()
settings.LOG_DIR.mkdir(parents=True, exist_ok=True)