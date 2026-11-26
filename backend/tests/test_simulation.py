
from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from app.models.simulation import SimulationState


def make_state(**overrides):
    data = {
        "simulation_id": "demo-001",
        "timestamp": datetime.now(timezone.utc),
        "elapsed_seconds": 10.0,
    }

    data.update(overrides)

    return SimulationState(**data)


def test_valid_simulation_state():
    state = make_state()

    assert state.simulation_id == "demo-001"
    assert state.source == "simulator"
    assert state.mode == "SIMULATED"
    assert state.elapsed_seconds == 10.0
    assert "SIMULATED" in state.quality_flags


def test_naive_timestamp_rejected():
    with pytest.raises(ValidationError):
        make_state(timestamp=datetime(2026, 1, 1))


def test_negative_elapsed_time_rejected():
    with pytest.raises(ValidationError):
        make_state(elapsed_seconds=-1.0)


def test_nonfinite_value_rejected():
    with pytest.raises(ValidationError):
        make_state(elapsed_seconds=float("nan"))


def test_invalid_mode_rejected():
    with pytest.raises(ValidationError):
        make_state(mode="LIVE")


def test_unexpected_field_rejected():
    with pytest.raises(ValidationError):
        make_state(unknown_field=123)
