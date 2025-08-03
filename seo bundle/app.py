import streamlit as st
from typing import Dict, Any
from urllib.parse import urlparse

# ==============================================================================
# IMPORT ALL 40 SEO TOOLS
# Since we are creating a single-file application, we need to import every
# tool class directly into this file. This makes app.py the central hub.
# ==============================================================================
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
from tools.structured_data_finder.structured_data_finder import StructuredDataFinder
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

# ==============================================================================
# UI/UX Enhancements with Custom CSS
# This section uses Markdown to inject custom CSS for a more polished look.
# ==============================================================================
st.markdown(
    """
    <style>
    /* Main container and typography */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1 {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 700;
        color: #1a1a1a;
        font-size: 3rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    h2 {
        font-weight: 600;
        color: #333;
    }
    .stSelectbox label {
        font-weight: 600;
        color: #444;
    }

    /* Streamlit-specific component styling */
    div.stButton > button {
        background-color: #007bff;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    div.stButton > button:hover {
        background-color: #0056b3;
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }
    .stExpander div[role="button"] p {
        font-weight: bold;
        font-size: 1.1em;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ==============================================================================
# Main Application Logic
# This is the single-file implementation, where everything is handled here.
# ==============================================================================

# Set wide layout for better usability
st.set_page_config(
    page_title="SEO Toolkit",
    layout="wide"
)

# A dictionary to hold all tool instances, making it easy to select and run them.
TOOLS = {
    "Meta Title Length Checker": MetaTitleLengthChecker(),
    "Meta Description Length Checker": MetaDescriptionLengthChecker(),
    "Keyword Density Calculator": KeywordDensityCalculator(),
    "H1 Tag Extractor": H1TagExtractor(),
    "Image Alt Tag Checker": ImageAltTagChecker(),
    "Word Count Checker": WordCountChecker(),
    "URL Slug Optimizer": URLSlugOptimizer(),
    "Canonical Tag Checker": CanonicalTagChecker(),
    "Robots.txt Fetcher & Parser": RobotsTxtFetcherParser(),
    "Sitemap.xml Fetcher & Validator": SitemapXmlFetcherValidator(),
    "Broken Link Checker": BrokenLinkChecker(),
    "Page Load Time Tester": PageLoadTimeTester(),
    "Internal Link Counter": InternalLinkCounter(),
    "External Link Counter": ExternalLinkCounter(),
    "Anchor Text Analyzer": AnchorTextAnalyzer(),
    "Favicon Checker": FaviconChecker(),
    "Structured Data Finder": StructuredDataFinder(),
    "Heading Tag Structure Analyzer": HeadingTagStructureAnalyzer(),
    "Mobile Responsive Check": MobileResponsiveCheck(),
    "Social Meta Tag Extractor": SocialMetaTagExtractor(),
    "Schema Markup Presence Checker": SchemaMarkupPresenceChecker(),
    "Link Redirect Checker": LinkRedirectChecker(),
    "Page Status Code Checker": PageStatusCodeChecker(),
    "Keyword Suggestions from Related Words": KeywordSuggestionsFromRelatedWords(),
    "Readability Score Calculator": ReadabilityScoreCalculator(),
    "Keyword Case Converter": KeywordCaseConverter(),
    "HTML Minifier": HtmlMinifier(),
    "CSS Minifier": CssMinifier(),
    "JS Minifier": JsMinifier(),
    "SERP Preview Simulator": SerpPreviewSimulator(),
    "Open Graph Preview": OpenGraphPreview(),
    "Twitter Card Preview": TwitterCardPreview(),
    "Alt Tag Missing Finder": AltTagMissingFinder(),
    "Word Frequency Counter": WordFrequencyCounter(),
    "Keyword Position Estimator": KeywordPositionEstimator(),
    "Backlink List Parser": BacklinkListParser(),
    "YouTube Video Tag Extractor": YoutubeVideoTagExtractor(),
    "Text-to-Keyword Generator": TextToKeywordGenerator(),
    "Domain Age Checker": DomainAgeChecker(),
    "Email Obfuscator Generator": EmailObfuscatorGenerator(),
}


def is_valid_url(url: str) -> bool:
    """Checks if a string is a valid URL."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def main():
    """Main function to run the Streamlit app."""
    # Use columns for a clean, two-panel layout
    selector_col, results_col = st.columns([1, 2])

    with selector_col:
        st.header("Tool Selector")
        st.info("Choose a tool and enter a URL to start the analysis.")
        
        # Dropdown to select a tool
        selected_tool_name = st.selectbox(
            "Select an SEO Tool:",
            options=list(TOOLS.keys()),
            help="Choose from over 40 different SEO analysis tools."
        )

        st.markdown("---")

        # URL input and analysis button
        url_input = st.text_input(
            "Enter URL:",
            placeholder="https://example.com"
        )

        run_button = st.button("Run Analysis", use_container_width=True)

    with results_col:
        st.header(f"Results for: {selected_tool_name}")
        
        if run_button:
            if not is_valid_url(url_input):
                st.error("Please enter a valid URL.")
            else:
                st.info(f"Running '{selected_tool_name}' on `{url_input}`...")
                
                # Get the selected tool instance
                selected_tool = TOOLS[selected_tool_name]
                
                # Use a spinner to show that work is in progress
                with st.spinner("Analyzing..."):
                    # Run the tool's logic and get the results dictionary
                    try:
                        results = selected_tool.run(url_input)
                        
                        # Display results in a structured way
                        st.subheader("Analysis Complete!")
                        st.json(results)
                        
                        # Add a download button for the JSON results
                        st.download_button(
                            label="Download Results as JSON",
                            data=str(results),
                            file_name=f"{selected_tool_name.replace(' ', '_').lower()}_results.json",
                            mime="application/json"
                        )
                    except Exception as e:
                        st.error(f"An error occurred while running the tool: {e}")
        else:
            st.warning("Please select a tool and click 'Run Analysis' to see results.")

if __name__ == "__main__":
    main()
