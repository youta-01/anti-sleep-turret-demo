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
