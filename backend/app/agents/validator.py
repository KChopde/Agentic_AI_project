from __future__ import annotations

from pydantic import ValidationError

from .schemas import PlanResponse


class ValidatorAgent:
    def validate(self, payload: dict) -> list[str]:
        errors: list[str] = []
        try:
            PlanResponse.model_validate(payload)
        except ValidationError as exc:
            errors.extend([str(error) for error in exc.errors()])
        return errors
