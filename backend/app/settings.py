from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@localhost:5432/financial_planner"

    class Config:
        env_prefix = "APP_"


Settings()
