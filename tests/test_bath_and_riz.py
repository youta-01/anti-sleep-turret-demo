from ast_demo.models import InterventionSource, State
from ast_demo.state_machine import AstDemo
from ast_demo.riz_flow import RIZ_PRESENTATION_COLOR


def forced_app():
    app = AstDemo()
    app.require_bath(InterventionSource.SLEEP_DETECTION, "test")
    return app


def test_forced_bath_requires_start_qr():
    app = forced_app()
    assert app.status.state == State.BATH_REQUIRED
    assert app.start_qr()
    assert app.status.state == State.BATH_STARTED


def test_too_early_completion_rejected():
    app = forced_app(); app.start_qr(); app.clock.advance(479)
    assert app.complete_qr() == "too_early"
    assert app.status.state == State.BATH_STARTED


def test_eight_minutes_completes():
    app = forced_app(); app.start_qr(); app.clock.advance(480)
    assert app.complete_qr() == "complete"
    assert app.status.state == State.MONITORING


def test_fifteen_minutes_completes():
    app = forced_app(); app.start_qr(); app.clock.advance(900)
    assert app.complete_qr() == "complete"


def test_over_fifteen_minutes_times_out():
    app = forced_app(); app.start_qr(); app.clock.advance(901)
    assert app.complete_qr() == "timeout"
    assert app.status.state == State.BATH_TIMEOUT


def test_timeout_requires_new_start_qr():
    app = forced_app(); app.start_qr(); app.clock.advance(901); app.tick()
    assert not app.status.start_qr_seen
    assert app.start_qr()


def test_completion_grants_three_minute_grace():
    app = forced_app(); app.start_qr(); app.clock.advance(480); app.complete_qr()
    assert app.status.grace_until - app.clock.now() == 180


def test_presence_guard_has_start_grace():
    app = forced_app(); app.start_qr(); app.clock.advance(15)
    assert not app.presence(face_visible=True)


def test_presence_guard_resets_after_grace():
    app = forced_app(); app.start_qr(); app.clock.advance(16)
    assert app.presence(sufficient_motion=True)
    assert app.status.state == State.BATH_REQUIRED
    assert not app.status.start_qr_seen


def test_manual_bath_starts_without_qr():
    app = AstDemo()
    assert app.start_manual_bath()
    assert app.status.state == State.BATH_STARTED
    assert not app.status.start_qr_seen


def test_manual_bath_five_minimum():
    app = AstDemo(); app.start_manual_bath(); app.clock.advance(300)
    assert app.complete_qr() == "complete"


def test_manual_bath_before_five_is_early():
    app = AstDemo(); app.start_manual_bath(); app.clock.advance(299)
    assert app.complete_qr() == "too_early"


def test_manual_bath_forty_five_maximum():
    app = AstDemo(); app.start_manual_bath(); app.clock.advance(2700)
    assert app.complete_qr() == "complete"


def test_manual_bath_over_maximum_times_out():
    app = AstDemo(); app.start_manual_bath(); app.clock.advance(2701)
    assert app.complete_qr() == "timeout"


def test_manual_bath_ignores_presence_guard():
    app = AstDemo(); app.start_manual_bath(); app.clock.advance(16)
    assert not app.presence(face_visible=True)


def riz_app():
    app = AstDemo(); app.phone_start_riz(); app.start_qr(); return app


def test_riz_is_context_not_state():
    app = riz_app()
    assert app.status.riz_active
    assert app.status.state == State.BATH_REQUIRED
    assert "RIZ" not in State.__members__


def test_riz_orange_presentation():
    assert RIZ_PRESENTATION_COLOR == "orange"


def test_riz_requires_three_second_charger_stability():
    app = riz_app(); app.charger(True); app.clock.advance(2.9); app.charger(True)
    assert app.status.state == State.BATH_REQUIRED
    app.clock.advance(.1); app.charger(True)
    assert app.status.state == State.BATH_STARTED


def test_riz_disconnect_resets_progress():
    app = riz_app(); app.charger(True); app.clock.advance(3); app.charger(True); app.charger(False)
    assert app.status.state == State.BATH_REQUIRED
    assert not app.status.start_qr_seen


def test_riz_presence_resets_progress():
    app = riz_app(); app.charger(True); app.clock.advance(3); app.charger(True); app.clock.advance(16)
    assert app.presence(face_visible=True)
    assert app.status.state == State.BATH_REQUIRED


