import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

# 2.3 - See which players have scored the most goals across multiple World Cups
# 2.4 - Compare team performance across different stages (group vs knockout)

st.title('🥇 Top Scorers')
st.write('Identify the most consistent goal scorers across World Cup history.')
st.write('---')

API_BASE = 'http://web-api:4000'

try:
    # ---- Top Scorers ----
    events_resp = requests.get(f'{API_BASE}/match-events', params={'event_type': 'goal'})
    events_resp.raise_for_status()
    goals = events_resp.json()

    if goals:
        df = pd.DataFrame(goals)

        # Count goals per player
        scorer_counts = df.groupby('player_name').agg(
            total_goals=('event_id', 'count'),
            team=('team_name', 'first'),
            tournaments=('year', 'nunique')
        ).reset_index().sort_values('total_goals', ascending=False)

        st.write(f'### All-Time Goal Rankings')
        st.dataframe(scorer_counts, use_container_width=True, hide_index=True)

        # ---- Bar chart of top 10 ----
        st.write('---')
        st.write('### Top 10 Scorers')
        top10 = scorer_counts.head(10).set_index('player_name')
        st.bar_chart(top10['total_goals'])

    else:
        st.info('No goal data found.')

    # ---- Team Performance by Stage ----
    st.write('---')
    st.write('### Team Performance by Stage')

    teams_resp = requests.get(f'{API_BASE}/teams')
    teams_resp.raise_for_status()
    teams_list = teams_resp.json()

    team_names = [t['team_name'] for t in teams_list]
    selected_team = st.selectbox('Select a team', team_names)
    team_obj = next(t for t in teams_list if t['team_name'] == selected_team)

    matches_resp = requests.get(f'{API_BASE}/matches', params={'team_id': team_obj['team_id']})
    matches_resp.raise_for_status()
    matches = matches_resp.json()

    if matches:
        matches_df = pd.DataFrame(matches)
        if 'stage' in matches_df.columns:
            stage_summary = matches_df.groupby('stage').agg(
                matches_played=('match_id', 'count'),
            ).reset_index()
            st.dataframe(stage_summary, use_container_width=True, hide_index=True)
    else:
        st.info('No match data found for this team.')

except requests.exceptions.RequestException as e:
    st.error(f'Error connecting to the API: {e}')
    st.info('Make sure the API server is running.')
