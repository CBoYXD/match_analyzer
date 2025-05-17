"""Team service implementation."""

import pandas as pd
from typing import Dict, List, Optional

from ..api.football_api import FootballAPIClient
from ..models.team_stats import TeamStats


class TeamService:
    def __init__(self, api_client: FootballAPIClient):
        self.api_client = api_client

    def get_team_matches_dataframe(
        self, matches: List[Dict], team_id: int
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

    def _get_match_result(self, match: Dict, team_id: int) -> str:
        """Determine match result for the team."""
        if match["score"]["winner"] == "DRAW":
            return "Нічия"
        elif (
            match["homeTeam"]["id"] == team_id
            and match["score"]["winner"] == "HOME_TEAM"
        ) or (
            match["awayTeam"]["id"] == team_id
            and match["score"]["winner"] == "AWAY_TEAM"
        ):
            return "Перемога"
        return "Поразка"
