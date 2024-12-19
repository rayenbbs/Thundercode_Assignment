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
    "KPIs": "generate_kpi_json_task",
    "Overall QA Review": "reporting_task",
    "Accessibility": "analyze_web_accessibility_task",
    "Best Practices": "analyze_web_best_practices_task",
    "HTML and Content": "analyze_html_task",
    "Performance": "analyze_web_performance_task",
    "Security": "analyze_http_security_task",
    "SEO": "analyze_SEO_task"
}

#initializing the crewAI crew
testing_crew=QaReview()


st.title("QA Review")
st.write("Analyze web performance, accessibility, and best practices.")
loading_placeholder = st.empty()
url = st.text_input("Enter the URL to analyze:", placeholder="https://example.com (always type in this format)")
result_dict={}
if st.button("Run Analysis"):
    if (url and is_valid_url(url)):
        with st.spinner("Running analysis..."):
            try:
                inputs = {"website_url": url,"topic":"Quality Assurance"}
                results = testing_crew.crew().kickoff(inputs=inputs).tasks_output
                result_dict = {item.name: item.raw for item in results}
                st.write(result_dict)
                st.session_state["analysis_complete"] = True
                st.success("Analysis completed! Use the sidebar to navigate between sections.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a valid URL.")

if "analysis_complete" in st.session_state and st.session_state["analysis_complete"]:
    st.sidebar.title("Website QA Analysis Dashboard")
    selected_section = st.sidebar.radio("Select a Section:", list(sections.keys()))
    if(selected_section !="KPIs"):
        st.title(f"{selected_section} Analysis")
        try:
            content = result_dict[sections[selected_section]]
            display_download_buttons(content,selected_section)
            st.markdown(content, unsafe_allow_html=True)
        except FileNotFoundError:
            st.error(f"Content for {selected_section} not found. Please ensure the file exists.")
    else:
         st.title("KPIs Visualization:")
         display_charts(result_dict[sections[selected_section]])
else:
    st.info("Run the analysis to unlock the dashboard.")
    
    
