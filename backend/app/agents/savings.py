from __future__ import annotations

from .schemas import Debt, SavingsPlan, SavingsMonthAction


class SavingsAgent:
    def build_plan(
        self,
        surplus: float,
        debts: list[Debt],
        emergency_fund_months: int,
        emergency_fund_target: int,
        timeline_months: int,
    ) -> SavingsPlan:
        monthly_actions: list[SavingsMonthAction] = []
        surplus = max(0.0, surplus)
        total_debt_paid = 0.0
        total_saved = 0.0

        debt_priority = sorted(debts, key=lambda d: d.apr, reverse=True)
        for month in range(1, timeline_months + 1):
            emergency_contribution = 0.0
            if emergency_fund_months < emergency_fund_target:
                emergency_contribution = surplus * 0.4
                emergency_fund_months += 0.5

            debt_payment = surplus * 0.4
            if debt_priority:
                debt_payment += sum(debt.minimum_payment for debt in debt_priority)

            save_amount = surplus - emergency_contribution - (surplus * 0.4)
            notes = []
            if emergency_contribution > 0:
                notes.append("Build emergency fund")
            if debt_priority:
                notes.append(f"Focus on {debt_priority[0].name} (highest APR)")

            monthly_actions.append(
                SavingsMonthAction(
                    month=month,
                    save_amount=round(save_amount, 2),
                    debt_payment=round(debt_payment, 2),
                    emergency_fund_contribution=round(emergency_contribution, 2),
                    notes=notes,
                )
            )
            total_debt_paid += debt_payment
            total_saved += save_amount + emergency_contribution

        return SavingsPlan(
            monthly_actions=monthly_actions,
            total_saved=round(total_saved, 2),
            total_debt_paid=round(total_debt_paid, 2),
        )