def test_riz_completion_requires_hold():
    app = riz_app(); app.charger(True); app.clock.advance(3); app.charger(True); app.clock.advance(480)
    assert app.complete_qr() == "hold"
    app.clock.advance(9); app.tick(); assert app.status.state == State.BATH_STARTED
    app.clock.advance(1); app.tick(); assert app.status.state == State.MONITORING


def test_new_riz_session_does_not_reuse_old_charger_timestamp():
    app = AstDemo(); app.clock.advance(100)
    app.status.charger_connected = True
    app.status.charger_connected_since = 1
    app.status.start_qr_seen = True
    app.status.bath_started_at = 2
    app.status.completion_scanned_at = 3
    app.status.grace_until = 200
    app.phone_start_riz()
    assert not app.status.start_qr_seen
    assert app.status.bath_started_at is None
    assert not app.status.charger_connected
    assert app.status.charger_connected_since is None
    assert app.status.completion_scanned_at is None
    assert app.status.grace_until == 0


def test_start_qr_plus_stale_charger_timestamp_does_not_start_riz_bath():
    app = AstDemo(); app.clock.advance(100)
    app.status.charger_connected = True
    app.status.charger_connected_since = 1
    app.phone_start_riz(); app.start_qr(); app.charger(True)
    assert app.status.state == State.BATH_REQUIRED
    assert app.status.charger_connected_since == 100


def test_charger_reconnect_starts_a_new_stability_interval():
    app = riz_app(); app.charger(True); app.clock.advance(2); app.charger(False)
    assert app.start_qr(); app.clock.advance(100); app.charger(True)
    assert app.status.charger_connected_since == 102
    app.clock.advance(2.9); app.charger(True)
    assert app.status.state == State.BATH_REQUIRED
    app.clock.advance(.1); app.charger(True)
    assert app.status.state == State.BATH_STARTED


def test_riz_completion_requires_current_charger_connection():
    app = riz_app(); app.charger(True); app.clock.advance(3); app.charger(True); app.clock.advance(480)
    assert app.complete_qr() == "hold"
    app.status.charger_connected = False
    app.clock.advance(10); app.tick()
    assert app.status.state == State.BATH_STARTED


def test_emergency_clears_riz_transient_fields():
    app = riz_app(); app.charger(True); app.clock.advance(3); app.charger(True); app.clock.advance(480)
    assert app.complete_qr() == "hold"
    app.start_emergency()
    assert app.status.state == State.EMERGENCY_SAFE_MODE
    assert not app.status.riz_active
    assert not app.status.start_qr_seen
    assert app.status.bath_started_at is None
    assert not app.status.charger_connected
    assert app.status.charger_connected_since is None
    assert app.status.completion_scanned_at is None
    assert app.status.intervention_source == InterventionSource.NONE


def test_manual_bath_timeout_returns_to_monitoring():
    app = AstDemo(); app.start_manual_bath(); app.clock.advance(2701); app.tick()
    assert app.status.state == State.MONITORING
    assert app.status.history[-1].reason == "manual bath timed out"


def test_manual_bath_timeout_cannot_restart_through_start_qr():
    app = AstDemo(); app.start_manual_bath(); app.clock.advance(2701); app.tick()
    assert not app.start_qr()
    assert app.status.state == State.MONITORING


def test_forced_bath_timeout_still_requires_new_start_qr():
    app = forced_app(); app.start_qr(); app.clock.advance(901); app.tick()
    assert app.status.state == State.BATH_TIMEOUT
    assert app.status.bath_started_at is None
    assert not app.status.start_qr_seen
    assert app.start_qr()
    assert app.status.state == State.BATH_STARTED


def test_monitoring_invariants_hold_after_every_successful_completion():
    forced = forced_app(); forced.start_qr(); forced.clock.advance(480); forced.complete_qr()
    manual = AstDemo(); manual.start_manual_bath(); manual.clock.advance(300); manual.complete_qr()
    riz = riz_app(); riz.charger(True); riz.clock.advance(3); riz.charger(True); riz.clock.advance(480)
    riz.complete_qr(); riz.clock.advance(10); riz.tick()

    for app in (forced, manual, riz):
        assert app.status.state == State.MONITORING
        assert not app.status.riz_active
        assert not app.status.start_qr_seen
        assert app.status.bath_started_at is None
        assert not app.status.charger_connected
        assert app.status.charger_connected_since is None
        assert app.status.completion_scanned_at is None
        assert app.status.intervention_source == InterventionSource.NONE
