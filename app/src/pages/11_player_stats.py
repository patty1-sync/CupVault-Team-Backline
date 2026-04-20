import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

# 2.1 - Quick access to player stats across multiple World Cup tournaments
# 2.2 - Filter data by team, player, and tournament

st.title('🔍 Player Stats Explorer')
st.write('Filter and analyze player performance across multiple World Cup tournaments.')
st.write('---')

API_BASE = 'http://web-api:4000'

try:
    # Load filter options
    teams_resp = requests.get(f'{API_BASE}/teams')
    teams_resp.raise_for_status()
    teams_list = teams_resp.json()

    tourney_resp = requests.get(f'{API_BASE}/tournaments')
    tourney_resp.raise_for_status()
    tourney_list = tourney_resp.json()

    # ---- Filters ----
    col1, col2, col3 = st.columns(3)

    with col1:
        player_search = st.text_input('Search player name...', '')
    with col2:
        team_options = ['All Teams'] + [t['team_name'] for t in teams_list]
        selected_team = st.selectbox('Team', team_options)
    with col3:
        year_options = ['All Years'] + sorted([t['year'] for t in tourney_list], reverse=True)
        selected_year = st.selectbox('Tournament Year', year_options)

    # ---- Fetch players ----
    params = {}
    if selected_team != 'All Teams':
        team_obj = next(t for t in teams_list if t['team_name'] == selected_team)
        params['team_id'] = team_obj['team_id']

    players_resp = requests.get(f'{API_BASE}/players', params=params)
    players_resp.raise_for_status()
    players = players_resp.json()

    if player_search:
        players = [p for p in players
                   if player_search.lower() in f"{p.get('first_name','')} {p.get('last_name','')}".lower()]

    if players:
        st.write(f'**{len(players)} players found**')
        df = pd.DataFrame(players)
        st.dataframe(df, use_container_width=True)
    else:
        st.info('No players match your filters.')

    # ---- Match Events section ----
    st.write('---')
    st.write('### Match Events')

    event_params = {}
    if selected_team != 'All Teams':
        event_params['team_id'] = team_obj['team_id']

    event_type_filter = st.selectbox('Event Type', ['All', 'goal', 'yellow_card', 'red_card'])
    if event_type_filter != 'All':
        event_params['event_type'] = event_type_filter

    events_resp = requests.get(f'{API_BASE}/match-events', params=event_params)
    events_resp.raise_for_status()
    events = events_resp.json()

    if selected_year != 'All Years':
        events = [e for e in events if e.get('year') == selected_year]

    if events:
        events_df = pd.DataFrame(events)
        st.write(f'**{len(events_df)} events found**')
        st.dataframe(events_df, use_container_width=True)
    else:
        st.info('No events match your filters.')

except requests.exceptions.RequestException as e:
    st.error(f'Error connecting to the API: {e}')
    st.info('Make sure the API server is running.')
