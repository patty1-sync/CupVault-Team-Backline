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

# 1.2 - As a fan, I need to be able to look up any player's World Cup goal
# record so that I can see if my favorite player stacks up against the
# all-time greats.

st.title('⚽ Player Goal Records')
st.write("Look up any player's World Cup goal record.")
st.write('---')

# ---- API Call ---------------------------------------------------------------

API_BASE = 'http://web-api:4000'

try:
    players_response = requests.get(f'{API_BASE}/players')
    players_response.raise_for_status()
    players = players_response.json()

    # ---- Search -------------------------------------------------------------

    search = st.text_input('Search for a player...', '')
    if search:
        players = [p for p in players if search.lower() in p.get('player_name', '').lower()]

    if players:
        player_names = [p['player_name'] for p in players]
        selected_name = st.selectbox('Select a player', player_names)
        selected_player = next(p for p in players if p['player_name'] == selected_name)

        # ---- Player Detail --------------------------------------------------

        detail_response = requests.get(f"{API_BASE}/players/{selected_player['player_id']}")
        if detail_response.status_code == 200:
            detail = detail_response.json()
            st.write('---')
            col1, col2, col3, col4 = st.columns(4)
            col1.metric('Total WC Goals', detail.get('total_wc_goals', 0))
            col2.metric('Tournaments', detail.get('tournaments', 0))
            col3.metric('Matches Played', detail.get('matches_played', 0))
            col4.metric('Position', detail.get('prim_position', 'N/A'))

    # ---- All Time Top Scorers -----------------------------------------------

    st.write('---')
    st.write('### All-Time Top Scorers')
    all_response = requests.get(f'{API_BASE}/players')
    if all_response.status_code == 200:
        all_players = all_response.json()
        df = pd.DataFrame(all_players)
        if not df.empty:
            st.dataframe(df, use_container_width=True)

except requests.exceptions.RequestException as e:
    st.error(f'Error connecting to the API: {e}')
    st.info('Make sure the API server is running.')