from ast_demo.risk_episode_guard import RiskEpisodeGuard


def rearm(guard, now):
    guard.update(0, now)
    guard.update(0, now + 15)


def test_first_episode_is_recorded():
    guard = RiskEpisodeGuard()
    assert not guard.update(50, 0)
    assert guard.episodes == [0]


def test_continuous_high_does_not_double_count():
    guard = RiskEpisodeGuard()
    guard.update(50, 0)
    guard.update(80, 10)
    assert len(guard.episodes) == 1


def test_above_rearm_threshold_does_not_start_timer():
    guard = RiskEpisodeGuard()
    guard.update(50, 0)
    guard.update(36, 1)
    assert guard.rearm_since is None


def test_rearm_threshold_is_inclusive():
    guard = RiskEpisodeGuard()
    guard.update(50, 0)
    guard.update(35, 1)
    assert guard.rearm_since == 1


def test_stable_rearm_time_required():
    guard = RiskEpisodeGuard()
    guard.update(50, 0)
    guard.update(0, 1)
    guard.update(0, 15.9)
    assert not guard.armed
    guard.update(0, 16)
    assert guard.armed


def test_rearm_timer_resets_when_risk_rises():
    guard = RiskEpisodeGuard()
    guard.update(50, 0)
    guard.update(0, 1)
    guard.update(40, 5)
    assert guard.rearm_since is None


def test_old_events_expire():
    guard = RiskEpisodeGuard()
    guard.update(50, 0)
    rearm(guard, 1)
    guard.update(50, 3601)
    assert guard.episodes == [3601]


def test_third_episode_escalates():
    guard = RiskEpisodeGuard()
    assert not guard.update(50, 0)
    rearm(guard, 1)
    assert not guard.update(50, 20)
    rearm(guard, 21)
    assert guard.update(50, 40)


def test_rearm_countdown():
    guard = RiskEpisodeGuard()
    guard.update(50, 0)
    guard.update(0, 5)
    assert guard.rearm_remaining(10) == 10
