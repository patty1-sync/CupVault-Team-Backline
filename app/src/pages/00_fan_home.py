import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

# ---- Page Config ------------------------------------------------------------

st.set_page_config(layout='wide')
SideBarLinks()

# ---- Welcome ----------------------------------------------------------------

st.title(f"Welcome, {st.session_state['first_name']}! 🏟️")
st.write('### What would you like to explore today?')
st.write('---')

# ---- Navigation Buttons -----------------------------------------------------

if st.button('🏆 View Team World Cup History',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/01_favorites.py')

if st.button('⚽ Look Up Player Goal Records',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/02_player_goals.py')

if st.button('📅 View Match Schedule & Brackets',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/03_match_schedule.py')