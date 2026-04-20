import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title(f"Welcome, {st.session_state['first_name']}! 📊")
st.write('### What would you like to analyze today?')
st.write('---')

if st.button('🔍 Player Stats Explorer',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/11_player_stats.py')

if st.button('🥇 Top Scorers Across Tournaments',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/12_top_scorers.py')

if st.button('📝 Scouting Notes',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/13_scout_notes.py')
