import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

# 3.1 - See which team has received the most yellow cards historically
# 3.2 - See how many penalties were recorded in the last World Cup

st.title('🟨 Disciplinary & Penalty Stats')
st.write('Explore yellow card and penalty data to inform your prop bets.')
st.write('---')

API_BASE = 'http://web-api:4000'

try:
    tab1, tab2 = st.tabs(['Yellow Cards', 'Penalties'])

    # ---- Yellow Cards Tab ----
    with tab1:
        st.write('### Yellow Cards by Team')

        events_resp = requests.get(f'{API_BASE}/match-events', params={'event_type': 'yellow_card'})
        events_resp.raise_for_status()
        cards = events_resp.json()

        if cards:
            df = pd.DataFrame(cards)
            card_counts = df.groupby('team_name').agg(
                total_yellow_cards=('event_id', 'count')
            ).reset_index().sort_values('total_yellow_cards', ascending=False)

            st.dataframe(card_counts, use_container_width=True, hide_index=True)

            st.write('---')
            st.write('### Yellow Cards by Team — Chart')
            chart_data = card_counts.set_index('team_name')
            st.bar_chart(chart_data['total_yellow_cards'])
        else:
            st.info('No yellow card data found.')

    # ---- Penalties Tab ----
    with tab2:
        st.write('### Penalty Goals by Tournament')

        all_events_resp = requests.get(f'{API_BASE}/match-events')
        all_events_resp.raise_for_status()
        all_events = all_events_resp.json()

        penalty_events = [e for e in all_events if e.get('is_penalty_goal')]

        if penalty_events:
            pen_df = pd.DataFrame(penalty_events)
            pen_by_year = pen_df.groupby('year').agg(
                total_penalty_goals=('event_id', 'count')
            ).reset_index().sort_values('year', ascending=False)

            st.dataframe(pen_by_year, use_container_width=True, hide_index=True)

            st.write('---')
            st.write('### Penalty Goals Trend')
            chart_data = pen_by_year.set_index('year')
            st.bar_chart(chart_data['total_penalty_goals'])
        else:
            st.info('No penalty goal data found.')

except requests.exceptions.RequestException as e:
    st.error(f'Error connecting to the API: {e}')
    st.info('Make sure the API server is running.')
