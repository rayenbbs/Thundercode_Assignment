import os
import re
import streamlit as st
from src.qa_review.crew import QaReview
from dotenv import load_dotenv
load_dotenv()


def is_valid_url(url):
    # Regular expression for URL validation
    pattern = r"^https://[a-zA-Z0-9\-]+(\.[a-zA-Z0-9\-]+)+.*$"
    return re.match(pattern, url)


def load_markdown(file_path):
    with open(file_path, "r", encoding="utf-8",errors="ignore") as f:
        return f.read()

sections = {
    "Overall": "./outputs//report.md",
    "Accessibility": "./outputs/accessibility_report.md",
    "Best Practices": "./outputs/best_practices_report.md",
    "HTML and Content": "./outputs/html_report.md",
    "Performance": "./outputs/performance_report.md",
    "Security": "./outputs/security_report.md",
    "SEO": "./outputs/SEO_report.md"
}

#initializing the crewAI crew
testing_crew=QaReview()

#UI
st.title("QA Review")
st.write("Analyze web performance, accessibility, and best practices.")

loading_placeholder = st.empty()
url = st.text_input("Enter the URL to analyze:", placeholder="https://example.com (always type in this format)")


if st.button("Run Analysis"):
    if (url and is_valid_url(url)):
        with st.spinner("Running analysis..."):
            try:
                inputs = {"website_url": url,"topic":"Quality Assurance"}
                results = testing_crew.crew().kickoff(inputs=inputs)
                st.session_state["analysis_complete"] = True
                st.success("Analysis completed! Use the sidebar to navigate between sections.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a valid URL.")
        
        
if "analysis_complete" in st.session_state and st.session_state["analysis_complete"]:
    st.sidebar.title("Website QA Analysis Dashboard")
    selected_section = st.sidebar.radio("Select a Section:", list(sections.keys()))
    st.title(f"{selected_section} Analysis")
    try:
        # Load and display the Markdown file for the selected section
        content = load_markdown(sections[selected_section])
        st.markdown(content, unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Content for {selected_section} not found. Please ensure the file exists.")
else:
    st.info("Run the analysis to unlock the dashboard.")