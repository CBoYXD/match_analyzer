"""Team statistics model."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


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
    def from_matches(cls, matches: list[dict[str, Any]], team_id: int) -> TeamStats:
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

            match match["score"]["winner"]:
                case "DRAW":
                    draws += 1
                case "HOME_TEAM" if is_home:
                    wins += 1
                case "AWAY_TEAM" if not is_home:
                    wins += 1
                case _:
                    losses += 1

        return cls(
            wins=wins,
            draws=draws,
            losses=losses,
            goals_scored=goals_scored,
            goals_conceded=goals_conceded,
            total_matches=len(matches),
        )
