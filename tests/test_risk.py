import pytest

from ast_demo.models import SensorSnapshot
from ast_demo.risk_engine import calculate_risk, warning_level


@pytest.mark.parametrize(("field", "value", "expected"), [
    ("eye_closed_seconds", 45, 50),
    ("eye_closed_seconds", 90, 100),
    ("head_down_seconds", 600, 50),
    ("head_down_seconds", 1200, 100),
    ("face_missing_seconds", 600, 50),
    ("face_missing_seconds", 1200, 100),
])
def test_signal_normalization(field, value, expected):
    values = {"eye_closed_seconds": 0, "head_down_seconds": 0, "face_missing_seconds": 0}
    values[field] = value
    assert calculate_risk(SensorSnapshot(**values)).value == expected


def test_maximum_signal_wins():
    result = calculate_risk(SensorSnapshot(30, 900, 100))
    assert result.value == 75
    assert result.reason == "head_down_seconds"


def test_risk_clips_above_one_hundred():
    assert calculate_risk(SensorSnapshot(900, 0, 0)).value == 100


def test_negative_values_clip_at_zero():
    assert calculate_risk(SensorSnapshot(-10, -20, -30)).value == 0


def test_detection_unavailable():
    result = calculate_risk(SensorSnapshot(None, None, None))
    assert (result.value, result.available, result.reason) == (0, False, "detection_unavailable")


@pytest.mark.parametrize(("snapshot", "level"), [
    (SensorSnapshot(19, 299, 599), 0),
    (SensorSnapshot(20, 0, 0), 1),
    (SensorSnapshot(0, 600, 0), 2),
    (SensorSnapshot(0, 0, 1200), 3),
])
def test_warning_levels(snapshot, level):
    assert warning_level(snapshot) == level
