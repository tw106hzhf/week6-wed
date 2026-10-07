import streamlit as st
import pandas as pd
import numpy as np

# EM gave instructions to Gemini to create this chode to have three columns with all examples of 
# widgets and other streamlit layout features.

# Set the page to wide mode to comfortably fit 3 columns
st.set_page_config(page_title="Streamlit Essentials Reference", layout="wide")

st.title("🧩 Streamlit Essentials Cheatsheet")
st.write("A quick reference guide for beginners showing component names, python code, and live rendered widgets.")

# Header for our table
col_header1, col_header2, col_header3 = st.columns([1, 2, 2])
with col_header1:
    st.markdown("### Feature")
with col_header2:
    st.markdown("### Python Code")
with col_header3:
    st.markdown("### Live Rendered Widget")

st.divider()


def create_row(feature_name, code_snippet, render_func):
    """Helper function to create row layout cleanly.
    """
    col1, col2, col3 = st.columns([1, 2, 2])
    with col1:
        st.subheader(feature_name)
    with col2:
        st.code(code_snippet, language="python")
    with col3:
        render_func()
    st.divider()

# --- 1. Text Elements ---
create_row(
    "Title & Headers",
    'st.title("Main Title")\nst.header("Section Header")\nst.subheader("Sub-header")',
    lambda: (st.title("Main Title"), st.header("Section Header"), st.subheader("Sub-header"))
)

create_row(
    "Formatted Text & Markdown",
    'st.write("Regular text")\nst.markdown("**Bold** text and *italics*")',
    lambda: (st.write("Regular text"), st.markdown("**Bold** text and *italics*"))
)

# --- 2. Interactive Input Widgets ---
create_row(
    "Button",
    'if st.button("Click Me!"):\n    st.write("Button Clicked!")',
    lambda: st.write("Button Clicked!") if st.button("Click Me!") else None
)

create_row(
    "Checkbox",
    'agree = st.checkbox("I agree")\nif agree:\n    st.write("Agreed!")',
    lambda: st.write("Agreed!") if st.checkbox("I agree") else None
)

create_row(
    "Selectbox (Dropdown)",
    'option = st.selectbox("Choose a class", ["First", "Second", "Third"])\nst.write("Selected:", option)',
    lambda: st.write("Selected:", st.selectbox("Choose a class", ["First", "Second", "Third"]))
)

create_row(
    "Radio Buttons",
    'choice = st.radio("Choose Option", ["Option A", "Option B"])\nst.write("Chosen:", choice)',
    lambda: st.write("Chosen:", st.radio("Choose Option", ["Option A", "Option B"]))
)

create_row(
    "Multi-select",
    'options = st.multiselect("Select Categories", ["Tech", "Finance", "Health"])\nst.write("Selected:", options)',
    lambda: st.write("Selected:", st.multiselect("Select Categories", ["Tech", "Finance", "Health"]))
)

create_row(
    "Slider",
    'age = st.slider("Select Age", min_value=0, max_value=100, value=25)\nst.write("Age:", age)',
    lambda: st.write("Age:", st.slider("Select Age", min_value=0, max_value=100, value=25))
)

create_row(
    "Text Input",
    'name = st.text_input("Passenger Name", "John Doe")\nst.write("Hello,", name)',
    lambda: st.write("Hello,", st.text_input("Passenger Name", "John Doe"))
)

create_row(
    "Number Input",
    'num = st.number_input("Enter Fare ($)", min_value=0.0, max_value=500.0, value=15.0)\nst.write("Fare:", num)',
    lambda: st.write("Fare:", st.number_input("Enter Fare ($)", min_value=0.0, max_value=500.0, value=15.0))
)

create_row(
    "Date Input",
    'd = st.date_input("Select Date")\nst.write("Date:", d)',
    lambda: st.write("Date:", st.date_input("Select Date"))
)

create_row(
    "File Uploader",
    'uploaded_file = st.file_uploader("Upload CSV", type=["csv"])\nif uploaded_file:\n    st.write("File loaded!")',
    lambda: st.write("File loaded!") if st.file_uploader("Upload CSV", type=["csv"]) else None
)

# --- 3. Data & Status Displays ---
create_row(
    "Interactive DataFrame",
    'df = pd.DataFrame({"Class": ["1st", "2nd"], "Fare": [80, 20]})\nst.dataframe(df)',
    lambda: st.dataframe(pd.DataFrame({"Class": ["1st", "2nd"], "Fare": [80, 20]}))
)

create_row(
    "Key Metric Card",
    'st.metric(label="Total Passengers", value="891", delta="+12%")',
    lambda: st.metric(label="Total Passengers", value="891", delta="+12%")
)

create_row(
    "Status Messages",
    'st.success("Success!")\nst.warning("Warning!")\nst.error("Error!")\nst.info("Info!")',
    lambda: (
        st.success("Success!"),
        st.warning("Warning!"),
        st.error("Error!"),
        st.info("Info!")
    )
)

# --- 4. Charts & Data Visualization ---
create_row(
    "Line & Bar Charts",
    'chart_data = pd.DataFrame(np.random.randn(20, 2), columns=["A", "B"])\nst.line_chart(chart_data)',
    lambda: st.line_chart(pd.DataFrame(np.random.randn(20, 2), columns=["A", "B"]))
)

# --- 5. Layout & Organization ---
def render_layout_demo():
    c1, c2 = st.columns(2)
    with c1:
        st.info("Col 1")
    with c2:
        st.info("Col 2")
    with st.expander("Click to view details"):
        st.write("Hidden collapsible content.")

create_row(
    "Columns & Expander",
    'col1, col2 = st.columns(2)\nwith col1:\n    st.info("Col 1")\nwith col2:\n    st.info("Col 2")\n\nwith st.expander("Click to view details"):\n    st.write("Hidden content.")',
    render_layout_demo
)

# --- 6. State & Performance ---
def render_state_demo():
    if "counter" not in st.session_state:
        st.session_state.counter = 0
    if st.button("Increment Count"):
        st.session_state.counter += 1
    st.write("Current Count:", st.session_state.counter)

create_row(
    "Session State",
    'if "counter" not in st.session_state:\n    st.session_state.counter = 0\nif st.button("Increment Count"):\n    st.session_state.counter += 1\nst.write("Current Count:", st.session_state.counter)',
    render_state_demo
)

create_row(
    "Data Caching",
    '@st.cache_data\ndef load_data():\n    return pd.DataFrame({"A": [1, 2]})\n\ndf = load_data()',
    lambda: st.write("⚡ Function output cached successfully!")
)