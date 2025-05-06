import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- Google Sheets Setup ---
def connect_to_gsheet(sheet_name="MyFitnessProgress"):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = st.secrets["google"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name)
    return sheet

def append_measurement(data):
    sheet = connect_to_gsheet()
    data_sheet = sheet.worksheet("Data")
    data_sheet.append_row(data)

def save_goals(goal_data):
    sheet = connect_to_gsheet()
    try:
        goal_sheet = sheet.worksheet("Goals")
    except:
        goal_sheet = sheet.add_worksheet(title="Goals", rows="10", cols="20")
    goal_sheet.clear()
    goal_sheet.append_row(["Month", "Weight", "Chest", "Tummy", "Glutes"])
    for month, row in goal_data.items():
        goal_sheet.append_row([month] + row)

def fetch_data():
    sheet = connect_to_gsheet()
    data = sheet.worksheet("Data").get_all_records()
    return pd.DataFrame(data)

def fetch_goals():
    sheet = connect_to_gsheet()
    goal_sheet = sheet.worksheet("Goals")
    data = goal_sheet.get_all_records()
    return pd.DataFrame(data)

# --- Sidebar Navigation ---
with st.sidebar:
    selected = option_menu(
        "Navigation",
        ["Track", "Set Goals", "Progress"],
        icons=["clipboard-plus", "bullseye", "graph-up"],
        default_index=0,
        styles={
            "container": {"background-color": "#e0f8e9"},  # pastel mint
            "icon": {"color": "#6c757d", "font-size": "20px"},
            "nav-link": {"font-size": "18px", "text-align": "left", "margin": "0px", "--hover-color": "#d3f9d8"},
            "nav-link-selected": {"background-color": "#c8e6c9"}
        }
    )

# --- Background Color Customization ---
background_colors = {
    "Track": "#f3e5f5",       # pastel lilac-pink
    "Set Goals": "#ffe4f2",   # soft blush pink
    "Progress": "#fffde7"     # light pastel yellow
}

st.markdown(f"""
    <style>
        .stApp {{
            background-color: {background_colors.get(selected, '#ffffff')};
        }}
        section[data-testid="stSidebar"] > div:first-child {{
            background-color: #e0f8e9;
        }}
        h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
            color: #a64d79;
        }}
        .stButton > button {{
            background-color: #f48fb1;
            color: white;
            border-radius: 12px;
            font-weight: bold;
            padding: 10px 20px;
        }}
        .stTextInput > div > input,
        .stNumberInput > div > input {{
            background-color: #fde2f3;
            border-radius: 8px;
        }}
        .stMetric {{
            background-color: #f8bbd0;
            padding: 1em;
            border-radius: 10px;
        }}
        .emoji {{
            font-size: 30px;
            animation: bounce 1s infinite;
        }}
        @keyframes bounce {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-5px); }}
        }}
    </style>
""", unsafe_allow_html=True)

# --- TRACK TAB ---
if selected == "Track":
    st.title("🌟 Daily Measurement Tracker")
    st.markdown("Track your body measurements each day! <span class='emoji'>💃</span>", unsafe_allow_html=True)

    date = st.date_input("Date", value=datetime.date.today())
    weight = st.number_input("Weight (kg)", min_value=0.0, step=0.1)
    chest = st.number_input("Chest (cm)", min_value=0.0, step=0.1)
    tummy = st.number_input("Tummy (cm)", min_value=0.0, step=0.1)
    glutes = st.number_input("Glutes (cm)", min_value=0.0, step=0.1)

    if st.button("Submit"):
        append_measurement([str(date), weight, chest, tummy, glutes])
        st.success("Your progress has been saved! 🎉")
        st.balloons()

# --- GOALS TAB ---
elif selected == "Set Goals":
    st.title("🌟 Set Monthly Goals")
    st.markdown("Define your body goals and own your fitness journey! <span class='emoji'>🔥</span>", unsafe_allow_html=True)

    months = [
        ("May", "🌷"),
        ("June", "🌞"),
        ("July", "🏖️")
    ]
    goal_data = {}
    for month, icon in months:
        with st.expander(f"Set Goals for {month} {icon}"):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                g_weight = st.number_input(f"{month} Weight", key=month + "w")
            with col2:
                g_chest = st.number_input(f"{month} Chest", key=month + "c")
            with col3:
                g_stomach = st.number_input(f"{month} Tummy", key=month + "s")
            with col4:
                g_glutes = st.number_input(f"{month} Glutes", key=month + "g")
            goal_data[month] = [g_weight, g_chest, g_stomach, g_glutes]

    if st.button("Save Goals"):
        save_goals(goal_data)
        st.markdown("✅ Goals saved! 📊 You got this! <span class='emoji'>💪</span>", unsafe_allow_html=True)

# --- PROGRESS TAB ---
elif selected == "Progress":
    st.title("📊 Your Progress Overview")

    df = fetch_data()
    if df.empty:
        st.markdown("ℹ️ No data available yet. Start tracking to see your transformation! <span class='emoji'>✨</span>", unsafe_allow_html=True)
    else:
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.sort_values("Date")

        st.subheader("🌸 Progress Graphs")
        fig = px.line(
            df,
            x="Date",
            y=["Weight", "Chest", "Tummy", "Glutes"],
            markers=True,
            title="Measurement Trends Over Time",
            color_discrete_map={
                "Weight": "#f06292",
                "Chest": "#ce93d8",
                "Tummy": "#f8bbd0",
                "Glutes": "#ba68c8"
            },
            template="plotly_white"
        )
        fig.update_traces(line=dict(width=3), marker=dict(size=8))
        fig.update_layout(
            title_font=dict(size=24, color="#9b59b6"),
            xaxis_title="Date",
            yaxis_title="Measurement",
            legend_title_text='Metric'
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("📅 Weekly Summary")
        latest = df["Date"].max()
        week_data = df[df["Date"] > latest - pd.Timedelta(days=7)]
        if not week_data.empty:
            col1, col2 = st.columns(2)
            col1.metric("Avg Weight", f"{week_data['Weight'].mean():.1f} kg")
            col2.metric("Avg Tummy", f"{week_data['Tummy'].mean():.1f} cm")

            if week_data["Weight"].iloc[-1] < week_data["Weight"].iloc[0]:
                st.markdown("✅ Great job this week! You're making progress! <span class='emoji'>🎯</span>", unsafe_allow_html=True)
            else:
                st.markdown("💪 Keep going! Every day counts! <span class='emoji'>🚀</span>", unsafe_allow_html=True)
