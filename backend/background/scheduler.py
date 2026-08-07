"""Lifecycle boundary for the local notification scheduler.

Notification generation remains request-scoped and local-only, preserving existing
behaviour while keeping any future timed runner separate from HTTP routing.
"""
from __future__ import annotations


class LocalNotificationScheduler:
    """A deliberately inert lifecycle object; it performs no external delivery."""

    def __init__(self) -> None:
        self.running = False

    def start(self) -> None:
        self.running = True

    def stop(self) -> None:
        self.running = False
