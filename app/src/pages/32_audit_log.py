import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

# 4.4 - View a log of recent changes made to the database
# 4.5 - Search and filter records by tournament year, team, or player

st.title('🔎 Audit Log')
st.write('Review recent changes made to the CupVault database.')
st.write('---')

API_BASE = 'http://web-api:4000'

try:
    # ---- Filters ----
    col1, col2 = st.columns(2)

    with col1:
        table_filter = st.selectbox('Filter by Table',
                                    ['All', 'Match', 'MatchEvent', 'Player',
                                     'Team', 'Tournament', 'ScoutNotes'])
    with col2:
        action_filter = st.selectbox('Filter by Action',
                                     ['All', 'INSERT', 'UPDATE', 'DELETE'])

    params = {}
    if table_filter != 'All':
        params['table_name'] = table_filter
    if action_filter != 'All':
        params['action_type'] = action_filter

    # ---- Fetch logs ----
    logs_resp = requests.get(f'{API_BASE}/audit-log', params=params)
    logs_resp.raise_for_status()
    logs = logs_resp.json()

    if logs:
        st.write(f'**{len(logs)} log entries found**')
        df = pd.DataFrame(logs)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # ---- Summary stats ----
        st.write('---')
        st.write('### Activity Summary')

        col1, col2, col3 = st.columns(3)
        inserts = len([l for l in logs if l.get('action_type') == 'INSERT'])
        updates = len([l for l in logs if l.get('action_type') == 'UPDATE'])
        deletes = len([l for l in logs if l.get('action_type') == 'DELETE'])
        col1.metric('Inserts', inserts)
        col2.metric('Updates', updates)
        col3.metric('Deletes', deletes)
    else:
        st.info('No audit log entries found matching your filters.')

except requests.exceptions.RequestException as e:
    st.error(f'Error connecting to the API: {e}')
    st.info('Make sure the API server is running.')
