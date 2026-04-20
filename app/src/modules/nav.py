import streamlit as st


# ---- General ----------------------------------------------------------------

def home_nav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


# ---- Role: fan --------------------------------------------------------------

def fan_home_nav():
    st.sidebar.page_link("pages/00_fan_home.py", label="Fan Home", icon="🏟️")

def player_goals_nav():
    st.sidebar.page_link("pages/02_player_goals.py", label="Player Goals", icon="⚽")

def favorites_nav():
    st.sidebar.page_link("pages/01_favorites.py", label="My Favorites", icon="⭐")

def match_schedule_nav():
    st.sidebar.page_link("pages/03_match_schedule.py", label="Match Schedule", icon="📅")


# ---- Role: analyst ----------------------------------------------------------

def analyst_home_nav():
    st.sidebar.page_link("pages/10_analyst_home.py", label="Analyst Home", icon="📊")

def player_stats_nav():
    st.sidebar.page_link("pages/11_player_stats.py", label="Player Stats Explorer", icon="🔍")

def top_scorers_nav():
    st.sidebar.page_link("pages/12_top_scorers.py", label="Top Scorers", icon="🥇")

def scout_notes_nav():
    st.sidebar.page_link("pages/13_scout_notes.py", label="Scouting Notes", icon="📝")


# ---- Role: bettor -----------------------------------------------------------

def bettor_home_nav():
    st.sidebar.page_link("pages/20_bettor_home.py", label="Bettor Home", icon="💰")

def card_stats_nav():
    st.sidebar.page_link("pages/21_card_stats.py", label="Disciplinary Stats", icon="🟨")

def match_history_nav():
    st.sidebar.page_link("pages/22_match_history.py", label="Match History", icon="🔁")

def goals_trends_nav():
    st.sidebar.page_link("pages/23_goals_trends.py", label="Goals Trends", icon="📈")


# ---- Role: admin ------------------------------------------------------------

def admin_home_nav():
    st.sidebar.page_link("pages/30_admin_home.py", label="Admin Home", icon="🛠️")

def manage_records_nav():
    st.sidebar.page_link("pages/31_manage_records.py", label="Manage Records", icon="📋")

def audit_log_nav():
    st.sidebar.page_link("pages/32_audit_log.py", label="Audit Log", icon="🔎")

def data_integrity_nav():
    st.sidebar.page_link("pages/33_data_integrity.py", label="Data Integrity", icon="✅")


# ---- Sidebar assembly -------------------------------------------------------

def SideBarLinks(show_home=False):
    st.sidebar.image("assets/cupvaultapplogo.jpg", width=150)

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        home_nav()

    if st.session_state["authenticated"]:

        if st.session_state["role"] == "fan":
            fan_home_nav()
            player_goals_nav()
            favorites_nav()
            match_schedule_nav()

        if st.session_state["role"] == "analyst":
            analyst_home_nav()
            player_stats_nav()
            top_scorers_nav()
            scout_notes_nav()

        if st.session_state["role"] == "bettor":
            bettor_home_nav()
            card_stats_nav()
            match_history_nav()
            goals_trends_nav()

        if st.session_state["role"] == "admin":
            admin_home_nav()
            manage_records_nav()
            audit_log_nav()
            data_integrity_nav()

    if st.session_state["authenticated"]:
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")