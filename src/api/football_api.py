"""Football Data API client implementation."""

from __future__ import annotations

import logging
from typing import Any, TypedDict

import httpx

from ..config.settings import API_BASE_URL

logger = logging.getLogger(__name__)


class TeamInfo(TypedDict):
    """Type definition for team information."""

    id: int
    league: str


class FootballAPIClient:
    """Football Data API client."""

    def __init__(self, api_key: str) -> None:
        """Initialize the API client."""
        self.headers = {"X-Auth-Token": api_key}
        self.base_url = API_BASE_URL

    def get_teams(self, competition_code: str) -> dict[str, TeamInfo]:
        """Fetch teams for a specific competition."""
        logger.info(f"Fetching teams for league: {competition_code}")
        url = f"{self.base_url}/competitions/{competition_code}/teams"

        try:
            response = httpx.get(url, headers=self.headers)
            response.raise_for_status()

            teams = response.json().get("teams", [])
            logger.info(f"Retrieved {len(teams)} teams")
            return {
                team["name"]: {"id": team["id"], "league": competition_code}
                for team in teams
            }
        except httpx.HTTPError as e:
            logger.error(f"Error fetching teams: {e}")
            return {}

    def get_team_matches(self, team_id: int, limit: int = 10) -> list[dict[str, Any]]:
        """Fetch last matches for a specific team."""
        logger.info(f"Fetching last {limit} matches for team {team_id}")
        url = f"{self.base_url}/teams/{team_id}/matches?status=FINISHED&limit={limit}"

        try:
            response = httpx.get(url, headers=self.headers)
            response.raise_for_status()

            matches = response.json().get("matches", [])
            logger.info(f"Retrieved {len(matches)} matches for team {team_id}")
            return matches
        except httpx.HTTPError as e:
            logger.error(f"Error fetching matches for team {team_id}: {e}")
            return []
