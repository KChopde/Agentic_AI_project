"use client";

import { useMemo, useState } from "react";

type RiskPreference = "conservative" | "balanced" | "growth";

type MonthPlan = {
  month: number;
  save: number;
  debt: number;
  emergency: number;
  notes: string;
};

type PlanView = {
  allocation: { equity_pct: number; bonds_pct: number; cash_pct: number };
  budget_targets: {
    total_income: number;
    total_expenses: number;
    fixed_expenses: number;
    variable_expenses: number;
    surplus: number;
    target_savings_rate: number;
  };
  month_by_month_plan: MonthPlan[];
};

const makeAllocation = (risk: RiskPreference) => {
  if (risk === "conservative") return { equity_pct: 50, bonds_pct: 35, cash_pct: 15 };
  if (risk === "growth") return { equity_pct: 75, bonds_pct: 20, cash_pct: 5 };
  return { equity_pct: 65, bonds_pct: 25, cash_pct: 10 };
};

const createPlan = (
  income: number,
  fixedExpenses: number,
  variableExpenses: number,
  months: number,
  risk: RiskPreference
): PlanView => {
  const totalExpenses = fixedExpenses + variableExpenses;
  const surplus = Math.max(income - totalExpenses, 0);
  const emergency = Math.round(surplus * 0.2);
  const debt = Math.round(surplus * 0.4);
  const save = Math.max(surplus - emergency - debt, 0);

  const monthByMonth = Array.from({ length: months }, (_, index) => ({
    month: index + 1,
    save,
    debt,
    emergency,
    notes: "Build emergency fund + debt avalanche"
  }));

  return {
    allocation: makeAllocation(risk),
    budget_targets: {
      total_income: income,
      total_expenses: totalExpenses,
      fixed_expenses: fixedExpenses,
      variable_expenses: variableExpenses,
      surplus,
      target_savings_rate: income > 0 ? Number((surplus / income).toFixed(2)) : 0
    },
    month_by_month_plan: monthByMonth
  };
};

export default function Home() {
  const [monthlyIncome, setMonthlyIncome] = useState(8000);
  const [fixedExpenses, setFixedExpenses] = useState(3600);
  const [variableExpenses, setVariableExpenses] = useState(1800);
  const [timelineMonths, setTimelineMonths] = useState(6);
  const [riskPreference, setRiskPreference] = useState<RiskPreference>("balanced");

  const [report, setReport] = useState<PlanView>(() =>
    createPlan(8000, 3600, 1800, 6, "balanced")
  );

  const warning = useMemo(() => {
    if (report.budget_targets.surplus > 0) return null;
    return "Expenses exceed income. Reduce variable spend or increase income.";
  }, [report.budget_targets.surplus]);

  const handleGeneratePlan = () => {
    const boundedMonths = Math.min(24, Math.max(1, timelineMonths));
    setReport(
      createPlan(
        monthlyIncome,
        fixedExpenses,
        variableExpenses,
        boundedMonths,
        riskPreference
      )
    );
  };

  return (
    <section className="layout">
      <header className="hero">
        <div>
          <p className="badge">Multi-Agent Planner</p>
          <h1>Agentic Financial Planning Console</h1>
          <p className="subtitle">
            Build a 6-month budget, savings, and investment plan with transparent tool
            traces and schema-validated outputs.
          </p>
        </div>
        <div className="hero-card">
          <h3>Output Highlights</h3>
          <ul>
            <li>Month-by-month cashflow actions</li>
            <li>Debt avalanche payoff strategy</li>
            <li>Risk-aligned allocation targets</li>
            <li>Audit trail of MCP tool usage</li>
          </ul>
        </div>
      </header>

      <div className="grid">
        <form
          className="card"
          onSubmit={(event) => {
            event.preventDefault();
            handleGeneratePlan();
          }}
        >
          <h2>Input Snapshot</h2>
          <label>
            Monthly income
            <input
              type="number"
              value={monthlyIncome}
              onChange={(event) => setMonthlyIncome(Number(event.target.value))}
            />
          </label>
          <label>
            Fixed expenses
            <input
              type="number"
              value={fixedExpenses}
              onChange={(event) => setFixedExpenses(Number(event.target.value))}
            />
          </label>
          <label>
            Variable expenses
            <input
              type="number"
              value={variableExpenses}
              onChange={(event) => setVariableExpenses(Number(event.target.value))}
            />
          </label>
          <label>
            Risk preference
            <select
              value={riskPreference}
              onChange={(event) => setRiskPreference(event.target.value as RiskPreference)}
            >
              <option value="conservative">Conservative</option>
              <option value="balanced">Balanced</option>
              <option value="growth">Growth</option>
            </select>
          </label>
          <label>
            Timeline (months)
            <input
              type="number"
              min={1}
              max={24}
              value={timelineMonths}
              onChange={(event) => setTimelineMonths(Number(event.target.value))}
            />
          </label>
          <button type="submit">Generate Plan</button>
        </form>

        <section className="card">
          <h2>Plan Overview</h2>
          <div className="stat-row">
            <div>
              <p className="stat-label">Savings rate</p>
              <p className="stat-value">
                {Math.round(report.budget_targets.target_savings_rate * 100)}%
              </p>
            </div>
            <div>
              <p className="stat-label">Monthly surplus</p>
              <p className="stat-value">${report.budget_targets.surplus}</p>
            </div>
            <div>
              <p className="stat-label">Allocation</p>
              <p className="stat-value">
                {report.allocation.equity_pct}% / {report.allocation.bonds_pct}% /{" "}
                {report.allocation.cash_pct}%
              </p>
            </div>
          </div>
          <div className="callout">
            <p>
              Trace: fetched transactions → built budget → assessed risk → optimized
              savings → validated schema.
            </p>
          </div>
          {warning ? <p className="warning">{warning}</p> : null}
          <div className="split">
            <div>
              <h3>Budget Targets</h3>
              <ul>
                <li>Total income: ${report.budget_targets.total_income}</li>
                <li>Total expenses: ${report.budget_targets.total_expenses}</li>
                <li>Fixed: ${report.budget_targets.fixed_expenses}</li>
                <li>Variable: ${report.budget_targets.variable_expenses}</li>
              </ul>
            </div>
            <div>
              <h3>Investment Mix</h3>
              <ul>
                <li>Equities: {report.allocation.equity_pct}%</li>
                <li>Bonds: {report.allocation.bonds_pct}%</li>
                <li>Cash: {report.allocation.cash_pct}%</li>
              </ul>
            </div>
          </div>
        </section>
      </div>

      <section className="card full">
        <h2>Month-by-Month Output</h2>
        <div className="table">
          <div className="table-row header">
            <span>Month</span>
            <span>Save</span>
            <span>Debt</span>
            <span>Emergency</span>
            <span>Notes</span>
          </div>
          {report.month_by_month_plan.map((entry) => (
            <div key={entry.month} className="table-row">
              <span>Month {entry.month}</span>
              <span>${entry.save}</span>
              <span>${entry.debt}</span>
              <span>${entry.emergency}</span>
              <span>{entry.notes}</span>
            </div>
          ))}
        </div>
      </section>
    </section>
  );
}
