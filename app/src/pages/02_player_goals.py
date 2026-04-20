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

    for p in players:
        p['full_name'] = f"{p['first_name']} {p['last_name']}"

    # ---- Search -------------------------------------------------------------

    search = st.text_input('Search for a player...', '')
    if search:
        players = [p for p in players if search.lower() in p['full_name'].lower()]

    if players:
        player_names = [p['full_name'] for p in players]
        selected_name = st.selectbox('Select a player', player_names)
        selected_player = next(p for p in players if p['full_name'] == selected_name)

        # ---- Player Detail --------------------------------------------------

        detail_response = requests.get(f"{API_BASE}/players/{selected_player['player_id']}")
        if detail_response.status_code == 200:
            detail = detail_response.json()
            st.write('---')
            col1, col2, col3 = st.columns(3)
            col1.metric('Position', detail.get('prim_position', 'N/A'))
            col2.metric('Team', detail.get('team_name', 'N/A'))
            col3.metric('Birth Date', str(detail.get('birth_date', 'N/A')))

    # ---- All Players Table --------------------------------------------------

    st.write('---')
    st.write('### All Players')
    if players:
        df = pd.DataFrame(players)
        st.dataframe(df[['full_name', 'team_name', 'prim_position', 'birth_date']], use_container_width=True)

except requests.exceptions.RequestException as e:
    st.error(f'Error connecting to the API: {e}')
    st.info('Make sure the API server is running.')