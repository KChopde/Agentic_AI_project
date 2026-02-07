from __future__ import annotations

from datetime import datetime

from .schemas import (
    BudgetBreakdown,
    InvestmentAllocation,
    PlanReport,
    RiskProfile,
    SavingsPlan,
)


class ReportAgent:
    def build_report(
        self,
        budget: BudgetBreakdown,
        risk: RiskProfile,
        savings: SavingsPlan,
        allocation: InvestmentAllocation,
    ) -> PlanReport:
        month_by_month = [
            {
                "month": action.month,
                "save_amount": action.save_amount,
                "debt_payment": action.debt_payment,
                "emergency_fund": action.emergency_fund_contribution,
                "notes": action.notes,
            }
            for action in savings.monthly_actions
        ]

        assumptions = [
            "No income shocks assumed over the next 6 months.",
            "Debt minimum payments remain constant.",
            "Investment allocation uses a static glide path.",
        ]

        debt_strategy = "Avalanche (highest APR first)"
        narrative = (
            "This plan prioritizes building a safety buffer while reducing high-interest debt. "
            "Once the emergency fund reaches the target, surplus cash shifts to investments."
        )

        return PlanReport(
            headline=f"6-Month plan generated on {datetime.utcnow().date().isoformat()}",
            assumptions=assumptions,
            month_by_month_plan=month_by_month,
            budget_targets=budget,
            savings_rate=budget.target_savings_rate,
            debt_strategy=debt_strategy,
            allocation=allocation,
            narrative=narrative,
        )
