# Agentic Financial Planner

An end-to-end demo of a multi-agent financial planning system with a FastAPI backend, a Next.js UI, and PostgreSQL storage.

## Features

- **Supervisor orchestration**: Input → data fetch → Budget → Risk → Savings → Report → Validate → Output
- **Multi-agent responsibilities**: Budget, Risk, Savings, Report, Validator
- **MCP-style tooling**: allowlists, audit logs, and plan persistence
- **API-first design**: JSON output plus human-readable report content
- **LLM router**: provider switching interface with retries and timeouts

## Backend (FastAPI)

### Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run

```bash
uvicorn app.main:app --reload
```

### Endpoints

- `POST /plan` → generate a 6-month plan
- `GET /plan/{plan_id}` → retrieve a stored plan
- `POST /simulate/dependency_down` → test resilience
- `GET /health` → healthcheck
- `GET /metrics` → request metrics

## Frontend (Next.js)

### Setup

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Data Layer

Uses PostgreSQL via SQLAlchemy. Configure your connection string with `APP_DATABASE_URL`.

## Demo Scenario

1. Submit input with income, expenses, debts, goals, risk preference, timeline.
2. Receive month-by-month plan, budget targets, debt payoff strategy, and investment allocation.
3. Inspect the tool-call trace for transparency.

## Example Input

```json
{
  "user_id": "demo-user",
  "monthly_income": 8000,
  "expenses": [
    { "name": "Rent", "monthly_amount": 2200, "category": "housing", "fixed": true },
    { "name": "Utilities", "monthly_amount": 400, "category": "utilities", "fixed": true },
    { "name": "Groceries", "monthly_amount": 700, "category": "food", "fixed": false }
  ],
  "debts": [
    { "name": "Credit Card", "balance": 12000, "apr": 0.23, "minimum_payment": 250 }
  ],
  "goals": [
    { "name": "Home down payment", "target_amount": 40000, "target_date": "2026-06-01" }
  ],
  "risk_preference": "balanced",
  "timeline_months": 6,
  "emergency_fund_months": 2
}
```

## Output Highlights

- JSON and human-readable report content
- Tool trace for auditability
- Allocation recommendations based on risk profile

## License

MIT
