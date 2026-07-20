from __future__ import annotations

from collections.abc import Callable

from .bath_flow import FORCED_BATH, MANUAL_BATH, POST_COMPLETION_GRACE_SECONDS, PRESENCE_GRACE_SECONDS, BathPolicy, completion_result
from .models import FakeClock, InterventionSource, SensorSnapshot, State, Status, Transition
from .risk_engine import calculate_risk, warning_level
from .risk_episode_guard import RiskEpisodeGuard
from .riz_flow import CHARGER_START_STABLE_SECONDS, COMPLETION_HOLD_SECONDS


class AstDemo:
    def __init__(self, clock: FakeClock | None = None) -> None:
        self.clock = clock or FakeClock()
        self.status = Status()
        self.sensors = SensorSnapshot()
        self.guard = RiskEpisodeGuard()
        self.call_uses: list[float] = []

    def _transition(self, state: State, reason: str) -> None:
        old = self.status.state
        self.status.state = state
        self.status.history.append(Transition(self.clock.now(), old, state, reason))

    def reset(self) -> None:
        self.status = Status()
        self.sensors = SensorSnapshot()
        self.guard = RiskEpisodeGuard()
        self.call_uses = []

    def monitor(self, snapshot: SensorSnapshot) -> State:
        self.sensors = snapshot
        result = calculate_risk(snapshot)
        self.status.risk, self.status.risk_reason = result.value, result.reason
        if self.status.state == State.EXAM_MODE or self.clock.now() < self.status.grace_until:
            return self.status.state
        if self.guard.update(result.value, self.clock.now()):
            self.require_bath(InterventionSource.REPEATED_RISK, "three risk episodes")
            return self.status.state
        level = warning_level(snapshot)
        if level >= 3:
            self.require_bath(InterventionSource.SLEEP_DETECTION, "Lv3 threshold")
        elif level == 2:
            self._transition(State.LV2_WARNING, "Lv2 threshold")
        elif level == 1:
            self._transition(State.LV1_WARNING, "Lv1 threshold")
        elif self.status.state in {State.LV1_WARNING, State.LV2_WARNING}:
            self._transition(State.MONITORING, "signals cleared")
        return self.status.state

    def require_bath(self, source: InterventionSource, reason: str) -> None:
        self.status.intervention_source = source
        self.status.riz_active = source == InterventionSource.RIZ
        self.status.bath_started_at = None
        self.status.start_qr_seen = False
        self.status.completion_scanned_at = None
        self._transition(State.BATH_REQUIRED, reason)

    def phone_start_riz(self) -> None:
        self.require_bath(InterventionSource.RIZ, "Riz phone start")

    def start_qr(self) -> bool:
        if self.status.state not in {State.BATH_REQUIRED, State.BATH_TIMEOUT}:
            return False
        self.status.start_qr_seen = True
        if not self.status.riz_active:
            self._start_bath()
        return True

    def _start_bath(self) -> None:
        self.status.bath_started_at = self.clock.now()
        self.status.completion_scanned_at = None
        self._transition(State.BATH_STARTED, "bath started")

    def start_manual_bath(self) -> bool:
        if self.status.state != State.MONITORING:
            return False
        self.status.intervention_source = InterventionSource.MANUAL
        self.status.riz_active = False
        self.status.start_qr_seen = False
        self._start_bath()
        return True

    def charger(self, connected: bool) -> None:
        if not self.status.riz_active:
            return
        now = self.clock.now()
        if not connected:
            self._invalidate_bath("charger disconnected")
            return
        if self.status.charger_connected_since is None:
            self.status.charger_connected_since = now
        if self.status.state == State.BATH_REQUIRED and self.status.start_qr_seen and now - self.status.charger_connected_since >= CHARGER_START_STABLE_SECONDS:
            self._start_bath()

    def presence(self, face_visible: bool = False, sufficient_motion: bool = False) -> bool:
        if self.status.state != State.BATH_STARTED or self.status.intervention_source == InterventionSource.MANUAL:
            return False
        started = self.status.bath_started_at
        if started is None or self.clock.now() - started <= PRESENCE_GRACE_SECONDS:
            return False
        if face_visible or sufficient_motion:
            self._invalidate_bath("presence guard")
            return True
        return False

    def _invalidate_bath(self, reason: str) -> None:
        self.status.bath_started_at = None
        self.status.start_qr_seen = False
        self.status.charger_connected_since = None
        self.status.completion_scanned_at = None
        self._transition(State.BATH_REQUIRED, reason)

    def complete_qr(self) -> str:
        if self.status.state != State.BATH_STARTED or self.status.bath_started_at is None:
            return "bad_state"
        policy = MANUAL_BATH if self.status.intervention_source == InterventionSource.MANUAL else FORCED_BATH
        result = completion_result(self.clock.now() - self.status.bath_started_at, policy)
        if result == "timeout":
            self.status.start_qr_seen = False
            self._transition(State.BATH_TIMEOUT, "bath timeout")
        elif result == "complete" and self.status.riz_active:
            self.status.completion_scanned_at = self.clock.now()
            result = "hold"
        elif result == "complete":
            self._finish_bath()
        return result

    def tick(self) -> None:
        now = self.clock.now()
        if self.status.state == State.BATH_STARTED and self.status.bath_started_at is not None:
            policy = MANUAL_BATH if self.status.intervention_source == InterventionSource.MANUAL else FORCED_BATH
            if now - self.status.bath_started_at > policy.maximum_seconds:
                self.status.start_qr_seen = False
                self._transition(State.BATH_TIMEOUT, "bath timeout")
        if self.status.riz_active and self.status.completion_scanned_at is not None:
            if self.status.charger_connected_since is not None and now - self.status.completion_scanned_at >= COMPLETION_HOLD_SECONDS:
                self._finish_bath()
        if self.status.state == State.DAILY_REST_MODE and self.status.mode_ends_at is not None and now >= self.status.mode_ends_at:
            self._transition(State.MONITORING, "daily rest ended")

    def _finish_bath(self) -> None:
        self.status.grace_until = self.clock.now() + POST_COMPLETION_GRACE_SECONDS
        self.status.riz_active = False
        self.status.bath_started_at = None
        self.status.completion_scanned_at = None
        self.status.charger_connected_since = None
        self.status.intervention_source = InterventionSource.NONE
        self._transition(State.MONITORING, "bath complete")

    def start_daily_rest(self) -> bool:
        if self.status.daily_rest_used or self.status.state != State.MONITORING:
            return False
        self.status.daily_rest_used = True
        self.status.mode_ends_at = self.clock.now() + 30 * 60
        self._transition(State.DAILY_REST_MODE, "daily rest")
        return True

    def start_exam(self) -> bool:
        if self.status.riz_active:
            return False
        self._transition(State.EXAM_MODE, "exam mode")
        return True

    def end_exam(self) -> bool:
        if self.status.state != State.EXAM_MODE:
            return False
        self.status.grace_until = self.clock.now() + 180
        self._transition(State.MONITORING, "exam ended")
        return True

    def start_emergency(self) -> None:
        self.status.riz_active = False
        self._transition(State.EMERGENCY_SAFE_MODE, "emergency safe mode")

    def end_emergency(self) -> bool:
        if self.status.state != State.EMERGENCY_SAFE_MODE:
            return False
        self.require_bath(InterventionSource.EMERGENCY_END, "emergency ended")
        return True

    def start_call_safe_mode(self) -> bool:
        now = self.clock.now()
        self.call_uses[:] = [value for value in self.call_uses if now - value <= 3 * 3600]
        self.call_uses.append(now)
        if len(self.call_uses) >= 4:
            self.require_bath(InterventionSource.CALL_OVERUSE, "four calls in three hours")
            return False
        self._transition(State.SAFE_MODE, "call safe mode")
        return True

    def end_safe_mode(self) -> bool:
        if self.status.state != State.SAFE_MODE:
            return False
        self._transition(State.MONITORING, "safe mode ended")
        return True
