from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class RiskEpisodeGuard:
    threshold: float = 50.0
    required_occurrences: int = 3
    window_seconds: float = 3600.0
    rearm_below: float = 35.0
    rearm_stable_seconds: float = 15.0
    armed: bool = True
    episodes: list[float] = field(default_factory=list)
    rearm_since: float | None = None

    def update(self, risk: float, now: float) -> bool:
        self.episodes[:] = [event for event in self.episodes if now - event <= self.window_seconds]
        if self.armed and risk >= self.threshold:
            self.episodes.append(now)
            self.armed = False
            self.rearm_since = None
            return len(self.episodes) >= self.required_occurrences
        if not self.armed:
            if risk <= self.rearm_below:
                if self.rearm_since is None:
                    self.rearm_since = now
                elif now - self.rearm_since >= self.rearm_stable_seconds:
                    self.armed = True
                    self.rearm_since = None
            else:
                self.rearm_since = None
        return False

    def rearm_remaining(self, now: float) -> float:
        if self.armed:
            return 0.0
        if self.rearm_since is None:
            return self.rearm_stable_seconds
        return max(0.0, self.rearm_stable_seconds - (now - self.rearm_since))
