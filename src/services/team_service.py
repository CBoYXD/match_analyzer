"""Team service implementation."""

from __future__ import annotations

from typing import Any, TypedDict

import pandas as pd

from ..api.football_api import FootballAPIClient
from ..models.team_stats import TeamStats


class MatchData(TypedDict):
    """Type definition for match data."""

    utcDate: str
    competition: dict[str, str]
    homeTeam: dict[str, Any]
    awayTeam: dict[str, Any]
    score: dict[str, dict[str, int | None]]


class TeamService:
    """Service for handling team-related operations."""

    def __init__(self, api_client: FootballAPIClient) -> None:
        """Initialize the team service."""
        self.api_client = api_client

    def get_team_matches_dataframe(
        self, matches: list[MatchData], team_id: int
    ) -> pd.DataFrame:
        """Convert matches data to pandas DataFrame."""
        matches_data = [
            {
                "№": idx + 1,
                "Дата": m["utcDate"][:10],
                "Турнір": m["competition"]["name"],
                "Господарі": m["homeTeam"]["name"],
                "Гості": m["awayTeam"]["name"],
                "Рахунок": f"{m['score']['fullTime']['home']}-{m['score']['fullTime']['away']}",
                "Результат": self._get_match_result(m, team_id),
            }
            for idx, m in enumerate(matches)
        ]

        return pd.DataFrame(
            matches_data,
            columns=[
                "№",
                "Дата",
                "Турнір",
                "Господарі",
                "Гості",
                "Рахунок",
                "Результат",
            ],
        )

    def _get_match_result(self, match: MatchData, team_id: int) -> str:
        """Determine match result for the team."""
        is_home = match["homeTeam"]["id"] == team_id

        match match["score"]["winner"]:
            case "DRAW":
                return "Нічия"
            case "HOME_TEAM" if is_home:
                return "Перемога"
            case "AWAY_TEAM" if not is_home:
                return "Перемога"
            case _:
                return "Поразка"
