# =============================================================================
# IMPORTS
# =============================================================================

import streamlit as st           # Streamlit Web app
import pandas as pd                            
import numpy as np                             
import plotly.express as px      # For interactive dashboards




# =============================================================================
# PAGE CONFIG
# =============================================================================

#(https://docs.streamlit.io/develop/api-reference/configuration/st.set_page_config)

st.set_page_config(
    page_title="Online Retail Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
#    menu_items={
#        'Get Help': '',
#        'Report a bug': "",
#        'About': "This is an *extremely* cool app!"
#    }
)


# --------------------------------------------------------------------------- 
# 2. HIGH-VISIBILITY COLOURS - Streamlit's built-in theme (.streamlit/config.toml)
# ---------------------------------------------------------------------------

# White text on a black background gives the highest contrast (Polyuk, 2026)

PRIMARY = st.get_option("theme.primaryColor") or "#FFD400"      # Bright colour from theme
TEXT    = st.get_option("theme.textColor") or "#FFFFFF"         # Text colour from theme

BG = "#000000"         # Page background - black
TEXT = "#FFFFFF"       # Text colour - white
CHART = "#36454F"      #chart background - dark grey
BORDER = "#FFD400"     # Bright yellow border
GRID = "#555555"       # Grey chart gridlines

YELLOW = "#FFD400"
CYAN = "#00E5FF"              
GREEN = "#69F0AE"             
ORANGE = "#FF8A65"             


# --------------------------------------------------------------------------- 
# 3. STYLING
# ---------------------------------------------------------------------------

# Larger fonts help older readers a lot (Yeh, 2020).

st.markdown("""
<style>
/* Easy-to-read system fonts */
html, body, [class*="css"] {
    font-family: Verdana, Tahoma, Arial, sans-serif;
    font-size: 22px;
    line-height: 1.7;
}
h1 { font-size: 48px !important; }
h2 { font-size: 34px !important; }
h3 { font-size: 28px !important; }
p, li, label, [data-testid="stMarkdownContainer"] { font-size: 22px !important; }

/* KPI cards rounded with padding*/
div[data-testid="stMetric"] { border-radius: 12px; padding: 16px 18px; }
div[data-testid="stMetricValue"] { font-size: 26px !important; font-weight: 700; } 

/* Bigger tab labels and a wider sidebar */
button[data-baseweb="tab"] { font-size: 22px !important; padding: 14px 22px !important; }
section[data-testid="stSidebar"] { min-width: 330px; }
</style>
""", unsafe_allow_html = True)


def style_chart(fig, height = 460):
    """Make every chart large and readable. Colours from Streamlit theme."""
    fig.update_layout(
        paper_bgcolor = "rgba(0,0,0,0)", plot_bgcolor = "rgba(0,0,0,0)",   # See through
        font = dict(size = 18, color = TEXT),                              # Large text in theme colour
        height = height, margin = dict(t = 20, b = 10, l = 10),
        xaxis = dict(color = TEXT), yaxis = dict(color = TEXT),
    )
    return fig





# =============================================================================
# LOAD AND CACHE DATA
# =============================================================================

@st.cache_data                                                          # Cache to load once
def load_data():
    csv_path = "df_clean.csv"                                          # file path (same folder)
    df = pd.read_csv(csv_path, parse_dates = ["InvoiceDate"])           # Load data and parse InvoiceDate

    df["Revenue (GBP)"] = df["Quantity"] * df["ItemPrice"]                    # Add revenue col, = quantity x price
   
    return df


#@st.cache_data                                                          # Cache the headline numbers
#def get_kpis(df):
#    return {"revenue":   df["Revenue (GBP)"].sum(),                           # Total sales value
#            "customers": df["User"].nunique(),                          # Distinct shoppers
#            "products":  df["Item"].nunique(),                          # Distinct products
#            "orders":    df["Invoice"].nunique()}                       # Distinct orders/baskets




df = load_data()                                                        # Load data




#def recommend_items(user_id):
    # recommendation logic
#    return recommendations




# =============================================================================
# SIDEBAR
# =============================================================================

st.sidebar.header("🔎 Choose what to see")                              # sidebar heading

show_all = st.sidebar.checkbox("Show every country", value = True)    # checkbox text
if show_all:
    chosen_countries = sorted(df["Country"].unique())                 # All countries
else:
    chosen_countries = st.sidebar.multiselect(                        # Or pick countries
        "Pick one or more countries:",
        sorted(df["Country"].unique()),
        default = ["United Kingdom"],
    )

all_years = sorted(df["InvoiceDate"].dt.year.unique())                # years in the data
chosen_years = st.sidebar.multiselect("Pick one or more years:", all_years, default = all_years)

# Keep only the chosen rows
view = df[df["Country"].isin(chosen_countries) & df["InvoiceDate"].dt.year.isin(chosen_years)]
if view.empty:
    view = df                                                         # If nothing is selected - use all the data
 




# =============================================================================
# MAIN PAGE
# =============================================================================

st.title("🛒 Online Retail Dashboard")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(df)

st.subheader('Retail Summary')

