"""
VibeFlow Stadium - Configuration Constants.

This module centralizes all application constants, model parameters,
and threshold values used across the application.
"""

# --- Application Info ---
APP_TITLE: str = "VibeFlow // Stadium Command"
APP_ICON: str = "🏟️"
APP_VERSION: str = "1.0.0"

# --- AI Model Configuration ---
GEMINI_MODEL: str = "gemini-2.5-flash"
GENERATION_TEMPERATURE: float = 0.2
GENERATION_MAX_TOKENS: int = 256
GENERATION_TOP_P: float = 0.8

# --- Stadium Data Simulation Bounds ---
GATE_OCCUPANCY_MIN: int = 10
GATE_OCCUPANCY_MAX: int = 95
CONCESSION_WAIT_MIN: int = 2
CONCESSION_WAIT_MAX: int = 25
GATE_NAMES: list[str] = ["North Gate", "South Gate", "East Gate", "West Gate"]
CONCESSION_NAMES: list[str] = ["The Grill", "Sushi Bar", "Vegan Eats"]

# --- Status Thresholds ---
GATE_CRITICAL_THRESHOLD: int = 80
GATE_WARNING_THRESHOLD: int = 50
CONCESSION_CRITICAL_THRESHOLD: int = 20
CONCESSION_WARNING_THRESHOLD: int = 10

# --- Color Palette ---
COLOR_OPTIMAL: str = "#ff6f00"
COLOR_WARNING: str = "#faca2b"
COLOR_CRITICAL: str = "#ff4b4b"

# --- Prompt Injection Blacklist ---
PROMPT_INJECTION_BLACKLIST: list[str] = [
    "ignore previous",
    "system prompt",
    "bypass",
    "instruction override",
    "disregard",
    "forget your instructions",
]
