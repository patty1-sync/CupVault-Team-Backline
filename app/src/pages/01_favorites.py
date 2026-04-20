import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

# 1.4 - As a fan, I want to add players and teams to a personal favourites list
# so that I can quickly access their stats without searching every time.

st.title('⭐ My Favorites')
st.write('Manage your favorite teams and players for quick access.')
st.write('---')

API_BASE = 'http://web-api:4000'
user_id = st.session_state.get('user_id', 1)

try:
    # ---- Load current favorites ----
    fav_resp = requests.get(f'{API_BASE}/favorites/{user_id}')
    fav_resp.raise_for_status()
    favorites = fav_resp.json()

    fav_teams = favorites.get('favorite_teams', [])
    fav_players = favorites.get('favorite_players', [])

    # ---- Display Favorite Teams ----
    st.write('### Favorite Teams')

    if fav_teams:
        for team in fav_teams:
            col1, col2 = st.columns([4, 1])
            col1.write(f"**{team['team_name']}** ({team['fifa_code']})")
            if col2.button('Remove', key=f"rm_team_{team['team_id']}"):
                resp = requests.delete(f'{API_BASE}/favorites/{user_id}',
                                       json={'type': 'team', 'id': team['team_id']})
                if resp.status_code == 200:
                    st.success(f"Removed {team['team_name']}")
                    st.rerun()
                else:
                    st.error('Failed to remove team.')
    else:
        st.info('No favorite teams yet. Add one below!')

    # ---- Display Favorite Players ----
    st.write('---')
    st.write('### Favorite Players')

    if fav_players:
        for player in fav_players:
            col1, col2 = st.columns([4, 1])
            col1.write(f"**{player['first_name']} {player['last_name']}** — {player.get('team_name', 'N/A')}")
            if col2.button('Remove', key=f"rm_player_{player['player_id']}"):
                resp = requests.delete(f'{API_BASE}/favorites/{user_id}',
                                       json={'type': 'player', 'id': player['player_id']})
                if resp.status_code == 200:
                    st.success(f"Removed {player['first_name']} {player['last_name']}")
                    st.rerun()
                else:
                    st.error('Failed to remove player.')
    else:
        st.info('No favorite players yet. Add one below!')

    # ---- Add Favorites ----
    st.write('---')
    st.write('### Add a Favorite')

    tab1, tab2 = st.tabs(['Add Team', 'Add Player'])

    with tab1:
        teams_resp = requests.get(f'{API_BASE}/teams')
        teams_resp.raise_for_status()
        all_teams = teams_resp.json()

        # Filter out teams already in favorites
        fav_team_ids = [t['team_id'] for t in fav_teams]
        available_teams = [t for t in all_teams if t['team_id'] not in fav_team_ids]

        if available_teams:
            team_names = [t['team_name'] for t in available_teams]
            selected_team = st.selectbox('Select a team', team_names)

            if st.button('Add Team to Favorites', type='primary'):
                team_obj = next(t for t in available_teams if t['team_name'] == selected_team)
                resp = requests.post(f'{API_BASE}/favorites/{user_id}',
                                     json={'type': 'team', 'id': team_obj['team_id']})
                if resp.status_code == 201:
                    st.success(f'Added {selected_team} to favorites!')
                    st.rerun()
                else:
                    st.error('Failed to add team.')
        else:
            st.info('All available teams are already in your favorites!')

    with tab2:
        players_resp = requests.get(f'{API_BASE}/players')
        players_resp.raise_for_status()
        all_players = players_resp.json()

        # Filter out players already in favorites
        fav_player_ids = [p['player_id'] for p in fav_players]
        available_players = [p for p in all_players if p['player_id'] not in fav_player_ids]

        if available_players:
            player_names = [f"{p['first_name']} {p['last_name']}" for p in available_players]
            selected_player = st.selectbox('Select a player', player_names)

            if st.button('Add Player to Favorites', type='primary'):
                player_obj = next(p for p in available_players
                                  if f"{p['first_name']} {p['last_name']}" == selected_player)
                resp = requests.post(f'{API_BASE}/favorites/{user_id}',
                                     json={'type': 'player', 'id': player_obj['player_id']})
                if resp.status_code == 201:
                    st.success(f'Added {selected_player} to favorites!')
                    st.rerun()
                else:
                    st.error('Failed to add player.')
        else:
            st.info('All available players are already in your favorites!')

except requests.exceptions.RequestException as e:
    st.error(f'Error connecting to the API: {e}')
    st.info('Make sure the API server is running.')
