"""Configuration settings for the Football Analytics application."""

# API Configuration
API_BASE_URL = "https://api.football-data.org/v4"
API_REFRESH_INTERVAL = 600000  # 10 minutes in milliseconds

# League Configuration
LEAGUES = {
    "Premier League": "PL",
    "La Liga": "PD",
    "Bundesliga": "BL1",
    "Serie A": "SA",
    "Ligue 1": "FL1",
}

# Application Settings
DEFAULT_MATCH_LIMIT = 10
DEFAULT_TEAM = "Real Madrid"
