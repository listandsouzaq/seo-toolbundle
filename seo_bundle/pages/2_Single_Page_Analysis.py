import streamlit as st
from tools.meta_title_length_checker.meta_title_length_checker import MetaTitleLengthChecker
# Example: from tools.h1_tag_extractor.h1_tag_extractor import H1TagExtractor

# Add other tools as you implement them
TOOLS = {
    "Meta Title Length Checker": MetaTitleLengthChecker(),
    # "H1 Tag Extractor": H1TagExtractor(),
}

st.set_page_config(page_title="Single Page Analysis", layout="wide")
st.title("Single Page Analysis")

url = st.text_input("Enter the URL for analysis")
if st.button("Analyze"):
    if not url:
        st.error("Please enter a valid URL.")
    else:
        for tool_name, tool in TOOLS.items():
            with st.expander(tool_name):
                st.write(f"**Description:** {tool.description}")
                result = tool.run(url)
                if "error" in result:
                    st.error(result["error"])
                else:
                    for k, v in result.items():
                        st.write(f"**{k.capitalize()}**: {v}")