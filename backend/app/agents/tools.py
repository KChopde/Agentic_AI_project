from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from .schemas import Debt, Goal


@dataclass
class ToolCall:
    name: str
    status: str
    details: dict = field(default_factory=dict)


class MCPTools:
    def __init__(self) -> None:
        self.audit_log: list[ToolCall] = []

    def _record(self, name: str, status: str, details: dict) -> None:
        self.audit_log.append(ToolCall(name=name, status=status, details=details))

    def get_transactions(self, user_id: str, start_date: str, end_date: str) -> list[dict]:
        self._record(
            "get_transactions",
            "success",
            {"user_id": user_id, "start_date": start_date, "end_date": end_date},
        )
        return []

    def get_recurring_bills(self, user_id: str) -> list[dict]:
        self._record("get_recurring_bills", "success", {"user_id": user_id})
        return []

    def get_debts(self, user_id: str) -> list[Debt]:
        self._record("get_debts", "success", {"user_id": user_id})
        return []

    def get_goal_profile(self, user_id: str) -> list[Goal]:
        self._record("get_goal_profile", "success", {"user_id": user_id})
        return []

    def write_plan(self, user_id: str, plan_json: dict) -> str:
        plan_id = f"plan_{datetime.utcnow().timestamp():.0f}"
        self._record("write_plan", "success", {"user_id": user_id, "plan_id": plan_id})
        return plan_id
