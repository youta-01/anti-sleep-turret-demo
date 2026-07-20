from __future__ import annotations

from collections.abc import Callable

from .models import InterventionSource, SensorSnapshot
from .state_machine import AstDemo


def monitoring(app: AstDemo) -> None:
    app.monitor(SensorSnapshot())


def eye_lv1(app: AstDemo) -> None:
    app.monitor(SensorSnapshot(eye_closed_seconds=20))


def eye_lv2(app: AstDemo) -> None:
    app.monitor(SensorSnapshot(eye_closed_seconds=45))


def direct_lv3(app: AstDemo) -> None:
    app.monitor(SensorSnapshot(eye_closed_seconds=90))


def risk_episode(app: AstDemo) -> None:
    app.monitor(SensorSnapshot(eye_closed_seconds=45))


def three_risk_episodes(app: AstDemo) -> None:
    for _ in range(3):
        app.monitor(SensorSnapshot(eye_closed_seconds=45))
        app.monitor(SensorSnapshot())
        app.clock.advance(15)
        app.monitor(SensorSnapshot())


def successful_forced_bath(app: AstDemo) -> None:
    app.require_bath(InterventionSource.SLEEP_DETECTION, "scenario")
    app.start_qr()
    app.clock.advance(8 * 60)
    app.complete_qr()


def too_early(app: AstDemo) -> None:
    app.require_bath(InterventionSource.SLEEP_DETECTION, "scenario")
    app.start_qr()
    app.clock.advance(60)
    app.complete_qr()


def presence_reset(app: AstDemo) -> None:
    app.require_bath(InterventionSource.SLEEP_DETECTION, "scenario")
    app.start_qr()
    app.clock.advance(16)
    app.presence(face_visible=True)


def manual_bath(app: AstDemo) -> None:
    app.start_manual_bath()
    app.clock.advance(5 * 60)
    app.complete_qr()


def riz_continuity(app: AstDemo) -> None:
    app.phone_start_riz()
    app.start_qr()
    app.charger(True)
    app.clock.advance(3)
    app.charger(True)
    app.clock.advance(8 * 60)
    app.complete_qr()
    app.clock.advance(10)
    app.tick()


def exam_mode(app: AstDemo) -> None:
    app.start_exam()


def emergency_end(app: AstDemo) -> None:
    app.start_emergency()
    app.end_emergency()


SCENARIOS: dict[str, Callable[[AstDemo], None]] = {
    "monitoring": monitoring,
    "eye-lv1": eye_lv1,
    "eye-lv2": eye_lv2,
    "direct-lv3": direct_lv3,
    "risk-episode": risk_episode,
    "repeated-risk": three_risk_episodes,
    "successful-bath": successful_forced_bath,
    "too-early": too_early,
    "presence-reset": presence_reset,
    "manual-bath": manual_bath,
    "riz-continuity": riz_continuity,
    "exam-mode": exam_mode,
    "emergency-end": emergency_end,
}
