import streamlit as st
from streamlit_autorefresh import st_autorefresh
import httpx
import pandas as pd
import logging

# Автоматичне оновлення сторінки кожні 10 хвилин (600000 мс)
st.set_page_config(page_title="Football Team Analytics", page_icon="⚽", layout="wide")
st.title("⚽ Football Team Analytics")

st_autorefresh(interval=600000, key="keep_alive")

# 🔐 Використовуємо ключ із secrets
headers = {"X-Auth-Token": st.secrets["football_api_key"]}

# Налаштування логування у файл та консоль
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("main")

# Словник з топ-5 лігами
LEAGUES = {
    "Premier League": "PL",
    "La Liga": "PD",
    "Bundesliga": "BL1",
    "Serie A": "SA",
    "Ligue 1": "FL1",
}


# Функція для отримання команд з ліги
@st.cache_data
def fetch_teams(competition_code):
    logger.info(f"Запит команд для ліги: {competition_code}")
    url = f"https://api.football-data.org/v4/competitions/{competition_code}/teams"
    response = httpx.get(url, headers=headers)
    if response.status_code == 200:
        teams = response.json().get("teams", [])
        logger.info(f"Отримано {len(teams)} команд")
        return {
            team["name"]: {"id": team["id"], "league": competition_code}
            for team in teams
        }
    else:
        logger.error(f"Error fetching teams: {response.status_code}")
        return {}


# Функція для отримання останніх матчів команди
def fetch_team_last_matches(team_id, limit=10):
    logger.info(f"Запит останніх {limit} матчів для команди {team_id}")
    url = f"https://api.football-data.org/v4/teams/{team_id}/matches?status=FINISHED&limit={limit}"
    response = httpx.get(url, headers=headers)
    if response.status_code == 200:
        logger.info(
            f"Отримано {len(response.json().get('matches', []))} матчів для команди {team_id}"
        )
        return response.json().get("matches", [])
    else:
        logger.error(
            f"Error fetching matches for team {team_id}: {response.status_code}"
        )
        return []


# Функція для підрахунку статистики матчів
def calculate_team_stats(matches, team_id):
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

    return {
        "wins": wins,
        "draws": draws,
        "losses": losses,
        "goals_scored": goals_scored,
        "goals_conceded": goals_conceded,
        "total_matches": len(matches),
    }


# Вибір ліги та команди
league = st.selectbox("Вибери лігу", list(LEAGUES.keys()))
teams_dict = fetch_teams(LEAGUES[league])
team_name = st.selectbox(
    "Вибери команду",
    list(teams_dict.keys()),
    index=list(teams_dict.keys()).index("Real Madrid")
    if "Real Madrid" in teams_dict
    else 0,
)

if st.button("🔍 Показати статистику команди"):
    logger.info(f"Користувач натиснув кнопку аналізу для {team_name}")
    team_id = teams_dict.get(team_name, {}).get("id")

    if team_id:
        st.header(f"Статистика команди: {team_name} ({league})")
        st.markdown("---")

        # Отримуємо останні матчі
        matches = fetch_team_last_matches(team_id)

        if matches:
            # Сортуємо матчі від найновішого до найстарішого
            matches = sorted(matches, key=lambda m: m["utcDate"], reverse=True)

            # Розраховуємо статистику
            stats = calculate_team_stats(matches, team_id)

            # Відображаємо загальну статистику
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Перемоги", stats["wins"])
            with col2:
                st.metric("Нічиї", stats["draws"])
            with col3:
                st.metric("Поразки", stats["losses"])
            with col4:
                st.metric("Всього матчів", stats["total_matches"])

            # Відображаємо статистику голів
            st.subheader("🥅 Голи")
            goals_df = pd.DataFrame(
                {
                    "Показник": ["Забито", "Пропущено"],
                    "Кількість": [stats["goals_scored"], stats["goals_conceded"]],
                }
            )
            st.bar_chart(goals_df.set_index("Показник"))

            # Відображаємо історію матчів
            st.subheader("📅 Останні матчі")
            matches_data = [
                {
                    "№": idx + 1,
                    "Дата": m["utcDate"][:10],
                    "Турнір": m["competition"]["name"],
                    "Господарі": m["homeTeam"]["name"],
                    "Гості": m["awayTeam"]["name"],
                    "Рахунок": f"{m['score']['fullTime']['home']}-{m['score']['fullTime']['away']}",
                    "Результат": "Нічия"
                    if m["score"]["winner"] == "DRAW"
                    else "Перемога"
                    if (
                        m["homeTeam"]["id"] == team_id
                        and m["score"]["winner"] == "HOME_TEAM"
                    )
                    or (
                        m["awayTeam"]["id"] == team_id
                        and m["score"]["winner"] == "AWAY_TEAM"
                    )
                    else "Поразка",
                }
                for idx, m in enumerate(matches)
            ]
            matches_df = pd.DataFrame(
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
            st.dataframe(matches_df)

            # Додаємо кнопку для завантаження CSV
            csv = matches_df.to_csv(index=False, sep=",", encoding="utf-8-sig").encode(
                "utf-8-sig"
            )
            st.download_button(
                label="⬇️ Завантажити статистику (CSV)",
                data=csv,
                file_name=f"{team_name}_matches.csv",
                mime="text/csv",
            )

        else:
            st.info("Матчів для цієї команди не знайдено.")

        st.markdown("---")
    else:
        st.error("Команду не знайдено.")
        logger.error(f"Не знайдено ID для {team_name}")
