import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

# 3.3 - See how Brazil performed against Argentina in the past
# 3.4 - Look up any team's penalty shootout record

st.title('🔁 Match History')
st.write('Explore head-to-head records and match history between teams.')
st.write('---')

API_BASE = 'http://web-api:4000'

try:
    teams_resp = requests.get(f'{API_BASE}/teams')
    teams_resp.raise_for_status()
    teams_list = teams_resp.json()
    team_names = [t['team_name'] for t in teams_list]

    # ---- Head to Head ----
    st.write('### Head-to-Head Comparison')

    col1, col2 = st.columns(2)
    with col1:
        team1_name = st.selectbox('Team 1', team_names, index=0)
    with col2:
        team2_name = st.selectbox('Team 2', team_names, index=min(1, len(team_names) - 1))

    if team1_name == team2_name:
        st.warning('Please select two different teams.')
    else:
        team1 = next(t for t in teams_list if t['team_name'] == team1_name)
        team2 = next(t for t in teams_list if t['team_name'] == team2_name)

        # Get all matches for team1
        matches_resp = requests.get(f'{API_BASE}/matches', params={'team_id': team1['team_id']})
        matches_resp.raise_for_status()
        all_matches = matches_resp.json()

        # Filter to only matches involving both teams
        h2h = [m for m in all_matches
               if (team1_name in [m.get('home_team'), m.get('away_team')] and
                   team2_name in [m.get('home_team'), m.get('away_team')])]

        if h2h:
            team1_wins = 0
            team2_wins = 0
            draws = 0

            for m in h2h:
                home_score = m.get('home_score', 0)
                away_score = m.get('away_score', 0)
                home_team = m.get('home_team', '')

                if home_score == away_score:
                    draws += 1
                elif home_score > away_score:
                    if home_team == team1_name:
                        team1_wins += 1
                    else:
                        team2_wins += 1
                else:
                    if home_team == team1_name:
                        team2_wins += 1
                    else:
                        team1_wins += 1

            col1, col2, col3 = st.columns(3)
            col1.metric(f'{team1_name} Wins', team1_wins)
            col2.metric('Draws', draws)
            col3.metric(f'{team2_name} Wins', team2_wins)

            st.write('---')
            st.write('### Match Details')
            h2h_df = pd.DataFrame(h2h)
            st.dataframe(h2h_df, use_container_width=True, hide_index=True)
        else:
            st.info(f'No head-to-head matches found between {team1_name} and {team2_name}.')

    # ---- Full Match History for a Team ----
    st.write('---')
    st.write('### Full Match History')

    selected_team_name = st.selectbox('Select a team to view all matches', team_names, key='full_hist')
    selected_team = next(t for t in teams_list if t['team_name'] == selected_team_name)

    full_resp = requests.get(f'{API_BASE}/matches', params={'team_id': selected_team['team_id']})
    full_resp.raise_for_status()
    full_matches = full_resp.json()

    if full_matches:
        full_df = pd.DataFrame(full_matches)
        st.write(f'**{len(full_df)} matches found**')
        st.dataframe(full_df, use_container_width=True, hide_index=True)
    else:
        st.info('No matches found for this team.')

except requests.exceptions.RequestException as e:
    st.error(f'Error connecting to the API: {e}')
    st.info('Make sure the API server is running.')
