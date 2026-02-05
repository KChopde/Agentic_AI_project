from __future__ import annotations

from .schemas import BudgetBreakdown, Expense


class BudgetAgent:
    def build_budget(self, monthly_income: float, expenses: list[Expense]) -> BudgetBreakdown:
        total_expenses = sum(expense.monthly_amount for expense in expenses)
        fixed_expenses = sum(expense.monthly_amount for expense in expenses if expense.fixed)
        variable_expenses = total_expenses - fixed_expenses
        surplus = monthly_income - total_expenses
        savings_rate = max(0.0, min(0.4, surplus / monthly_income if monthly_income else 0.0))

        recommended_cuts = [
            f"Trim {expense.name} by 5-10%" for expense in expenses if not expense.fixed
        ][:3]
        if surplus < 0:
            recommended_cuts.insert(0, "Reduce variable spending to eliminate deficit")

        return BudgetBreakdown(
            total_income=monthly_income,
            total_expenses=total_expenses,
            fixed_expenses=fixed_expenses,
            variable_expenses=variable_expenses,
            surplus=surplus,
            target_savings_rate=round(savings_rate, 2),
            recommended_cuts=recommended_cuts,
        )
