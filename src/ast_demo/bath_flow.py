from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BathPolicy:
    minimum_seconds: float
    maximum_seconds: float
    requires_start_qr: bool = True
    presence_guard: bool = True


FORCED_BATH = BathPolicy(8 * 60, 15 * 60)
MANUAL_BATH = BathPolicy(5 * 60, 45 * 60, requires_start_qr=False, presence_guard=False)
PRESENCE_GRACE_SECONDS = 15.0
POST_COMPLETION_GRACE_SECONDS = 180.0


def completion_result(elapsed: float, policy: BathPolicy) -> str:
    if elapsed < policy.minimum_seconds:
        return "too_early"
    if elapsed > policy.maximum_seconds:
        return "timeout"
    return "complete"
