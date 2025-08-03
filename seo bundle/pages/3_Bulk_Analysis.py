import streamlit as st
import pandas as pd
from tools.meta_title_length_checker.meta_title_length_checker import MetaTitleLengthChecker
# Add other tools as you implement them

TOOLS = {
    "Meta Title Length Checker": MetaTitleLengthChecker(),
    # Add other tools here as you implement them
}

st.set_page_config(page_title="Bulk Analysis", layout="wide")
st.title("Bulk Analysis")

uploaded_file = st.file_uploader("Upload a CSV with a column named 'url'", type=["csv"])

tool_choice = st.selectbox("Choose a tool to run", list(TOOLS.keys()))

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        if "url" not in df.columns:
            st.error("CSV must contain a 'url' column.")
        else:
            if st.button("Run Bulk Analysis"):
                tool = TOOLS[tool_choice]
                results = []
                for url in df["url"]:
                    res = tool.run(url)
                    results.append({
                        "url": url,
                        **{k: v for k, v in res.items() if k != "error"}
                    })
                results_df = pd.DataFrame(results)
                st.dataframe(results_df)
                csv = results_df.to_csv(index=False).encode('utf-8')
                st.download_button("Download Results as CSV", data=csv, file_name="bulk_seo_results.csv", mime="text/csv")
    except Exception as e:
        st.error(f"Error processing file: {e}")