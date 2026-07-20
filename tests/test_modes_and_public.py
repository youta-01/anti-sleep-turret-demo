from pathlib import Path

from ast_demo.models import InterventionSource, SensorSnapshot, State
from ast_demo.state_machine import AstDemo


def test_daily_rest_is_thirty_minutes():
    app = AstDemo(); assert app.start_daily_rest(); app.clock.advance(1799); app.tick()
    assert app.status.state == State.DAILY_REST_MODE
    app.clock.advance(1); app.tick(); assert app.status.state == State.MONITORING


def test_daily_rest_once_per_synthetic_day():
    app = AstDemo(); app.start_daily_rest(); app.clock.advance(1800); app.tick()
    assert not app.start_daily_rest()


def test_exam_pauses_detection():
    app = AstDemo(); assert app.start_exam(); app.monitor(SensorSnapshot(eye_closed_seconds=90))
    assert app.status.state == State.EXAM_MODE


def test_exam_cannot_start_during_riz():
    app = AstDemo(); app.phone_start_riz()
    assert not app.start_exam()


def test_exam_end_has_180_second_grace():
    app = AstDemo(); app.start_exam(); app.end_exam()
    assert app.status.state == State.MONITORING
    assert app.status.grace_until == 180


def test_emergency_end_requires_bath():
    app = AstDemo(); app.start_emergency(); assert app.end_emergency()
    assert app.status.state == State.BATH_REQUIRED
    assert app.status.intervention_source == InterventionSource.EMERGENCY_END


def test_fourth_call_within_three_hours_requires_bath():
    app = AstDemo()
    for _ in range(3):
        assert app.start_call_safe_mode(); app.end_safe_mode(); app.clock.advance(1)
    assert not app.start_call_safe_mode()
    assert app.status.intervention_source == InterventionSource.CALL_OVERUSE


def test_old_call_use_expires():
    app = AstDemo(); app.start_call_safe_mode(); app.end_safe_mode(); app.clock.advance(10801)
    for _ in range(3):
        assert app.start_call_safe_mode(); app.end_safe_mode()
    assert app.status.state == State.MONITORING


def test_retired_states_are_absent():
    names = set(State.__members__)
    assert "RETURN_TO_PC" not in names
    assert "RECOVERY_WORK" not in names
    assert "SUCCESS_COOLDOWN" not in names
    assert "BATH_READY" not in names


def test_public_ui_has_no_retired_controls():
    source = (Path(__file__).parents[1] / "src" / "ast_demo" / "ui.py").read_text(encoding="utf-8")
    forbidden = ["Return" + " to PC", "Resume" + " AST", "Hide" + " AST for Recovery"]
    assert all(label not in source for label in forbidden)