#KPIs in 4 cols

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total sales",   "£{:,.0f}".format(view["Revenue (GBP)"].sum()))          # Money in £ (rounded, comma separated)
col2.metric("Customers",     "{:,}".format(view["User"].nunique()))                   # Distinct customers
col3.metric("Products sold", "{:,}".format(view["Item"].nunique()))                  # Distinct products
col4.metric("Orders",        "{:,}".format(view["Invoice"].nunique()))                # Distinct orders



# =============================================================================
# TABS (https://docs.streamlit.io/develop/api-reference/layout/st.tabs)
# =============================================================================


tab1, tab2, tab3 = st.tabs(["📈  Sales over time",
                            "🏆  Best sellers & Countries",
                            "📊  Spread of orders",
                           ])


#  TAB 1: Sales over time ------------------------------------------------- ------------------------------------
with tab1:
    st.header("How sales changed over time")
    period = st.radio("Show sales by:", ["Month", "Quarter"], horizontal = True)   # choice
    rule = "MS" if period == "Month" else "QS"                                     # Month start or Quarter start

    # Add up the sales for each month/quarter
    trend = view.set_index("InvoiceDate")["Revenue (GBP)"].resample(rule).sum().reset_index()
    trend.columns = ["Period", "Sales"]

    fig = px.area(trend, x = "Period", y = "Sales", color_discrete_sequence = [YELLOW])
    fig.update_traces(line = dict(width = 4))                         # Thick line
    fig.update_layout(yaxis_title = "Sales (£)", xaxis_title = "")
    st.plotly_chart(style_chart(fig), width = "stretch")
   
    

# TAB 2: Best sellers and countries ------------------------------------------------------------------------------

with tab2:
    
    how_many = st.slider("How many 'top products' to display?", 5, 20, 10)   # Beginner-friendly slider
    left, right = st.columns(2)

    with left:
        st.header("Top " + str(how_many) + " products")
        
        # Add up sales for each product, keep the biggest ones
        products = view.groupby("Description")["Revenue (GBP)"].sum().sort_values(ascending = False)
        products = products.head(how_many).reset_index()
        products.columns = ["Product", "Sales"]
        
        figp = px.bar(products, x = "Sales", y = "Product", orientation = "h",
                      color_discrete_sequence = [CYAN])
        figp.update_layout(yaxis = dict(autorange = "reversed"),      # Biggest at the top
                           xaxis_title = "Sales (£)", yaxis_title = "")
        st.plotly_chart(style_chart(figp, 520), width = "stretch")

    with right:
        st.header("Top 10 countries")
        # Add up sales for each country, then keep the top 10
        countries = view.groupby("Country")["Revenue (GBP)"].sum().sort_values(ascending = False)
        countries = countries.head(10).reset_index()
        countries.columns = ["Country", "Sales"]
        
        figc = px.bar(countries, x = "Sales", y = "Country", orientation = "h",
                      color_discrete_sequence = [GREEN])
        figc.update_layout(yaxis = dict(autorange = "reversed"),
                           xaxis_title = "Sales (£)", yaxis_title = "")
        st.plotly_chart(style_chart(figc, 520), width = "stretch")


    
#TAB 3: Distribution (histogram) ---------------------------------------------------------------------------------
with tab3:
    st.header("How orders are spread out:")
    measure = st.selectbox("Show the spread of:",                     # Pick what to measure
                           ["Order value (£)", "Items per order", "Price per item (£)"])
    bins = st.slider("How detailed?", 10, 50, 30)                     # Number of bars in the histogram

    # Work out the numbers to plot, based on the choice
    if measure == "Order value (£)":
        values = view.groupby("Invoice")["Revenue (GBP)"].sum()            # Total spend per order
    elif measure == "Items per order":
        values = view.groupby("Invoice")["Item"].nunique()           # Different items per order
    else:
        values = view["ItemPrice"]                                   # Price of a single item

    values = values[values > 0]                                      # Remove zero/negative values
    values = values[values <= values.quantile(0.99)]                 # Drop the top 1% so the chart is clear
    spread = pd.DataFrame({"value": values})                         # Put the values in a df

    figd = px.histogram(spread, x = "value", nbins = bins, color_discrete_sequence = [ORANGE])
    figd.update_layout(xaxis_title = measure, yaxis_title = "Number of orders", bargap = 0.05)
    st.plotly_chart(style_chart(figd), width = "stretch")






# =============================================================================
# FOOTER
# =============================================================================

st.markdown("---")
st.caption("Integrated Machine Learning & Data Visualisation Project 2026")







# =============================================================================
# REFERENCES
# =============================================================================

    

#Grabowski, S. (2024) ‘A guide to interface design for older adults’, Adchitects, 2 October. Available at: https://adchitects.co/blog/guide-to-interface-design-for-older-adults


#Polyuk, S. (2026) ‘Age Before Beauty – A Guide to Interface Design for Older Adults’, Toptal, 19 May. Available at: https://www.toptal.com/designers/ui/ui-design-for-older-adults


#Yeh, P.-C. (2020) 'Impact of button position and touchscreen font size on healthcare device operation by older adults', Heliyon, 6(6), e04147. Available at: https://doi.org/10.1016/j.heliyon.2020.e04147


#Streamlit (no date) st.tabs. Available at: https://docs.streamlit.io/develop/api-reference/layout/st.tabs















