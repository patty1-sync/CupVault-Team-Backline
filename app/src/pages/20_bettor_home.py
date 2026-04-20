import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title(f"Welcome, {st.session_state['first_name']}! 💰")
st.write('### What are you betting on today?')
st.write('---')

if st.button('🟨 Disciplinary & Card Stats',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/21_card_stats.py')

if st.button('🔁 Match History',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/22_match_history.py')

if st.button('📈 Goals Trends Across Tournaments',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/23_goals_trends.py')
