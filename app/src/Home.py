import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
st.session_state['authenticated'] = False
SideBarLinks(show_home=True)

logger.info("Loading the Home page of the app")

st.title('⚽ CupVault')
st.write('### Your historical World Cup data platform')
st.write('---')
st.write('#### Select a user and log in to get started')

fan_users     = ['Jason Rivera (Fan)']
analyst_users = ['Maria Santos (Analyst)']
bettor_users  = ['Andrew Chen (Bettor)']
admin_users   = ['Jake Williams (Admin)']

col1, col2 = st.columns(2)

with col1:
    st.write('**🏟️ Fan**')
    fan_selection = st.selectbox('Select Fan', fan_users, label_visibility='collapsed')
    if st.button('Log in as Fan', type='primary', use_container_width=True):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'fan'
        st.session_state['first_name'] = 'Jason'
        st.session_state['user_id'] = 1
        st.switch_page('pages/00_Fan_Home.py')

    st.write('')
    st.write('**📊 Sports Analyst**')
    analyst_selection = st.selectbox('Select Analyst', analyst_users, label_visibility='collapsed')
    if st.button('Log in as Analyst', type='primary', use_container_width=True):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'analyst'
        st.session_state['first_name'] = 'Maria'
        st.session_state['user_id'] = 2
        st.switch_page('pages/10_Analyst_Home.py')

with col2:
    st.write('**💰 Sports Bettor**')
    bettor_selection = st.selectbox('Select Bettor', bettor_users, label_visibility='collapsed')
    if st.button('Log in as Bettor', type='primary', use_container_width=True):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'bettor'
        st.session_state['first_name'] = 'Andrew'
        st.session_state['user_id'] = 3
        st.switch_page('pages/20_Bettor_Home.py')

    st.write('')
    st.write('**🛠️ Database Admin**')
    admin_selection = st.selectbox('Select Admin', admin_users, label_visibility='collapsed')
    if st.button('Log in as Admin', type='primary', use_container_width=True):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'admin'
        st.session_state['first_name'] = 'Jake'
        st.session_state['user_id'] = 4
        st.switch_page('pages/30_Admin_Home.py')