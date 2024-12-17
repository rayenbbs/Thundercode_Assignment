


import streamlit as st
from src.qa_review.crew import QaReview
from dotenv import load_dotenv
from UI.utilities.helpers import is_valid_url, load_markdown, display_charts,display_download_buttons


load_dotenv()
sections = {
    "KPIs":"./outputs/kpis.json",
    "Overall QA Review": "./outputs/report.md",
    "Accessibility": "./outputs/accessibility_report.md",
    "Best Practices": "./outputs/best_practices_report.md",
    "HTML and Content": "./outputs/html_report.md",
    "Performance": "./outputs/performance_report.md",
    "Security": "./outputs/security_report.md",
    "SEO": "./outputs/SEO_report.md"
}

#initializing the crewAI crew
testing_crew=QaReview()


st.title("QA Review")
st.write("Analyze web performance, accessibility, and best practices.")
loading_placeholder = st.empty()
url = st.text_input("Enter the URL to analyze:", placeholder="https://example.com (always type in this format)")

if st.button("Run Analysis"):
    if (url and is_valid_url(url)):
        with st.spinner("Running analysis..."):
            try:
                inputs = {"website_url": url,"topic":"Quality Assurance"}
                #results = testing_crew.crew().kickoff(inputs=inputs)
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
    
    
