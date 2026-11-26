
from datetime import datetime, timezone
from unittest.mock import Mock

import numpy as np
import pytest

from app.twin.propagator import OrbitPropagator


def test_naive_timestamp_rejected():
    satellite = Mock()
    propagator = OrbitPropagator(satellite)

    with pytest.raises(ValueError, match="timezone-aware"):
        propagator.propagate(datetime(2026, 1, 1))

    satellite.sgp4.assert_not_called()


def test_propagation_error_rejected():
    satellite = Mock()
    satellite.sgp4.return_value = (
        1,
        (0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0),
    )

    propagator = OrbitPropagator(satellite)

    with pytest.raises(RuntimeError, match="SGP4 propagation failed"):
        propagator.propagate(datetime.now(timezone.utc))


def test_nonfinite_position_rejected():
    satellite = Mock()
    satellite.sgp4.return_value = (
        0,
        (np.nan, 0.0, 0.0),
        (0.0, 0.0, 0.0),
    )

    propagator = OrbitPropagator(satellite)

    with pytest.raises(ValueError, match="Invalid propagated position"):
        propagator.propagate(datetime.now(timezone.utc))


def test_nonfinite_velocity_rejected():
    satellite = Mock()
    satellite.sgp4.return_value = (
        0,
        (0.0, 0.0, 0.0),
        (np.inf, 0.0, 0.0),
    )

    propagator = OrbitPropagator(satellite)

    with pytest.raises(ValueError, match="Invalid propagated velocity"):
        propagator.propagate(datetime.now(timezone.utc))
