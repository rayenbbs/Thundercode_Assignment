import re
import markdown2
import plotly.express as px
import pandas as pd
import json
import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

def convert_markdown_to_pdf(markdown_content):
    # Convert markdown to HTML
    html_content = markdown2.markdown(markdown_content)

    # Create a PDF buffer
    pdf_buffer = BytesIO()
    pdf = SimpleDocTemplate(pdf_buffer)
    
    styles = getSampleStyleSheet()
    # Break content into structured elements
    story = []
    for line in html_content.split("\n"):
        if line.startswith("<h1>") and line.endswith("</h1>"):
            story.append(Paragraph(line[4:-5], styles["Heading1"]))
        elif line.startswith("<h2>") and line.endswith("</h2>"):
            story.append(Paragraph(line[4:-5], styles["Heading2"]))
        elif line.startswith("<ul>"):
            items = re.findall(r"<li>(.*?)</li>", line)
            list_items = [ListItem(Paragraph(item, styles["BodyText"])) for item in items]
            story.append(ListFlowable(list_items, bulletType="bullet"))
        else:
            story.append(Paragraph(line.strip(), styles["BodyText"]))

    # Build the PDF
    pdf.build(story)
    pdf_buffer.seek(0)
    return pdf_buffer

def is_valid_url(url):
    pattern = r"^https://[a-zA-Z0-9\-]+(\.[a-zA-Z0-9\-]+)+.*$"
    return re.match(pattern, url)

def load_markdown(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()
    
    
def display_download_buttons(content,selected_section):
            pdf_buffer = None
            pdf_conversion_error = False

            try:
                pdf_buffer = convert_markdown_to_pdf(content)
            except Exception:
                pdf_conversion_error = True

            markdown_buffer = BytesIO(content.encode("utf-8"))

            col1, col2 = st.columns([1,1])
            with col1:
                if(not pdf_conversion_error):
                    st.download_button(
                        label="Download Report as PDF",
                        data=pdf_buffer,
                        file_name=f"{selected_section.replace(' ', '_').lower()}_report.pdf",
                        mime="application/pdf",
                    )
                else:
                    st.button(
                        label="Download Report as PDF",            
                        disabled=True
                    )
            with col2:
                st.download_button(
                    label="Download Report as Markdown",
                    data=markdown_buffer,
                    file_name=f"{selected_section.replace(' ', '_').lower()}_report.md",
                    mime="text/markdown"
                )


def display_charts(json_data):
    try:
        json_data=json.loads(json_data)
        # Convert JSON data into a DataFrame
        data = []
        for key, value in json_data.items():
            value["category"] = key
            data.append(value)
        df = pd.DataFrame(data)

        df = df[df["data_unavailable"] == False]
        df = df.drop(columns=["data_unavailable"])

        st.header("Line Chart of Scores")
        fig_line_scores = px.line(
            df,
            x="category",
            y="score",
            title="Progression of Scores Across Categories",
            markers=True
        )
        st.plotly_chart(fig_line_scores)

        st.header("Pie Chart of Critical Issues")
        fig_pie_critical = px.pie(
            df,
            names="category",
            values="critical_issues",
            title="Distribution of Critical Issues",
            color_discrete_sequence=px.colors.sequential.Reds
        )
        st.plotly_chart(fig_pie_critical)

        st.header("Bar Chart of Issues")
        fig_bar = px.bar(
            df,
            x="category",
            y=["critical_issues", "total_issues"],
            title="Comparison of Critical and Total Issues",
            labels={"value": "Number of Issues", "variable": "Issue Type"},
            barmode="group",
        )
        st.plotly_chart(fig_bar)

        st.header("Scatter Chart: Total Issues vs Scores")
        fig_scatter = px.scatter(
            df,
            x="score",
            y="total_issues",
            text="category",
            title="Total Issues vs Scores",
            labels={"score": "Score", "total_issues": "Total Issues"},
            color="total_issues",
            size="total_issues",
            color_continuous_scale="Viridis"
        )
        fig_scatter.update_traces(textposition="top center")
        st.plotly_chart(fig_scatter)

        st.header("Data in Table Format")
        st.dataframe(df)
    except Exception:
        st.write("No Data to visualize!")
         
