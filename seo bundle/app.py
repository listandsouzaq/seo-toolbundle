import streamlit as st
import json
import requests
from urllib.parse import urlparse
from typing import Dict, Any, List
from streamlit_lottie import st_lottie

# ==============================================================================
# LOTTIE ANIMATION HELPER
# ==============================================================================
def load_lottie_url(url: str) -> Dict[str, Any] | None:
    """Fetches a Lottie animation from a URL and returns it as a dictionary."""
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
        return None
    except requests.exceptions.RequestException:
        return None

# ==============================================================================
# IMPORT ALL 40 SEO TOOLS (Place your tool classes here)
# ==============================================================================
# NOTE: Assumes these tool classes exist in the 'tools' directory.
# You must have these files and classes defined for the code to run fully.
# The code below will work assuming these are correctly set up.
try:
    from tools.meta_title_length_checker.meta_title_length_checker import MetaTitleLengthChecker
    from tools.meta_description_length_checker.meta_description_length_checker import MetaDescriptionLengthChecker
    from tools.keyword_density_calculator.keyword_density_calculator import KeywordDensityCalculator
    from tools.h1_tag_extractor.h1_tag_extractor import H1TagExtractor
    from tools.image_alt_tag_checker.image_alt_tag_checker import ImageAltTagChecker
    from tools.word_count_checker.word_count_checker import WordCountChecker
    from tools.url_slug_optimizer.url_slug_optimizer import URLSlugOptimizer
    from tools.canonical_tag_checker.canonical_tag_checker import CanonicalTagChecker
    from tools.robots_txt_fetcher_parser.robots_txt_fetcher_parser import RobotsTxtFetcherParser
    from tools.sitemap_xml_fetcher_validator.sitemap_xml_fetcher_validator import SitemapXmlFetcherValidator
    from tools.broken_link_checker.broken_link_checker import BrokenLinkChecker
    from tools.page_load_time_tester.page_load_time_tester import PageLoadTimeTester
    from tools.internal_link_counter.internal_link_counter import InternalLinkCounter
    from tools.external_link_counter.external_link_counter import ExternalLinkCounter
    from tools.anchor_text_analyzer.anchor_text_analyzer import AnchorTextAnalyzer
    from tools.favicon_checker.favicon_checker import FaviconChecker
    from tools.structured_data_json_ld_finder.structured_data_json_ld_finder import StructuredDataFinder
    from tools.heading_tag_structure_analyzer.heading_tag_structure_analyzer import HeadingTagStructureAnalyzer
    from tools.mobile_responsive_check.mobile_responsive_check import MobileResponsiveCheck
    from tools.social_meta_tag_extractor.social_meta_tag_extractor import SocialMetaTagExtractor
    from tools.schema_markup_presence_checker.schema_markup_presence_checker import SchemaMarkupPresenceChecker
    from tools.link_redirect_checker.link_redirect_checker import LinkRedirectChecker
    from tools.page_status_code_checker.page_status_code_checker import PageStatusCodeChecker
    from tools.keyword_suggestions_from_related_words.keyword_suggestions_from_related_words import KeywordSuggestionsFromRelatedWords
    from tools.readability_score_calculator.readability_score_calculator import ReadabilityScoreCalculator
    from tools.keyword_case_converter.keyword_case_converter import KeywordCaseConverter
    from tools.html_minifier.html_minifier import HtmlMinifier
    from tools.css_minifier.css_minifier import CssMinifier
    from tools.js_minifier.js_minifier import JsMinifier
    from tools.serp_preview_simulator.serp_preview_simulator import SerpPreviewSimulator
    from tools.open_graph_preview.open_graph_preview import OpenGraphPreview
    from tools.twitter_card_preview.twitter_card_preview import TwitterCardPreview
    from tools.alt_tag_missing_finder.alt_tag_missing_finder import AltTagMissingFinder
    from tools.word_frequency_counter.word_frequency_counter import WordFrequencyCounter
    from tools.keyword_position_estimator.keyword_position_estimator import KeywordPositionEstimator
    from tools.backlink_list_parser.backlink_list_parser import BacklinkListParser
    from tools.youtube_video_tag_extractor.youtube_video_tag_extractor import YoutubeVideoTagExtractor
    from tools.text_to_keyword_generator.text_to_keyword_generator import TextToKeywordGenerator
    from tools.domain_age_checker.domain_age_checker import DomainAgeChecker
    from tools.email_obfuscator_generator.email_obfuscator_generator import EmailObfuscatorGenerator
