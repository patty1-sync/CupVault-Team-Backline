import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

# 4.1 - Add new tournament data (matches, goals, players)
# 4.2 - Edit or correct existing records
# 4.3 - Delete duplicate entries

st.title('📋 Manage Records')
st.write('Add, edit, and delete records in the CupVault database.')
st.write('---')

API_BASE = 'http://web-api:4000'

try:
    tab1, tab2, tab3, tab4 = st.tabs(['Teams', 'Players', 'Matches', 'Match Events'])

    # ==== TEAMS TAB ====
    with tab1:
        st.write('### Teams')

        teams_resp = requests.get(f'{API_BASE}/teams')
        teams_resp.raise_for_status()
        teams_list = teams_resp.json()

        if teams_list:
            st.dataframe(pd.DataFrame(teams_list), use_container_width=True, hide_index=True)

        # Add Team
        st.write('#### Add New Team')
        with st.form('add_team_form', clear_on_submit=True):
            team_name = st.text_input('Team Name')
            fifa_code = st.text_input('FIFA Code (3 letters)', max_chars=3)
            federation = st.text_input('Federation (e.g., CONMEBOL, UEFA)')

            if st.form_submit_button('Add Team', type='primary'):
                if not team_name or not fifa_code:
                    st.error('Team Name and FIFA Code are required.')
                else:
                    resp = requests.post(f'{API_BASE}/teams',
                                         json={'team_name': team_name,
                                               'fifa_code': fifa_code.upper(),
                                               'federation': federation})
                    if resp.status_code == 201:
                        st.success('Team added!')
                        st.rerun()
                    else:
                        st.error(f"Error: {resp.json().get('error', 'Unknown error')}")

        # Edit Team
        st.write('#### Edit Team')
        if teams_list:
            edit_team_name = st.selectbox('Select team to edit',
                                          [t['team_name'] for t in teams_list],
                                          key='edit_team_select')
            edit_team = next(t for t in teams_list if t['team_name'] == edit_team_name)

            with st.form('edit_team_form'):
                new_name = st.text_input('Team Name', value=edit_team['team_name'])
                new_code = st.text_input('FIFA Code', value=edit_team['fifa_code'], max_chars=3)
                new_fed = st.text_input('Federation', value=edit_team.get('federation', ''))

                if st.form_submit_button('Update Team', type='primary'):
                    resp = requests.put(f"{API_BASE}/teams/{edit_team['team_id']}",
                                        json={'team_name': new_name,
                                              'fifa_code': new_code.upper(),
                                              'federation': new_fed})
                    if resp.status_code == 200:
                        st.success('Team updated!')
                        st.rerun()
                    else:
                        st.error(f"Error: {resp.json().get('error', 'Unknown error')}")

    # ==== PLAYERS TAB ====
    with tab2:
        st.write('### Players')

        players_resp = requests.get(f'{API_BASE}/players')
        players_resp.raise_for_status()
        players_list = players_resp.json()

        if players_list:
            st.dataframe(pd.DataFrame(players_list), use_container_width=True, hide_index=True)

        # Add Player
        st.write('#### Add New Player')

        teams_for_select = requests.get(f'{API_BASE}/teams').json()

        with st.form('add_player_form', clear_on_submit=True):
            first_name = st.text_input('First Name')
            last_name = st.text_input('Last Name')
            position = st.selectbox('Position', ['Forward', 'Midfielder', 'Defender', 'Goalkeeper'])
            birth_date = st.date_input('Birth Date')
            nationality = st.selectbox('Nationality',
                                       [t['team_name'] for t in teams_for_select])

            if st.form_submit_button('Add Player', type='primary'):
                if not first_name or not last_name:
                    st.error('First and Last Name are required.')
                else:
                    nat_team = next(t for t in teams_for_select if t['team_name'] == nationality)
                    resp = requests.post(f'{API_BASE}/players',
                                         json={'first_name': first_name,
                                               'last_name': last_name,
                                               'prim_position': position,
                                               'birth_date': str(birth_date),
                                               'nationality_team_id': nat_team['team_id']})
                    if resp.status_code == 201:
                        st.success('Player added!')
                        st.rerun()
                    else:
                        st.error(f"Error: {resp.json().get('error', 'Unknown error')}")

    # ==== MATCHES TAB ====
    with tab3:
        st.write('### Matches')

        matches_resp = requests.get(f'{API_BASE}/matches')
        matches_resp.raise_for_status()
        matches_list = matches_resp.json()

        if matches_list:
            st.dataframe(pd.DataFrame(matches_list), use_container_width=True, hide_index=True)

        # Add Match
        st.write('#### Add New Match')

        tourney_resp = requests.get(f'{API_BASE}/tournaments')
        tourney_list = tourney_resp.json()
        teams_for_match = requests.get(f'{API_BASE}/teams').json()

        with st.form('add_match_form', clear_on_submit=True):
            tournament = st.selectbox('Tournament',
                                      [f"{t['year']} — {t['host_country']}" for t in tourney_list])
            stage = st.selectbox('Stage', ['Group Stage', 'Round of 16', 'Quarter-Final',
                                           'Semi-Final', 'Third Place', 'Final'])
            match_date = st.date_input('Match Date')
            home_team = st.selectbox('Home Team', [t['team_name'] for t in teams_for_match],
                                     key='home_match')
            away_team = st.selectbox('Away Team', [t['team_name'] for t in teams_for_match],
                                     key='away_match')
            col1, col2 = st.columns(2)
            with col1:
                home_score = st.number_input('Home Score', min_value=0, value=0)
            with col2:
                away_score = st.number_input('Away Score', min_value=0, value=0)
            status = st.selectbox('Status', ['scheduled', 'completed', 'live'])

            if st.form_submit_button('Add Match', type='primary'):
                selected_tourney = tourney_list[[f"{t['year']} — {t['host_country']}"
                                                 for t in tourney_list].index(tournament)]
                home_obj = next(t for t in teams_for_match if t['team_name'] == home_team)
                away_obj = next(t for t in teams_for_match if t['team_name'] == away_team)

                resp = requests.post(f'{API_BASE}/matches',
                                     json={'tournament_id': selected_tourney['tourney_id'],
                                           'stage': stage,
                                           'match_date': str(match_date),
                                           'home_team_id': home_obj['team_id'],
                                           'away_team_id': away_obj['team_id'],
                                           'home_score': home_score,
                                           'away_score': away_score,
                                           'status': status})
                if resp.status_code == 201:
                    st.success('Match added!')
                    st.rerun()
                else:
                    st.error(f"Error: {resp.json().get('error', 'Unknown error')}")

        # Edit Match
        st.write('#### Edit Match Score / Status')
        if matches_list:
            match_labels = [f"#{m['match_id']} — {m.get('home_team','')} vs {m.get('away_team','')} ({m.get('year','')})"
                            for m in matches_list]
            selected_label = st.selectbox('Select match to edit', match_labels)
            selected_idx = match_labels.index(selected_label)
            sel_match = matches_list[selected_idx]

            with st.form('edit_match_form'):
                new_home_score = st.number_input('Home Score',
                                                  min_value=0,
                                                  value=sel_match.get('home_score', 0))
                new_away_score = st.number_input('Away Score',
                                                  min_value=0,
                                                  value=sel_match.get('away_score', 0))
                new_status = st.selectbox('Status',
                                          ['scheduled', 'completed', 'live'],
                                          index=['scheduled', 'completed', 'live'].index(
                                              sel_match.get('status', 'scheduled')))

                if st.form_submit_button('Update Match', type='primary'):
                    resp = requests.put(f"{API_BASE}/matches/{sel_match['match_id']}",
                                        json={'home_score': new_home_score,
                                              'away_score': new_away_score,
                                              'status': new_status})
                    if resp.status_code == 200:
                        st.success('Match updated!')
                        st.rerun()
                    else:
                        st.error(f"Error: {resp.json().get('error', 'Unknown error')}")

    # ==== MATCH EVENTS TAB ====
    with tab4:
        st.write('### Match Events')

        events_resp = requests.get(f'{API_BASE}/match-events')
        events_resp.raise_for_status()
        events_list = events_resp.json()

        if events_list:
            st.dataframe(pd.DataFrame(events_list), use_container_width=True, hide_index=True)

        # Add Event
        st.write('#### Add New Event')

        matches_for_event = requests.get(f'{API_BASE}/matches').json()
        teams_for_event = requests.get(f'{API_BASE}/teams').json()
        players_for_event = requests.get(f'{API_BASE}/players').json()

        with st.form('add_event_form', clear_on_submit=True):
            event_match = st.selectbox(
                'Match',
                [f"#{m['match_id']} — {m.get('home_team','')} vs {m.get('away_team','')}"
                 for m in matches_for_event],
                key='event_match')
            event_team = st.selectbox('Team', [t['team_name'] for t in teams_for_event],
                                      key='event_team')
            event_player = st.selectbox(
                'Player',
                [f"{p['first_name']} {p['last_name']}" for p in players_for_event],
                key='event_player')
            event_minute = st.number_input('Minute', min_value=0, max_value=130, value=0)
            event_type = st.selectbox('Event Type', ['goal', 'yellow_card', 'red_card',
                                                      'substitution', 'own_goal'])
            card_type = st.selectbox('Card Type (if applicable)', ['None', 'yellow', 'red'])
            is_penalty = st.checkbox('Penalty Goal?')

            if st.form_submit_button('Add Event', type='primary'):
                match_obj = matches_for_event[
                    [f"#{m['match_id']} — {m.get('home_team','')} vs {m.get('away_team','')}"
                     for m in matches_for_event].index(event_match)]
                team_obj = next(t for t in teams_for_event if t['team_name'] == event_team)
                player_obj = next(p for p in players_for_event
                                  if f"{p['first_name']} {p['last_name']}" == event_player)

                payload = {
                    'match_id': match_obj['match_id'],
                    'team_id': team_obj['team_id'],
                    'player_id': player_obj['player_id'],
                    'minute': event_minute,
                    'event_type': event_type,
                    'is_penalty_goal': 1 if is_penalty else 0
                }
                if card_type != 'None':
                    payload['card_type'] = card_type

                resp = requests.post(f'{API_BASE}/match-events', json=payload)
                if resp.status_code == 201:
                    st.success('Event added!')
                    st.rerun()
                else:
                    st.error(f"Error: {resp.json().get('error', 'Unknown error')}")

except requests.exceptions.RequestException as e:
    st.error(f'Error connecting to the API: {e}')
    st.info('Make sure the API server is running.')
