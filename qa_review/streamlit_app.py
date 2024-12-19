__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
from src.qa_review.crew import QaReview
from dotenv import load_dotenv
from UI.utilities.helpers import is_valid_url, load_markdown, display_charts,display_download_buttons
import sys
from pathlib import Path
dir = Path(__file__).absolute().parent
sys.path.append(str(dir.parent))  # Go one level up from the current directory
load_dotenv()

sections = {
    "KPIs": Path(dir, "qa_review", "outputs", "kpis.json"),
    "Overall QA Review": Path(dir, "qa_review", "outputs", "report.md"),
    "Accessibility": Path(dir, "qa_review", "outputs", "accessibility_report.md"),
    "Best Practices": Path(dir, "qa_review", "outputs", "best_practices_report.md"),
    "HTML and Content": Path(dir, "qa_review", "outputs", "html_report.md"),
    "Performance": Path(dir, "qa_review", "outputs", "performance_report.md"),
    "Security": Path(dir, "qa_review", "outputs", "security_report.md"),
    "SEO": Path(dir, "qa_review", "outputs", "SEO_report.md")
}

#initializing the crewAI crew
testing_crew=QaReview()


st.title("QA Review")
st.write("Analyze web performance, accessibility, and best practices.")
loading_placeholder = st.empty()
url = st.text_input("Enter the URL to analyze:", placeholder="https://example.com (always type in this format)")
results=None
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


for agent_name, output in results.items():
        st.write(f"### {agent_name}")
        st.write(output)  # You can also use st.json or other components

if "analysis_complete" in st.session_state and st.session_state["analysis_complete"]:
    st.sidebar.title("Website QA Analysis Dashboard")
    selected_section = st.sidebar.radio("Select a Section:", list(sections.keys()))
    if(selected_section !="KPIs"):
        st.title(f"{selected_section} Analysis")
        try:
            content = load_markdown(sections[selected_section])
            display_download_buttons(content,selected_section)
            st.markdown(content, unsafe_allow_html=True)
        except FileNotFoundError:
            st.error(f"Content for {selected_section} not found. Please ensure the file exists.")
    else:
         st.title("KPIs Visualization:")
         display_charts(sections[selected_section])
else:
    st.info("Run the analysis to unlock the dashboard.")
    
    
