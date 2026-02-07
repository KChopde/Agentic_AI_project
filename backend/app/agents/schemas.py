from __future__ import annotations

from datetime import date
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class RiskLabel(str, Enum):
    conservative = "conservative"
    balanced = "balanced"
    growth = "growth"


class Expense(BaseModel):
    name: str
    monthly_amount: float
    category: str
    fixed: bool


class Debt(BaseModel):
    name: str
    balance: float
    apr: float
    minimum_payment: float


class Goal(BaseModel):
    name: str
    target_amount: float
    target_date: date


class PlanRequest(BaseModel):
    user_id: str
    monthly_income: float
    expenses: List[Expense]
    debts: List[Debt]
    goals: List[Goal]
    risk_preference: RiskLabel
    timeline_months: int = Field(ge=1, le=24)
    emergency_fund_months: Optional[int] = Field(default=0, ge=0, le=12)


class BudgetBreakdown(BaseModel):
    total_income: float
    total_expenses: float
    fixed_expenses: float
    variable_expenses: float
    surplus: float
    target_savings_rate: float
    recommended_cuts: List[str]


class RiskProfile(BaseModel):
    risk_score: int = Field(ge=1, le=10)
    risk_label: RiskLabel
    constraints: List[str]
    emergency_fund_target_months: int
    notes: List[str]


class SavingsMonthAction(BaseModel):
    month: int
    save_amount: float
    debt_payment: float
    emergency_fund_contribution: float
    notes: List[str]


class SavingsPlan(BaseModel):
    monthly_actions: List[SavingsMonthAction]
    total_saved: float
    total_debt_paid: float


class InvestmentAllocation(BaseModel):
    equity_pct: int
    bonds_pct: int
    cash_pct: int
    notes: List[str]


class PlanReport(BaseModel):
    headline: str
    assumptions: List[str]
    month_by_month_plan: List[dict]
    budget_targets: BudgetBreakdown
    savings_rate: float
    debt_strategy: str
    allocation: InvestmentAllocation
    narrative: str


class ToolTrace(BaseModel):
    tool: str
    status: str
    details: dict


class PlanResponse(BaseModel):
    plan_id: str
    user_id: str
    budget: BudgetBreakdown
    risk: RiskProfile
    savings: SavingsPlan
    report: PlanReport
    trace: List[ToolTrace]
    created_at: str


class StoredPlan(BaseModel):
    plan_id: str
    user_id: str
    payload: dict
    created_at: str
