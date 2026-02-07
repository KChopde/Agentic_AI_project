"use client";

import { useState } from "react";

const defaultPlan = {
  month_by_month_plan: [],
  allocation: { equity_pct: 65, bonds_pct: 25, cash_pct: 10 },
  budget_targets: {
    total_income: 8000,
    total_expenses: 5400,
    fixed_expenses: 3600,
    variable_expenses: 1800,
    surplus: 2600,
    target_savings_rate: 0.32
  }
};

export default function Home() {
  const [report, setReport] = useState(defaultPlan);

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
        <form className="card">
          <h2>Input Snapshot</h2>
          <label>
            Monthly income
            <input type="number" defaultValue={8000} />
          </label>
          <label>
            Fixed expenses
            <input type="number" defaultValue={3600} />
          </label>
          <label>
            Variable expenses
            <input type="number" defaultValue={1800} />
          </label>
          <label>
            Risk preference
            <select defaultValue="balanced">
              <option value="conservative">Conservative</option>
              <option value="balanced">Balanced</option>
              <option value="growth">Growth</option>
            </select>
          </label>
          <label>
            Timeline (months)
            <input type="number" defaultValue={6} />
          </label>
          <button type="button" onClick={() => setReport(defaultPlan)}>
            Generate Plan
          </button>
        </form>

        <section className="card">
          <h2>Plan Overview</h2>
          <div className="stat-row">
            <div>
              <p className="stat-label">Savings rate</p>
              <p className="stat-value">{Math.round(report.budget_targets.target_savings_rate * 100)}%</p>
            </div>
            <div>
              <p className="stat-label">Monthly surplus</p>
              <p className="stat-value">${report.budget_targets.surplus}</p>
            </div>
            <div>
              <p className="stat-label">Allocation</p>
              <p className="stat-value">
                {report.allocation.equity_pct}% / {report.allocation.bonds_pct}% / {report.allocation.cash_pct}%
              </p>
            </div>
          </div>
          <div className="callout">
            <p>Trace: fetched transactions → built budget → assessed risk → optimized savings → validated schema.</p>
          </div>
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
          {[1, 2, 3, 4, 5, 6].map((month) => (
            <div key={month} className="table-row">
              <span>Month {month}</span>
              <span>$850</span>
              <span>$1,040</span>
              <span>$520</span>
              <span>Build EF + avalanche</span>
            </div>
          ))}
        </div>
      </section>
    </section>
  );
}
