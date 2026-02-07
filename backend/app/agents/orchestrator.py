from __future__ import annotations

from datetime import datetime

from .budget import BudgetAgent
from .report import ReportAgent
from .risk import RiskAgent
from .savings import SavingsAgent
from .schemas import (
    InvestmentAllocation,
    PlanRequest,
    PlanResponse,
    ToolTrace,
)
from .tools import MCPTools
from .validator import ValidatorAgent


class Supervisor:
    def __init__(self) -> None:
        self.budget_agent = BudgetAgent()
        self.risk_agent = RiskAgent()
        self.savings_agent = SavingsAgent()
        self.report_agent = ReportAgent()
        self.validator = ValidatorAgent()
        self.tools = MCPTools()
        self.tool_allowlist = {
            "budget": {"get_transactions", "get_recurring_bills"},
            "risk": {"get_debts", "get_goal_profile"},
            "savings": {"get_debts"},
            "report": {"write_plan"},
        }

    def _allocation_from_risk(self, risk_score: int) -> InvestmentAllocation:
        if risk_score <= 4:
            equity, bonds, cash = 50, 35, 15
        elif risk_score <= 7:
            equity, bonds, cash = 65, 25, 10
        else:
            equity, bonds, cash = 75, 20, 5
        return InvestmentAllocation(
            equity_pct=equity,
            bonds_pct=bonds,
            cash_pct=cash,
            notes=["Allocation respects risk constraints and liquidity needs."],
        )

    def run(self, request: PlanRequest) -> PlanResponse:
        self.tools.get_transactions(request.user_id, "-90d", "today")
        self.tools.get_recurring_bills(request.user_id)

        budget = self.budget_agent.build_budget(request.monthly_income, request.expenses)
        risk = self.risk_agent.assess(
            request.risk_preference,
            age=None,
            debts=request.debts,
            emergency_fund_months=request.emergency_fund_months or 0,
        )
        allocation = self._allocation_from_risk(risk.risk_score)
        savings = self.savings_agent.build_plan(
            budget.surplus,
            request.debts,
            request.emergency_fund_months or 0,
            risk.emergency_fund_target_months,
            request.timeline_months,
        )
        report = self.report_agent.build_report(budget, risk, savings, allocation)

        plan_id = self.tools.write_plan(request.user_id, report.model_dump())
        trace = [
            ToolTrace(tool=call.name, status=call.status, details=call.details)
            for call in self.tools.audit_log
        ]

        response = PlanResponse(
            plan_id=plan_id,
            user_id=request.user_id,
            budget=budget,
            risk=risk,
            savings=savings,
            report=report,
            trace=trace,
            created_at=datetime.utcnow().isoformat(),
        )

        validation_errors = self.validator.validate(response.model_dump())
        if validation_errors:
            response.report.assumptions.append(
                f"Validator detected issues: {validation_errors}"
            )
        return response
