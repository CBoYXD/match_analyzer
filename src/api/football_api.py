"""Football Data API client implementation."""

import httpx
import logging
from typing import Dict, List, Optional

from ..config.settings import API_BASE_URL

logger = logging.getLogger(__name__)


class FootballAPIClient:
    def __init__(self, api_key: str):
        self.headers = {"X-Auth-Token": api_key}
        self.base_url = API_BASE_URL

    def get_teams(self, competition_code: str) -> Dict:
        """Fetch teams for a specific competition."""
        logger.info(f"Fetching teams for league: {competition_code}")
        url = f"{self.base_url}/competitions/{competition_code}/teams"
        response = httpx.get(url, headers=self.headers)

        if response.status_code == 200:
            teams = response.json().get("teams", [])
            logger.info(f"Retrieved {len(teams)} teams")
            return {
                team["name"]: {"id": team["id"], "league": competition_code}
                for team in teams
            }
        else:
            logger.error(f"Error fetching teams: {response.status_code}")
            return {}

    def get_team_matches(self, team_id: int, limit: int = 10) -> List[Dict]:
        """Fetch last matches for a specific team."""
        logger.info(f"Fetching last {limit} matches for team {team_id}")
        url = f"{self.base_url}/teams/{team_id}/matches?status=FINISHED&limit={limit}"
        response = httpx.get(url, headers=self.headers)

        if response.status_code == 200:
            matches = response.json().get("matches", [])
            logger.info(f"Retrieved {len(matches)} matches for team {team_id}")
            return matches
        else:
            logger.error(
                f"Error fetching matches for team {team_id}: {response.status_code}"
            )
            return []
