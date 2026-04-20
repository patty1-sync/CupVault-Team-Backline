import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title(f"Welcome, {st.session_state['first_name']}! 🛠️")
st.write('### Database Administration Panel')
st.write('---')

if st.button('📋 Manage Records',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/31_manage_records.py')

if st.button('🔎 Audit Log',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/32_audit_log.py')

if st.button('✅ Data Integrity Check',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/33_data_integrity.py')
