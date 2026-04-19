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

# 1.1 - As a fan, I need to be able to see how many World Cups my national team
# has won compared to other countries so that I can finally win arguments with
# friends who won't stop talking about their team's history.

# 1.3 - As a fan, I want to see the opponents' stats in previous World Cups so
# that I know the matchup better when I watch my team play.

st.title('🏆 Team World Cup History')
st.write('Compare World Cup records across all national teams.')
st.write('---')

# ---- Filters ----------------------------------------------------------------

search = st.text_input('Search for a country...', '')

# ---- API Call ---------------------------------------------------------------

API_BASE = 'http://web-api:4000'

try:
    response = requests.get(f'{API_BASE}/teams')
    response.raise_for_status()
    teams = response.json()

    if search:
        teams = [t for t in teams if search.lower() in t['team_name'].lower()]

    if teams:
        df = pd.DataFrame(teams)
        st.write(f"**{len(df)} teams found**")
        st.dataframe(df, use_container_width=True)

        # ---- Team Detail ------------------------------------------------

        st.write('---')
        st.write('### Team Details')
        team_names = [t['team_name'] for t in teams]
        selected = st.selectbox('Select a team to view details', team_names)
        selected_team = next(t for t in teams if t['team_name'] == selected)

        detail_response = requests.get(f"{API_BASE}/teams/{selected_team['team_id']}")
        if detail_response.status_code == 200:
            detail = detail_response.json()
            col1, col2, col3 = st.columns(3)
            col1.metric('World Cup Titles', detail.get('titles_won', 0))
            col2.metric('Total Matches', detail.get('total_matches', 0))
            col3.metric('Goals Scored', detail.get('total_goals', 0))
    else:
        st.info('No teams found.')

except requests.exceptions.RequestException as e:
    st.error(f'Error connecting to the API: {e}')
    st.info('Make sure the API server is running.')