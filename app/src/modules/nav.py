import streamlit as st


# ---- General ----------------------------------------------------------------

def home_nav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def about_page_nav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")


# ---- Role: fan --------------------------------------------------------------

def fan_home_nav():
    st.sidebar.page_link("pages/00_Fan_Home.py", label="Fan Home", icon="🏟️")

def team_history_nav():
    st.sidebar.page_link("pages/01_Team_History.py", label="Team History", icon="🏆")

def player_goals_nav():
    st.sidebar.page_link("pages/02_Player_Goals.py", label="Player Goals", icon="⚽")

def match_schedule_nav():
    st.sidebar.page_link("pages/03_Match_Schedule.py", label="Match Schedule", icon="📅")


# ---- Role: analyst ----------------------------------------------------------

def analyst_home_nav():
    st.sidebar.page_link("pages/10_Analyst_Home.py", label="Analyst Home", icon="📊")

def player_stats_nav():
    st.sidebar.page_link("pages/11_Player_Stats.py", label="Player Stats Explorer", icon="🔍")

def top_scorers_nav():
    st.sidebar.page_link("pages/12_Top_Scorers.py", label="Top Scorers", icon="🥇")

def scout_notes_nav():
    st.sidebar.page_link("pages/13_Scout_Notes.py", label="Scouting Notes", icon="📝")


# ---- Role: bettor -----------------------------------------------------------

def bettor_home_nav():
    st.sidebar.page_link("pages/20_Bettor_Home.py", label="Bettor Home", icon="💰")

def card_stats_nav():
    st.sidebar.page_link("pages/21_Card_Stats.py", label="Disciplinary Stats", icon="🟨")

def head_to_head_nav():
    st.sidebar.page_link("pages/22_Head_to_Head.py", label="Head to Head", icon="⚔️")

def goals_trends_nav():
    st.sidebar.page_link("pages/23_Goals_Trends.py", label="Goals Trends", icon="📈")


# ---- Role: admin ------------------------------------------------------------

def admin_home_nav():
    st.sidebar.page_link("pages/30_Admin_Home.py", label="Admin Home", icon="🛠️")

def manage_records_nav():
    st.sidebar.page_link("pages/31_Manage_Records.py", label="Manage Records", icon="📋")

def audit_log_nav():
    st.sidebar.page_link("pages/32_Audit_Log.py", label="Audit Log", icon="🔎")

def data_integrity_nav():
    st.sidebar.page_link("pages/33_Data_Integrity.py", label="Data Integrity", icon="✅")


# ---- Sidebar assembly -------------------------------------------------------

def SideBarLinks(show_home=False):
    st.sidebar.image("assets/logo.png", width=150)

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        home_nav()

    if st.session_state["authenticated"]:

        if st.session_state["role"] == "fan":
            fan_home_nav()
            team_history_nav()
            player_goals_nav()
            match_schedule_nav()

        if st.session_state["role"] == "analyst":
            analyst_home_nav()
            player_stats_nav()
            top_scorers_nav()
            scout_notes_nav()

        if st.session_state["role"] == "bettor":
            bettor_home_nav()
            card_stats_nav()
            head_to_head_nav()
            goals_trends_nav()

        if st.session_state["role"] == "admin":
            admin_home_nav()
            manage_records_nav()
            audit_log_nav()
            data_integrity_nav()

    about_page_nav()

    if st.session_state["authenticated"]:
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")