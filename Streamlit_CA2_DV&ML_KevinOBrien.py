# =============================================================================
# IMPORTS
# =============================================================================

import streamlit as st                         # Streamlit Web app
import pandas as pd                            
import numpy as np                             
import plotly.express as px                    # For interactive dashboards




# =============================================================================
# PAGE CONFIG
# =============================================================================
#(https://docs.streamlit.io/develop/api-reference/configuration/st.set_page_config)
st.set_page_config(
    page_title="Online Shop Summary",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)




# =============================================================================
# LOAD DATA / MODELS
# =============================================================================

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Data loaded ok!")

#@st.cache_resource
#def load_model():
#    # load model here
#    return model

df = load_data(10000)
#model = load_model()






# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def recommend_items(user_id):
    # recommendation logic
    return recommendations



    

# =============================================================================
# SIDEBAR
# =============================================================================

#Dark mode toggle

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

st.session_state.dark_mode = st.sidebar.toggle(
    "🌙 Dark Mode",
    value=st.session_state.dark_mode
)

if st.session_state.dark_mode:
    st.markdown("""
    <style>
        .stApp {
            background-color: #121212;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)

    
# User selection/filters


    
st.sidebar.title("⚙️ Controls")

#user_id = st.sidebar.selectbox(
#    "Select User",
#    sorted(df["User"].unique())
#)

top_n = st.sidebar.slider(
    "Number of Recommendations",
    min_value=5,
    max_value=25,
    value=10
)
 




# =============================================================================
# MAIN PAGE
# =============================================================================

st.title("🛒 Retail Recommendation System")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

# hour in the range 0-23
hour_to_filter=st.slider("hour", 0, 23, 17)
filtered_data=data[data[DATE_COLUMN].dt.hour==hour_to_filter]
st.subheader(f"Map of all Pickups at {hour_to_filter}:00")
st.map(filtered_data)







# =============================================================================
# USER ACTIONS
# =============================================================================








# =============================================================================
# VISUALIZATIONS
# =============================================================================

st.subheader("📈 Dataset Overview")

st.bar_chart(
    df["date/time"].value_counts().head(10)
)






# =============================================================================
# FOOTER
# =============================================================================

st.markdown("---")
st.caption("Integrated Machine Learning & Data Visualisation Project")









    





























