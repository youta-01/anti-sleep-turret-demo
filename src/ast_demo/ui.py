from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from .scenarios import SCENARIOS
from .state_machine import AstDemo

COLORS = {
    "MONITORING": "#102a43",
    "LV1_WARNING": "#334e68",
    "LV2_WARNING": "#b7791f",
    "BATH_REQUIRED": "#9b2c2c",
    "BATH_STARTED": "#9b2c2c",
    "BATH_TIMEOUT": "#742a2a",
    "EXAM_MODE": "#4a5568",
}

CONTROLS = [
    ("Monitoring", "monitoring"),
    ("Eye Closure to Lv1", "eye-lv1"),
    ("Eye Closure to Lv2", "eye-lv2"),
    ("Direct Lv3", "direct-lv3"),
    ("Risk 50 Episode", "risk-episode"),
    ("Three Risk Episodes", "repeated-risk"),
    ("Successful Forced Bath", "successful-bath"),
    ("Too-Early Complete", "too-early"),
    ("Presence Guard Reset", "presence-reset"),
    ("Manual Bath", "manual-bath"),
    ("Riz Continuity", "riz-continuity"),
    ("Exam Mode", "exam-mode"),
    ("Emergency End", "emergency-end"),
]


class DemoWindow:
    def __init__(self, root: tk.Tk, initial: str) -> None:
        self.root = root
        self.app = AstDemo()
        root.title("Anti-Sleep Turret — Public Portfolio Demo")
        root.geometry("1100x720")
        self.header = tk.Frame(root, padx=20, pady=16)
        self.header.pack(fill="x")
        self.state_label = tk.Label(self.header, font=("Segoe UI", 26, "bold"), fg="white")
        self.state_label.pack(anchor="w")
        self.summary = tk.Label(self.header, font=("Segoe UI", 11), fg="white", justify="left")
        self.summary.pack(anchor="w", pady=(8, 0))

        body = ttk.Frame(root, padding=14)
        body.pack(fill="both", expand=True)
        controls = ttk.LabelFrame(body, text="合成シナリオ", padding=10)
        controls.pack(side="left", fill="y", padx=(0, 12))
        ttk.Label(
            controls,
            text="各シナリオは初期状態から実行します",
            justify="left",
            wraplength=220,
        ).pack(fill="x", pady=(0, 8))
        for text, scenario in CONTROLS:
            ttk.Button(controls, text=text, command=lambda name=scenario: self.run(name)).pack(fill="x", pady=2)
        ttk.Button(controls, text="Reset", command=self.reset).pack(fill="x", pady=(12, 2))

        details = ttk.Frame(body)
        details.pack(side="left", fill="both", expand=True)
        self.sensor_label = ttk.Label(details, font=("Consolas", 11), justify="left")
        self.sensor_label.pack(anchor="w")
        ttk.Label(details, text="Transition history", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(18, 4))
        self.history = tk.Listbox(details, font=("Consolas", 10), height=22)
        self.history.pack(fill="both", expand=True)
        self.run(initial)

    def run(self, name: str) -> None:
        # Scenario buttons are demonstrations, not incremental controls.
        # Starting each one from a clean state keeps the UI consistent with
        # the deterministic headless runner and avoids order-dependent results.
        self.app.reset()
        SCENARIOS[name](self.app)
        self.refresh()

    def reset(self) -> None:
        self.app.reset()
        self.refresh()

    def refresh(self) -> None:
        status = self.app.status
        color = "#c05621" if status.riz_active else COLORS.get(status.state.value, "#2d3748")
        self.header.configure(bg=color)
        self.state_label.configure(text=status.state.value, bg=color)
        self.summary.configure(
            text=(f"Sleep Risk: {status.risk:.1f} / 100    reason: {status.risk_reason}\n"
                  f"Risk 50 episodes: {len(self.app.guard.episodes)}    rearm: {self.app.guard.rearm_remaining(self.app.clock.now()):.1f}s    "
                  f"source: {status.intervention_source.value}"),
            bg=color,
        )
        sensors = self.app.sensors
        self.sensor_label.configure(text=(
            "Synthetic sensors\n"
            f"  eye_closed_seconds   = {sensors.eye_closed_seconds}\n"
            f"  head_down_seconds    = {sensors.head_down_seconds}\n"
            f"  face_missing_seconds = {sensors.face_missing_seconds}\n"
            f"  riz_active           = {status.riz_active}"
        ))
        self.history.delete(0, tk.END)
        for item in status.history:
            self.history.insert(tk.END, f"{item.at:7.1f}s  {item.old.value:20} -> {item.new.value:20}  {item.reason}")


def launch(initial: str = "monitoring") -> None:
    root = tk.Tk()
    DemoWindow(root, initial)
    root.mainloop()
