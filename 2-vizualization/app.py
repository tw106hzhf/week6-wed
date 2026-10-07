import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# --- Page Setup ---
st.set_page_config(page_title="Titanic EDA - Interactive App", layout="wide")

# --- Load Data Directly ---
@st.cache_data
def load_data():
    # Reads local titanic.csv directly
    df = pd.read_csv("../titanic.csv")
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("`titanic.csv` not found in current directory. Please ensure the file exists.")
    st.stop()

# Set up clean theme
alt.themes.enable("default")

st.title("🚢 Titanic Dataset - Exploratory Data Analysis")

# --- Sidebar Navigation ---
st.sidebar.title("Navigation")
menu = [
    "1. Basic Exploration",
    "2. Distribution of Fare",
    "3. Boxplots by Class",
    "4. Swarm / Strip Plot",
    "5. Countplot of Sex",
    "6. Correlation Heatmap",
    "7. FacetGrid Histograms",
    "8. Jointplot (Age vs Fare)"
]
choice = st.sidebar.radio("Select Section", menu)

# --- 1. Basic Exploration ---
if choice == "1. Basic Exploration":
    st.header("1. Basic Exploration")
    
    st.subheader("Data Preview (head)")
    st.dataframe(df.head())
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Dataset Summary Statistics")
        st.dataframe(df.describe(include="all"))
    
    with col2:
        st.subheader("Dataset Info")
        buffer = []
        buffer.append(f"**Total Rows:** {df.shape[0]}")
        buffer.append(f"**Total Columns:** {df.shape[1]}")
        buffer.append("**Missing Values per Column:**")
        for col, val in df.isnull().sum().items():
            if val > 0:
                buffer.append(f"- `{col}`: {val} missing")
        st.markdown("\n".join(buffer))

# --- 2. Distribution of Fare (Histogram) ---
elif choice == "2. Distribution of Fare":
    st.header("2. Distribution of Fare")
    st.write("Explore the distribution of passenger fares with configurable bin counts.")
    
    bins = st.slider("Select Bin Count", min_value=10, max_value=100, value=30)
    
    chart = (
        alt.Chart(df)
        .mark_bar(color="crimson", opacity=0.6)
        .encode(
            x=alt.X("fare:Q", bin=alt.Bin(maxbins=bins), title="Fare"),
            y=alt.Y("count():Q", title="Count"),
            tooltip=["count()"]
        )
        .properties(height=400)
        .interactive()
    )
    st.altair_chart(chart, use_container_width=True)

# --- 3. Boxplots ---
elif choice == "3. Boxplots by Class":
    st.header("3. Boxplots")
    st.write("Select one or more numerical variables to display interactive box plots.")
    
    # Identify numeric columns for selection
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    selected_vars = st.multiselect(
        "Select Numerical Variable(s) for Boxplots",
        options=numeric_cols,
        default=["age"] if "age" in numeric_cols else [numeric_cols[0]]
    )
    
    category_col = st.selectbox(
        "Group by Category Column",
        options=["pclass", "sex", "embarked", "survived"],
        index=0
    )
    
    if selected_vars:
        for var in selected_vars:
            st.subheader(f"Boxplot: `{var}` grouped by `{category_col}`")
            box_chart = (
                alt.Chart(df)
                .mark_boxplot(extent="min-max")
                .encode(
                    x=alt.X(f"{category_col}:N", title=category_col.capitalize()),
                    y=alt.Y(f"{var}:Q", title=var.capitalize()),
                    color=alt.Color(f"{category_col}:N")
                )
                .properties(height=350)
            )
            st.altair_chart(box_chart, use_container_width=True)
    else:
        st.warning("Please select at least one numerical variable above.")

# --- 4. Swarm / Strip Plot ---
elif choice == "4. Swarm / Strip Plot":
    st.header("4. Strip / Jitter Plot (Granular Point View)")
    st.write("Equivalent to a swarmplot: showing individual data points across passenger classes.")
    
    strip_chart = (
        alt.Chart(df.dropna(subset=["age"]))
        .mark_circle(size=30)
        .encode(
            x=alt.X("pclass:N", title="Passenger Class"),
            y=alt.Y("age:Q", title="Age"),
            color=alt.Color("pclass:N"),
            xOffset="jitter:Q",
            tooltip=["sex", "age", "fare", "survived"]
        )
        .transform_calculate(jitter="sqrt(-2 * log(random())) * cos(2 * PI * random())")
        .properties(height=450)
        .interactive()
    )
    st.altair_chart(strip_chart, use_container_width=True)

# --- 5. Countplot of Sex ---
elif choice == "5. Countplot of Sex":
    st.header("5. Countplot of Sex")
    
    bar_chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X("sex:N", title="Sex"),
            y=alt.Y("count():Q", title="Count"),
            color=alt.Color("sex:N"),
            tooltip=["sex", "count()"]
        )
        .properties(height=350)
    )
    st.altair_chart(bar_chart, use_container_width=True)

# --- 6. Correlation Heatmap ---
elif choice == "6. Correlation Heatmap":
    st.header("6. Correlation Heatmap (Numeric Columns)")
    
    numeric_df = df.select_dtypes(include=[np.number])
    corr_matrix = numeric_df.corr().reset_index().melt(id_vars="index")
    corr_matrix.columns = ["Variable 1", "Variable 2", "Correlation"]
    
    heatmap = (
        alt.Chart(corr_matrix)
        .mark_rect()
        .encode(
            x=alt.X("Variable 1:N", title=""),
            y=alt.Y("Variable 2:N", title=""),
            color=alt.Color("Correlation:Q", scale=alt.Scale(scheme="redblue", domain=[-1, 1])),
            tooltip=["Variable 1", "Variable 2", alt.Tooltip("Correlation:Q", format=".2f")]
        )
        .properties(height=450)
    )
    
    text = heatmap.mark_text().encode(
        text=alt.Text("Correlation:Q", format=".2f"),
        color=alt.condition(
            "abs(datum.Correlation) > 0.5",
            alt.value("white"),
            alt.value("black")
        )
    )
    
    st.altair_chart(heatmap + text, use_container_width=True)

# --- 7. FacetGrid Histograms ---
elif choice == "7. FacetGrid Histograms":
    st.header("7. Faceted Histograms (Age by Sex)")
    
    facet_chart = (
        alt.Chart(df.dropna(subset=["age"]))
        .mark_bar(opacity=0.7)
        .encode(
            x=alt.X("age:Q", bin=alt.Bin(maxbins=15), title="Age"),
            y=alt.Y("count():Q", title="Count"),
            column=alt.Column("sex:N", title="Sex"),
            color=alt.Color("sex:N")
        )
        .properties(width=300, height=350)
    )
    st.altair_chart(facet_chart)

# --- 8. Jointplot (Age vs Fare) ---
elif choice == "8. Jointplot (Age vs Fare)":
    st.header("8. Jointplot (Scatter Plot of Age vs Fare)")
    
    scatter = (
        alt.Chart(df.dropna(subset=["age"]))
        .mark_point(clip=True)
        .encode(
            x=alt.X("fare:Q", title="Fare", scale=alt.Scale(domain=[0, 300])),
            y=alt.Y("age:Q", title="Age"),
            color=alt.Color("sex:N"),
            tooltip=["pclass", "sex", "age", "fare", "survived"]
        )
        .properties(height=500)
        .interactive()
    )
    st.altair_chart(scatter, use_container_width=True)