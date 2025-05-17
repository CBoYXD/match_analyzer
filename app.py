"""Main Streamlit application."""

from __future__ import annotations

import logging

import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from src.config.settings import (
    LEAGUES,
    API_REFRESH_INTERVAL,
    DEFAULT_TEAM,
    DEFAULT_MATCH_LIMIT,
)
from src.api.football_api import FootballAPIClient
from src.models.team_stats import TeamStats
from src.services.team_service import TeamService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Main application entry point."""
    st.set_page_config(
        page_title="Football Team Analytics", page_icon="⚽", layout="wide"
    )
    st.title("⚽ Football Team Analytics")

    # Auto-refresh page every 10 minutes
    st_autorefresh(interval=API_REFRESH_INTERVAL, key="keep_alive")

    # Initialize API client and services
    api_client = FootballAPIClient(st.secrets["football_api_key"])
    team_service = TeamService(api_client)

    # League and team selection
    league = st.selectbox("Вибери лігу", list(LEAGUES.keys()))
    teams_dict = api_client.get_teams(LEAGUES[league])

    default_index = (
        list(teams_dict.keys()).index(DEFAULT_TEAM) if DEFAULT_TEAM in teams_dict else 0
    )
    team_name = st.selectbox(
        "Вибери команду", list(teams_dict.keys()), index=default_index
    )

    if st.button("🔍 Показати статистику команди"):
        logger.info(f"User requested analysis for {team_name}")
        team_id = teams_dict.get(team_name, {}).get("id")

        if not team_id:
            st.error("Команду не знайдено.")
            logger.error(f"Team ID not found for {team_name}")
            return

        st.header(f"Статистика команди: {team_name} ({league})")
        st.markdown("---")

        # Get team matches
        matches = api_client.get_team_matches(team_id, DEFAULT_MATCH_LIMIT)
        matches = sorted(matches, key=lambda m: m["utcDate"], reverse=True)

        if not matches:
            st.info("Матчів для цієї команди не знайдено.")
            return

        # Calculate and display statistics
        stats = TeamStats.from_matches(matches, team_id)

        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Перемоги", stats.wins)
        with col2:
            st.metric("Нічиї", stats.draws)
        with col3:
            st.metric("Поразки", stats.losses)
        with col4:
            st.metric("Всього матчів", stats.total_matches)

        # Display goals chart
        st.subheader("🥅 Голи")
        goals_df = pd.DataFrame(
            {
                "Показник": ["Забито", "Пропущено"],
                "Кількість": [stats.goals_scored, stats.goals_conceded],
            }
        )
        st.bar_chart(goals_df.set_index("Показник"))

        # Display matches table
        st.subheader("📅 Останні матчі")
        matches_df = team_service.get_team_matches_dataframe(matches, team_id)
        st.dataframe(matches_df)

        # Download button
        csv = matches_df.to_csv(index=False, sep=",", encoding="utf-8-sig").encode(
            "utf-8-sig"
        )
        st.download_button(
            label="⬇️ Завантажити статистику (CSV)",
            data=csv,
            file_name=f"{team_name}_matches.csv",
            mime="text/csv",
        )

        st.markdown("---")


if __name__ == "__main__":
    main()