except ImportError as e:
    st.error(f"Error importing a tool. Make sure all tool files are correctly placed in the 'tools' directory. Details: {e}")
    st.stop()


# ==============================================================================
# THEME CSS (Updated for animations and flexible UI)
# ==============================================================================
DARK_THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

:root {
    --primary-bg: #121212;
    --secondary-bg: #1E1E1E;
    --text-primary: #FFFFFF;
    --text-secondary: #E0E0E0;
    --accent-purple: #BB86FC;
    --soft-blue: #03DAC6;
    --border-color: #424242;
    --success-green: #00C853;
    --warning-yellow: #FFD600;
    --error-red: #FF5252;
}

body, .stApp {
    background-color: var(--primary-bg);
    color: var(--text-primary);
    font-family: 'Poppins', sans-serif;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background-color: var(--secondary-bg) !important;
    border-right: 1px solid var(--border-color) !important;
    padding-top: 2rem;
}
[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}

/* Page Title & Headings */
h1, h2, h3, h4, h5, h6 {
    color: var(--soft-blue) !important;
    font-weight: 600;
}
.stApp h1:first-of-type {
    font-size: 3em;
    font-weight: 700;
    background: linear-gradient(90deg, var(--soft-blue), var(--accent-purple));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 10px rgba(3, 218, 198, 0.5);
}

.stButton button {
    background-color: var(--secondary-bg) !important;
    color: var(--text-primary) !important;
    border: 2px solid var(--border-color) !important;
    border-radius: 12px;
    padding: 20px 24px !important;
    width: 100%;
    font-size: 1.1em;
    font-weight: 600;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.stButton button:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
    border-color: var(--accent-purple) !important;
    color: var(--accent-purple) !important;
}

.stButton button:active {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

/* Floating animation for cards/buttons */
@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-3px); }
    100% { transform: translateY(0px); }
}

.float-animation {
    animation: float 4s ease-in-out infinite;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--accent-purple), #4B0082) !important;
    color: var(--text-primary) !important;
    border: none !important;
    font-weight: 700;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

