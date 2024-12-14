import os
import re
import streamlit as st
from src.qa_review.crew import QaReview
from dotenv import load_dotenv

def is_valid_url(url):
    # Regular expression for URL validation
    pattern = r"^https://[a-zA-Z0-9\-]+(\.[a-zA-Z0-9\-]+)+.*$"
    return re.match(pattern, url)

load_dotenv()

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
                report_path = "./report.md" 
                if os.path.exists(report_path):
                        with open(report_path, "r") as f:
                            report_content = f.read()

                        # Display the markdown content
                        st.markdown(report_content)
                        
                        # Example Data for Visualization (customize with real results)
                        # Let's assume `results` contains performance, accessibility, and best practices scores
                        example_data = {
                            "Performance": 85,
                            "Accessibility": 75,
                            "Best Practices": 90,
                        }
                        # Streamlit's Built-in Chart Example
                        st.write("### Summary Metrics")
                        st.bar_chart(example_data)
                else:
                    st.error("Report not found. Please check the task configuration.")

            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a valid URL.")