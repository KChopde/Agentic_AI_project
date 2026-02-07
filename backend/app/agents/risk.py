from __future__ import annotations

from .schemas import Debt, RiskProfile, RiskLabel


class RiskAgent:
    def assess(self, risk_preference: RiskLabel, age: int | None, debts: list[Debt], emergency_fund_months: int) -> RiskProfile:
        debt_load = sum(debt.balance for debt in debts)
        risk_score = 5
        if risk_preference == RiskLabel.conservative:
            risk_score = 3
        elif risk_preference == RiskLabel.growth:
            risk_score = 8

        if debt_load > 50000:
            risk_score = max(2, risk_score - 1)

        emergency_target = 6 if risk_score <= 4 else 4
        constraints = ["no_crypto"]
        if risk_score <= 4:
            constraints.append("max_equity_pct<=60")
        else:
            constraints.append("max_equity_pct<=75")

        notes = [
            f"Emergency fund target set to {emergency_target} months.",
            f"Current emergency fund is {emergency_fund_months} months.",
        ]
        if age:
            notes.append(f"Age provided: {age}. Adjust risk for life stage in review.")

        return RiskProfile(
            risk_score=risk_score,
            risk_label=risk_preference,
            constraints=constraints,
            emergency_fund_target_months=emergency_target,
            notes=notes,
        )
