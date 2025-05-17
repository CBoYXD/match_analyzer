"""Team statistics model."""

from dataclasses import dataclass
from typing import List, Dict


@dataclass
class TeamStats:
    """Team statistics data class."""

    wins: int
    draws: int
    losses: int
    goals_scored: int
    goals_conceded: int
    total_matches: int

    @classmethod
    def from_matches(cls, matches: List[Dict], team_id: int) -> "TeamStats":
        """Create TeamStats instance from match data."""
        wins = 0
        draws = 0
        losses = 0
        goals_scored = 0
        goals_conceded = 0

        for match in matches:
            is_home = match["homeTeam"]["id"] == team_id
            home_goals = match["score"]["fullTime"]["home"]
            away_goals = match["score"]["fullTime"]["away"]

            if is_home:
                goals_scored += home_goals
                goals_conceded += away_goals
            else:
                goals_scored += away_goals
                goals_conceded += home_goals

            if match["score"]["winner"] == "DRAW":
                draws += 1
            elif (is_home and match["score"]["winner"] == "HOME_TEAM") or (
                not is_home and match["score"]["winner"] == "AWAY_TEAM"
            ):
                wins += 1
            else:
                losses += 1

        return cls(
            wins=wins,
            draws=draws,
            losses=losses,
            goals_scored=goals_scored,
            goals_conceded=goals_conceded,
            total_matches=len(matches),
        )
