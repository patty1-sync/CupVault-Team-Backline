import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

# ---- Page Config ------------------------------------------------------------

st.set_page_config(layout='wide')
SideBarLinks()

# ---- Header -----------------------------------------------------------------

# 1.5 - As a fan, I want to see the full bracket of any past World Cup so that
# I can trace exactly how the champion got there and relive iconic moments.

# 1.6 - As a fan, I want to see each day's live match updates and scores so
# that I can stay caught up and talk with my friends with up-to-date info.

st.title('📅 Match Schedule & Brackets')
st.write('View full brackets for any past World Cup and check live match scores.')
st.write('---')

# ---- API Call ---------------------------------------------------------------

API_BASE = 'http://web-api:4000'

try:
    tournaments_response = requests.get(f'{API_BASE}/tournaments')
    tournaments_response.raise_for_status()
    tournaments = tournaments_response.json()
    years = sorted([t['year'] for t in tournaments], reverse=True)
    selected_year = st.selectbox('Select a World Cup year', years)
    selected_tourney = next(t for t in tournaments if t['year'] == selected_year)

    # ---- Tabs ---------------------------------------------------------------

    tab1, tab2 = st.tabs(['Full Bracket', "Today's Matches"])

    with tab1:
        matches_response = requests.get(
            f'{API_BASE}/matches',
            params={'tournament_id': selected_tourney['tourney_id']}
        )
        if matches_response.status_code == 200:
            matches = matches_response.json()
            if matches:
                df = pd.DataFrame(matches)
                stages = df['stage'].unique().tolist() if 'stage' in df.columns else []
                for stage in stages:
                    st.write(f'#### {stage}')
                    stage_df = df[df['stage'] == stage]
                    for _, row in stage_df.iterrows():
                        col1, col2, col3 = st.columns([3, 1, 3])
                        col1.write(f"**{row.get('home_team', '')}**")
                        col2.write(f"{row.get('home_score', '-')} - {row.get('away_score', '-')}")
                        col3.write(f"**{row.get('away_team', '')}**")
            else:
                st.info('No matches found for this tournament.')

    with tab2:
        live_response = requests.get(f'{API_BASE}/matches', params={'status': 'live'})
        if live_response.status_code == 200:
            live_matches = live_response.json()
            if live_matches:
                for m in live_matches:
                    col1, col2, col3 = st.columns([3, 1, 3])
                    col1.write(f"**{m.get('home_team', '')}**")
                    col2.write(f"{m.get('home_score', '-')} - {m.get('away_score', '-')}")
                    col3.write(f"**{m.get('away_team', '')}**")
            else:
                st.info('No live matches right now.')

except requests.exceptions.RequestException as e:
    st.error(f'Error connecting to the API: {e}')
    st.info('Make sure the API server is running.')