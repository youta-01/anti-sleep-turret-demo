from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class State(str, Enum):
    MONITORING = "MONITORING"
    LV1_WARNING = "LV1_WARNING"
    LV2_WARNING = "LV2_WARNING"
    BATH_REQUIRED = "BATH_REQUIRED"
    BATH_STARTED = "BATH_STARTED"
    BATH_TIMEOUT = "BATH_TIMEOUT"
    SAFE_MODE = "SAFE_MODE"
    DAILY_REST_MODE = "DAILY_REST_MODE"
    EXAM_MODE = "EXAM_MODE"
    EMERGENCY_SAFE_MODE = "EMERGENCY_SAFE_MODE"


class InterventionSource(str, Enum):
    NONE = "NONE"
    SLEEP_DETECTION = "SLEEP_DETECTION"
    REPEATED_RISK = "REPEATED_RISK"
    MANUAL = "MANUAL"
    RIZ = "RIZ"
    CALL_OVERUSE = "CALL_OVERUSE"
    EMERGENCY_END = "EMERGENCY_END"


@dataclass(slots=True)
class SensorSnapshot:
    eye_closed_seconds: float | None = 0.0
    head_down_seconds: float | None = 0.0
    face_missing_seconds: float | None = 0.0


@dataclass(slots=True)
class RiskResult:
    value: float
    reason: str
    available: bool


@dataclass(slots=True)
class Transition:
    at: float
    old: State
    new: State
    reason: str


@dataclass(slots=True)
class Status:
    state: State = State.MONITORING
    risk: float = 0.0
    risk_reason: str = "none"
    intervention_source: InterventionSource = InterventionSource.NONE
    riz_active: bool = False
    bath_started_at: float | None = None
    start_qr_seen: bool = False
    charger_connected_since: float | None = None
    completion_scanned_at: float | None = None
    grace_until: float = 0.0
    daily_rest_used: bool = False
    mode_ends_at: float | None = None
    history: list[Transition] = field(default_factory=list)


@dataclass(slots=True)
class FakeClock:
    current: float = 0.0

    def now(self) -> float:
        return self.current

    def advance(self, seconds: float) -> float:
        if seconds < 0:
            raise ValueError("time cannot move backwards")
        self.current += seconds
        return self.current
