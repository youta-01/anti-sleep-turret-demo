from __future__ import annotations

from .models import RiskResult, SensorSnapshot

LV3_THRESHOLDS = {
    "eye_closed_seconds": 90.0,
    "head_down_seconds": 1200.0,
    "face_missing_seconds": 1200.0,
}


def calculate_risk(snapshot: SensorSnapshot) -> RiskResult:
    candidates: list[tuple[str, float]] = []
    for name, threshold in LV3_THRESHOLDS.items():
        raw = getattr(snapshot, name)
        if raw is not None:
            candidates.append((name, max(0.0, float(raw)) / threshold * 100.0))
    if not candidates:
        return RiskResult(0.0, "detection_unavailable", False)
    reason, value = max(candidates, key=lambda item: item[1])
    return RiskResult(min(100.0, value), reason, True)


def warning_level(snapshot: SensorSnapshot) -> int:
    values = (
        (snapshot.eye_closed_seconds, 20.0, 45.0, 90.0),
        (snapshot.head_down_seconds, 300.0, 600.0, 1200.0),
        (snapshot.face_missing_seconds, 600.0, 900.0, 1200.0),
    )
    level = 0
    for raw, lv1, lv2, lv3 in values:
        if raw is None:
            continue
        level = max(level, 3 if raw >= lv3 else 2 if raw >= lv2 else 1 if raw >= lv1 else 0)
    return level