/* Inputs */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input {
    background-color: var(--secondary-bg) !important;
    color: var(--text-primary) !important;
    border: 2px solid var(--border-color) !important;
    font-size: 16px;
    border-radius: 8px;
    transition: border-color 0.3s, box-shadow 0.3s;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stNumberInput > div > div > input:focus {
    border: 2px solid var(--soft-blue) !important;
    box-shadow: 0 0 0 2px rgba(3, 218, 198, 0.2);
}

/* Card-like containers for content */
div.stCard {
    background-color: var(--secondary-bg);
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    border: 1px solid var(--border-color);
}

.stAlert {
    border: 1px solid var(--border-color) !important;
    border-left: 5px solid;
    border-radius: 8px;
    background-color: var(--secondary-bg) !important;
    color: var(--text-primary) !important;
}

.stAlert.info { border-left-color: var(--soft-blue) !important; }
.stAlert.success { border-left-color: var(--success-green) !important; }
.stAlert.warning { border-left-color: var(--warning-yellow) !important; }
.stAlert.error { border-left-color: var(--error-red) !important; }

hr {
    border-top: 1px solid var(--border-color) !important;
}

/* Remove default Streamlit padding */
.block-container, .stApp > div {
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 5rem;
    padding-right: 5rem;
}
</style>
"""

LIGHT_THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

:root {
    --primary-bg: #F0F2F6;
    --secondary-bg: #FFFFFF;
    --text-primary: #0E1117;
    --text-secondary: #3A3A3A;
    --accent-purple: #6200EE;
    --soft-blue: #007BFF;
    --border-color: #E6E6E6;
    --success-green: #28A745;
    --warning-yellow: #FFC107;
    --error-red: #DC3545;
}

body, .stApp {
    background-color: var(--primary-bg);
    color: var(--text-primary);
    font-family: 'Poppins', sans-serif;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background-color: var(--secondary-bg) !important;
    border-right: 1px solid var(--border-color) !important;
    padding-top: 2rem;
}
[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}

/* Page Title & Headings */
h1, h2, h3, h4, h5, h6 {
    color: var(--soft-blue) !important;
    font-weight: 600;
}
.stApp h1:first-of-type {
    font-size: 3em;
    font-weight: 700;
    background: linear-gradient(90deg, var(--soft-blue), var(--accent-purple));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.stButton button {
    background-color: var(--secondary-bg) !important;
    color: var(--text-primary) !important;
    border: 2px solid var(--border-color) !important;
    border-radius: 12px;
    padding: 20px 24px !important;
    width: 100%;
    font-size: 1.1em;
    font-weight: 600;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.stButton button:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    border-color: var(--accent-purple) !important;
    color: var(--accent-purple) !important;
}

.stButton button:active {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
}

/* Floating animation for cards/buttons */
@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-3px); }
    100% { transform: translateY(0px); }
}

.float-animation {
    animation: float 4s ease-in-out infinite;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--accent-purple), #4B0082) !important;
    color: var(--text-primary) !important;
    border: none !important;
    font-weight: 700;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

/* Inputs */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input {
    background-color: var(--secondary-bg) !important;
    color: var(--text-primary) !important;
    border: 2px solid var(--border-color) !important;
    font-size: 16px;
    border-radius: 8px;
    transition: border-color 0.3s, box-shadow 0.3s;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stNumberInput > div > div > input:focus {
    border: 2px solid var(--soft-blue) !important;
    box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.1);
}

/* Card-like containers for content */
div.stCard {
    background-color: var(--secondary-bg);
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    border: 1px solid var(--border-color);
}

.stAlert {
    border: 1px solid var(--border-color) !important;
    border-left: 5px solid;
    border-radius: 8px;
    background-color: var(--secondary-bg) !important;
    color: var(--text-primary) !important;
}

.stAlert.info { border-left-color: var(--soft-blue) !important; }
.stAlert.success { border-left-color: var(--success-green) !important; }
.stAlert.warning { border-left-color: var(--warning-yellow) !important; }
.stAlert.error { border-left-color: var(--error-red) !important; }

hr {
    border-top: 1px solid var(--border-color) !important;
}

/* Remove default Streamlit padding */
.block-container, .stApp > div {
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 5rem;
    padding-right: 5rem;
}
</style>
"""

# ==============================================================================
# TOOL CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="SEO Toolkit",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Tool instances and categories
TOOLS_INSTANCES = {
    "Meta Title Length Checker": MetaTitleLengthChecker(), "Meta Description Length Checker": MetaDescriptionLengthChecker(),
    "Keyword Density Calculator": KeywordDensityCalculator(), "H1 Tag Extractor": H1TagExtractor(),
    "Image Alt Tag Checker": ImageAltTagChecker(), "Word Count Checker": WordCountChecker(),
    "URL Slug Optimizer": URLSlugOptimizer(), "Canonical Tag Checker": CanonicalTagChecker(),
    "Robots.txt Fetcher & Parser": RobotsTxtFetcherParser(), "Sitemap.xml Fetcher & Validator": SitemapXmlFetcherValidator(),
    "Broken Link Checker": BrokenLinkChecker(), "Page Load Time Tester": PageLoadTimeTester(),
    "Internal Link Counter": InternalLinkCounter(), "External Link Counter": ExternalLinkCounter(),
    "Anchor Text Analyzer": AnchorTextAnalyzer(), "Favicon Checker": FaviconChecker(),
    "Structured Data Finder": StructuredDataFinder(), "Heading Tag Structure Analyzer": HeadingTagStructureAnalyzer(),
    "Mobile Responsive Check": MobileResponsiveCheck(), "Social Meta Tag Extractor": SocialMetaTagExtractor(),
    "Schema Markup Presence Checker": SchemaMarkupPresenceChecker(), "Link Redirect Checker": LinkRedirectChecker(),
    "Page Status Code Checker": PageStatusCodeChecker(), "Keyword Suggestions from Related Words": KeywordSuggestionsFromRelatedWords(),
    "Readability Score Calculator": ReadabilityScoreCalculator(), "Keyword Case Converter": KeywordCaseConverter(),
    "HTML Minifier": HtmlMinifier(), "CSS Minifier": CssMinifier(),
    "JS Minifier": JsMinifier(), "SERP Preview Simulator": SerpPreviewSimulator(),
    "Open Graph Preview": OpenGraphPreview(), "Twitter Card Preview": TwitterCardPreview(),
    "Alt Tag Missing Finder": AltTagMissingFinder(), "Word Frequency Counter": WordFrequencyCounter(),
    "Keyword Position Estimator": KeywordPositionEstimator(), "Backlink List Parser": BacklinkListParser(),
    "YouTube Video Tag Extractor": YoutubeVideoTagExtractor(), "Text-to-Keyword Generator": TextToKeywordGenerator(),
    "Domain Age Checker": DomainAgeChecker(), "Email Obfuscator Generator": EmailObfuscatorGenerator(),
}

TOOL_CATEGORIES = {
    "🛠️ Meta & Tags": ["Meta Title Length Checker", "Meta Description Length Checker", "H1 Tag Extractor", "Image Alt Tag Checker", "Social Meta Tag Extractor", "Canonical Tag Checker", "Schema Markup Presence Checker", "Alt Tag Missing Finder", "Structured Data Finder", "Heading Tag Structure Analyzer", "Favicon Checker"],
    "📝 Content Analysis": ["Keyword Density Calculator", "Word Count Checker", "Readability Score Calculator", "Word Frequency Counter", "Text-to-Keyword Generator"],
    "⚙️ Technical SEO": ["Robots.txt Fetcher & Parser", "Sitemap.xml Fetcher & Validator", "URL Slug Optimizer", "Mobile Responsive Check", "Page Status Code Checker", "HTML Minifier", "CSS Minifier", "JS Minifier"],
    "🔗 Link Analysis": ["Broken Link Checker", "Internal Link Counter", "External Link Counter", "Anchor Text Analyzer", "Link Redirect Checker", "Backlink List Parser"],
    "🔎 Keyword Research": ["Keyword Suggestions from Related Words", "Keyword Position Estimator", "Keyword Case Converter", "YouTube Video Tag Extractor"],
    "⚡ Performance & UX": ["Page Load Time Tester"],
    "👀 Preview & Simulation": ["SERP Preview Simulator", "Open Graph Preview", "Twitter Card Preview"],
    "🧰 Other Utilities": ["Domain Age Checker", "Email Obfuscator Generator"],
}

# ==============================================================================
# MAIN APPLICATION LOGIC
# ==============================================================================
def main():
    """The main function to run the Streamlit SEO Toolkit app."""
    # Initialize session state for theme, selected tool, and URL input.
    # This ensures variables are set before any widgets use them.
    if 'theme' not in st.session_state:
        st.session_state.theme = 'Dark Mode'
    if 'selected_tool' not in st.session_state:
        st.session_state.selected_tool = None
    
    # Corrected: Initialize 'url_input' in session state.
    if 'url_input' not in st.session_state:
        st.session_state.url_input = ""

    if st.session_state.theme == 'Dark Mode':
        st.markdown(DARK_THEME_CSS, unsafe_allow_html=True)
    else:
        st.markdown(LIGHT_THEME_CSS, unsafe_allow_html=True)

    # --- Sidebar for user input and settings ---
    with st.sidebar:
        # High visibility text
        st.markdown("<h2 style='color: var(--text-primary);'>App</h2>", unsafe_allow_html=True)
        
        # Navigation
        st.markdown("---")
        st.markdown("<h3 style='color: var(--text-primary);'>Dashboard</h3>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: var(--text-primary);'>Single Page Analysis</h3>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: var(--text-primary);'>Bulk Analysis</h3>", unsafe_allow_html=True)
        st.markdown("---")
        
        st.header("Settings")
        st.session_state.theme = st.radio(
            "Choose Theme:",
            ('Dark Mode', 'Light Mode'),
            index=0 if st.session_state.theme == 'Dark Mode' else 1,
            key="theme_radio"
        )
        st.markdown("---")
        
        st.header("Run Analysis")
        
        if st.session_state.selected_tool:
            st.info(f"**Selected Tool:** {st.session_state.selected_tool}")
        else:
            st.warning("Please select a tool from the main page.")

        # The widget itself manages the state now. We don't need to reassign its value.
        st.text_input(
            "Enter URL:",
            placeholder="https://example.com",
            key="url_input"
        )
        
        run_button = st.button("Run Analysis", use_container_width=True, type="primary", key="run_button")
        st.markdown("---")

    # --- Main content area for welcome and results ---
    st.title("SEO Toolkit")
    st.markdown("A comprehensive suite of 40+ tools for website analysis.")
    st.markdown("---")

    lottie_seo = load_lottie_url("https://lottie.host/80a08e01-a53b-4560-af30-4e09f5a0928e/K90T5P7i5b.json")
    
    if not st.session_state.selected_tool:
        st.info("👈 Please select a tool from the options below to begin your analysis.")
        if lottie_seo:
            st_lottie(lottie_seo, height=200, key="lottie_welcome")

        st.header("Select a Tool")
        
        # Display tools with animated floating card buttons
        for category, tools in TOOL_CATEGORIES.items():
            st.subheader(category)
            cols = st.columns(4)
            for i, tool_name in enumerate(tools):
                with cols[i % 4]:
                    # The animation is applied via a CSS class on the Streamlit button
                    if st.button(tool_name, key=f"tool_btn_{tool_name}"):
                        st.session_state.selected_tool = tool_name
                        st.experimental_rerun()
            st.markdown("---")
            
    else:
        st.success(f"Tool selected: **{st.session_state.selected_tool}**")
        
        # Logic to run the analysis
        if run_button:
            st.header(f"Results for: {st.session_state.selected_tool}")
            if not st.session_state.url_input or not is_valid_url(st.session_state.url_input):
                st.error("Please enter a valid URL to run the analysis.")
            else:
                with st.spinner(f"Running '{st.session_state.selected_tool}' on {st.session_state.url_input}..."):
                    try:
                        selected_tool = TOOLS_INSTANCES[st.session_state.selected_tool]
                        results = selected_tool.run(st.session_state.url_input)

                        st.markdown("### Analysis Complete!")
                        st.json(results, expanded=False)

                        st.download_button(
                            label="Download Results as JSON",
                            data=json.dumps(results, indent=4),
                            file_name=f"{st.session_state.selected_tool.replace(' ', '_').lower()}_results.json",
                            mime="application/json"
                        )
                    except Exception as e:
                        st.error(f"An error occurred while running the tool: {e}")
                        st.warning("Make sure the URL is accessible and the tool is configured correctly.")

# --- URL validation helper function ---
def is_valid_url(url: str) -> bool:
    """Checks if a string is a valid URL."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

if __name__ == "__main__":
    main()