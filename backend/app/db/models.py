from __future__ import annotations

from sqlalchemy import Column, DateTime, JSON, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Plan(Base):
    __tablename__ = "plans"

    plan_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    payload = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
