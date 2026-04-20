import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

# 2.6 - Update saved scouting notes on a team or player

st.title('📝 Scouting Notes')
st.write('Create, edit, and manage your scouting notes on teams and players.')
st.write('---')

API_BASE = 'http://web-api:4000'
user_id = st.session_state.get('user_id', 2)

try:
    # ---- Load reference data ----
    teams_resp = requests.get(f'{API_BASE}/teams')
    teams_resp.raise_for_status()
    teams_list = teams_resp.json()

    players_resp = requests.get(f'{API_BASE}/players')
    players_resp.raise_for_status()
    players_list = players_resp.json()

    # ---- Create New Note ----
    st.write('### Add New Note')

    with st.form('new_note_form', clear_on_submit=True):
        note_text = st.text_area('Note Text', placeholder='Write your scouting observations here...')

        col1, col2 = st.columns(2)
        with col1:
            team_options = ['None'] + [t['team_name'] for t in teams_list]
            selected_team = st.selectbox('Team (optional)', team_options)
        with col2:
            player_options = ['None'] + [f"{p['first_name']} {p['last_name']}" for p in players_list]
            selected_player = st.selectbox('Player (optional)', player_options)

        submitted = st.form_submit_button('Save Note', type='primary')

        if submitted:
            if not note_text.strip():
                st.error('Note text cannot be empty.')
            else:
                payload = {'note_text': note_text}

                if selected_team != 'None':
                    team_obj = next(t for t in teams_list if t['team_name'] == selected_team)
                    payload['team_id'] = team_obj['team_id']

                if selected_player != 'None':
                    player_obj = next(p for p in players_list
                                      if f"{p['first_name']} {p['last_name']}" == selected_player)
                    payload['player_id'] = player_obj['player_id']

                resp = requests.post(f'{API_BASE}/notes/{user_id}', json=payload)
                if resp.status_code == 201:
                    st.success('Note saved successfully!')
                    st.rerun()
                else:
                    st.error(f'Error saving note: {resp.json().get("error", "Unknown error")}')

    # ---- Existing Notes ----
    st.write('---')
    st.write('### Your Notes')

    notes_resp = requests.get(f'{API_BASE}/notes/{user_id}')
    notes_resp.raise_for_status()
    notes = notes_resp.json()

    if not notes:
        st.info('You have no scouting notes yet. Create one above!')
    else:
        for note in notes:
            with st.expander(
                f"Note #{note['note_id']} — "
                f"{note.get('team_name') or ''} "
                f"{note.get('player_name') or ''}"
            ):
                st.write(note['note_text'])

                # ---- Edit ----
                new_text = st.text_area(
                    'Edit note',
                    value=note['note_text'],
                    key=f"edit_{note['note_id']}"
                )

                col1, col2 = st.columns(2)
                with col1:
                    if st.button('Update', key=f"update_{note['note_id']}", type='primary'):
                        update_resp = requests.put(
                            f"{API_BASE}/notes/detail/{note['note_id']}",
                            json={'note_text': new_text}
                        )
                        if update_resp.status_code == 200:
                            st.success('Note updated!')
                            st.rerun()
                        else:
                            st.error('Failed to update note.')

                with col2:
                    if st.button('Delete', key=f"delete_{note['note_id']}"):
                        delete_resp = requests.delete(
                            f"{API_BASE}/notes/detail/{note['note_id']}"
                        )
                        if delete_resp.status_code == 200:
                            st.success('Note deleted!')
                            st.rerun()
                        else:
                            st.error('Failed to delete note.')

except requests.exceptions.RequestException as e:
    st.error(f'Error connecting to the API: {e}')
    st.info('Make sure the API server is running.')
