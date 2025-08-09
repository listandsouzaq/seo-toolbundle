import streamlit as st
from core.config import TOOL_CONFIG

st.set_page_config(page_title="SEO Toolkit Dashboard", layout="wide")
st.title("SEO Toolkit Dashboard")
st.subheader("Welcome to the SEO Toolkit! Manage your tools below.")

# Use session state to store tool visibility
if "tool_visibility" not in st.session_state:
    st.session_state.tool_visibility = TOOL_CONFIG.copy()

st.header("Tool Visibility Settings")
st.write("Toggle tools on or off. Disabled tools will be hidden from the navigation sidebar.")

for tool_name in TOOL_CONFIG:
    st.session_state.tool_visibility[tool_name] = st.toggle(
        f"Enable {tool_name}",
        value=st.session_state.tool_visibility[tool_name],
        key=f"toggle_{tool_name}"
    )