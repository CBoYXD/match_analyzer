"""Configuration settings for the Football Analytics application."""

from __future__ import annotations

from typing import Final

# API Configuration
API_BASE_URL: Final[str] = "https://api.football-data.org/v4"
API_REFRESH_INTERVAL: Final[int] = 600000  # 10 minutes in milliseconds

# League Configuration
LEAGUES: Final[dict[str, str]] = {
    "Premier League": "PL",
    "La Liga": "PD",
    "Bundesliga": "BL1",
    "Serie A": "SA",
    "Ligue 1": "FL1",
}

# Application Settings
DEFAULT_MATCH_LIMIT: Final[int] = 10
DEFAULT_TEAM: Final[str] = "Real Madrid"
