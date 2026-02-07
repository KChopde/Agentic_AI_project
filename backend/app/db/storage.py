from __future__ import annotations

from sqlalchemy.orm import Session

from .models import Plan


class PlanStorage:
    def __init__(self, db: Session) -> None:
        self.db = db

    def save_plan(self, plan_id: str, user_id: str, payload: dict) -> Plan:
        plan = Plan(plan_id=plan_id, user_id=user_id, payload=payload)
        self.db.add(plan)
        self.db.commit()
        self.db.refresh(plan)
        return plan

    def get_plan(self, plan_id: str) -> Plan | None:
        return self.db.query(Plan).filter(Plan.plan_id == plan_id).first()
