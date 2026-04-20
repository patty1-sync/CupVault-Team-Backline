import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

# 3.6 - Compare average goals per game across different World Cup tournaments

st.title('📈 Goals Trends')
st.write('Analyze scoring trends across World Cup tournaments for smarter over/under bets.')
st.write('---')

API_BASE = 'http://web-api:4000'

try:
    # ---- Load tournaments ----
    tourney_resp = requests.get(f'{API_BASE}/tournaments')
    tourney_resp.raise_for_status()
    tournaments = tourney_resp.json()

    # ---- Goals per tournament ----
    st.write('### Average Goals Per Match by Tournament')

    results = []
    for t in tournaments:
        matches_resp = requests.get(f'{API_BASE}/matches',
                                    params={'tournament_id': t['tourney_id']})
        if matches_resp.status_code == 200:
            matches = matches_resp.json()
            if matches:
                total_goals = sum(m.get('home_score', 0) + m.get('away_score', 0) for m in matches)
                total_matches = len(matches)
                avg_goals = round(total_goals / total_matches, 2) if total_matches > 0 else 0
                results.append({
                    'Year': t['year'],
                    'Host': t['host_country'],
                    'Matches': total_matches,
                    'Total Goals': total_goals,
                    'Avg Goals/Match': avg_goals
                })

    if results:
        df = pd.DataFrame(results).sort_values('Year', ascending=False)
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.write('---')
        st.write('### Scoring Trend Over Time')
        chart_df = df.sort_values('Year').set_index('Year')
        st.line_chart(chart_df['Avg Goals/Match'])

        st.write('---')
        st.write('### Total Goals by Tournament')
        st.bar_chart(chart_df['Total Goals'])
    else:
        st.info('No tournament data available.')

except requests.exceptions.RequestException as e:
    st.error(f'Error connecting to the API: {e}')
    st.info('Make sure the API server is running.')
