import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

# 4.6 - Query for records with missing or incomplete fields

st.title('✅ Data Integrity Check')
st.write('Identify records with missing or incomplete fields across the database.')
st.write('---')

API_BASE = 'http://web-api:4000'

try:
    issues_found = 0

    # ---- Players with missing fields ----
    st.write('### Players — Missing Fields')

    players_resp = requests.get(f'{API_BASE}/players')
    players_resp.raise_for_status()
    players = players_resp.json()

    incomplete_players = [p for p in players
                          if not p.get('prim_position')
                          or not p.get('birth_date')
                          or not p.get('team_name')]

    if incomplete_players:
        issues_found += len(incomplete_players)
        st.warning(f'{len(incomplete_players)} players with missing data')
        df = pd.DataFrame(incomplete_players)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.success('All player records are complete.')

    # ---- Teams check ----
    st.write('---')
    st.write('### Teams — Missing Fields')

    teams_resp = requests.get(f'{API_BASE}/teams')
    teams_resp.raise_for_status()
    teams = teams_resp.json()

    incomplete_teams = [t for t in teams if not t.get('federation')]

    if incomplete_teams:
        issues_found += len(incomplete_teams)
        st.warning(f'{len(incomplete_teams)} teams missing federation info')
        df = pd.DataFrame(incomplete_teams)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.success('All team records are complete.')

    # ---- Matches check ----
    st.write('---')
    st.write('### Matches — Status Check')

    matches_resp = requests.get(f'{API_BASE}/matches')
    matches_resp.raise_for_status()
    matches = matches_resp.json()

    scheduled = [m for m in matches if m.get('status') == 'scheduled']

    if scheduled:
        st.info(f'{len(scheduled)} matches still marked as "scheduled"')
        df = pd.DataFrame(scheduled)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.success('No pending scheduled matches.')

    # ---- Tournaments missing champion ----
    st.write('---')
    st.write('### Tournaments — Missing Champion')

    tourney_resp = requests.get(f'{API_BASE}/tournaments')
    tourney_resp.raise_for_status()
    tournaments = tourney_resp.json()

    no_champ = [t for t in tournaments if not t.get('champion')]

    if no_champ:
        issues_found += len(no_champ)
        st.warning(f'{len(no_champ)} tournaments missing champion data')
        df = pd.DataFrame(no_champ)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.success('All tournaments have champion data.')

    # ---- Summary ----
    st.write('---')
    if issues_found > 0:
        st.error(f'Total issues found: {issues_found}')
    else:
        st.success('No data integrity issues found! Database looks clean.')

except requests.exceptions.RequestException as e:
    st.error(f'Error connecting to the API: {e}')
    st.info('Make sure the API server is running.')
