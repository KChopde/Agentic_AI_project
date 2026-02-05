from __future__ import annotations

import hashlib
import time
from typing import Any

from fastapi import FastAPI, HTTPException

from .agents.orchestrator import Supervisor
from .agents.schemas import PlanRequest, PlanResponse
from .db.database import SessionLocal
from .db.models import Base
from .db.storage import PlanStorage

app = FastAPI(title="Agentic Financial Planner")

metrics: dict[str, Any] = {
    "requests": 0,
    "failures": 0,
    "avg_latency_ms": 0.0,
}

supervisor = Supervisor()


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=SessionLocal.kw["bind"])


@app.middleware("http")
async def metrics_middleware(request, call_next):
    start = time.time()
    metrics["requests"] += 1
    try:
        response = await call_next(request)
        return response
    except Exception:
        metrics["failures"] += 1
        raise
    finally:
        elapsed = (time.time() - start) * 1000
        metrics["avg_latency_ms"] = round(
            (metrics["avg_latency_ms"] + elapsed) / 2, 2
        )


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.get("/metrics")
async def get_metrics() -> dict:
    return metrics


@app.post("/plan", response_model=PlanResponse)
async def create_plan(request: PlanRequest) -> PlanResponse:
    try:
        plan = supervisor.run(request)
    except Exception as exc:
        metrics["failures"] += 1
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    db = SessionLocal()
    try:
        storage = PlanStorage(db)
        storage.save_plan(plan.plan_id, plan.user_id, plan.model_dump())
    finally:
        db.close()

    return plan


@app.get("/plan/{plan_id}")
async def get_plan(plan_id: str) -> dict:
    db = SessionLocal()
    try:
        storage = PlanStorage(db)
        plan = storage.get_plan(plan_id)
    finally:
        db.close()

    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    return plan.payload


@app.post("/simulate/dependency_down")
async def simulate_dependency_down() -> dict:
    metrics["failures"] += 1
    return {"status": "simulated", "error": "LLM_TIMEOUT"}


@app.get("/trace/{user_id}")
async def get_trace(user_id: str) -> dict:
    hashed_user = hashlib.sha256(user_id.encode()).hexdigest()
    return {
        "user_hash": hashed_user,
        "tool_calls": [call.model_dump() for call in supervisor.tools.audit_log],
    }
