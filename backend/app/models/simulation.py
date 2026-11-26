
from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class SimulationState(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        allow_inf_nan=False,
    )

    simulation_id: str = Field(min_length=1)

    timestamp: datetime

    source: Literal["simulator"] = "simulator"

    mode: Literal["SIMULATED"] = "SIMULATED"

    elapsed_seconds: float = Field(ge=0)

    quality_flags: list[str] = Field(
        default_factory=lambda: ["SIMULATED"]
    )

    @field_validator("timestamp")
    @classmethod
    def validate_timestamp(
        cls, value: datetime
    ) -> datetime:

        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError(
                "Timestamp must be timezone-aware"
            )

        return value.astimezone(timezone.utc)
